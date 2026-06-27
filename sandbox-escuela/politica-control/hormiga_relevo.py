#!/usr/bin/env python3
# Hormiga_Relevo v1.1
# Base: v1.0 estable del backup
# Nuevo: lee memoria_quimica.json y emite ajustes_feromona
# NUNCA modifica el payload — solo informa al Bus
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
MEMORIA_FILE = os.path.join(BASE, 'memoria_quimica.json')

ZONAS = [
    {
        'id': 'ZONA_SILENCIO',
        'rango': (0.0, 0.59),
        'agentes': ['hormiga_core'],
        'energia': 'MINIMA',
        'razon': 'Zona silencio. Solo Core.'
    },
    {
        'id': 'ZONA_DIPLOMATICA',
        'rango': (0.60, 0.79),
        'agentes': ['hormiga_core'],
        'energia': 'BAJA',
        'razon': 'Zona diplomatica. Core decide solo.'
    },
    {
        'id': 'ZONA_ESPEJO',
        'rango': (0.80, 0.89),
        'agentes': [
            'hormiga_core', 'hormiga_suctora', 'hormiga_arbitro'
        ],
        'energia': 'MEDIA',
        'razon': 'Zona espejo. Suctora + Arbitro activos.'
    },
    {
        'id': 'ZONA_ESCALADA',
        'rango': (0.90, 0.94),
        'agentes': [
            'hormiga_core', 'hormiga_suctora', 'hormiga_arbitro'
        ],
        'energia': 'ALTA',
        'razon': 'Zona escalada. Pipeline completo sin actuadora.'
    },
    {
        'id': 'ZONA_CRITICA',
        'rango': (0.95, 1.0),
        'agentes': [
            'hormiga_core', 'hormiga_suctora',
            'hormiga_arbitro', 'hormiga_actuadora'
        ],
        'energia': 'MAXIMA',
        'razon': 'Zona critica. Pipeline completo.'
    }
]

def cargar_memoria():
    """Lee el sabor acumulado. Si no existe, retorna None."""
    if not os.path.exists(MEMORIA_FILE):
        return None
    try:
        with open(MEMORIA_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def calcular_relevo(payload):
    i = payload.get('intensidad_i', 0)
    tipo = payload.get('tipo_ataque', '')
    amenaza = payload.get('amenaza_soberania', False)
    escalada = payload.get('escalada_activa', False)
    # Zona base por intensidad
    zona_base = ZONAS[0]
    for zona in ZONAS:
        rmin, rmax = zona['rango']
        if rmin <= i <= rmax:
            zona_base = zona
            break
    agentes = list(zona_base['agentes'])
    ajustes = []
    # Ajuste: amenaza/escalada eleva zona
    if (amenaza or escalada) and 'hormiga_suctora' not in agentes:
        agentes.append('hormiga_suctora')
        agentes.append('hormiga_arbitro')
        ajustes.append('elevacion_por_criterio_ley15')
    # Ajuste: consumo en diplomatica activa suctora
    if (
        tipo in ('RECURSOS', 'ATENCION')
        and zona_base['id'] == 'ZONA_DIPLOMATICA'
        and 'hormiga_suctora' not in agentes
    ):
        agentes.append('hormiga_suctora')
        ajustes.append('suctora_por_consumo_diplomatica')
    # NUEVO v1.1: leer memoria quimica
    # El sabor informa al Bus pero NO modifica el payload
    ajustes_feromona = []
    consejo_previo = None
    memoria = cargar_memoria()
    if memoria:
        feromona = memoria.get('feromona_humana', {})
        sabor = memoria.get('sabor_acumulado', {})
        tension = memoria.get('tension_colonia', 0)
        umbral_rec = feromona.get('umbral_tolerancia_recursos', 0.89)
        umbral_ate = feromona.get('umbral_tolerancia_atencion', 0.89)
        # Feromona humana: consejo previo para el Bus
        if tipo == 'RECURSOS' and i > umbral_rec:
            consejo_previo = 'FILTRAR'
            ajustes_feromona.append(
                f'feromona_humana:RECURSOS>{umbral_rec}'
            )
        elif tipo == 'ATENCION' and i > umbral_ate:
            consejo_previo = 'FILTRAR'
            ajustes_feromona.append(
                f'feromona_humana:ATENCION>{umbral_ate}'
            )
        # Sabor acumulado: patron conocido
        tipo_sabor = sabor.get(tipo, {})
        if (
            tipo_sabor.get('patron_dominante') == 'CONSUMO_BLOQUEADO'
            and tension > 0.70
            and consejo_previo is None
        ):
            consejo_previo = 'FILTRAR'
            ajustes_feromona.append(
                f'sabor_acumulado:tension={tension:.2f}'
            )
    # Deduplicar agentes manteniendo orden
    orden = [
        'hormiga_core', 'hormiga_suctora',
        'hormiga_arbitro', 'hormiga_actuadora'
    ]
    agentes_unicos = []
    vistos = set()
    for ag in orden:
        if ag in agentes and ag not in vistos:
            agentes_unicos.append(ag)
            vistos.add(ag)
    return {
        'zona': zona_base['id'],
        'energia': zona_base['energia'],
        'agentes_activos': agentes_unicos,
        'total_agentes': len(agentes_unicos),
        'razon': zona_base['razon'],
        'ajustes': ajustes,
        'ajustes_feromona': ajustes_feromona,
        'consejo_previo': consejo_previo,
        'tension_colonia': (
            memoria.get('tension_colonia', 0)
            if memoria else 0
        ),
        'ciclos_previos': (
            memoria.get('ciclos_completados', 0)
            if memoria else 0
        ),
        'intensidad': i
    }

def main():
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            for linea in raw.splitlines():
                if '[SENSOR_PAYLOAD]' in linea and '->' in linea:
                    raw = linea.split('->', 1)[1].strip()
                    break
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            print(json.dumps({'error': str(e)}))
            sys.exit(1)
    elif len(sys.argv) > 1:
        try:
            payload = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            sys.exit(1)
    else:
        payload = {
            'intensidad_i': 0.92,
            'tipo_ataque': 'RECURSOS',
            'amenaza_soberania': False,
            'escalada_activa': False
        }
    resultado = calcular_relevo(payload)
    print(
        f'[RELEVO_PLAN] -> '
        f'{json.dumps(resultado, ensure_ascii=False)}'
    )
    sys.stdout.flush()

if __name__ == '__main__':
    main()
