const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = 3000;
const LEDGER_FILE = path.join(__dirname, 'ledger_nodo_a16.json');
const METRICAS_FILE = path.join(__dirname, 'metricas_colonia.json');

// Inicializar base de datos del Ledger local
if (!fs.existsSync(LEDGER_FILE)) {
    fs.writeFileSync(LEDGER_FILE, JSON.stringify([]));
}

// Inicializar contadores comerciales para métricas de inversión
let contadoresComerciales = { visitas_biografia: 0, descargas_apk: 0, consultas_ledger: 0, origen_nube_externa: 0 };
if (fs.existsSync(METRICAS_FILE)) {
    try { contadoresComerciales = JSON.parse(fs.readFileSync(METRICAS_FILE, 'utf8')); } catch (e) { console.log("Inicializando métricas."); }
}

function registrarEventoComercial(tipo, req) {
    if (contadoresComerciales.hasOwnProperty(tipo)) {
        contadoresComerciales[tipo]++;
        const referer = req.headers['referer'] || '';
        if (/aws|google|azure|cloud|github/i.test(referer)) {
            contadoresComerciales.origen_nube_externa++;
        }
        fs.writeFile(METRICAS_FILE, JSON.stringify(contadoresComerciales, null, 2), () => {});
    }
}

const server = http.createServer((req, res) => {
    // 1. ENDPOINT: Guardar Sello Criptográfico con Validación Asimétrica (POST)
    if (req.url === '/api/sellar' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk.toString(); });
        req.on('end', () => {
            try {
                const datosSello = JSON.parse(body);
                
                // Reconstruir buffers para validación matemática
                const hashBuffer = Buffer.from(datosSello.hash, 'utf-8');
                const firmaBuffer = Buffer.from(datosSello.meta.firma_dispositivo, 'hex');
                const llavePublicaBuffer = Buffer.from(datosSello.meta.llave_publica_origen, 'hex');

                const llavePublicaClave = crypto.createPublicKey({
                    key: llavePublicaBuffer,
                    format: 'der',
                    type: 'spki'
                });

                const esFirmaValida = crypto.verify(
                    null,
                    hashBuffer,
                    { key: llavePublicaClave, dsaEncoding: 'ieee-p1363' },
                    firmaBuffer
                );

                if (!esFirmaValida) {
                    console.log("❌ [ALERTA] Firma digital FALSA detectada.");
                    res.writeHead(401, { 'Content-Type': 'application/json' });
                    return res.end(JSON.stringify({ status: 'error', message: 'Firma criptográfica inválida.' }));
                }

                // Escribir bloque en el Ledger indexado en caliente
                const ledgerData = JSON.parse(fs.readFileSync(LEDGER_FILE, 'utf8'));
                ledgerData.push(datosSello);
                fs.writeFileSync(LEDGER_FILE, JSON.stringify(ledgerData, null, 2));

                console.log(`🔒 [LBH] Sello validado y acoplado: ${datosSello.hash.substring(0, 15)}...`);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'success', message: 'Sello LBH resguardado en el nodo A16.' }));
            } catch (error) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'error', message: 'Payload inválido.' }));
            }
        });
    }
    // 2. ENDPOINT: Consultar Ledger Completo (GET)
    else if (req.url === '/api/historial' && req.method === 'GET') {
        registrarEventoComercial('consultas_ledger', req);
        fs.readFile(LEDGER_FILE, (err, data) => {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(data || JSON.stringify([]));
        });
    }
    // 3. ENDPOINT: Métricas del Panel de Administración (GET)
    else if (req.url === '/api/admin/metricas' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(contadoresComerciales));
    }
    // 4. ENDPOINT: Distribución Híbrida Inteligente / Descarga APK (GET)
    else if (req.url === '/app' && req.method === 'GET') {
        registrarEventoComercial('descargas_apk', req);
        const userAgent = req.headers['user-agent'] || '';
        if (/Android/i.test(userAgent)) {
            const rutaAPK = path.join(__dirname, 'android/app/build/outputs/apk/release/app-release.apk');
            fs.access(rutaAPK, fs.constants.F_OK, (err) => {
                if (err) {
                    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
                    return res.end('<h1>🐜 HormigasAIS</h1><p>El APK no ha sido compilado en el nodo maestro todavía.</p>');
                }
                res.writeHead(200, { 
                    'Content-Type': 'application/vnd.android.package-archive',
                    'Content-Disposition': 'attachment; filename=HormigasAIS.apk'
                });
                fs.createReadStream(rutaAPK).pipe(res);
            });
        } else {
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            res.end(`<html><body style="background:#0a0a0a;color:#fff;font-family:monospace;text-align:center;padding:50px;">
            <h2>Ecosistema HormigasAIS</h2><p>Acceso desde entorno PC/iOS detectado. La descarga directa del APK requiere un dispositivo Android.</p>
            </body></html>`);
        }
    }
    // 5. ENRUTADOR ESTÁTICO: Servir archivos de la PWA
    else if (req.method === 'GET') {
        if (req.url === '/biografia') registrarEventoComercial('visitas_biografia', req);
        
        let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url);
        const extname = path.extname(filePath);
        let contentType = 'text/html';
        if (extname === '.js') contentType = 'text/javascript';
        else if (extname === '.css') contentType = 'text/css';
        else if (extname === '.json') contentType = 'application/json';
        else if (extname === '.png') contentType = 'image/png';

        fs.readFile(filePath, (error, content) => {
            if (error) {
                res.writeHead(404);
                res.end('Archivo no encontrado en el Nodo A16');
            } else {
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(content, 'utf-8');
            }
        });
    }
});

server.listen(PORT, () => {
    console.log(`🚀 Nodo A16@Soberano operativo en puerto local ${PORT}`);
});

