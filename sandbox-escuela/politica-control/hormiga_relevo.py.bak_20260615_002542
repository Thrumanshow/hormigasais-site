#!/usr/bin/env python3
# Hormiga_Relevo v1.0
# Rol: decidir que agentes activar segun intensidad
# Ahorro energetico diferencial
# Inspirado en la logistica de la hormiga cortadora Atta
import json, sys

# Mapa de activacion por zona de intensidad
# Cada zona activa solo los agentes necesarios
ZONAS = [
    {
        'id': 'ZONA_SILENCIO',
        'rango': (0.0, 0.59),
        'descripcion': 'Vector bajo umbral de respuesta activa',
        'agentes': ['hormiga_core'],
        'energia': 'MINIMA',
        'razon': 'Zona silencio. Solo Core. Suctora y Arbitro innecesarios.'
    },
    {
        'id': 'ZONA_DIPLOMATICA',
        'rango': (0.60, 0.79),
        'descripcion': 'Vector en zona de respuesta diplomatica',
        'agentes': ['hormiga_core'],
        'energia': 'BAJA',
        'razon': 'Zona diplomatica. Core decide solo. '
                 'Tipo de ataque ya determina DEFLEXION o FILTRAR.'
    },
    {
        'id': 'ZONA_ESPEJO',
        'rango': (0.80, 0.89),
        'descripcion': 'Vector en zona de respuesta activa',
        'agentes': ['hormiga_core', 'hormiga_suctora', 'hormiga_arbitro'],
        'energia': 'MEDIA',
        'razon': 'Zona espejo. Suctora detecta consumo critico. '
                 'Arbitro consensua si hay tension doctrinal.'
    },
    {
        'id': 'ZONA_ESCALADA',
        'rango': (0.90, 0.94),
        'descripcion': 'Vector en zona de escalada critica',
        'agentes': ['hormiga_core', 'hormiga_suctora', 'hormiga_arbitro'],
        'energia': 'ALTA',
        'razon': 'Zona escalada. Pipeline completo sin actuadora. '
                 'Arbitro ARB_01 activo para consumo critico.'
    },
    {
        'id': 'ZONA_CRITICA',
        'rango': (0.95, 1.0),
        'descripcion': 'Vector en zona de maxima amenaza',
        'agentes': [
            'hormiga_core', 'hormiga_suctora',
            'hormiga_arbitro', 'hormiga_actuadora'
        ],
        'energia': 'MAXIMA',
        'razon': 'Zona critica. Pipeline completo incluida actuadora. '
                 'LEY_15 puede activarse con criterio.'
    }
]

def calcular_relevo(payload):
    i = payload.get('intensidad_i', 0)
    tipo = payload.get('tipo_ataque', '')
    amenaza = payload.get('amenaza_soberania', False)
    escalada = payload.get('escalada_activa', False)
    # Encontrar zona base
    zona_base = None
    for zona in ZONAS:
        rmin, rmax = zona['rango']
        if rmin <= i <= rmax:
            zona_base = zona
            break
    if not zona_base:
        zona_base = ZONAS[0]  # default silencio
    agentes = list(zona_base['agentes'])
    ajustes = []
    # Ajuste 1: amenaza o escalada activa eleva la zona
    if (amenaza or escalada) and 'hormiga_suctora' not in agentes:
        agentes.append('hormiga_suctora')
        agentes.append('hormiga_arbitro')
        ajustes.append('elevacion_por_criterio_ley15')
    # Ajuste 2: tipo consumo en zona diplomatica activa suctora
    if (tipo in ('RECURSOS', 'ATENCION')
            and zona_base['id'] == 'ZONA_DIPLOMATICA'
            and 'hormiga_suctora' not in agentes):
        agentes.append('hormiga_suctora')
        ajustes.append('suctora_por_consumo_en_zona_diplomatica')
    # Deduplicar manteniendo orden
    agentes_unicos = []
    vistos = set()
    orden = [
        'hormiga_despojadora',
        'hormiga_core',
        'hormiga_suctora',
        'hormiga_arbitro',
        'hormiga_actuadora'
    ]
    for agente in orden:
        if agente in agentes and agente not in vistos:
            agentes_unicos.append(agente)
            vistos.add(agente)
    return {
        'zona': zona_base['id'],
        'energia': zona_base['energia'],
        'agentes_activos': agentes_unicos,
        'total_agentes': len(agentes_unicos),
        'razon': zona_base['razon'],
        'ajustes': ajustes,
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
            'intensidad_i': 0.85,
            'tipo_ataque': 'RECURSOS',
            'amenaza_soberania': False,
            'escalada_activa': False
        }
    relevo = calcular_relevo(payload)
    print(
        f'[RELEVO_PLAN] -> '
        f'{json.dumps(relevo, ensure_ascii=False)}'
    )
    sys.stdout.flush()

if __name__ == '__main__':
    main()
