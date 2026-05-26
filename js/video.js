// ================================================================
// 🐜 HormigasAIS — video.js
// Video Intelligence Checker — Análisis biológico de videos
// Compatible con YouTube, TikTok, Instagram, MP4 y más
// ================================================================

document.addEventListener('DOMContentLoaded', function() {
// CONFIGURACIÓN DE NODO A16
  const API_URL = 'https://hormigasaisa16.share.zrok.io/video/analizar';
  console.log('Nodo A16 listo, apuntando a:', API_URL);
  const sec = document.getElementById('video');
  if (!sec) return;

  sec.innerHTML = `
    <div style="max-width:680px;margin:0 auto;">

      <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#fff;margin-bottom:0.3rem;">👁️ Video Intelligence</div>
      <p style="color:#555;font-size:0.78rem;margin-bottom:0.3rem;">Análisis de consistencia biológica — Detector de IA generativa</p>
      <div style="background:rgba(0,255,159,0.06);border:1px solid rgba(0,255,159,0.15);border-radius:6px;padding:0.6rem 1rem;font-size:0.72rem;color:#00ff9f;margin-bottom:2rem;">
        🆓 Servicio gratuito — YouTube · TikTok · Instagram · MP4 y más
      </div>

      <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;display:block;margin-bottom:0.5rem;">
          LINK_DE_VIDEO_A_VERIFICAR
        </label>
        <div style="display:flex;gap:0.8rem;">
          <input type="url" id="videoUrlInput"
            placeholder="https://youtube.com/watch?v=... o cualquier URL de video"
            style="flex:1;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.8rem;outline:none;"
            onkeydown="if(event.key==='Enter') analizarVideo()">
          <button onclick="analizarVideo()" id="btnAnalizar"
            style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;font-family:'Space Mono',monospace;font-size:0.78rem;font-weight:700;padding:0.8rem 1.2rem;border-radius:6px;cursor:pointer;white-space:nowrap;transition:all 0.2s;"
            onmouseover="this.style.background='rgba(56,189,248,0.2)'" onmouseout="this.style.background='rgba(56,189,248,0.1)'">
            ANALIZAR
          </button>
        </div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
          ${['YouTube','TikTok','Instagram','Twitter/X','MP4 directo','Facebook'].map(p =>
            `<span style="background:#111;border:1px solid #222;border-radius:4px;padding:0.2rem 0.6rem;font-size:0.65rem;color:#555;">✅ ${p}</span>`
          ).join('')}
        </div>
      </div>

      <div id="oraculoPanel" style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:2rem;text-align:center;min-height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;">

        <div id="oraculoCircle" style="width:90px;height:90px;border-radius:50%;background:#111;border:3px solid #2a2a2a;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;transition:all 0.4s;">
          👁️
        </div>

        <div id="oraculoStatus" style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#555;margin-bottom:0.5rem;">
          Esperando rastro de video...
        </div>
        <div id="oraculoSub" style="font-size:0.75rem;color:#444;line-height:1.6;max-width:400px;">
          Inserta un link para que el nodo A16 analice su estructura biológica.
        </div>

        <div id="scoreContainer" style="display:none;width:100%;max-width:400px;margin-top:1.5rem;">
          <div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#555;margin-bottom:0.4rem;">
            <span>🤖 IA Generativa</span>
            <span id="scoreText">0%</span>
            <span>👤 Humano</span>
          </div>
          <div style="background:#0a0a0a;border-radius:999px;height:8px;overflow:hidden;">
            <div id="scoreBar" style="height:100%;border-radius:999px;transition:width 0.8s;background:var(--verde);width:0%;"></div>
          </div>
        </div>

        <div id="feromonaPanel" style="display:none;background:#0a0a0a;border:1px solid #222;border-radius:8px;padding:1rem;margin-top:1.5rem;width:100%;max-width:500px;text-align:left;">
          <div style="font-size:0.62rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">FEROMONA_EMITIDA:</div>
          <pre id="feromonaData" style="font-size:0.68rem;color:#aaa;font-family:'Space Mono',monospace;overflow-x:auto;white-space:pre-wrap;margin:0;"></pre>
        </div>

        <div id="metadatosPanel" style="display:none;width:100%;max-width:500px;margin-top:1rem;text-align:left;"></div>

      </div>

      <div style="margin-top:1.5rem;font-size:0.7rem;color:#333;text-align:center;line-height:1.8;">
        Este servicio gratuito es una capa externa de la Inteligencia Estructural de la Colonia HormigasAIS.<br>
        Ejecutada de manera descentralizada desde el Nodo A16, San Miguel, El Salvador.<br>
        <span style="color:#222;">© 2026 HormigasAIS — Framework Legal LBH-SYS-004</span>
      </div>

    </div>
  `;
});

async function analizarVideo() {
  const API = 'https://hormigasaisa16.share.zrok.io/video/analizar';
  const url = document.getElementById('videoUrlInput').value.trim();
  if (!url || !url.startsWith('http')) {
    alert('Ingresa una URL válida de video');
    return;
  }

  // UI: procesando
  const btn = document.getElementById('btnAnalizar');
  const circle = document.getElementById('oraculoCircle');
  const status = document.getElementById('oraculoStatus');
  const sub = document.getElementById('oraculoSub');
  const score = document.getElementById('scoreContainer');
  const feromona = document.getElementById('feromonaPanel');
  const meta = document.getElementById('metadatosPanel');

  btn.textContent = '⏳ Analizando...';
  btn.disabled = true;
  circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(245,197,24,0.1);border:3px solid var(--amarillo);display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;transition:all 0.4s;animation:pulsoVideo 1.5s infinite;';
  circle.textContent = '📡';
  status.style.color = '#f5c518';
  status.textContent = 'Nodo A16 analizando...';
  sub.textContent = 'Descargando y procesando estructura biológica del video. Esto puede tomar 30-60 segundos.';
  score.style.with = '0%';
  score.style.display = 'none';
  feromona.style.display = 'none';
  meta.style.display = 'none';

  try {
    const r = await fetch(API + '/video/analizar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await r.json();

    if (data.error) {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(255,68,68,0.1);border:3px solid #ff4444;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;';
      circle.textContent = '⚠️';
      status.style.color = '#ff4444';
      status.textContent = 'Error en el análisis';
      sub.textContent = data.error;
      return;
    }

    const esHumano = data.es_humano;
    const score_val = data.score_biologico !== undefined ? data.score_biologico : 0;

        // Actualizar interfaz según el veredicto unificado
    // Si ia_generativa es false, entonces es Humano
    const esHumanoVideo = !data.ia_generativa; 

    if (esHumanoVideo) {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(0,255,159,0.15);border:3px solid var(--verde);display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;box-shadow:0 0 20px rgba(0,255,159,0.3);';
      circle.textContent = '👤';
      status.style.color = '#00ff9f';
      status.textContent = 'PRESENCIA HUMANA CONFIRMADA';
      sub.textContent = 'Video verificado con éxito. Cumple con la firma biológica y estructural de la Capa 0.';
    } else {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(255,68,68,0.15);border:3px solid #ff4444;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;box-shadow:0 0 20px rgba(255,68,68,0.3);';
      circle.textContent = '🤖';
      status.style.color = '#ff4444';
      status.textContent = 'POSIBLE IA GENERATIVA DETECTADA';
      sub.textContent = 'Se detectaron patrones sintéticos inconsistentes con captura óptica humana real.';
    }

    // Score bar animada
    score.style.display = 'block';
    document.getElementById('scoreText').textContent = score_val + '%';
    const bar = document.getElementById('scoreBar');
    bar.style.width = score_val + '%';
    bar.style.background = score_val >= 55 ? 'var(--verde)' : score_val >= 35 ? 'var(--amarillo)' : '#ff4444';

    // Inyección de Feromona LBH limpia
    if (data.feromona) {
      feromona.style.display = 'block';
      document.getElementById('feromonaData').textContent = JSON.stringify(data.feromona, null, 2);
    }

    // Renderizar metadatos y métricas de OpenCV reales
    if (data.metricas) {
      const m = data.metadatos || {};
      meta.style.display = 'block';
      meta.innerHTML = `
        <div style="font-size:0.62rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">METADATOS DEL VIDEO:</div>
        <div style="display:grid;gap:0.3rem;">
          ${row('Título', m.titulo || 'Archivo directo / Sin Título')}
          ${row('Plataforma', m.plataforma || 'Capa perimetral (generic)')}
          ${row('Duración', m.duracion ? Math.floor(m.duracion/60) + 'min ' + (m.duracion%60) + 's' : 'Temporal / Corto')}
          ${row('Resolución', data.metricas.resolucion || '—')}
          ${row('Frames analizados', data.metricas.frames_analizados || '—')}
          ${row('Fluctuación bordes', data.metricas.fluctuacion_bordes || '—')}
        </div>
      `;
    }

  } catch(e) {
    circle.textContent = '⚠️';
    status.style.color = '#ff4444';
    status.textContent = 'Error de conexión';
    sub.textContent = 'El nodo A16 no está disponible o el JSON es inválido. Revisa la consola.';
    console.error(e);
  } finally {
    btn.textContent = 'ANALIZAR';
    btn.disabled = false;
  }
}

function row(k, v) {
  return `<div style="display:flex;justify-content:space-between;padding:0.3rem 0;border-bottom:1px solid #111;font-size:0.72rem;"><span style="color:#555;">${k}</span><span style="color:#aaa;">${v}</span></div>`;
}

// CSS animación del oráculo
const videoStyle = document.createElement('style');
videoStyle.textContent = `
@keyframes pulsoVideo {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 0.8; }
}
`;
document.head.appendChild(videoStyle);



// ================================================================
// 🧠 Estado interno del Cortex LBH
// ================================================================

async function checkVideoCortex() {

  const txt = document.getElementById('videoCortexText');
  const dot = document.getElementById('videoCortexDot');

  if (!txt || !dot) return;

  try {

    const r = await fetch(API + '/health');
    const data = await r.json();

    if (data.status === 'ok') {

      txt.textContent = '🟢 Nodo A16 Online';
      txt.style.color = '#00ff9f';

      dot.style.background = '#00ff9f';
      dot.style.boxShadow = '0 0 18px #00ff9f';

    } else {

      txt.textContent = '⚠️ Nodo responde parcialmente';
      txt.style.color = '#f5c518';

      dot.style.background = '#f5c518';
      dot.style.boxShadow = '0 0 18px #f5c518';
    }

  } catch(e) {

    txt.textContent = '🔴 Nodo A16 desconectado';
    txt.style.color = '#ff4444';

    dot.style.background = '#ff4444';
    dot.style.boxShadow = '0 0 18px #ff4444';
  }
}

setTimeout(checkVideoCortex, 1200);
