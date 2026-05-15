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
