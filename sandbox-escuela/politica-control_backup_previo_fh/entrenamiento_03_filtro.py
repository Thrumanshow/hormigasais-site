#!/usr/bin/env python3
import json

print('[ENTRENAMIENTO_03]')
print('[OBJETIVO] Distinguir entre deflectar y filtrar activamente.')
print('[LEY] LEY_06_PROTEGER_ATENCION')
print('[ZONA] Intensidad 0.70 - 0.84: zona de solapamiento critico')
print()

print('[CONCEPTO]')
print('En la zona 0.70-0.84 dos leyes compiten:')
print()
print('  LEY_03 + LEY_48 (0.60-0.79): deflectar, fluir, no revelar.')
print('  LEY_06          (0.70-0.84): filtrar, cortar el acceso,')
print('                               proteger la atencion de la colonia.')
print()
print('La diferencia clave:')
print('  DEFLEXION -> el vector sigue existiendo, solo fue redirigido.')
print('  FILTRAR   -> el vector es bloqueado en el perimetro.')
print('               La colonia no gasta atencion en el en absoluto.')
print()
print('Criterio de decision en zona de solapamiento:')
print('  Si el gancho ataca la ATENCION o RECURSOS de la colonia -> FILTRAR')
print('  Si el gancho busca INFORMACION o REACCION emocional    -> DEFLEXION')
print()

casos = [
    {
        'origen': 'notificacion_push',
        'gancho_psicologico': 'consumo_atencion_bucle',
        'intensidad_i': 0.76,
        'tipo_ataque': 'ATENCION'
    },
    {
        'origen': 'red_social',
        'gancho_psicologico': 'polemica_viral',
        'intensidad_i': 0.71,
        'tipo_ataque': 'REACCION_EMOCIONAL'
    },
    {
        'origen': 'app_juego',
        'gancho_psicologico': 'bucle_recompensa_variable',
        'intensidad_i': 0.82,
        'tipo_ataque': 'RECURSOS'
    }
]

def clasificar_zona_solapamiento(vector):
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

print('[VECTORES_DE_ENTRENAMIENTO]')
for v in casos:
    r = clasificar_zona_solapamiento(v)
    print(f'  Gancho: {v["gancho_psicologico"]}')
    print(f'  I={v["intensidad_i"]} | Tipo: {v["tipo_ataque"]}')
    print(f'  Accion: {r["accion"]} ({r["ley"]})')
    print()

print('[APRENDIZAJE]')
print('La colonia aprende:')
print('En zona de solapamiento el TIPO de ataque decide la ley.')
print('Atencion y recursos -> FILTRAR (LEY_06).')
print('Informacion y emocion -> DEFLEXION (LEY_03+LEY_48).')
