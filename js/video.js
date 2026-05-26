async function analizarVideo() {
    const videoUrl = document.getElementById('videoUrlInput')?.value;
    const resDiv = document.getElementById('cortex-report');
    
    if (!videoUrl) {
        alert("Introduce una URL válida");
        return;
    }

    resDiv.innerHTML = "🐜 Analizando feromonas en tiempo real...";

    try {
        // Usamos la IP pública con protocolo explícito
        const response = await fetch('http://181.78.98.119:5001/video/analizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            mode: 'cors' // Necesario para CORS
        }, {
            body: JSON.stringify({ url: videoUrl })
        });

        const d = await response.json();

        resDiv.innerHTML = `
            <div style="margin-top:15px; padding:15px; border:1px solid #444; border-radius:5px; background:#0a0a0a; color:#fff; font-family:monospace;">
                <div style="font-weight:bold; color:${d.ia_generativa ? '#ff4d4d' : '#00ff9f'}">
                    RESULTADO: ${d.ia_generativa ? '⚠️ SINTÉTICO (IA)' : '✅ HUMANO'}
                </div>
                <div style="font-size:0.8rem; margin-top:5px; color:#aaa;">
                    Score Biológico: ${d.score_biologico}/100<br>
                    Varianza: ${d.metricas.varianza_bordes} | Entropía: ${d.metricas.entropia_informacion}
                </div>
            </div>
        `;
    } catch (e) {
        resDiv.innerHTML = `
            <div style="color:#ff4d4d; padding:10px; border:1px solid #ff4d4d;">
                ❌ Error de Conexión. Asegúrate de que el servidor Flask esté corriendo y el firewall permita el puerto 5001.
            </div>
        `;
        console.error("Cortex Error:", e);
    }
}
