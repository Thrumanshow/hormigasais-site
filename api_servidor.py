import http.server
import json
import hashlib
import hmac
import sqlite3
import datetime

PORT = 5000
NODE_ID = "A16"
NODE_SECRET = b"HormigasAIS_Corporate_Secret_2026"

print("🐜 Actualizando la API del Nodo A16 a la estructura corporativa...")

def init_corporate_db():
    conn = sqlite3.connect("hormigasais_borde.db")
    cursor = conn.cursor()
    
    # 1. Tabla de Usuarios Corporativos (El activo para las Big Tech)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            email TEXT PRIMARY KEY,
            fecha_registro TEXT,
            sellos_gratuitos_restantes INTEGER DEFAULT 3,
            plan_activo TEXT DEFAULT 'FREE'
        )
    """)
    
    # 2. Tabla de Sellos atados a un usuario específico
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_email TEXT,
            timestamp TEXT,
            data_hash TEXT UNIQUE,
            feromona_hmac TEXT,
            FOREIGN KEY(usuario_email) REFERENCES usuarios(email)
        )
    """)
    conn.commit()
    conn.close()

init_corporate_db()

class CorporateAPIHandler(http.server.BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        payload = json.loads(post_data.decode('utf-8'))
        
        # --- HITO 1: REGISTRO Y AUTENTICACIÓN ---
        if self.path == "/api/registro":
            email = payload.get("email", "").strip().lower()
            if not email or "@" not in email:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Correo inválido"}).encode('utf-8'))
                return
                
            conn = sqlite3.connect("hormigasais_borde.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (email, fecha_registro) VALUES (?, ?)", 
                               (email, datetime.datetime.utcnow().isoformat()))
                conn.commit()
                msg = "Usuario registrado. Disfruta de 3 sellos libres."
                sellos_restantes = 3
            except sqlite3.IntegrityError:
                # El usuario ya existe, consultamos cuántos tokens libres le quedan
                cursor.execute("SELECT sellos_gratuitos_restantes, plan_activo FROM usuarios WHERE email = ?", (email,))
                user = cursor.fetchone()
                msg = f"Sesión iniciada. Plan: {user[1]}"
                sellos_restantes = user[0]
            finally:
                conn.close()
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"mensaje": msg, "email": email, "sellos_restantes": sellos_restantes}).encode('utf-8'))

        # --- HITO 2: SELLADO VALIDADO CONTRA CUENTA ---
        elif self.path == "/api/sellar_corporativo":
            email = payload.get("email", "").strip().lower()
            contenido = payload.get("contenido", "").encode('utf-8')
            
            conn = sqlite3.connect("hormigasais_borde.db")
            cursor = conn.cursor()
            
            # Verificar si el usuario existe y tiene saldo/crédito
            cursor.execute("SELECT sellos_gratuitos_restantes, plan_activo FROM usuarios WHERE email = ?", (email,))
            user = cursor.fetchone()
            
            if not user:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Debes registrarte para usar el protocolo"}).encode('utf-8'))
                conn.close()
                return
                
            sellos_restantes, plan = user
            
            if plan == 'FREE' and sellos_restantes <= 0:
                self.send_response(402) # Payment Required
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Límite gratuito alcanzado. Adquiere un Plan Premium."}).encode('utf-8'))
                conn.close()
                return

            # Si pasa las reglas de negocio, ejecutamos la firma criptográfica externa
            sha256_hash = hashlib.sha256(contenido).hexdigest()
            timestamp = datetime.datetime.utcnow().isoformat() + "Z"
            mensaje = f"{sha256_hash}|{timestamp}|{NODE_ID}".encode('utf-8')
            feromona_hmac = hmac.new(NODE_SECRET, mensaje, hashlib.sha256).hexdigest()
            
            try:
                # Insertar el sello atado permanentemente al correo del usuario
                cursor.execute("INSERT INTO sellos (usuario_email, timestamp, data_hash, feromona_hmac) VALUES (?, ?, ?, ?)",
                               (email, timestamp, sha256_hash, feromona_hmac))
                
                # Descontar un sello del balance gratuito si está en plan FREE
                if plan == 'FREE':
                    cursor.execute("UPDATE usuarios SET sellos_gratuitos_restantes = ? WHERE email = ?", 
                                   (sellos_restantes - 1, email))
                
                conn.commit()
                resultado = {
                    "exito": True,
                    "data_hash": sha256_hash,
                    "feromona_lbh": feromona_hmac,
                    "sellos_restantes": (sellos_restantes - 1) if plan == 'FREE' else "Ilimitado"
                }
                self.send_response(200)
            except sqlite3.IntegrityError:
                self.send_response(409)
                resultado = {"error": "Este activo ya ha sido certificado previamente."}
            finally:
                conn.close()
                
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode('utf-8'))

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), CorporateAPIHandler)
    print(f"🐜 Servidor Corporativo HormigasAIS en línea en el puerto {PORT}")
    server.serve_forever()
