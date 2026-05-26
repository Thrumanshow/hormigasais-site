async function ejecutarTestCortex() {

  const contenedor = document.getElementById('estadoHormigaWeb');

  if (!contenedor) return;

  try {

    const respuesta = await fetch(
      'https://smile-defeat-wars-nuke.trycloudflare.com/video/analizar',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: 'https://www.w3schools.com/html/mov_bbb.mp4'
        })
      }
    );

    const d = await respuesta.json();

    contenedor.innerHTML = `
      <div style="
        border:1px solid #333;
        padding:15px;
        border-radius:10px;
        background:#0a0a0a;
        color:white;
        font-family:sans-serif;
        animation: fadeIn 0.5s;
      ">

        <div style="
          font-size:0.9rem;
          font-weight:bold;
          color:${d.ia_generativa ? '#ff4d4d' : '#00ff9f'};
        ">
          ${d.ia_generativa ? '⚠️ SINTÉTICO (IA)' : '✅ HUMANO'}
        </div>

        <div style="
          margin-top:8px;
          font-size:0.72rem;
          color:#aaa;
          line-height:1.7;
        ">
          <div>🧠 Score biológico: ${d.score_biologico}</div>
          <div>📡 Nodo: ${d.nodo}</div>
          <div>🧬 Modo: ${d.modo}</div>
          <div>📊 Entropía: ${d.metricas.entropia_informacion}</div>
        </div>

      </div>
    `;

  } catch (e) {

    contenedor.innerHTML = `
      <div style="
        border:1px solid #550000;
        padding:12px;
        border-radius:10px;
        background:#120000;
        color:#ff8080;
        font-size:0.75rem;
        font-family:sans-serif;
      ">
        ❌ Cortex A16 desconectado
      </div>
    `;

    console.error(e);

  }

}

document.addEventListener(
  'DOMContentLoaded',
  ejecutarTestCortex
);
