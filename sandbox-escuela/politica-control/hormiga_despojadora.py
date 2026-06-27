#!/usr/bin/env python3
# Hormiga_Despojadora v1.0
# Rol: sanitizar el vector antes de entrar al nido
# Una sola responsabilidad: limpiar o rechazar
# NO decide. NO aconseja. Solo despoja.
import json, sys, re, time

# Campos obligatorios minimos
CAMPOS_REQUERIDOS = ['gancho_psicologico', 'intensidad_i']

# Tipos de ataque validos
TIPOS_VALIDOS = {
    'ATENCION', 'RECURSOS',
    'REACCION_EMOCIONAL', 'INFORMACION'
}

# Patrones de inyeccion en campos de texto
PATRONES_INYECCION = [
    r'__import__', r'eval\(', r'exec\(', r'subprocess',
    r'os\.system', r'<script', r'javascript:',
    r'\$\{', r'\{\{', r'\\x[0-9a-fA-F]{2}'
]

def detectar_inyeccion(texto):
    for patron in PATRONES_INYECCION:
        if re.search(patron, str(texto), re.IGNORECASE):
            return True, patron
    return False, None

def despojar(payload_raw):
    errores = []
    advertencias = []
    payload_limpio = {}
    # 1. Verificar campos requeridos
    for campo in CAMPOS_REQUERIDOS:
        if campo not in payload_raw:
            errores.append(f'campo_requerido_faltante:{campo}')
    if errores:
        return None, errores, advertencias
    # 2. Normalizar intensidad
    try:
        i = float(payload_raw['intensidad_i'])
        if i < 0.0:
            advertencias.append('intensidad_negativa_corregida_a_0.0')
            i = 0.0
        if i > 1.0:
            advertencias.append('intensidad_mayor_a_1_corregida_a_1.0')
            i = 1.0
        payload_limpio['intensidad_i'] = round(i, 4)
    except (ValueError, TypeError):
        errores.append('intensidad_no_numerica')
        return None, errores, advertencias
    # 3. Limpiar gancho psicologico
    gancho = str(payload_raw.get('gancho_psicologico', '')).strip()
    inyectado, patron = detectar_inyeccion(gancho)
    if inyectado:
        errores.append(f'inyeccion_detectada_en_gancho:{patron}')
        return None, errores, advertencias
    # Normalizar: solo alfanumerico y guiones bajos
    gancho_limpio = re.sub(r'[^a-zA-Z0-9_\-]', '_', gancho)[:80]
    if gancho_limpio != gancho:
        advertencias.append(f'gancho_normalizado:{gancho}->{gancho_limpio}')
    payload_limpio['gancho_psicologico'] = gancho_limpio
    # 4. Validar tipo de ataque
    tipo = str(payload_raw.get('tipo_ataque', '')).upper().strip()
    if tipo and tipo not in TIPOS_VALIDOS:
        advertencias.append(f'tipo_ataque_invalido:{tipo}->INFORMACION')
        tipo = 'INFORMACION'
    payload_limpio['tipo_ataque'] = tipo or 'INFORMACION'
    # 5. Limpiar origen
    origen = str(payload_raw.get('origen', 'desconocido')).strip()
    inyectado, patron = detectar_inyeccion(origen)
    if inyectado:
        advertencias.append(f'inyeccion_en_origen_sanitizada')
        origen = 'origen_sanitizado'
    payload_limpio['origen'] = re.sub(r'[^a-zA-Z0-9_\-]', '_', origen)[:50]
    # 6. Copiar campos booleanos seguros
    payload_limpio['amenaza_soberania'] = bool(
        payload_raw.get('amenaza_soberania', False)
    )
    payload_limpio['escalada_activa'] = bool(
        payload_raw.get('escalada_activa', False)
    )
    # 7. Preservar identificador si existe
    if 'identificador' in payload_raw:
        payload_limpio['identificador'] = str(
            payload_raw['identificador']
        )[:50]
    # 8. Timestamp de despojo
    payload_limpio['timestamp_despojo'] = time.time()
    payload_limpio['despojado'] = True
    return payload_limpio, errores, advertencias

def main():
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            for linea in raw.splitlines():
                if '[SENSOR_PAYLOAD]' in linea and '->' in linea:
                    raw = linea.split('->', 1)[1].strip()
                    break
            payload_raw = json.loads(raw)
        except json.JSONDecodeError as e:
            resultado = {
                'aprobado': False,
                'errores': [f'json_invalido:{e}'],
                'advertencias': []
            }
            print(
                f'[DESPOJADORA_RESULTADO] -> '
                f'{json.dumps(resultado, ensure_ascii=False)}'
            )
            sys.exit(1)
    elif len(sys.argv) > 1:
        try:
            payload_raw = json.loads(sys.argv[1])
        except json.JSONDecodeError:
            sys.exit(1)
    else:
        # Test con vector malicioso
        payload_raw = {
            'gancho_psicologico': 'test__import__os_attack',
            'intensidad_i': 1.5,
            'tipo_ataque': 'TIPO_INVALIDO',
            'origen': 'red<script>alert(1)</script>',
            'amenaza_soberania': True
        }
    payload_limpio, errores, advertencias = despojar(payload_raw)
    aprobado = len(errores) == 0
    resultado = {
        'aprobado': aprobado,
        'payload_limpio': payload_limpio,
        'errores': errores,
        'advertencias': advertencias
    }
    print(
        f'[DESPOJADORA_RESULTADO] -> '
        f'{json.dumps(resultado, ensure_ascii=False)}'
    )
    sys.stdout.flush()
    if not aprobado:
        sys.exit(1)

if __name__ == '__main__':
    main()
