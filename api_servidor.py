from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# CARGA DIFERIDA: Solo importamos cv2 cuando se solicita el análisis
def get_cv2():
    try:
        import cv2
        return cv2
    except AttributeError:
        # Si falla el import interno, retornamos un objeto simulado para evitar crash
        return None

def analizar_consistencia(video_path):
    cv2 = get_cv2()
    if cv2 is None:
        return {"error": "OpenCV no pudo ser cargado en este entorno"}

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "No se pudo acceder al recurso"}

    varianzas = []
    for _ in range(3):
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        varianzas.append(cv2.Laplacian(gray, cv2.CV_64F).var())

    cap.release()
    avg_var = np.mean(varianzas) if varianzas else 0
    score = int(min(avg_var / 500, 1.0) * 100)
    
    return {
        "es_humano": score > 50,
        "score_biologico": score
    }

@app.route('/video/analizar', methods=['POST'])
def analizar_video():
    data = request.json
    return jsonify(analizar_consistencia(data.get('url', '')))

if __name__ == '__main__':
    # Arrancamos el servidor primero. 
    # El import de cv2 solo ocurrirá cuando alguien envíe un video.
    app.run(host='0.0.0.0', port=5001)
