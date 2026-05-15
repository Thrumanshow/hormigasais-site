// ================================================================
// 🐜 HormigasAIS — seal.js
// Sellar, Badge, Verificar firma y archivo
// ================================================================

// Drag & drop
document.addEventListener('DOMContentLoaded', function() {
  const zone = document.getElementById('uploadZone');
  if (!zone) return;
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('dragover');
    const f = e.dataTransfer.files[0]; if(f) handleFile(f);
  });
  const fi = document.getElementById('fileInput');
  if (fi) fi.addEventListener('change', e => { if(e.target.files[0]) handleFile(e.target.files[0]); });
});

function handleFile(file) {
  const zone = document.getElementById('uploadZone');
  if (zone) zone.querySelector('p').innerHTML = '<strong>' + file.name + '</strong> (' + (file.size/1024).toFixed(1) + ' KB)';
  const assetInput = document.getElementById('assetInput');
  if (assetInput && !assetInput.value) assetInput.value = file.name;
}

async function sha256(file) {
  const buf = await file.arrayBuffer();
  const h = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(h)).map(b => b.toString(16).padStart(2,'0')).join('');
}

async function sellarActivo() {
  const planEl = document.getElementById('planSelect');
  const plan = planEl ? planEl.value : 'free';
  if (plan === 'free' && window.LBH_FREE_COUNT >= 3) {
    alert('Límite Free alcanzado. Actualiza tu plan.');
    showSection('planes', document.querySelectorAll('nav button')[1]);
    return;
  }
  const file = document.getElementById('fileInput').files[0];
  const owner = document.getElementById('ownerInput').value.trim() || 'Anónimo';
  const asset = document.getElementById('assetInput').value.trim() || 'activo-digital';
  const btn = document.getElementById('btnSeal');
  const loading = document.getElementById('loadingSello');
  const result = document.getElementById('selloResult');
  result.classList.remove('visible');
  loading.classList.add('visible');
  if (btn) btn.disabled = true;
  try {
    let hash = '';
    if (file) hash = await sha256(file);
    const res = await fetch(API + '/seal', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ owner, asset, hash, plan })
    });
    const data = await res.json();
    if (data.status === 'SELLADO' && data.sello) {
      const s = data.sello;
      window.LBH.selloActual = s.signature;
      if (plan === 'free') window.LBH_FREE_COUNT = (window.LBH_FREE_COUNT || 0) + 1;
      const expiry = s.valido_hasta ? new Date(s.valido_hasta).toLocaleDateString() : 'Permanente';
      const rows = [
        ['Estado','✅ SELLADO'],['Firma',s.signature],['Propietario',s.owner],
        ['Activo',s.asset],['Plan',plan.toUpperCase()],['Válido hasta',expiry],
        ['Protocolo',s.protocol],['Nodo',s.nodo],['Timestamp',new Date(s.timestamp).toLocaleString()]
      ];
      if (hash) rows.push(['SHA-256', hash.substring(0,32)+'...']);
      document.getElementById('selloData').innerHTML = rows.map(([k,v]) =>
        '<div class="sello-row"><span class="sello-key">'+k+'</span><span class="sello-val">'+v+'</span></div>'
      ).join('');
      // Pre-llenar badge
      ['badgeSig','badgeOwner','badgeExpiry','badgePlan'].forEach((id,i) => {
        const el = document.getElementById(id);
        if (el) el.value = [s.signature, s.owner, expiry, plan][i];
      });
      result.classList.add('visible');
    }
  } catch(e) { alert('Error conectando con el nodo A16.'); }
  loading.classList.remove('visible');
  if (btn) btn.disabled = false;
}

function copiarSello() {
  navigator.clipboard.writeText(window.LBH.selloActual).then(() => {
    const btn = document.querySelector('.btn-dl');
    if (btn) { btn.textContent = '✅ Copiado'; setTimeout(() => btn.textContent = '📋 Copiar firma', 2000); }
  });
}

async function descargarManifest() {
  if (!window.LBH.selloActual) { alert('Primero genera un sello'); return; }
  const btn = document.getElementById('btnManifest');
  if (btn) btn.textContent = '⏳ Generando...';
  try {
    const r = await fetch(API + '/manifest/' + window.LBH.selloActual);
    const blob = await r.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'manifest-' + window.LBH.selloActual + '.json';
    a.click();
    if (btn) { btn.textContent = '✅ Descargado'; setTimeout(() => btn.textContent = '📄 Descargar Manifest →', 3000); }
  } catch(e) { alert('Error de conexión'); if (btn) btn.textContent = '📄 Descargar Manifest →'; }
}

// Badge generator
const PLAN_COLORS = {
  free:       { bg: '#1a1a1a', accent: '#f5c518', label: 'Free' },
  premium:    { bg: '#1a1220', accent: '#a855f7', label: 'Premium ⭐' },
  enterprise: { bg: '#0a1a1a', accent: '#00ff9f', label: 'Enterprise 🏢' }
};

function generarBadge() {
  const sig    = document.getElementById('badgeSig').value.trim() || 'CLHQ-XXXXXXXX';
  const plan   = document.getElementById('badgePlan').value;
  const owner  = document.getElementById('badgeOwner').value.trim() || 'Propietario';
  const expiry = document.getElementById('badgeExpiry').value.trim() || '—';
  const c = document.getElementById('badgeCanvas');
  const ctx = c.getContext('2d');
  const cfg = PLAN_COLORS[plan];
  ctx.fillStyle = cfg.bg; ctx.beginPath(); ctx.roundRect(0,0,400,120,10); ctx.fill();
  ctx.strokeStyle = cfg.accent; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.roundRect(1,1,398,118,10); ctx.stroke();
  ctx.fillStyle = cfg.accent; ctx.fillRect(0,0,4,120);
  ctx.font = 'bold 28px serif'; ctx.fillText('🐜',18,52);
  ctx.fillStyle = cfg.accent; ctx.font = 'bold 13px monospace'; ctx.fillText('CERTIFICADO LBH · '+cfg.label.toUpperCase(),58,28);
  ctx.fillStyle = '#ffffff'; ctx.font = 'bold 16px monospace'; ctx.fillText(sig,58,52);
  ctx.fillStyle = '#aaaaaa'; ctx.font = '11px monospace'; ctx.fillText('Propietario: '+owner,58,72);
  ctx.fillStyle = '#666666'; ctx.font = '10px monospace'; ctx.fillText('Válido hasta: '+expiry+' | hormigasais.com',58,90);
  ctx.fillStyle = cfg.accent; ctx.font = '9px monospace'; ctx.fillText('Protocolo: Lenguaje-Binario-HormigasAIS · Nodo: A16-SanMiguel-SV',18,110);
  const dataURL = c.toDataURL('image/png');
  document.getElementById('badgeCode').textContent =
    '<!-- Badge HormigasAIS LBH -->\n<a href="https://hormigasais.com" target="_blank">\n  <img src="[descarga el PNG]"\n       alt="Certificado LBH '+sig+'"\n       height="60">\n</a>\n<!-- Firma: '+sig+' | Plan: '+plan+' | Válido: '+expiry+' -->';
  document.getElementById('badgePreview').classList.add('visible');
}

function descargarBadge() {
  const c = document.getElementById('badgeCanvas');
  const sig = document.getElementById('badgeSig').value.trim() || 'badge-lbh';
  const a = document.createElement('a');
  a.download = 'badge-lbh-'+sig+'.png';
  a.href = c.toDataURL('image/png'); a.click();
}

function copiarCodigo() {
  const code = document.getElementById('badgeCode').textContent;
  navigator.clipboard.writeText(code).then(() => {
    const btns = document.querySelectorAll('.badge-btns .btn-dl');
    if (btns[1]) { btns[1].textContent = '✅ Copiado'; setTimeout(() => btns[1].textContent = '📋 Copiar código HTML', 2000); }
  });
}

// Verificar por firma
async function verificarSello() {
  const sig = document.getElementById('sigInput').value.trim();
  if (!sig) return;
  const loading = document.getElementById('loadingVerify');
  const result = document.getElementById('verifyResult');
  result.className = 'verify-result';
  loading.classList.add('visible');
  try {
    const res = await fetch(API + '/seal/' + sig);
    const data = await res.json();
    if (data.status === 'VERIFICADO' && data.sello) {
      const s = data.sello;
      const rows = [['Estado','✅ AUTÉNTICO'],['Firma',s.signature],['Propietario',s.owner],
        ['Activo',s.asset],['Protocolo',s.protocol],['Nodo emisor',s.nodo],
        ['Emitido',new Date(s.timestamp).toLocaleString()]];
      document.getElementById('verifyTitle').textContent = '✅ Sello verificado — Auténtico';
      document.getElementById('verifyData').innerHTML = rows.map(([k,v]) =>
        '<div class="sello-row"><span class="sello-key">'+k+'</span><span class="sello-val">'+v+'</span></div>'
      ).join('');
      result.classList.add('ok');
    } else {
      document.getElementById('verifyTitle').textContent = '❌ Sello no encontrado';
      document.getElementById('verifyData').innerHTML = '<div class="sello-row"><span class="sello-key">Mensaje</span><span class="sello-val" style="color:var(--rojo)">Esta firma no existe en la red</span></div>';
      result.classList.add('err');
    }
  } catch(e) { document.getElementById('verifyTitle').textContent = '⚠️ Error de conexión'; result.classList.add('err'); }
  loading.classList.remove('visible');
}

document.addEventListener('DOMContentLoaded', function() {
  const sigInput = document.getElementById('sigInput');
  if (sigInput) sigInput.addEventListener('keydown', e => { if(e.key==='Enter') verificarSello(); });
});

// Verificar por archivo
async function verificarArchivo() {
  const fileInput = document.getElementById('verifyFileInput');
  const file = fileInput ? fileInput.files[0] : null;
  if (!file) { alert('Selecciona un archivo'); return; }
  const btn = document.getElementById('btnVerifyFile');
  const result = document.getElementById('verifyFileResult');
  if (btn) btn.textContent = '⏳ Calculando hash...';
  if (result) result.style.display = 'none';
  try {
    const buf = await file.arrayBuffer();
    const hashBuf = await crypto.subtle.digest('SHA-256', buf);
    const hash = Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2,'0')).join('');
    if (btn) btn.textContent = '⏳ Verificando...';
    const r = await fetch(API + '/verify-file', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hash })
    });
    const data = await r.json();
    if (result) {
      result.style.display = 'block';
      if (data.status === 'VERIFICADO') {
        const s = data.sello;
        result.style.cssText = 'display:block;border:1px solid rgba(0,255,159,0.3);background:rgba(0,255,159,0.04);border-radius:8px;padding:1.2rem;';
        result.innerHTML = '<div style="color:#00ff9f;font-size:0.85rem;font-weight:700;margin-bottom:0.8rem;">✅ Archivo auténtico</div>' +
          '<div style="font-size:0.75rem;color:#aaa;line-height:1.8;">' +
          '<div>Firma: <span style="color:#00ff9f">'+s.signature+'</span></div>' +
          '<div>Propietario: '+s.owner+'</div>' +
          '<div>Activo: '+s.asset+'</div>' +
          '<div>Emitido: '+new Date(s.emitido).toLocaleString()+'</div>' +
          '</div>';
      } else {
        result.style.cssText = 'display:block;border:1px solid rgba(255,68,68,0.3);background:rgba(255,68,68,0.04);border-radius:8px;padding:1.2rem;';
        result.innerHTML = '<div style="color:#ff4444;font-size:0.85rem;font-weight:700;">❌ Archivo no registrado en LBH</div>';
      }
    }
  } catch(e) { if (result) result.innerHTML = '<div style="color:#ff4444">⚠️ Error de conexión</div>'; }
  if (btn) btn.textContent = '🔍 Verificar archivo';
}
