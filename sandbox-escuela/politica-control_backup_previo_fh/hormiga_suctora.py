#!/usr/bin/env python3
# Hormiga_Suctora v1.0 — Agente Consejero Semantico
# Rol: analizar el payload y emitir feromona de contexto
# NO decide. NO ejecuta. Solo enriquece.
import json, sys, os

# Patrones semanticos que elevan la gravedad operacional
PATRONES_CRITICOS = [
    'masiva', 'coordinad', 'persistente', 'infraestructura',
    'modelo', 'produccion', 'total', 'completo', 'vaciado',
    'robo', 'clon', 'suplantacion', 'botnet', 'ddos',
    'flood', 'loop', 'saturacion', 'agotamiento'
]

PATRONES_MODERADOS = [
    'extraccion', 'consumo', 'descarga', 'raspado',
    'bulk', 'sincronizacion', 'tunneling', 'scraper'
]

PATRONES_ESCALADA = [
    'reescalada', 'persistencia', 'reincidente',
    'coordinado', 'actor_estatal', 'botnet'
]

def analizar_semantica(payload):
    gancho = payload.get('gancho_psicologico', '').lower()
    origen = payload.get('origen', '').lower()
    tipo = payload.get('tipo_ataque', '')
    i = payload.get('intensidad_i', 0)
    # Contar patrones detectados
    hits_criticos = sum(
        1 for p in PATRONES_CRITICOS if p in gancho or p in origen
    )
    hits_moderados = sum(
        1 for p in PATRONES_MODERADOS if p in gancho or p in origen
    )
    hits_escalada = sum(
        1 for p in PATRONES_ESCALADA if p in gancho or p in origen
    )
    # Gravedad semantica
    if hits_criticos >= 2:
        gravedad = 'CRITICA'
    elif hits_criticos == 1:
        gravedad = 'ALTA'
    elif hits_moderados >= 1:
        gravedad = 'MODERADA'
    else:
        gravedad = 'BAJA'
    # Recomendacion semantica — NO es decision final
    recomendacion = None
    tipo_consumo = tipo in ('RECURSOS', 'ATENCION')
    if tipo_consumo and gravedad in ('CRITICA', 'ALTA') and i >= 0.90:
        recomendacion = 'FILTRAR'
        razon = 'consumo_critico_semantico_en_zona_alta'
    elif tipo_consumo and gravedad == 'CRITICA' and i >= 0.80:
        recomendacion = 'FILTRAR'
        razon = 'consumo_critico_semantico_en_zona_espejo'
    elif hits_escalada >= 1 and i >= 0.90:
        recomendacion = 'BLOQUEO_TOTAL'
        razon = 'patron_escalada_detectado'
    else:
        recomendacion = None
        razon = 'sin_alarma_semantica'
    return {
        'agente': 'Hormiga_Suctora_v1.0',
        'tipo_feromona': 'CONSEJO_SEMANTICO',
        'gravedad_semantica': gravedad,
        'hits_criticos': hits_criticos,
        'hits_moderados': hits_moderados,
        'hits_escalada': hits_escalada,
        'recomendacion': recomendacion,
        'razon': razon,
        'estado': 'CONSEJO_ONLY'
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
        except (json.JSONDecodeError, Exception) as e:
            print(json.dumps({'error': str(e), 'agente': 'Hormiga_Suctora'}))
            sys.exit(1)
    elif len(sys.argv) > 1:
        try:
            payload = json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(json.dumps({'error': str(e)}))
            sys.exit(1)
    else:
        payload = {
            'gancho_psicologico': 'extraccion_modelo_completo',
            'origen': 'botnet_detectada',
            'tipo_ataque': 'RECURSOS',
            'intensidad_i': 0.92
        }
    feromona = analizar_semantica(payload)
    print(f'[SUCTORA_FEROMONA] -> {json.dumps(feromona, ensure_ascii=False)}')
    sys.stdout.flush()

if __name__ == '__main__':
    main()
