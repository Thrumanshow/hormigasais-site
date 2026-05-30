import http.server
import json
import hashlib
import hmac
import sqlite3
import datetime
import os

PORT = 5000
NODE_ID = "A16"
LOCATION = "San Miguel, SV"
# Clave secreta criptográfica del nodo para firmar los HMAC (¡Mantén esta segura en producción!)
NODE_SECRET = b"HormigasAIS_Sovereign_Secret_Key_2026_LBHv2"

print(f"🐜 Inicializando base de datos local en el Nodo {NODE_ID}...")

# 1. Configuración del Almacenamiento Local (Capa de Persistencia)
def init_db():
    conn = sqlite3.connect("hormigasais_borde.db")
    cursor = conn.cursor()
    # Tabla principal para el Protocolo LBH v2.0
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data_hash TEXT UNIQUE,
            feromona_hmac TEXT,
            tipo_activo TEXT,
            nodo_emisor TEXT
        )
    """)
    # Tabla analítica para las futuras versiones (Saber qué y cómo se usa el sistema)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analitica_nodos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            accion TEXT,
            peso_bytes INTEGER,
            tiempo_procesamiento_ms REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# 2. Lógica del Protocolo LBH v2.0: Creación de Firmas y Feromonas
def generar_sello_lbh(contenido_binario, tipo_activo="documento"):
    start_time = datetime.datetime.now()
    
    # Capa 1: SHA-256 del contenido (Inmutabilidad del activo digital)
    sha256_hash = hashlib.sha256(contenido_binario).hexdigest()
    
    # Capa 2: Feromona Criptográfica (HMAC-SHA256 que vincula el hash al Nodo A16)
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    mensaje_a_firmar = f"{sha256_hash}|{timestamp}|{NODE_ID}|{LOCATION}".encode('utf-8')
    
    feromona_hmac = hmac.new(NODE_SECRET, mensaje_a_firmar, hashlib.sha256).hexdigest()
    
    # Guardar en SQLite (Persistencia Local de Borde)
    conn = sqlite3.connect("hormigasais_borde.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sellos (timestamp, data_hash, feromona_hmac, tipo_activo, nodo_emisor) VALUES (?, ?, ?, ?, ?)",
            (timestamp, sha256_hash, feromona_hmac, tipo_activo, NODE_ID)
        )
        
        # Guardar analítica para el futuro valor comercial del enjambre
        end_time = datetime.datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        cursor.execute(
            "INSERT INTO analitica_nodos (timestamp, accion, peso_bytes, tiempo_procesamiento_ms) VALUES (?, ?, ?, ?)",
            (timestamp, "SELLO_EMITIDO", len(contenido_binario), duration_ms)
        )
        conn.commit()
        exito = True
    except sqlite3.IntegrityError:
        # El archivo ya había sido sellado previamente
        exito = False
    finally:
        conn.close()
        
    return {
        "exito": exito,
        "nodo": NODE_ID,
        "ubicacion": LOCATION,
        "timestamp": timestamp,
        "data_hash": sha256_hash,
        "feromona_lbh": feromona_hmac,
        "protocolo": "LBH v2.0"
    }

# 3. Servidor API HTTP Nativo
class HormigasAPIHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        # Habilitar CORS para que tu frontend estático pueda consultar la API libremente
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            
            # Consultar estadísticas agregadas de la BD
            conn = sqlite3.connect("hormigasais_borde.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sellos")
            total_sellos = cursor.fetchone()[0]
            conn.close()
            
            status_data = {
                "nodo": NODE_ID,
                "estado": "ONLINE",
                "ubicacion": LOCATION,
                "total_sellos_locales": total_sellos,
                "protocolo": "LBH v2.0"
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))

    def do_POST(self):
        if self.path == "/api/sellar":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                # El frontend envía el contenido del archivo codificado en texto o los metadatos puros
                contenido = payload.get("contenido", "").encode('utf-8')
                tipo_activo = payload.get("tipo", "documento")
                
                resultado = generar_sello_lbh(contenido, tipo_activo)
                
                self.send_response(200 if resultado["exito"] else 409)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resultado).encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), HormigasAPIHandler)
    print(f"🐜 Servidor HormigasAIS corriendo en la Capa 0: Puerto {PORT} (http://localhost:{PORT})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🐜 Servidor detenido de forma segura.")
