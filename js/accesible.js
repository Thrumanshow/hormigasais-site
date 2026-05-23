// ================================================================
// 🐜 HormigasAIS — accesible.js
// Accesibilidad Braille LBH — Inclusión para personas no videntes
// Módulo: Braille Unicode + Web Speech API + Vibración
// ================================================================

// ── Mapa Braille LBH ─────────────────────────────────────────────
// Cada byte del Protocolo LBH se representa como celda Braille de 8 puntos
function byteACeldaBraille(byteVal) {
  return String.fromCodePoint(0x2800 + byteVal);
}

function hexABraille(hexStr) {
  const clean = hexStr.replace(/[^0-9a-fA-F]/g, '');
  if (clean.length % 2 !== 0) return null;
  const bytes = [];
  for (let i = 0; i < clean.length; i += 2) {
    bytes.push(parseInt(clean.substr(i, 2), 16));
  }
  return bytes.map(byteACeldaBraille).join(' ');
}

function firmaAHex(firma) {
  // Convierte firma CLHQ-XXXXXXXX a bytes para Braille
  const clean = firma.replace('CLHQ-', '').replace(/-/g, '');
  let hex = '';
  for (let i = 0; i < clean.length; i++) {
    hex += clean.charCodeAt(i).toString(16).padStart(2, '0');
  }
  return hex;
}

// ── Web Speech API ────────────────────────────────────────────────
function leerEnVoz(texto, idioma) {
  if (!window.speechSynthesis) return false;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(texto);
  utterance.lang = idioma || 'es-SV';
  utterance.rate = 0.85;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
  return true;
}

function detenerVoz() {
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

// ── Vibración ─────────────────────────────────────────────────────
function vibrarPatron(bytes) {
  if (!navigator.vibrate) return false;
  // Cada byte genera un patrón: bit 1 = vibra 50ms, bit 0 = silencio 50ms
  const patron = [];
  bytes.forEach((b, idx) => {
    for (let i = 7; i >= 0; i--) {
      const bit = (b >> i) & 1;
      patron.push(bit === 1 ? 50 : 0);
      patron.push(50); // pausa entre bits
    }
    patron.push(200); // pausa entre bytes
  });
  navigator.vibrate(patron);
  return true;
}

// ── Puntos Braille → Byte ─────────────────────────────────────────
function puntosAByte(puntosStr) {
  const mapeo = { '1':0, '2':1, '3':2, '4':3, '5':4, '6':5, '7':6, '8':7 };
  let byte = 0;
  for (const p of puntosStr) {
    if (mapeo[p] !== undefined) byte |= (1 << mapeo[p]);
  }
  return byte;
}

// ── Inicializar pestaña Accesible ─────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  const sec = document.getElementById('accesible');
  if (!sec) return;

  const tieneVoz = !!window.speechSynthesis;
  const tieneVibracion = !!navigator.vibrate;

  sec.innerHTML = `
    <div style="max-width:680px;margin:0 auto;">

      <!-- HEADER -->
      <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#fff;margin-bottom:0.3rem;">🔡 Accesibilidad LBH</div>
      <p style="color:#555;font-size:0.78rem;margin-bottom:0.5rem;">Protocolo LBH en Braille Unicode — Inclusión para personas no videntes</p>

      <!-- CAPACIDADES DEL DISPOSITIVO -->
      <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:2rem;">
        <span style="background:${tieneVoz ? 'rgba(0,255,159,0.1)' : 'rgba(255,68,68,0.1)'};border:1px solid ${tieneVoz ? 'rgba(0,255,159,0.3)' : 'rgba(255,68,68,0.3)'};border-radius:999px;padding:0.2rem 0.8rem;font-size:0.68rem;color:${tieneVoz ? '#00ff9f' : '#ff4444'};">
          ${tieneVoz ? '✅' : '❌'} Lectura en voz alta
        </span>
        <span style="background:${tieneVibracion ? 'rgba(0,255,159,0.1)' : 'rgba(245,197,24,0.1)'};border:1px solid ${tieneVibracion ? 'rgba(0,255,159,0.3)' : 'rgba(245,197,24,0.3)'};border-radius:999px;padding:0.2rem 0.8rem;font-size:0.68rem;color:${tieneVibracion ? '#00ff9f' : '#f5c518'};">
          ${tieneVibracion ? '✅' : '⚠️'} Vibración táctil
        </span>
        <span style="background:rgba(0,255,159,0.1);border:1px solid rgba(0,255,159,0.3);border-radius:999px;padding:0.2rem 0.8rem;font-size:0.68rem;color:#00ff9f;">
          ✅ Braille Unicode
        </span>
      </div>

      <!-- MÓDULO 1: VERIFICAR FIRMA EN BRAILLE -->
      <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">
          1. Verificar firma LBH en Braille
        </div>
        <p style="font-size:0.75rem;color:#666;margin-bottom:1rem;line-height:1.7;">
          Ingresa una firma CLHQ-XXXXXXXX para ver su representación en Braille Unicode y escucharla en voz alta.
        </p>
        <div style="display:flex;gap:0.8rem;margin-bottom:1rem;">
          <input type="text" id="firmaInput" placeholder="CLHQ-Q5PTRLA0"
            aria-label="Ingresa tu firma LBH"
            style="flex:1;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.82rem;padding:0.7rem 0.9rem;outline:none;letter-spacing:0.08em;"
            onkeydown="if(event.key==='Enter') traducirFirma()">
          <button onclick="traducirFirma()" aria-label="Traducir firma a Braille"
            style="background:var(--amarillo);color:#0a0a0a;border:none;font-family:'Space Mono',monospace;font-size:0.78rem;font-weight:700;padding:0.7rem 1.2rem;border-radius:6px;cursor:pointer;">
            Traducir
          </button>
        </div>
        <div id="resultadoBraille" style="display:none;background:#0a0a0a;border:1px solid rgba(0,255,159,0.2);border-radius:8px;padding:1.2rem;">
          <div style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Representación Braille LBH</div>
          <div id="celdaBraille" style="font-size:2.5rem;color:var(--verde);line-height:1.4;letter-spacing:0.1em;margin-bottom:1rem;" aria-live="polite"></div>
          <div id="bytesBraille" style="font-size:0.68rem;color:#555;font-family:'Space Mono',monospace;line-height:1.8;margin-bottom:1rem;"></div>
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
            <button onclick="leerFirmaVoz()" aria-label="Leer firma en voz alta"
              style="background:rgba(0,255,159,0.1);border:1px solid rgba(0,255,159,0.3);color:var(--verde);font-family:'Space Mono',monospace;font-size:0.72rem;padding:0.4rem 0.9rem;border-radius:4px;cursor:pointer;">
              🔊 Leer en voz alta
            </button>
            <button onclick="vibrarFirma()" aria-label="Sentir firma por vibración"
              style="background:rgba(245,197,24,0.1);border:1px solid rgba(245,197,24,0.3);color:var(--amarillo);font-family:'Space Mono',monospace;font-size:0.72rem;padding:0.4rem 0.9rem;border-radius:4px;cursor:pointer;">
              📳 Sentir por vibración
            </button>
            <button onclick="detenerVoz()" aria-label="Detener lectura"
              style="background:#1a1a1a;border:1px solid #333;color:#555;font-family:'Space Mono',monospace;font-size:0.72rem;padding:0.4rem 0.9rem;border-radius:4px;cursor:pointer;">
              ⏹ Detener
            </button>
          </div>
        </div>
      </div>

      <!-- MÓDULO 2: ENTRADA BRAILLE → SELLO LBH -->
      <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">
          2. Crear sello desde Braille
        </div>
        <p style="font-size:0.75rem;color:#666;margin-bottom:1rem;line-height:1.7;">
          Ingresa los puntos Braille activos (1-8) separados por espacio para construir tu identificador LBH. Ejemplo: <span style="color:var(--amarillo);font-family:'Space Mono',monospace">12 34 56 78</span>
        </p>
        <div style="background:#0a0a0a;border:1px solid #222;border-radius:6px;padding:0.8rem;margin-bottom:1rem;font-size:0.72rem;color:#555;line-height:1.8;">
          <strong style="color:#aaa;">Referencia de puntos Braille:</strong><br>
          Punto 1=arriba izq | 2=medio izq | 3=abajo izq<br>
          Punto 4=arriba der | 5=medio der | 6=abajo der<br>
          Punto 7=ext. abajo izq | 8=ext. abajo der
        </div>
        <div style="margin-bottom:1rem;">
          <input type="text" id="puntosInput" placeholder="12 345 67 8 (puntos Braille activos)"
            aria-label="Ingresa puntos Braille"
            style="width:100%;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.82rem;padding:0.7rem 0.9rem;outline:none;">
        </div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">
          ${['1','2','3','4','5','6','7','8','12','123','1234','12345678'].map(p =>
            `<button onclick="agregarPuntos('${p}')" aria-label="Punto Braille ${p}"
              style="background:#0a0a0a;border:1px solid #333;color:#aaa;font-family:'Space Mono',monospace;font-size:0.7rem;padding:0.3rem 0.6rem;border-radius:4px;cursor:pointer;">${p}</button>`
          ).join('')}
        </div>
        <div style="display:flex;gap:0.8rem;">
          <button onclick="procesarPuntosBraille()"
            style="flex:1;background:#1a1a1a;border:1px solid var(--amarillo);color:var(--amarillo);font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.8rem;border-radius:6px;cursor:pointer;">
            🐜 Generar identificador LBH
          </button>
          <button onclick="limpiarPuntos()"
            style="background:#1a1a1a;border:1px solid #333;color:#555;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.8rem 1rem;border-radius:6px;cursor:pointer;">
            ✕
          </button>
        </div>
        <div id="resultadoPuntos" style="margin-top:1rem;display:none;background:#0a0a0a;border:1px solid rgba(245,197,24,0.2);border-radius:8px;padding:1.2rem;" aria-live="polite"></div>
      </div>

      <!-- MÓDULO 3: VERIFICAR SELLO POR VOZ -->
      <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#fff;margin-bottom:0.3rem;">
          3. Verificar sello — respuesta en voz
        </div>
        <p style="font-size:0.75rem;color:#666;margin-bottom:1rem;line-height:1.7;">
          Ingresa una firma y el sistema verificará el sello en la red LBH y leerá el resultado en voz alta.
        </p>
        <div style="display:flex;gap:0.8rem;margin-bottom:1rem;">
          <input type="text" id="firmaVozInput" placeholder="CLHQ-Q5PTRLA0"
            aria-label="Firma para verificar con voz"
            style="flex:1;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.82rem;padding:0.7rem 0.9rem;outline:none;"
            onkeydown="if(event.key==='Enter') verificarConVoz()">
          <button onclick="verificarConVoz()"
            style="background:var(--amarillo);color:#0a0a0a;border:none;font-family:'Space Mono',monospace;font-size:0.78rem;font-weight:700;padding:0.7rem 1.2rem;border-radius:6px;cursor:pointer;">
            🔊 Verificar
          </button>
        </div>
        <div id="resultadoVoz" style="display:none;background:#0a0a0a;border:1px solid #222;border-radius:8px;padding:1.2rem;font-size:0.78rem;color:#aaa;" aria-live="assertive"></div>
      </div>

      <!-- NOTA DE ACCESIBILIDAD -->
      <div style="background:rgba(0,255,159,0.04);border:1px solid rgba(0,255,159,0.15);border-radius:8px;padding:1.2rem;font-size:0.75rem;color:#666;line-height:1.8;text-align:center;">
        🐜 El Protocolo LBH está diseñado para ser universalmente accesible.<br>
        Cada sello tiene representación en Braille, texto y vibración táctil.<br>
        <strong style="color:var(--verde);">Contacto accesibilidad:</strong>
        <a href="mailto:clhq@hormigasais.com" style="color:var(--amarillo);">clhq@hormigasais.com</a>
      </div>

    </div>
  `;
});

// ── Funciones del módulo ──────────────────────────────────────────
let firmaActual = '';
let bytesActuales = [];

function traducirFirma() {
  const firma = document.getElementById('firmaInput').value.trim().toUpperCase();
  if (!firma) return;
  firmaActual = firma;

  const hex = firmaAHex(firma);
  const bytes = [];
  for (let i = 0; i < hex.length; i += 2) {
    bytes.push(parseInt(hex.substr(i, 2), 16));
  }
  bytesActuales = bytes;

  const braille = bytes.map(byteACeldaBraille).join(' ');
  const detalle = bytes.map((b, i) => {
    const h = b.toString(16).padStart(2, '0');
    const bin = b.toString(2).padStart(8, '0');
    return `Byte ${i+1}: ${bin} → ${byteACeldaBraille(b)} (0x${h})`;
  }).join('\n');

  const resultado = document.getElementById('resultadoBraille');
  document.getElementById('celdaBraille').textContent = braille;
  document.getElementById('bytesBraille').textContent = detalle;
  resultado.style.display = 'block';

  // Anunciar para lectores de pantalla
  leerEnVoz(`Firma ${firma} representada en Braille. ${bytes.length} celdas generadas.`);
}

function leerFirmaVoz() {
  if (!firmaActual) return;
  const texto = `Firma LBH: ${firmaActual.split('').join(' ')}. Esta firma certifica un activo en el Protocolo LBH versión 2 punto 0. Nodo emisor: A16, San Miguel, El Salvador.`;
  leerEnVoz(texto);
}

function vibrarFirma() {
  if (bytesActuales.length === 0) return;
  if (!vibrarPatron(bytesActuales)) {
    leerEnVoz('Tu dispositivo no soporta vibración. Usa la opción de lectura en voz alta.');
  }
}

function agregarPuntos(puntos) {
  const input = document.getElementById('puntosInput');
  const val = input.value.trim();
  input.value = val ? val + ' ' + puntos : puntos;
  input.focus();
}

function limpiarPuntos() {
  document.getElementById('puntosInput').value = '';
  const r = document.getElementById('resultadoPuntos');
  r.style.display = 'none';
}

function procesarPuntosBraille() {
  const input = document.getElementById('puntosInput').value.trim();
  if (!input) return;

  const grupos = input.split(/\s+/);
  const bytes = grupos.map(g => puntosAByte(g));
  const hexStr = bytes.map(b => b.toString(16).padStart(2, '0')).join('');
  const braille = bytes.map(byteACeldaBraille).join(' ');

  const resultado = document.getElementById('resultadoPuntos');
  resultado.style.display = 'block';
  resultado.innerHTML =
    '<div style="font-size:0.65rem;color:#555;text-transform:uppercase;margin-bottom:0.5rem;">Identificador LBH generado</div>' +
    '<div style="font-size:2rem;color:var(--amarillo);letter-spacing:0.1em;margin-bottom:0.8rem;">' + braille + '</div>' +
    '<div style="font-size:0.75rem;color:#aaa;font-family:Space Mono,monospace;margin-bottom:0.8rem;">HEX: ' + hexStr.toUpperCase() + '</div>' +
    '<div style="font-size:0.72rem;color:#555;line-height:1.8;">' +
    bytes.map((b, i) => `Grupo ${i+1} [${grupos[i]}]: ${b.toString(2).padStart(8,'0')} → ${byteACeldaBraille(b)}`).join('<br>') +
    '</div>' +
    '<button onclick="vibrarPatron([' + bytes.join(',') + '])" style="margin-top:0.8rem;background:rgba(245,197,24,0.1);border:1px solid rgba(245,197,24,0.3);color:var(--amarillo);font-family:Space Mono,monospace;font-size:0.72rem;padding:0.4rem 0.9rem;border-radius:4px;cursor:pointer;">📳 Sentir vibración</button>';

  leerEnVoz(`Identificador Braille LBH generado. ${bytes.length} celdas. Código hexadecimal: ${hexStr.toUpperCase()}`);
  vibrarPatron(bytes);
}

async function verificarConVoz() {
  const firma = document.getElementById('firmaVozInput').value.trim().toUpperCase();
  if (!firma) {
    leerEnVoz('Por favor ingresa una firma LBH para verificar.');
    return;
  }

  const resultado = document.getElementById('resultadoVoz');
  resultado.style.display = 'block';
  resultado.innerHTML = '<div style="color:#f5c518;">📡 Verificando en el nodo A16...</div>';
  leerEnVoz('Verificando firma en el nodo A16 San Miguel.');

  try {
    const r = await fetch(API + '/seal/' + firma);
    const data = await r.json();

    if (data.status === 'VERIFICADO' && data.sello) {
      const s = data.sello;
      const braille = hexABraille(firmaAHex(firma));
      const fecha = new Date(s.timestamp).toLocaleDateString('es-SV');
      const texto = `Sello verificado y auténtico. Propietario: ${s.owner}. Activo: ${s.asset}. Plan: ${s.plan}. Emitido el ${fecha}. Nodo emisor: ${s.nodo}.`;

      resultado.innerHTML =
        '<div style="color:var(--verde);font-weight:700;margin-bottom:0.8rem;">✅ Sello auténtico verificado</div>' +
        '<div style="font-size:2rem;color:var(--verde);letter-spacing:0.1em;margin-bottom:0.8rem;">' + braille + '</div>' +
        '<div style="line-height:2;font-size:0.78rem;">' +
        '<div>Propietario: <strong style="color:#fff">' + s.owner + '</strong></div>' +
        '<div>Activo: ' + s.asset + '</div>' +
        '<div>Plan: ' + s.plan.toUpperCase() + '</div>' +
        '<div>Emitido: ' + fecha + '</div>' +
        '<div>Nodo: ' + s.nodo + '</div>' +
        '</div>' +
        '<button onclick="leerEnVoz(\'' + texto.replace(/'/g, '') + '\')" style="margin-top:0.8rem;background:rgba(0,255,159,0.1);border:1px solid rgba(0,255,159,0.3);color:var(--verde);font-family:Space Mono,monospace;font-size:0.72rem;padding:0.4rem 0.9rem;border-radius:4px;cursor:pointer;">🔊 Escuchar resultado</button>';

      leerEnVoz(texto);
    } else {
      resultado.innerHTML = '<div style="color:#ff4444;">❌ Firma no encontrada en la red LBH</div>';
      leerEnVoz('La firma ingresada no fue encontrada en la red LBH. Verifica que sea correcta.');
    }
  } catch(e) {
    resultado.innerHTML = '<div style="color:#ff4444;">⚠️ Error de conexión con el nodo A16</div>';
    leerEnVoz('Error de conexión con el nodo A16. Intenta de nuevo.');
  }
}
