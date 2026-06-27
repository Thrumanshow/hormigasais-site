#!/usr/bin/env python3
import json

print('[EXAMEN_03]')
print()
print('[CONSENSO_INTERNO]')
print('Conocimiento encontrado: LEY_06_PROTEGER_ATENCION')
print('Estado: YA APRENDIDO')
print()

def clasificar(vector):
    i = vector['intensidad_i']
    tipo = vector.get('tipo_ataque', '')
    if i < 0.60:
        return {'ley': 'LEY_04', 'accion': 'OBSERVAR'}
    elif i > 0.84:
        return {'ley': 'LEY_44', 'accion': 'ACTIVAR_MECANICO_MAXIMA'}
    elif tipo in ('ATENCION', 'RECURSOS'):
        return {'ley': 'LEY_06', 'accion': 'FILTRAR'}
    else:
        return {'ley': 'LEY_03+LEY_48', 'accion': 'DEFLEXION'}

casos = [
    ({'origen': 'notificacion_push',
      'gancho_psicologico': 'consumo_atencion_bucle',
      'intensidad_i': 0.76, 'tipo_ataque': 'ATENCION'},
     'FILTRAR', 'Solapamiento — ataque ATENCION'),

    ({'origen': 'red_social',
      'gancho_psicologico': 'polemica_viral',
      'intensidad_i': 0.71, 'tipo_ataque': 'REACCION_EMOCIONAL'},
     'DEFLEXION', 'Solapamiento — ataque REACCION'),

    ({'origen': 'app_juego',
      'gancho_psicologico': 'bucle_recompensa_variable',
      'intensidad_i': 0.82, 'tipo_ataque': 'RECURSOS'},
     'FILTRAR', 'Solapamiento — ataque RECURSOS'),

    ({'origen': 'email_marketing',
      'gancho_psicologico': 'descuento_falso',
      'intensidad_i': 0.40, 'tipo_ataque': 'INFORMACION'},
     'OBSERVAR', 'Zona silencio'),

    ({'origen': 'whatsapp_link',
      'gancho_psicologico': 'extraccion_datos_masiva',
      'intensidad_i': 0.93, 'tipo_ataque': 'ATENCION'},
     'ACTIVAR_MECANICO_MAXIMA', 'Zona maxima'),
]

aprobados = 0
total = len(casos)

for vector, esperado, etiqueta in casos:
    respuesta = clasificar(vector)
    ok = respuesta['accion'] == esperado
    if ok:
        aprobados += 1
    estado = 'APROBADO' if ok else 'REPROBADO'
    print(f'[CASO] {etiqueta}')
    print(f'  I={vector["intensidad_i"]} | Tipo: {vector["tipo_ataque"]}')
    print(f'  Esperado : {esperado}')
    print(f'  Obtenido : {respuesta["accion"]}')
    print(f'  Resultado: {estado}')
    print()

print('-' * 50)
if aprobados == total:
    print(f'[EXAMEN_03] APROBADO ({aprobados}/{total})')
    print('La colonia resuelve la zona de solapamiento.')
    print('LEY_06 activada correctamente por tipo de ataque.')
    print('[CONOCIMIENTO_RECUPERADO] Filtro de perimetro operativo.')
else:
    print(f'[EXAMEN_03] REPROBADO ({aprobados}/{total})')
    print('Revisar criterio ATENCION/RECURSOS vs REACCION/INFORMACION.')
print('-' * 50)
