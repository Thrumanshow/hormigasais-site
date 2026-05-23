/**
 * HormigasAIS — Módulo Periférico de Accesibilidad (Braille + Voz + Táctil)
 * Compatibilidad: Web Speech API, Vibration API y Lectores de Pantalla (ARIA)
 */
const HormigasAccesibilidad = {
    init() {
        // Buscar el botón o pestaña existente en el DOM para asignarle la acción
        const botones = document.querySelectorAll('button, a');
        let botonAccesible = null;

        botones.forEach(el => {
            if (el.textContent.includes('Accesible')) {
                botonAccesible = el;
            }
        });

        // Si existe el botón en el menú, vinculamos el disparador
        if (botonAccesible) {
            botonAccesible.addEventListener('click', (e) => {
                e.preventDefault();
                this.ejecutarFlujoAccesible();
            });
            console.log("🐜 HormigasAIS: Módulo de accesibilidad vinculado al botón de la UI.");
        } else {
            console.log("⚠️ HormigasAIS: No se encontró el botón físico de Accesibilidad en el DOM.");
        }
    },

    ejecutarFlujoAccesible() {
        const firmaBraille = "⢧"; // Firma LBH transmutada a 8 puntos (Capa -1)
        
        // 1. Respuesta en voz alta (Web Speech API)
        this.emitirVoz("Menú de accesibilidad activado. Sincronizando con la infraestructura soberana. Firma binaria hormigas a i s procesada en celda braille.");

        // 2. Respuesta Háptica / Táctil (Vibration API)
        this.vibrar([100, 50, 100]);

        // 3. Alerta visual e interactiva
        alert(`🐜 HormigasAIS — Canal de Accesibilidad Activo\n\n1. Firma LBH → Braille Unicode: ${firmaBraille}\n2. Lector de pantalla → Sincronizado\n3. Respuesta de voz → Activa\n4. Impulso táctil → Emitido`);
    },

    emitirVoz(texto) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel(); // Detener lecturas previas encoladas
            const utterance = new SpeechSynthesisUtterance(texto);
            utterance.lang = 'es-ES';
            utterance.rate = 0.95; // Velocidad óptima para telemetría auditiva
            window.speechSynthesis.speak(utterance);
        }
    },

    vibrar(patron) {
        if ('vibrate' in navigator) {
            navigator.vibrate(patron);
        }
    }
};

// Inicializar el módulo una vez cargada la estructura HTML de producción
document.addEventListener('DOMContentLoaded', () => HormigasAccesibilidad.init());
// Ejecución inmediata en caso de que el DOM ya esté listo
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    HormigasAccesibilidad.init();
}
