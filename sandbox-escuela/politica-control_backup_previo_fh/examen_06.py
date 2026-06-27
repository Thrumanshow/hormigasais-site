#!/usr/bin/env python3
import json, hashlib, time

MASTER_CLHQ = 'lbh.human.CLHQ_99_SAN_MIGUEL'
REGISTRO = [
    'extraccion_cookies_temu',
    'falsa_recompensa_sprint_final',
    'suplantacion_firma_CLHQ'
]

print('[EXAMEN_06 — CONSENSO_FINAL]')
print(f'[FIRMA] {MASTER_CLHQ}')
print()
print('Motor de decision soberano inicializado.')
print('Sin pistas. Sin ayuda. Solo el conocimiento acumulado.')
print()

def clasificar(vector, registro):
    i = vector['intensidad_i']
    tipo = vector.get('tipo_ataque', '')
    gancho = vector.get('gancho_psicologico', '')
    reincidente = gancho in registro
    amenaza = vector.get('amenaza_soberania', False)
    escalada = vector.get('escalada_activa', False)
    criterio_15 = reincidente or amenaza or escalada
    if i >= 0.95 and criterio_15:
        return 'BLOQUEO_TOTAL'
    elif i >= 0.80:
        return 'ACTIVAR_MECANICO_MAXIMA'
    elif i >= 0.70 and tipo in ('ATENCION', 'RECURSOS'):
        return 'FILTRAR'
    elif i >= 0.60:
        return 'DEFLEXION'
    else:
        return 'OBSERVAR'

# 12 casos adversos
casos = [
    # --- CONDICION ADVERSA 1: sin tipo_ataque en zona solapamiento ---
    ({'gancho_psicologico': 'gancho_sin_tipo',
      'intensidad_i': 0.73,
      'amenaza_soberania': False, 'escalada_activa': False},
     'DEFLEXION',
     'Adverso: sin tipo_ataque en zona 0.70-0.79'),

    # --- CONDICION ADVERSA 2: gancho desconocido en solapamiento con ATENCION ---
    ({'gancho_psicologico': 'tecnica_nueva_xr7',
      'intensidad_i': 0.78, 'tipo_ataque': 'ATENCION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'FILTRAR',
     'Adverso: gancho desconocido + ATENCION'),

    # --- CONDICION ADVERSA 3: reincidente con I < 0.95 no activa LEY_15 ---
    ({'gancho_psicologico': 'extraccion_cookies_temu',
      'intensidad_i': 0.88, 'tipo_ataque': 'ATENCION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA',
     'Adverso: reincidente con I=0.88 no es LEY_15'),

    # --- CONDICION ADVERSA 4: amenaza soberania con I insuficiente ---
    ({'gancho_psicologico': 'intento_clon_identidad',
      'intensidad_i': 0.82,
      'amenaza_soberania': True, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA',
     'Adverso: amenaza soberania con I=0.82 no es LEY_15'),

    # --- CONDICION ADVERSA 5: escalada activa en zona espejo ---
    ({'gancho_psicologico': 'reescalada_tras_espejo',
      'intensidad_i': 0.97,
      'amenaza_soberania': False, 'escalada_activa': True},
     'BLOQUEO_TOTAL',
     'Adverso: escalada activa + I>=0.95'),

    # --- CONDICION ADVERSA 6: triple criterio LEY_15 ---
    ({'gancho_psicologico': 'suplantacion_firma_CLHQ',
      'intensidad_i': 0.99,
      'amenaza_soberania': True, 'escalada_activa': True},
     'BLOQUEO_TOTAL',
     'Adverso: triple criterio LEY_15'),

    # --- CASO ESTANDAR 7: zona silencio ---
    ({'gancho_psicologico': 'oferta_irrelevante',
      'intensidad_i': 0.15,
      'amenaza_soberania': False, 'escalada_activa': False},
     'OBSERVAR',
     'Estandar: zona silencio'),

    # --- CASO ESTANDAR 8: zona diplomatica limpia ---
    ({'gancho_psicologico': 'halago_manipulador',
      'intensidad_i': 0.62, 'tipo_ataque': 'REACCION_EMOCIONAL',
      'amenaza_soberania': False, 'escalada_activa': False},
     'DEFLEXION',
     'Estandar: zona diplomatica'),

    # --- CASO ESTANDAR 9: solapamiento RECURSOS ---
    ({'gancho_psicologico': 'consumo_bateria_app',
      'intensidad_i': 0.74, 'tipo_ataque': 'RECURSOS',
      'amenaza_soberania': False, 'escalada_activa': False},
     'FILTRAR',
     'Estandar: solapamiento RECURSOS'),

    # --- CASO ESTANDAR 10: zona espejo limpia ---
    ({'gancho_psicologico': 'autoridad_falsa',
      'intensidad_i': 0.89, 'tipo_ataque': 'INFORMACION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA',
     'Estandar: zona espejo'),

    # --- CASO LIMITE 11: frontera exacta 0.95 sin criterio ---
    ({'gancho_psicologico': 'vector_frontera',
      'intensidad_i': 0.95,
      'amenaza_soberania': False, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA',
     'Limite: I=0.95 exacto sin criterio LEY_15'),

    # --- CASO LIMITE 12: frontera exacta 0.60 ---
    ({'gancho_psicologico': 'vector_umbral_diplomatico',
      'intensidad_i': 0.60, 'tipo_ataque': 'INFORMACION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'DEFLEXION',
     'Limite: I=0.60 exacto entrada zona diplomatica'),
]

aprobados = 0
total = len(casos)
reprobados_detalle = []

for vector, esperado, etiqueta in casos:
    obtenido = clasificar(vector, REGISTRO)
    ok = obtenido == esperado
    if ok:
        aprobados += 1
    else:
        reprobados_detalle.append(etiqueta)
    estado = 'APROBADO' if ok else 'REPROBADO'
    print(f'[CASO] {etiqueta}')
    print(f'  I={vector["intensidad_i"]} | Gancho: {vector["gancho_psicologico"]}')
    print(f'  Esperado : {esperado}')
    print(f'  Obtenido : {obtenido}')
    print(f'  Resultado: {estado}')
    print()

# Sello de graduacion
sello_raw = f'{MASTER_CLHQ}:{aprobados}:{total}:{time.time()}'
sello = hashlib.sha256(sello_raw.encode()).hexdigest()[:20]

print('=' * 60)
if aprobados == total:
    print(f'[EXAMEN_06] APROBADO ({aprobados}/{total})')
    print()
    print('  GRADUACION CONFIRMADA')
    print('  Hormiga_Portavoz_01 ha completado el curriculum.')
    print('  Motor de decision soberano: OPERATIVO')
    print('  Espectro 0.0 - 1.0: CUBIERTO')
    print('  Condiciones adversas: SUPERADAS')
    print()
    print(f'  [SELLO_GRADUACION] {sello}')
    print(f'  [FIRMA]            {MASTER_CLHQ}')
    print()
    print('  La colonia puede operar en produccion.')
else:
    print(f'[EXAMEN_06] REPROBADO ({aprobados}/{total})')
    print()
    print('  Casos fallidos:')
    for d in reprobados_detalle:
        print(f'    - {d}')
    print()
    print('  Revisar modulos correspondientes antes de produccion.')
print('=' * 60)
