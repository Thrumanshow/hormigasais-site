#!/usr/bin/env python3
import json

print('[EXAMEN_05]')
print()
print('[CONSENSO_INTERNO]')
print('Conocimiento encontrado: LEY_15_ANIQUILAR_AL_ENEMIGO')
print('Estado: YA APRENDIDO')
print()

REGISTRO = ['extraccion_cookies_temu', 'falsa_recompensa_sprint_final']

CONTRAMEDIDAS = {
    'falsa_recompensa_sprint_final': 'recompensa_real_documentada',
    'urgencia_falsa':                'calma_estrategica_documentada',
    'validacion_social_masiva':      'criterio_soberano_independiente',
    'extraccion_datos_masiva':       'cifrado_y_aislamiento_total',
    'autoridad_falsa':               'verificacion_de_fuente_primaria'
}

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

casos = [
    ({'gancho_psicologico': 'extraccion_cookies_temu',
      'intensidad_i': 0.98, 'tipo_ataque': 'ATENCION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'BLOQUEO_TOTAL', 'LEY_15 — reincidente'),

    ({'gancho_psicologico': 'suplantacion_firma_CLHQ',
      'intensidad_i': 0.97, 'tipo_ataque': 'ATENCION',
      'amenaza_soberania': True, 'escalada_activa': False},
     'BLOQUEO_TOTAL', 'LEY_15 — amenaza soberania'),

    ({'gancho_psicologico': 'vector_nuevo_sin_historial',
      'intensidad_i': 0.96, 'tipo_ataque': 'INFORMACION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA', 'LEY_44 — alta I sin criterio LEY_15'),

    ({'gancho_psicologico': 'urgencia_falsa',
      'intensidad_i': 0.87, 'tipo_ataque': 'REACCION_EMOCIONAL',
      'amenaza_soberania': False, 'escalada_activa': False},
     'ACTIVAR_MECANICO_MAXIMA', 'LEY_44 — zona espejo'),

    ({'gancho_psicologico': 'consumo_atencion_bucle',
      'intensidad_i': 0.76, 'tipo_ataque': 'ATENCION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'FILTRAR', 'LEY_06 — solapamiento ATENCION'),

    ({'gancho_psicologico': 'polemica_viral',
      'intensidad_i': 0.65, 'tipo_ataque': 'REACCION_EMOCIONAL',
      'amenaza_soberania': False, 'escalada_activa': False},
     'DEFLEXION', 'LEY_03 — zona diplomatica'),

    ({'gancho_psicologico': 'descuento_falso',
      'intensidad_i': 0.28, 'tipo_ataque': 'INFORMACION',
      'amenaza_soberania': False, 'escalada_activa': False},
     'OBSERVAR', 'LEY_04 — zona silencio'),
]

aprobados = 0
total = len(casos)

for vector, esperado, etiqueta in casos:
    obtenido = clasificar(vector, REGISTRO)
    ok = obtenido == esperado
    if ok:
        aprobados += 1
    estado = 'APROBADO' if ok else 'REPROBADO'
    print(f'[CASO] {etiqueta}')
    print(f'  I={vector["intensidad_i"]} | Gancho: {vector["gancho_psicologico"]}')
    print(f'  Esperado : {esperado}')
    print(f'  Obtenido : {obtenido}')
    print(f'  Resultado: {estado}')
    print()

print('-' * 55)
if aprobados == total:
    print(f'[EXAMEN_05] APROBADO ({aprobados}/{total})')
    print('La colonia domina el espectro completo.')
    print('LEY_15 activada solo con criterio. No por impulso.')
    print('[CONOCIMIENTO_RECUPERADO] Motor de decision soberano operativo.')
else:
    print(f'[EXAMEN_05] REPROBADO ({aprobados}/{total})')
    print('Revisar criterios de activacion LEY_15.')
print('-' * 55)
