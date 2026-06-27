#!/usr/bin/env python3
# Hormiga_Arbitro v1.0 — Consenso entre Core y Suctora
# Recibe: decision_core + feromona_suctora + payload
# Emite: decision_final con razon de arbitraje
# NO ejecuta. Solo arbitra.
import json, sys

REGLAS_ARBITRAJE = [
    {
        'id': 'ARB_01',
        'descripcion': 'Consumo critico en zona escalada',
        'condicion': {
            'core': 'ACTIVAR_MECANICO_MAXIMA',
            'consejo': 'FILTRAR',
            'gravedad': ['CRITICA', 'ALTA'],
            'tipo': ['RECURSOS', 'ATENCION'],
            'intensidad_min': 0.90
        },
        'decision_final': 'FILTRAR',
        'fundamento': 'Suctora detecta consumo critico en zona donde Core aplica Espejo'
    },
    {
        'id': 'ARB_02',
        'descripcion': 'Bloqueo total reforzado por consejo suctora',
        'condicion': {
            'core': 'ACTIVAR_MECANICO_MAXIMA',
            'consejo': 'BLOQUEO_TOTAL',
            'gravedad': ['CRITICA'],
            'tipo': ['RECURSOS', 'ATENCION'],
            'intensidad_min': 0.95
        },
        'decision_final': 'BLOQUEO_TOTAL',
        'fundamento': 'Suctora detecta patron escalada con intensidad critica'
    },
    {
        'id': 'ARB_03',
        'descripcion': 'Identidad amenazada requiere espejo no filtro',
        'condicion': {
            'core': 'FILTRAR',
            'consejo': None,
            'gravedad': ['ALTA', 'CRITICA'],
            'tipo': ['ATENCION'],
            'intensidad_min': 0.85,
            'patron_gancho': ['suplantacion', 'clon', 'identidad']
        },
        'decision_final': 'ACTIVAR_MECANICO_MAXIMA',
        'fundamento': 'Ataque de identidad requiere Espejo, no solo filtro'
    }
]

def arbitrar(decision_core, feromona, payload):
    i = payload.get('intensidad_i', 0)
    tipo = payload.get('tipo_ataque', '')
    gancho = payload.get('gancho_psicologico', '').lower()
    consejo = feromona.get('recomendacion') if feromona else None
    gravedad = feromona.get('gravedad_semantica', 'BAJA') if feromona else 'BAJA'
    for regla in REGLAS_ARBITRAJE:
        c = regla['condicion']
        # Verificar core
        if c['core'] != decision_core:
            continue
        # Verificar consejo (None significa que no importa)
        if c['consejo'] is not None and consejo != c['consejo']:
            continue
        # Verificar gravedad
        if gravedad not in c['gravedad']:
            continue
        # Verificar tipo
        if tipo not in c['tipo']:
            continue
        # Verificar intensidad
        if i < c['intensidad_min']:
            continue
        # Verificar patron gancho si existe
        if 'patron_gancho' in c:
            if not any(p in gancho for p in c['patron_gancho']):
                continue
        # Regla aplicada
        return {
            'decision_final': regla['decision_final'],
            'regla_aplicada': regla['id'],
            'descripcion': regla['descripcion'],
            'fundamento': regla['fundamento'],
            'decision_core_original': decision_core,
            'consejo_suctora': consejo,
            'gravedad_semantica': gravedad,
            'arbitrado': True
        }
    # Sin regla aplicada — Core mantiene su decision
    return {
        'decision_final': decision_core,
        'regla_aplicada': None,
        'fundamento': 'Core mantiene decision. Sin consenso de arbitraje.',
        'decision_core_original': decision_core,
        'consejo_suctora': consejo,
        'gravedad_semantica': gravedad,
        'arbitrado': False
    }

def main():
    if not sys.stdin.isatty():
        try:
            data = json.loads(sys.stdin.read().strip())
            resultado = arbitrar(
                data['decision_core'],
                data.get('feromona'),
                data.get('payload', {})
            )
            print(
                f'[ARBITRO_DECISION] -> '
                f'{json.dumps(resultado, ensure_ascii=False)}'
            )
        except Exception as e:
            print(json.dumps({'error': str(e)}))
    else:
        # Test standalone
        test = {
            'decision_core': 'ACTIVAR_MECANICO_MAXIMA',
            'feromona': {
                'recomendacion': 'FILTRAR',
                'gravedad_semantica': 'CRITICA'
            },
            'payload': {
                'intensidad_i': 0.92,
                'tipo_ataque': 'RECURSOS',
                'gancho_psicologico': 'extraccion_modelo_completo'
            }
        }
        r = arbitrar(
            test['decision_core'],
            test['feromona'],
            test['payload']
        )
        print(f'[TEST] {json.dumps(r, ensure_ascii=False, indent=2)}')

if __name__ == '__main__':
    main()
