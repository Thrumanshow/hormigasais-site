// ================================================================
// 🐜 HormigasAIS — core.js
// Constantes, navegación y utilidades globales
// ================================================================

const API = 'https://api.hormigasais.com';

// Navegación central — un solo lugar
function showSection(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  const target = document.getElementById(id);
  if (target) target.classList.add('active');
  if (btn) btn.classList.add('active');

  // Triggers por sección
  const triggers = {
    colonia:  () => typeof cargarColoniaPublica === 'function' && cargarColoniaPublica(),
    admin:    () => {},
    cuenta:   () => {},
    xoxo:     () => typeof cargarRegalos === 'function' && cargarRegalos(),
    home:     () => typeof loadStats === 'function' && loadStats()
  };
  if (triggers[id]) triggers[id]();
}

// Estado global del sitio
window.LBH = {
  selloActual: '',
  clienteApiKey: '',
  xoxoKey: '',
  emailParaCopiar: ''
};

// Verificar estado API
async function checkStatus() {
  try {
    const r = await fetch(API + '/verify');
    const d = await r.json();
    const el = document.getElementById('statusText');
    if (el) el.textContent = d.status === 'VALIDADO' ? 'Nodo A16 · Online' : 'Reconectando...';
  } catch(e) {
    const el = document.getElementById('statusText');
    if (el) el.textContent = 'Reconectando...';
  }
}

// Cargar stats del inicio
async function loadStats() {
  try {
    const r = await fetch(API + '/all');
    const d = await r.json();
    const el = document.getElementById('statSellos');
    if (el) el.textContent = Array.isArray(d) ? d.length : '—';
  } catch(e) {}
}

// Init
document.addEventListener('DOMContentLoaded', function() {
  checkStatus();
  loadStats();
});
