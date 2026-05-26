// ================================================================
// 🐜 HormigasAIS — colonia.js
// Dashboard colonia + panel admin auditoría
// ================================================================

function estadoColor(estado) {
  return { ACTIVO:'#00ff9f', DEGRADADO:'#f5c518', CRITICO:'#ff4444', INACTIVO:'#555' }[estado] || '#aaa';
}

function trustBar(trust) {
  const pct = Math.round(parseFloat(trust)*100);
  const color = pct>=70?'#00ff9f':pct>=40?'#f5c518':'#ff4444';
  return '<div style="background:#0a0a0a;border-radius:999px;height:6px;margin-top:4px;overflow:hidden;"><div style="width:'+pct+'%;height:100%;background:'+color+';border-radius:999px;transition:width 0.5s;"></div></div>';
}

async function cargarColoniaPublica() {
  const consensoEl = document.getElementById('consensoPublico');
  const nodosEl = document.getElementById('nodosPublicos');
  if (!consensoEl) return;
  try {
    const r = await fetch(API + '/colonia');
    const d = await r.json();
    const res = d.resumen || {};
    const consensoColor = { ACEPTAR:'#00ff9f', REVISAR:'#f5c518', RECHAZAR:'#ff4444' }[res.consenso] || '#aaa';
    consensoEl.innerHTML =
      '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#222;border-radius:8px;overflow:hidden;">' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:'+consensoColor+'">'+(res.consenso||'—')+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.3rem;text-transform:uppercase;">Consenso</div></div>' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+(res.nodos_activos||0)+'/'+(res.total_nodos||0)+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.3rem;text-transform:uppercase;">Nodos activos</div></div>' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+(res.total_sellos||0)+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.3rem;text-transform:uppercase;">Sellos</div></div>' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+parseFloat(res.trust_promedio||0).toFixed(2)+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.3rem;text-transform:uppercase;">Trust promedio</div></div>' +
      '</div>';
    if (!nodosEl) return;
    const nodos = d.nodos || [];
    if (nodos.length === 0) { nodosEl.innerHTML = '<div style="text-align:center;color:#333;font-size:0.8rem;padding:1rem;">Sin nodos registrados</div>'; return; }
    let html = '<div style="font-family:Syne,sans-serif;font-size:0.85rem;font-weight:700;color:#fff;margin-bottom:0.8rem;">Nodos de la colonia</div>';
    html += '<div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;overflow:hidden;">';
    html += '<div style="display:grid;grid-template-columns:1fr 80px 100px 80px;gap:0.5rem;padding:0.6rem 1rem;background:#111;font-size:0.65rem;color:#444;text-transform:uppercase;letter-spacing:0.06em;"><span>Nodo</span><span>Estado</span><span>Trust</span><span>Actividad</span></div>';
    nodos.forEach(n => {
      const color = estadoColor(n.estado);
      html += '<div style="display:grid;grid-template-columns:1fr 80px 100px 80px;gap:0.5rem;padding:0.7rem 1rem;border-top:1px solid #222;align-items:center;">' +
        '<span style="font-size:0.78rem;color:#aaa;">'+n.id+'</span>' +
        '<span style="font-size:0.7rem;color:'+color+';font-weight:700;">'+n.estado+'</span>' +
        '<div><div style="font-size:0.75rem;color:'+color+'">'+Math.round(parseFloat(n.trust)*100)+'%</div>'+trustBar(n.trust)+'</div>' +
        '<span style="font-size:0.7rem;color:#555;">'+n.ultima+'</span>' +
        '</div>';
    });
    html += '</div>';
    nodosEl.innerHTML = html;
  } catch(e) {
    if (consensoEl) consensoEl.innerHTML = '<div style="text-align:center;color:#555;font-size:0.8rem;">⚠️ No se pudo conectar con el nodo A16</div>';
  }
}

async function cargarColoniaAdmin() {
  const key = document.getElementById('coloniaAdminKey') ? document.getElementById('coloniaAdminKey').value.trim() : '';
  if (!key) { alert('Ingresa tu clave admin'); return; }
  const panel = document.getElementById('coloniaAdminData');
  if (!panel) return;
  panel.innerHTML = '<div style="color:#555;font-size:0.75rem;">Cargando...</div>';
  try {
    const r = await fetch(API + '/colonia?key=' + encodeURIComponent(key));
    const d = await r.json();
    if (d.error) { panel.innerHTML = '<div style="color:#ff4444;font-size:0.75rem;">❌ '+d.error+'</div>'; return; }
    let html = '<div style="font-size:0.75rem;color:#00ff9f;margin-bottom:0.8rem;">✅ Acceso admin</div>';
    (d.nodos||[]).forEach(n => {
      const color = estadoColor(n.estado);
      html += '<div style="background:#0a0a0a;border:1px solid #222;border-radius:6px;padding:0.8rem;margin-bottom:0.5rem;">' +
        '<div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">' +
        '<span style="font-size:0.78rem;color:#fff;font-weight:700;">'+n.id+'</span>' +
        '<span style="font-size:0.7rem;color:'+color+'">'+n.estado+'</span></div>' +
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.5rem;">' +
        '<div style="font-size:0.68rem;"><span style="color:#444">trust:</span> <span style="color:#f5c518">'+n.trust+'</span></div>' +
        '<div style="font-size:0.68rem;"><span style="color:#444">value:</span> <span style="color:#aaa">'+(n.value||'—')+'</span></div>' +
        '<div style="font-size:0.68rem;"><span style="color:#444">type:</span> <span style="color:#aaa">'+(n.type||'—')+'</span></div>' +
        '</div><div style="font-size:0.65rem;color:#333;margin-top:0.3rem;">'+(n.timestamp||'')+'</div></div>';
    });
    panel.innerHTML = html;
  } catch(e) { panel.innerHTML = '<div style="color:#ff4444;font-size:0.75rem;">⚠️ Error</div>'; }
}

// Admin auditoría
async function cargarAuditoria(tipo) {
  const key = document.getElementById('auditKey') ? document.getElementById('auditKey').value.trim() : '';
  if (!key) { alert('Ingresa tu clave de auditoría'); return; }
  const panel = document.getElementById('auditPanel');
  if (!panel) return;
  panel.innerHTML = '<div style="text-align:center;color:#f5c518;padding:2rem;font-size:0.8rem;">📡 Sincronizando...</div>';
  try {
    let url = API + '/audit?limit=50&key=' + encodeURIComponent(key);
    if (tipo) url += '&tipo=' + tipo;
    const r = await fetch(url);
    const data = await r.json();
    if (data.error) { panel.innerHTML = '<div style="color:#ff4444;text-align:center;padding:1rem;">❌ '+data.error+'</div>'; return; }
    const colors = { SEAL_EMITIDO:'#f5c518', SEAL_VERIFICADO:'#00ff9f', SEAL_ERROR:'#ff4444', AUDIT_ACCESO_DENEGADO:'#ff4444', VERIFY:'#4a9eff', VISIT:'#666', FEROMONA_PUSH:'#a855f7', CLIENTE_REGISTRADO:'#00ff9f', CLIENTE_LOGIN:'#4a9eff', XOXO_GIFT_CREADO:'#f5c518', XOXO_GIFT_CANJEADO:'#00ff9f' };
    const rows = (data.eventos||[]).map(e => {
      const color = colors[e.tipo] || '#aaa';
      return '<div style="display:grid;grid-template-columns:140px 160px 1fr;gap:0.5rem;padding:0.6rem 0;border-bottom:1px solid #1a1a1a;font-size:0.72rem;">' +
        '<span style="color:'+color+'">'+e.tipo+'</span>' +
        '<span style="color:#555">'+new Date(e.ts).toLocaleString()+'</span>' +
        '<span style="color:#888">'+(e.owner||e.signature||e.path||e.node||e.email||'')+(e.plan?' ['+e.plan+']':'')+(e.pais&&e.pais!=='unknown'?' 🌍'+e.pais:'')+'</span></div>';
    }).join('');
    panel.innerHTML = '<div style="display:flex;justify-content:space-between;margin-bottom:1rem;"><span style="color:#aaa;font-size:0.78rem;">Total: <strong style="color:#f5c518">'+data.total+'</strong></span></div>' +
      '<div style="display:grid;grid-template-columns:140px 160px 1fr;gap:0.5rem;padding:0.4rem 0;border-bottom:1px solid #333;font-size:0.65rem;color:#444;text-transform:uppercase;letter-spacing:0.06em;"><span>Tipo</span><span>Fecha/Hora</span><span>Detalle</span></div>' + rows;
  } catch(e) { panel.innerHTML = '<div style="color:#ff4444;text-align:center;">⚠️ Error de conexión</div>'; }
}

function filtrarAudit(tipo) { cargarAuditoria(tipo); }

async function cargarStats() {
  const key = document.getElementById('auditKey') ? document.getElementById('auditKey').value.trim() : '';
  if (!key) { alert('Ingresa tu clave'); return; }
  const statsPanel = document.getElementById('statsPanel');
  if (!statsPanel) return;
  statsPanel.style.display = 'block';
  statsPanel.innerHTML = 'Cargando stats...';
  try {
    const r = await fetch(API + '/audit/stats?key=' + encodeURIComponent(key));
    const data = await r.json();
    if (data.error) { statsPanel.innerHTML = '<span style="color:#ff4444">'+data.error+'</span>'; return; }
    const s = data.stats;
    const tiposHtml = Object.entries(s.por_tipo||{}).sort((a,b)=>b[1]-a[1])
      .map(([tipo,cnt]) => '<span style="color:#aaa;font-size:0.75rem;">'+tipo+': <strong style="color:#f5c518">'+cnt+'</strong></span>').join(' · ');
    statsPanel.innerHTML = '<div style="font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#00ff9f;margin-bottom:0.8rem;">📊 Estadísticas del Nodo A16</div>' +
      '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem;">' +
      '<div style="text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+s.total_sellos+'</div><div style="font-size:0.65rem;color:#555">SELLOS</div></div>' +
      '<div style="text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+s.total_eventos+'</div><div style="font-size:0.65rem;color:#555">EVENTOS</div></div>' +
      '<div style="text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+(s.total_clientes||0)+'</div><div style="font-size:0.65rem;color:#555">CLIENTES</div></div>' +
      '</div><div style="display:flex;flex-wrap:wrap;gap:0.8rem;">'+tiposHtml+'</div>';
  } catch(e) { statsPanel.innerHTML = '<span style="color:#ff4444">Error de conexión</span>'; }
}

// ── EMAIL SOBERANO desde Admin ────────────────────────────────
function mostrarComposer() {
  const panel = document.getElementById('auditPanel');
  if (!panel) return;
  const key = document.getElementById('auditKey') ? document.getElementById('auditKey').value.trim() : '';
  if (!key) {
    panel.innerHTML = '<div style="color:#ff4444;font-size:0.78rem;padding:1rem;text-align:center;">⚠️ Ingresa tu clave admin primero y haz clic en Acceder</div>';
    return;
  }

  panel.innerHTML = `
    <div style="font-family:'Syne',sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:1.2rem;">
      📧 Enviar correo soberano
      <span style="font-size:0.7rem;color:#555;font-family:'Space Mono',monospace;font-weight:400;margin-left:0.5rem;">desde clhq@hormigasais.com</span>
    </div>

    <div style="display:grid;gap:0.8rem;margin-bottom:1rem;">
      <div>
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.06em;display:block;margin-bottom:0.3rem;">Para</label>
        <input type="email" id="emailPara" placeholder="destinatario@email.com"
          style="width:100%;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.7rem 0.9rem;outline:none;">
      </div>
      <div>
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.06em;display:block;margin-bottom:0.3rem;">Nombre destinatario (opcional)</label>
        <input type="text" id="emailNombre" placeholder="Nombre del destinatario"
          style="width:100%;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.7rem 0.9rem;outline:none;">
      </div>
      <div>
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.06em;display:block;margin-bottom:0.3rem;">Asunto</label>
        <input type="text" id="emailAsunto" placeholder="Asunto del correo"
          style="width:100%;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.7rem 0.9rem;outline:none;">
      </div>
      <div>
        <label style="font-size:0.65rem;color:#555;text-transform:uppercase;letter-spacing:0.06em;display:block;margin-bottom:0.3rem;">Mensaje</label>
        <textarea id="emailMensaje" placeholder="Escribe tu mensaje aquí..." rows="6"
          style="width:100%;background:#0a0a0a;border:1px solid #333;border-radius:6px;color:#e8e8e8;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.7rem 0.9rem;outline:none;resize:vertical;line-height:1.6;"></textarea>
      </div>
    </div>

    <div style="display:flex;gap:0.8rem;">
      <button onclick="enviarEmailSoberano('${key}')"
        style="flex:1;background:var(--amarillo);color:#0a0a0a;border:none;font-family:'Space Mono',monospace;font-size:0.82rem;font-weight:700;padding:0.9rem;border-radius:8px;cursor:pointer;">
        📧 Enviar desde clhq@hormigasais.com
      </button>
      <button onclick="cargarAuditoria()"
        style="background:#1a1a1a;border:1px solid #333;color:#aaa;font-family:'Space Mono',monospace;font-size:0.78rem;padding:0.9rem 1rem;border-radius:8px;cursor:pointer;">
        ✕ Cancelar
      </button>
    </div>

    <div id="emailResult" style="margin-top:1rem;"></div>
  `;
}

async function enviarEmailSoberano(key) {
  const para    = document.getElementById('emailPara') ? document.getElementById('emailPara').value.trim() : '';
  const nombre  = document.getElementById('emailNombre') ? document.getElementById('emailNombre').value.trim() : '';
  const asunto  = document.getElementById('emailAsunto') ? document.getElementById('emailAsunto').value.trim() : '';
  const mensaje = document.getElementById('emailMensaje') ? document.getElementById('emailMensaje').value.trim() : '';
  const result  = document.getElementById('emailResult');

  if (!para || !asunto || !mensaje) {
    if (result) result.innerHTML = '<div style="color:#ff4444;font-size:0.78rem;">⚠️ Completa Para, Asunto y Mensaje</div>';
    return;
  }

  const btn = document.querySelector('#auditPanel button');
  if (btn) { btn.textContent = '⏳ Enviando...'; btn.disabled = true; }

  try {
    const r = await fetch(API + '/email/enviar?key=' + encodeURIComponent(key), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ para, asunto, mensaje, nombre_destinatario: nombre })
    });
    const d = await r.json();

    if (result) {
      if (d.status === 'EMAIL_ENVIADO') {
        result.innerHTML =
          '<div style="background:rgba(0,255,159,0.04);border:1px solid rgba(0,255,159,0.2);border-radius:8px;padding:1rem;">' +
          '<div style="color:#00ff9f;font-weight:700;font-size:0.82rem;margin-bottom:0.5rem;">✅ Email enviado exitosamente</div>' +
          '<div style="font-size:0.72rem;color:#aaa;line-height:1.8;">' +
          '<div>Para: <strong style="color:#fff">' + para + '</strong></div>' +
          '<div>Asunto: ' + asunto + '</div>' +
          '<div style="color:#555;font-size:0.65rem;margin-top:0.3rem;">Resend ID: ' + (d.resend_id || '—') + '</div>' +
          '<div style="color:#555;font-size:0.65rem;">' + new Date(d.timestamp).toLocaleString() + '</div>' +
          '</div></div>';
      } else {
        result.innerHTML =
          '<div style="background:rgba(255,68,68,0.06);border:1px solid rgba(255,68,68,0.2);border-radius:8px;padding:1rem;color:#ff4444;font-size:0.78rem;">' +
          '❌ Error: ' + (d.error || JSON.stringify(d)) + '</div>';
      }
    }
  } catch(e) {
    if (result) result.innerHTML = '<div style="color:#ff4444;font-size:0.78rem;">⚠️ Error de conexión</div>';
  }

  const btnFinal = document.querySelector('#auditPanel button');
  if (btnFinal) { btnFinal.textContent = '📧 Enviar desde clhq@hormigasais.com'; btnFinal.disabled = false; }
}

// Agregar botón Email al panel Admin cuando se autentica
const _origCargarAuditoria = typeof cargarAuditoria !== 'undefined' ? cargarAuditoria : null;
function inyectarBotonEmail() {
  const statsPanel = document.getElementById('statsPanel');
  if (!statsPanel) return;
  if (document.getElementById('btnEmailComposer')) return;

  const btnEmail = document.createElement('button');
  btnEmail.id = 'btnEmailComposer';
  btnEmail.onclick = mostrarComposer;
  btnEmail.style.cssText = 'background:#1a1a1a;border:1px solid rgba(245,197,24,0.3);color:var(--amarillo);font-family:Space Mono,monospace;font-size:0.7rem;padding:0.4rem 0.8rem;border-radius:4px;cursor:pointer;margin-left:0.5rem;';
  btnEmail.textContent = '📧 Enviar email';

  const filtersDiv = statsPanel.previousElementSibling;
  if (filtersDiv) filtersDiv.appendChild(btnEmail);
}

// ── HORMIGA DE WEB — Estado vivo en Colonia ──────────────────
function iniciarHormigaDeWeb() {
  const contenedor = document.getElementById('estadoHormigaWeb');
  if (!contenedor) return;
  async function actualizar() {
    try {
      const r = await fetch('/js/estado_hormiga.json?t=' + Date.now());
      const d = await r.json();
      contenedor.innerHTML =
        '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">' +
        '<div style="width:8px;height:8px;border-radius:50%;background:#00ff9f;box-shadow:0 0 6px #00ff9f;"></div>' +
        '<span style="font-size:0.72rem;color:#00ff9f;font-weight:700;">hormiga_de_web — ONLINE</span>' +
        '</div>' +
        '<div style="font-size:0.7rem;color:#aaa;line-height:1.8;">' +
        '<div>🧠 ' + (d.ultima_feromona || '—') + '</div>' +
        '<div>🐜 ' + (d.nodo || 'A16') + '</div>' +
        '<div style="color:#555;font-size:0.65rem;">⏱️ ' + new Date(d.timestamp).toLocaleString() + '</div>' +
        '</div>';
    } catch(e) {
      contenedor.innerHTML = '<div style="font-size:0.7rem;color:#333;">🐜 hormiga_de_web sincronizando...</div>';
    }
  }
  actualizar();
  setInterval(actualizar, 5000);
}
document.addEventListener('DOMContentLoaded', iniciarHormigaDeWeb);
