// ================================================================
// 🐜 HormigasAIS — account.js
// Login cliente, dashboard personal
// ================================================================

async function accederCuenta() {
  const apiKey = document.getElementById('apiKeyInput').value.trim();
  if (!apiKey) { alert('Ingresa tu API Key'); return; }
  window.LBH.clienteApiKey = apiKey;
  const dashboard = document.getElementById('dashboardCliente');
  const loginForm = document.getElementById('loginForm');
  if (dashboard) { dashboard.innerHTML = '<div style="text-align:center;color:#555;padding:2rem;font-size:0.8rem;">📡 Conectando con el nodo A16...</div>'; dashboard.style.display = 'block'; }
  try {
    const r = await fetch(API + '/cliente/dashboard', { headers: { 'X-API-Key': apiKey } });
    const data = await r.json();
    if (data.error) {
      if (dashboard) dashboard.innerHTML = '<div style="background:#1a1a1a;border:1px solid rgba(255,68,68,0.3);border-radius:8px;padding:1.5rem;text-align:center;color:#ff4444;font-size:0.85rem;">❌ '+data.error+'</div>';
      return;
    }
    const c = data.cliente;
    const planColor = { FREE:'#f5c518', PREMIUM:'#a855f7', ENTERPRISE:'#00ff9f' }[c.plan] || '#aaa';
    let html = '<div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:1.5rem;margin-bottom:1rem;">' +
      '<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">' +
      '<div><div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:#fff;">'+c.owner+'</div>' +
      '<div style="font-size:0.75rem;color:#555;margin-top:0.2rem;">'+c.email+'</div></div>' +
      '<div style="background:rgba(245,197,24,0.1);border:1px solid rgba(245,197,24,0.3);border-radius:999px;padding:0.3rem 1rem;font-size:0.75rem;font-weight:700;color:'+planColor+'">⭐ '+c.plan+'</div>' +
      '</div>' +
      '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#222;border-radius:8px;overflow:hidden;margin-top:1.2rem;">' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#f5c518">'+c.sellos_emitidos+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.2rem;text-transform:uppercase;">Sellos</div></div>' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:0.85rem;font-weight:700;color:#aaa;margin-top:0.3rem;">'+c.sellos_limite+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.2rem;text-transform:uppercase;">Límite</div></div>' +
      '<div style="background:#0a0a0a;padding:1rem;text-align:center;"><div style="font-family:Syne,sans-serif;font-size:0.85rem;font-weight:700;color:#00ff9f;margin-top:0.3rem;">'+c.dias_restantes+'</div><div style="font-size:0.65rem;color:#555;margin-top:0.2rem;text-transform:uppercase;">Validez</div></div>' +
      '</div></div>';
    const sellos = data.mis_sellos || [];
    if (sellos.length > 0) {
      html += '<div style="font-family:Syne,sans-serif;font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.8rem;">🔏 Mis sellos</div>';
      html += '<div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;overflow:hidden;">';
      sellos.forEach(s => {
        html += '<div style="display:grid;grid-template-columns:1fr 1fr 80px;gap:0.5rem;padding:0.7rem 1rem;border-top:1px solid #222;align-items:center;">' +
          '<span style="font-size:0.72rem;color:#00ff9f;">'+s.signature+'</span>' +
          '<span style="font-size:0.72rem;color:#aaa;">'+s.asset+'</span>' +
          '<a href="'+API+'/manifest/'+s.signature+'" target="_blank" style="font-size:0.65rem;color:#f5c518;text-decoration:none;border:1px solid rgba(245,197,24,0.3);padding:0.2rem 0.5rem;border-radius:4px;">📄</a>' +
          '</div>';
      });
      html += '</div>';
    } else {
      html += '<div style="background:#1a1a1a;border:1px solid #2a2a2a;border-radius:8px;padding:1.5rem;text-align:center;color:#555;font-size:0.8rem;">Sin sellos aún — <a href="#" onclick="showSection(\'sello\',document.querySelectorAll(\'nav button\')[3]);return false;" style="color:var(--amarillo)">Sellar ahora →</a></div>';
    }
    html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-top:1rem;">' +
      '<a href="https://github.com/sponsors/Thrumanshow" target="_blank" style="background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:1rem;text-align:center;text-decoration:none;">' +
      '<div style="font-size:1.2rem;margin-bottom:0.3rem;">⭐</div><div style="font-size:0.75rem;color:#fff;font-weight:700;">Renovar plan</div></a>' +
      '<button onclick="cerrarSesion()" style="background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:1rem;cursor:pointer;">' +
      '<div style="font-size:1.2rem;margin-bottom:0.3rem;">🚪</div><div style="font-size:0.75rem;color:#fff;font-weight:700;">Cerrar sesión</div></button>' +
      '</div>';
    if (dashboard) dashboard.innerHTML = html;
    if (loginForm) loginForm.style.display = 'none';
  } catch(e) {
    if (dashboard) dashboard.innerHTML = '<div style="color:#ff4444;font-size:0.8rem;text-align:center;">⚠️ Error de conexión</div>';
  }
}

function cerrarSesion() {
  window.LBH.clienteApiKey = '';
  const apiKeyInput = document.getElementById('apiKeyInput');
  const dashboard = document.getElementById('dashboardCliente');
  const loginForm = document.getElementById('loginForm');
  if (apiKeyInput) apiKeyInput.value = '';
  if (dashboard) dashboard.style.display = 'none';
  if (loginForm) loginForm.style.display = 'block';
}
