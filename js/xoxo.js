// ================================================================
// 🐜 HormigasAIS — xoxo.js
// XOXO-BUS: tarjetas de regalo Master CLHQ
// ================================================================

function accederXOXO() {
  const keyEl = document.getElementById('xoxoMasterKey');
  window.LBH.xoxoKey = keyEl ? keyEl.value.trim() : '';
  if (!window.LBH.xoxoKey) { alert('Ingresa tu clave Master'); return; }
  const loginForm = document.getElementById('xoxoLoginForm');
  const panel = document.getElementById('xoxoPanel');
  if (loginForm) loginForm.style.display = 'none';
  if (panel) panel.style.display = 'block';
  cargarRegalos();
}

function rowXOXO(k, v) {
  return '<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #1a1a1a;font-size:0.75rem;"><span style="color:#555;text-transform:uppercase;letter-spacing:0.06em;">'+k+'</span><span style="color:#aaa;">'+v+'</span></div>';
}

async function generarRegalo() {
  const plan = document.getElementById('giftPlan') ? document.getElementById('giftPlan').value : 'premium';
  const dest = document.getElementById('giftDest') ? document.getElementById('giftDest').value.trim() : '';
  const email = document.getElementById('giftEmail') ? document.getElementById('giftEmail').value.trim() : '';
  const msg = (document.getElementById('giftMsg') ? document.getElementById('giftMsg').value.trim() : '') || '🎁 Bienvenido a la Colonia HormigasAIS';
  try {
    const r = await fetch(API + '/xoxo/gift?key=' + encodeURIComponent(window.LBH.xoxoKey), {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan, destinatario: dest, email, mensaje: msg })
    });
    const d = await r.json();
    if (d.error) { alert('Error: ' + d.error); return; }
    const g = d.gift;
    window.LBH.emailParaCopiar = d.instrucciones_email.asunto + '\n\n' + d.instrucciones_email.cuerpo;
    const giftData = document.getElementById('giftData');
    const giftResult = document.getElementById('giftResult');
    if (giftData) giftData.innerHTML = '<div style="display:grid;gap:0.5rem;">' +
      rowXOXO('Código', '<span style="font-family:Space Mono,monospace;color:#f5c518;font-size:0.9rem;">'+g.codigo+'</span>') +
      rowXOXO('Plan', g.plan.toUpperCase()) +
      rowXOXO('Destinatario', g.destinatario||'—') +
      rowXOXO('Mensaje', g.mensaje) +
      rowXOXO('Válido hasta', new Date(g.expiry_gift).toLocaleDateString()) +
      '</div>';
    if (giftResult) giftResult.style.display = 'block';
    cargarRegalos();
  } catch(e) { alert('Error de conexión'); }
}

function copiarEmail() {
  navigator.clipboard.writeText(window.LBH.emailParaCopiar).then(() => {
    const btn = document.querySelector('#giftResult button');
    if (btn) { btn.textContent = '✅ Copiado'; setTimeout(() => btn.textContent = '📋 Copiar email', 2000); }
  });
}

async function cargarRegalos() {
  if (!window.LBH.xoxoKey) return;
  const lista = document.getElementById('giftsList');
  if (!lista) return;
  try {
    const r = await fetch(API + '/xoxo/lista?key=' + encodeURIComponent(window.LBH.xoxoKey));
    const d = await r.json();
    if (d.error) { lista.innerHTML = '<div style="color:#ff4444;font-size:0.75rem;">'+d.error+'</div>'; return; }
    if (d.total === 0) { lista.innerHTML = '<div style="color:#555;font-size:0.78rem;text-align:center;">Sin regalos emitidos aún</div>'; return; }
    let html = '<div style="font-size:0.72rem;color:#555;margin-bottom:0.8rem;">Total: '+d.total+' | Canjeados: '+d.canjeados+' | Pendientes: '+d.pendientes+'</div><div style="display:grid;gap:0.5rem;">';
    (d.regalos||[]).forEach(g => {
      const color = g.canjeado ? '#555' : '#f5c518';
      html += '<div style="background:#0a0a0a;border:1px solid #222;border-radius:6px;padding:0.8rem;">' +
        '<div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">' +
        '<span style="font-family:Space Mono,monospace;font-size:0.75rem;color:'+color+'">'+g.codigo+'</span>' +
        '<span style="font-size:0.65rem;background:'+(g.canjeado?'#1a1a1a':'rgba(245,197,24,0.1)')+';color:'+color+';padding:0.2rem 0.5rem;border-radius:4px;">'+(g.canjeado?'✅ Canjeado':'⏳ Pendiente')+'</span>' +
        '</div><div style="font-size:0.68rem;color:#555;">'+g.plan.toUpperCase()+' · '+(g.destinatario||'Sin destinatario')+'</div></div>';
    });
    html += '</div>';
    lista.innerHTML = html;
  } catch(e) { lista.innerHTML = '<div style="color:#ff4444;font-size:0.75rem;">Error de conexión</div>'; }
}

async function canjearRegalo() {
  const codigo = document.getElementById('redeemCode') ? document.getElementById('redeemCode').value.trim().toUpperCase() : '';
  const owner = document.getElementById('redeemOwner') ? document.getElementById('redeemOwner').value.trim() : '';
  const email = document.getElementById('redeemEmail') ? document.getElementById('redeemEmail').value.trim() : '';
  const result = document.getElementById('redeemResult');
  if (!codigo) { alert('Ingresa tu código de regalo'); return; }
  if (result) result.innerHTML = '<div style="color:#555;font-size:0.78rem;">📡 Verificando...</div>';
  try {
    const r = await fetch(API + '/xoxo/redeem', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo, owner, email })
    });
    const d = await r.json();
    if (!result) return;
    if (d.error) {
      result.innerHTML = '<div style="background:rgba(255,68,68,0.06);border:1px solid rgba(255,68,68,0.2);border-radius:8px;padding:1rem;color:#ff4444;font-size:0.78rem;">❌ '+d.error+'</div>';
      return;
    }
    result.innerHTML = '<div style="background:rgba(0,255,159,0.04);border:1px solid rgba(0,255,159,0.2);border-radius:8px;padding:1.2rem;">' +
      '<div style="color:var(--verde);font-weight:700;font-size:0.85rem;margin-bottom:0.8rem;">✅ ¡Regalo canjeado!</div>' +
      '<div style="font-size:0.75rem;color:#aaa;margin-bottom:0.5rem;">'+d.mensaje+'</div>' +
      '<div style="background:#0a0a0a;border:1px solid #222;border-radius:6px;padding:0.8rem;margin:0.8rem 0;">' +
      '<div style="font-size:0.7rem;color:#555;margin-bottom:0.3rem;">TU API KEY</div>' +
      '<div style="font-family:Space Mono,monospace;font-size:0.9rem;color:#f5c518;">'+d.api_key+'</div></div>' +
      '<div style="font-size:0.72rem;color:#666;">Plan: <strong style="color:#fff">'+d.cliente.plan+'</strong> · Válido: <strong style="color:#fff">'+d.cliente.expiry+'</strong></div>' +
      '<div style="font-size:0.7rem;color:#555;margin-top:0.5rem;">Guarda tu API Key y úsala en 👤 Mi Cuenta</div></div>';
  } catch(e) { if (result) result.innerHTML = '<div style="color:#ff4444;font-size:0.78rem;">⚠️ Error de conexión</div>'; }
}
