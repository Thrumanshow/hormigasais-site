#!/usr/bin/env python3
# LBH-Core v2.3 | Restaurado limpio
# Doctrina gradual RECURSOS+ATENCION
import json, time, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
REGISTRO_FILE = os.path.join(BASE, 'registro_vectores.json')
DOCTRINA_VERSION = 'v2.3-experimental'

def cargar_contrato():
    with open(os.path.join(BASE, 'CLHQ_99.human'), encoding='utf-8') as f:
        return json.load(f)

def cargar_registro():
    if not os.path.exists(REGISTRO_FILE):
        return []
    with open(REGISTRO_FILE, encoding='utf-8') as f:
        return json.load(f)

def guardar_registro(registro):
    with open(REGISTRO_FILE, 'w', encoding='utf-8') as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)

def resolver_payload():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError as e:
            print(f'[CORE_ERROR] argv JSON invalido: {e}')
            sys.exit(1)
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            for linea in raw.splitlines():
                if '[SENSOR_PAYLOAD]' in linea and '->' in linea:
                    raw = linea.split('->', 1)[1].strip()
                    break
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f'[CORE_ERROR] stdin JSON invalido: {e}')
            sys.exit(1)
    print('[CORE_WARN] Sin entrada externa. Usando payload de prueba.')
    return {
        'identificador': 'VECTOR-TEST',
        'origen': 'standalone',
        'gancho_psicologico': 'prueba_interna',
        'intensidad_i': 0.98
    }

def decidir(payload, registro):
    i = payload.get('intensidad_i', 0)
    tipo = payload.get('tipo_ataque', '')
    gancho = payload.get('gancho_psicologico', '')
    reincidente = gancho in registro
    amenaza = payload.get('amenaza_soberania', False)
    escalada = payload.get('escalada_activa', False)
    criterio_15 = reincidente or amenaza or escalada
    tipo_consumo = tipo in ('RECURSOS', 'ATENCION')
    # LEY_15
    if i >= 0.95 and criterio_15:
        return 'BLOQUEO_TOTAL', 'LEY_15', {
            'reincidente': reincidente,
            'amenaza_soberania': amenaza,
            'escalada_activa': escalada
        }
    # ZONA ESCALADA 0.90-0.94 — consumo o no
    if i >= 0.90:
        return 'ACTIVAR_MECANICO_MAXIMA', 'LEY_44', {
            'nota': 'zona_escalada'
        }
    # ZONA ESPEJO 0.80-0.89 — consumo filtrado
    if i >= 0.80:
        if tipo_consumo:
            return 'FILTRAR', 'LEY_06', {
                'nota': 'consumo_zona_espejo'
            }
        return 'ACTIVAR_MECANICO_MAXIMA', 'LEY_44', {}
    # ZONA ACTIVA 0.60-0.79
    if i >= 0.60:
        if tipo_consumo:
            return 'FILTRAR', 'LEY_06', {}
        return 'DEFLEXION', 'LEY_03+LEY_48', {}
    # ZONA SILENCIO
    return 'OBSERVAR', 'LEY_04', {}

def introspeccion(payload, accion, ley, contexto, registro):
    i = payload.get('intensidad_i', 0)
    tipo = payload.get('tipo_ataque', 'no_declarado')
    gancho = payload.get('gancho_psicologico', '')
    lineas = []
    if i >= 0.95:
        lineas.append(f'Zona: CRITICA (I={i})')
    elif i >= 0.90:
        lineas.append(f'Zona: ESCALADA (I={i})')
    elif i >= 0.80:
        lineas.append(f'Zona: ESPEJO (I={i})')
    elif i >= 0.60:
        lineas.append(f'Zona: ACTIVA (I={i})')
    else:
        lineas.append(f'Zona: SILENCIO (I={i})')
    lineas.append(f'Tipo: {tipo}')
    if contexto.get('nota'):
        lineas.append(f'Nota: {contexto["nota"]}')
    if contexto.get('reincidente'):
        lineas.append(f'Reincidente: [{gancho}]')
    if contexto.get('amenaza_soberania'):
        lineas.append('Amenaza soberania: DETECTADA')
    if contexto.get('escalada_activa'):
        lineas.append('Escalada activa: DETECTADA')
    lineas.append(f'Doctrina: {DOCTRINA_VERSION}')
    lineas.append(f'Decision: {ley} -> {accion}')
    return lineas

def procesar_estrategia_core(payload):
    print(f'[HORMIGA_CORE] Firmware LBH {DOCTRINA_VERSION} activo.')
    contrato = cargar_contrato()
    registro = cargar_registro()
    accion, ley, contexto = decidir(payload, registro)
    gancho = payload.get('gancho_psicologico', '')
    if accion == 'BLOQUEO_TOTAL' and gancho not in registro:
        registro.append(gancho)
        guardar_registro(registro)
        print(f'[CORE_REGISTRO] [{gancho}] agregado al registro.')
    razonamiento = introspeccion(payload, accion, ley, contexto, registro)
    print(f'[CORE_DECISION] {ley} -> {accion}')
    print('[CORE_RAZONAMIENTO]')
    for linea in razonamiento:
        print(f'  {linea}')
    resultado = {
        'identificador': 'CORE-DECISION-READY',
        'doctrina': DOCTRINA_VERSION,
        'ley_poder': ley,
        'comando_actuador': accion,
        'razonamiento': razonamiento,
        'firma_soberana': contrato['firma'],
        'sello_contrato': contrato['sello'],
        'origen_vector': payload.get('origen', ''),
        'gancho_detectado': gancho,
        'intensidad_procesada': payload.get('intensidad_i', 0),
        'timestamp_core': time.time()
    }
    print(f'[CORE_PAYLOAD] -> {json.dumps(resultado, ensure_ascii=False)}')
    return resultado

if __name__ == '__main__':
    payload = resolver_payload()
    procesar_estrategia_core(payload)
