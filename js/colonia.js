async function ejecutarTestCortex() {
    const contenedor = document.getElementById('estadoHormigaWeb');
    if (!contenedor) return;

    try {
        const respuesta = await fetch('http://181.78.98.119:5001/video/analizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: 'ia-test.mp4' })
        });
        
        const d = await respuesta.json();
        
        contenedor.innerHTML = `
            <div style="border:1px solid #444; padding:15px; border-radius:8px; background:#0a0a0a; color:#fff; font-family:sans-serif; animation: fadeIn 0.5s;">
                <div style="font-size:0.9rem; font-weight:bold; color:${d.ia_generativa ? '#ff4d4d' : '#00ff9f'};">
                    ${d.ia_generativa ? '⚠️ SINTÉTICO (IA)' : '✅ HUMANO'}
                </div>
                <div style="font-size:0.7rem; color:#aaa; margin-top:5px;">
                    Score: ${d.score_biologico}/100 | Entropía: ${d.metricas.entropia_informacion}
                </div>
            </div>
        `;
    } catch (e) {
        contenedor.innerHTML = `
            <div style="border:1px solid #550000; padding:10px; color:white; font-size:0.7rem;">
                ❌ Cortex A16 desconectado. Error de red (Bloqueo HTTPS/CORS).
            </div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', ejecutarTestCortex);
