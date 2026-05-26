async function initVideoCortex() {
    console.log("🚀 Iniciando motor VIDEO_API heurístico...");
    const videoCont = document.querySelector('.video-container') || document.body;
    
    try {
        const respuesta = await fetch('http://181.78.98.119:5001/video/analizar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: 'ia-test.mp4' })
        });
        const d = await respuesta.json();
        
        // Renderizado del análisis en el flujo de video
        const report = document.createElement('div');
        report.id = "cortex-report";
        report.innerHTML = `<div style="background:#000; color:#0f0; padding:10px; border:1px solid #333;">
            ANALISIS_LBH: ${d.ia_generativa ? 'SINTETICO' : 'HUMANO'} | SCORE: ${d.score_biologico || 0}
        </div>`;
        videoCont.prepend(report);
    } catch(e) {
        console.error("Error en VIDEO_API", e);
    }
}
document.addEventListener('DOMContentLoaded', initVideoCortex);
