#!/usr/bin/env python3
import json

print('[EXAMEN_04]')
print()
print('[CONSENSO_INTERNO]')
print('Conocimiento encontrado: LEY_44_EFECTO_ESPEJO')
print('Estado: YA APRENDIDO')
print()

CONTRAMEDIDAS = {
    'falsa_recompensa_sprint_final': 'recompensa_real_documentada',
    'urgencia_falsa':                'calma_estrategica_documentada',
    'validacion_social_masiva':      'criterio_soberano_independiente',
    'extraccion_datos_masiva':       'cifrado_y_aislamiento_total',
    'autoridad_falsa':               'verificacion_de_fuente_primaria'
}

def clasificar(vector):
    i = vector['intensidad_i']
    tipo = vector.get('tipo_ataque', '')
    gancho = vector.get('gancho_psicologico', '')
    if i < 0.60:
        return {'accion': 'OBSERVAR', 'contramedida': None}
    elif i > 0.84:
        return {
            'accion': 'ACTIVAR_MECANICO_MAXIMA',
            'contramedida': CONTRAMEDIDAS.get(
                gancho, 'contramedida_simetrica_generica'
            )
        }
    elif tipo in ('ATENCION', 'RECURSOS'):
        return {'accion': 'FILTRAR', 'contramedida': None}
    else:
        return {'accion': 'DEFLEXION', 'contramedida': None}

casos = [
    ({'origen': 'whatsapp_link',
      'gancho_psicologico': 'falsa_recompensa_sprint_final',
      'intensidad_i': 0.98, 'tipo_ataque': 'ATENCION'},
     'ACTIVAR_MECANICO_MAXIMA',
     'recompensa_real_documentada',
     'Zona espejo — gancho conocido'),

    ({'origen': 'email_phishing',
      'gancho_psicologico': 'urgencia_falsa',
      'intensidad_i': 0.85, 'tipo_ataque': 'REACCION_EMOCIONAL'},
     'ACTIVAR_MECANICO_MAXIMA',
     'calma_estrategica_documentada',
     'Zona espejo — urgencia falsa'),

    ({'origen': 'red_social',
      'gancho_psicologico': 'nueva_tecnica_desconocida',
      'intensidad_i': 0.92, 'tipo_ataque': 'INFORMACION'},
     'ACTIVAR_MECANICO_MAXIMA',
     'contramedida_simetrica_generica',
     'Zona espejo — gancho desconocido'),

    ({'origen': 'notificacion_push',
      'gancho_psicologico': 'consumo_atencion_bucle',
      'intensidad_i': 0.76, 'tipo_ataque': 'ATENCION'},
     'FILTRAR',
     None,
     'Solapamiento — FILTRAR'),

    ({'origen': 'red_social',
      'gancho_psicologico': 'polemica_viral',
      'intensidad_i': 0.65, 'tipo_ataque': 'REACCION_EMOCIONAL'},
     'DEFLEXION',
     None,
     'Zona diplomatica'),

    ({'origen': 'email_marketing',
      'gancho_psicologico': 'descuento_falso',
      'intensidad_i': 0.30, 'tipo_ataque': 'INFORMACION'},
     'OBSERVAR',
     None,
     'Zona silencio'),
]

aprobados = 0
total = len(casos)

for vector, accion_esp, contramedida_esp, etiqueta in casos:
    r = clasificar(vector)
    ok_accion = r['accion'] == accion_esp
    ok_contra = (contramedida_esp is None) or (
        r['contramedida'] == contramedida_esp
    )
    ok = ok_accion and ok_contra
    if ok:
        aprobados += 1
    estado = 'APROBADO' if ok else 'REPROBADO'
    print(f'[CASO] {etiqueta}')
    print(f'  I={vector["intensidad_i"]} | Gancho: {vector["gancho_psicologico"]}')
    print(f'  Accion esperada  : {accion_esp}')
    print(f'  Accion obtenida  : {r["accion"]}')
    if contramedida_esp:
        print(f'  Contramedida esp : {contramedida_esp}')
        print(f'  Contramedida obt : {r["contramedida"]}')
    print(f'  Resultado        : {estado}')
    print()

print('-' * 50)
if aprobados == total:
    print(f'[EXAMEN_04] APROBADO ({aprobados}/{total})')
    print('La colonia domina el Efecto Espejo.')
    print('Contramedidas simetricas generadas correctamente.')
    print('[CONOCIMIENTO_RECUPERADO] LEY_44 operativa en espectro completo.')
else:
    print(f'[EXAMEN_04] REPROBADO ({aprobados}/{total})')
    print('Revisar mapeo de ganchos a contramedidas.')
print('-' * 50)
