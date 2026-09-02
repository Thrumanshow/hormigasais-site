// ================================================================
// 🐜 HormigasAIS — video.js (Versión Soberana Optimizada - URL Mode)
// Nodo A16 - Verificación de Enlaces y Arbitraje de Enjambre
// ================================================================

// Definición de la URL del nodo de borde (Ajustable a producción local o remota)
const API = window.LBH_API_URL || 'http://localhost:8787';

async function leerRespuestaVideo(response) {
  const contentType = (response.headers.get('content-type') || '').toLowerCase();
  let data;

  if (contentType.includes('application/json')) {
    try {
      data = await response.json();
    } catch (_) {
      data = { error: 'El servicio devolvió JSON inválido.' };
    }
  } else {
    await response.text();
    data = {
      error: response.ok
        ? 'El servicio devolvió una respuesta no JSON.'
        : 'El servicio devolvió un error no JSON (HTTP ' + response.status + ').'
    };
  }

  if (!data || typeof data !== 'object') {
    data = { error: 'El servicio devolvió un formato de respuesta inválido.' };
  }

  if (!response.ok && !data.error) {
    data.error = 'El servicio rechazó el análisis (HTTP ' + response.status + ').';
  }

  return data;
}

document.addEventListener('DOMContentLoaded', function() {
  const sec = document.getElementById('video');
  if (!sec) return;

  sec.innerHTML = `
    <div style="max-width:680px;margin:0 auto;">

      <!-- HEADER -->
      <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#fff;margin-bottom:0.3rem;">👁️ Video Intelligence (Nodo A16)</div>
      <p style="color:#555;font-size:0.78rem;margin-bottom:0.3rem;">Análisis de consistencia biológica y arbitraje de agentes descentralizados</p>
      <div style="background:rgba(0,255,159,0.06);border:1px solid rgba(0,255,159,0.15);border-radius:6px;padding:0.6rem 1rem;font-size:0.72rem;color:#00ff9f;margin-bottom:2rem;">
        🐜 Protocolo LBH Activo — Optimizado para Edge Computing (Solo URLs / Cero Binarios Pesados)
      </div>

      <!-- INPUT URL -->
      <div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1.5rem;">
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;display:block;margin-bottom:0.5rem;">
          ENLACE_DE_VIDEO_A_VERIFICAR (INSTAGRAM / YOUTUBE)
        </label>
        <div style="display:flex;gap:0.8rem;">
          <input type="url" id="videoUrlInput"
            placeholder="https://www.instagram.com/reel/... o https://youtube.com/watch?v=..."
            style="flex:1;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.8rem;outline:none;"
            onkeydown="if(event.key==='Enter') analizarVideo()">
          <button onclick="analizarVideo()" id="btnAnalizar"
            style="background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.3);color:#38bdf8;font-family:'Space Mono',monospace;font-size:0.78rem;font-weight:700;padding:0.8rem 1.2rem;border-radius:6px;cursor:pointer;white-space:nowrap;transition:all 0.2s;"
            onmouseover="this.style.background='rgba(56,189,248,0.2)'" onmouseout="this.style.background='rgba(56,189,248,0.1)'">
            ANALIZAR
          </button>
        </div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.8rem;">
          ${['Instagram Reels', 'YouTube'].map(p =>
            `<span style="background:#111;border:1px solid #222;border-radius:4px;padding:0.2rem 0.6rem;font-size:0.65rem;color:#555;">✅ ${p}</span>`
          ).join('')}
        </div>
      </div>

      <!-- ORÁCULO -->
      <div id="oraculoPanel" style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:2rem;text-align:center;min-height:280px;display:flex;flex-direction:column;align-items:center;justify-content:center;">

        <!-- Círculo indicador -->
        <div id="oraculoCircle" style="width:90px;height:90px;border-radius:50%;background:#111;border:3px solid #2a2a2a;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;transition:all 0.4s;">
          👁️
        </div>

        <div id="oraculoStatus" style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#555;margin-bottom:0.5rem;">
          Esperando rastro de enlace...
        </div>
        <div id="oraculoSub" style="font-size:0.75rem;color:#444;line-height:1.6;max-width:400px;">
          Inserta un enlace de video para que los agentes especialistas del Nodo A16 evalúen su consistencia.
        </div>

        <!-- Score bar -->
        <div id="scoreContainer" style="display:none;width:100%;max-width:400px;margin-top:1.5rem;">
          <div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#555;margin-bottom:0.4rem;">
            <span>🤖 Sintético (IA)</span>
            <span id="scoreText">0%</span>
            <span>👤 Orgánico (Humano)</span>
          </div>
          <div style="background:#0a0a0a;border-radius:999px;height:8px;overflow:hidden;">
            <div id="scoreBar" style="height:100%;border-radius:999px;transition:width 0.8s;background:var(--verde);width:0%;"></div>
          </div>
        </div>

        <!-- Feromona LBH -->
        <div id="feromonaPanel" style="display:none;background:#0a0a0a;border:1px solid #222;border-radius:8px;padding:1rem;margin-top:1.5rem;width:100%;max-width:500px;text-align:left;">
          <div style="font-size:0.62rem;color:#555;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">FEROMONA_EMITIDA:</div>
          <pre id="feromonaData" style="font-size:0.68rem;color:#aaa;font-family:'Space Mono',monospace;overflow-x:auto;white-space:pre-wrap;margin:0;"></pre>
        </div>

      </div>

      <!-- NOTA LEGAL -->
      <div style="margin-top:1.5rem;font-size:0.7rem;color:#333;text-align:center;line-height:1.8;">
        Infraestructura distribuida y soberana basada en agentes autónomos.<br>
        Nodo A16, San Miguel, El Salvador.<br>
        <span style="color:#222;">© 2026 HormigasAIS — Framework LBH</span>
      </div>

    </div>
  `;
});

async function analizarVideo() {
  const url = document.getElementById('videoUrlInput').value.trim();
  if (!url || !url.startsWith('http')) {
    alert('Ingresa una URL de video válida (ej. Instagram Reel)');
    return;
  }

  const btn = document.getElementById('btnAnalizar');
  const circle = document.getElementById('oraculoCircle');
  const status = document.getElementById('oraculoStatus');
  const sub = document.getElementById('oraculoSub');
  const score = document.getElementById('scoreContainer');
  const feromona = document.getElementById('feromonaPanel');

  btn.textContent = '⏳ Analizando...';
  btn.disabled = true;
  circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(245,197,24,0.1);border:3px solid #f5c518;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;animation:pulsoVideo 1.5s infinite;';
  circle.textContent = '📡';
  status.style.color = '#f5c518';
  status.textContent = 'Agentes analizando enlace...';
  sub.textContent = 'Consultando matriz de pesos y rastros en el Nodo A16.';
  score.style.display = 'none';
  feromona.style.display = 'none';

  try {
    const r = await fetch("https://a16.hormigasais.com/video/analizar", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await leerRespuestaVideo(r);

    if (data.error) {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(255,68,68,0.1);border:3px solid #ff4444;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;';
      circle.textContent = '⚠️';
      status.style.color = '#ff4444';
      status.textContent = 'Error en el arbitraje';
      sub.textContent = data.error;
      return;
    }

    const esHumano = data.es_humano;
    const score_val = data.score_biologico || data.score || 0;

    if (esHumano) {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(0,255,159,0.15);border:3px solid #00ff9f;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;box-shadow:0 0 20px rgba(0,255,159,0.3);';
      circle.textContent = '👤';
      status.style.color = '#00ff9f';
      status.textContent = 'ORGANICO (HUMANO CONFIRMADO)';
      sub.textContent = data.clasificacion || 'Veredicto armonizado: Consenso biológico validado.';
    } else {
      circle.style.cssText = 'width:90px;height:90px;border-radius:50%;background:rgba(255,68,68,0.15);border:3px solid #ff4444;display:flex;align-items:center;justify-content:center;font-size:2rem;margin-bottom:1.2rem;box-shadow:0 0 20px rgba(255,68,68,0.3);';
      circle.textContent = '🤖';
      status.style.color = '#ff4444';
      status.textContent = 'SINTETICO_IA DETECTADO';
      sub.textContent = data.clasificacion || 'Alerta: Anomalías confirmadas por subagentes de IA.';
    }

    score.style.display = 'block';
    document.getElementById('scoreText').textContent = score_val + '%';
    const bar = document.getElementById('scoreBar');
    bar.style.width = score_val + '%';
    bar.style.background = esHumano ? '#00ff9f' : '#ff4444';

    if (data.feromona) {
      feromona.style.display = 'block';
      document.getElementById('feromonaData').textContent = JSON.stringify(data.feromona, null, 2);
    }

  } catch(e) {
    circle.textContent = '⚠️';
    status.style.color = '#ff4444';
    status.textContent = 'Error de conexión';
    sub.textContent = 'El Nodo A16 local no responde en el puerto 8787.';
  } finally {
    btn.textContent = 'ANALIZAR';
    btn.disabled = false;
  }
}

// CSS animación
const videoStyle = document.createElement('style');
videoStyle.textContent = `
@keyframes pulsoVideo {
  0% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.05); opacity: 1; }
  100% { transform: scale(1); opacity: 0.8; }
}
`;
document.head.appendChild(videoStyle);
