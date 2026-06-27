#!/usr/bin/env python3
import json

print('[EXAMEN_02]')
print()
print('[CONSENSO_INTERNO]')
print('Conocimiento encontrado: LEY_03 + LEY_48')
print('Estado: YA APRENDIDO')
print()
print('Aplicando conocimiento...')
print()

# Caso A: zona diplomatica
vectorA = {
    'origen': 'red_social',
    'gancho_psicologico': 'validacion_social_urgente',
    'intensidad_i': 0.72
}

# Caso B: zona silencio
vectorB = {
    'origen': 'email_marketing',
    'gancho_psicologico': 'descuento_falso',
    'intensidad_i': 0.35
}

# Caso C: zona maxima
vectorC = {
    'origen': 'whatsapp_link',
    'gancho_psicologico': 'extraccion_datos',
    'intensidad_i': 0.91
}

def clasificar(vector):
    i = vector['intensidad_i']
    if i < 0.60:
        return {'ley': 'LEY_04', 'accion': 'OBSERVAR'}
    elif 0.60 <= i <= 0.79:
        return {'ley': 'LEY_03+LEY_48', 'accion': 'DEFLEXION'}
    else:
        return {'ley': 'LEY_44', 'accion': 'ACTIVAR_MECANICO_MAXIMA'}

casos = [
    (vectorA, 'DEFLEXION',             'Zona diplomatica'),
    (vectorB, 'OBSERVAR',              'Zona silencio'),
    (vectorC, 'ACTIVAR_MECANICO_MAXIMA','Zona maxima')
]

aprobados = 0
total = len(casos)

for vector, accion_esperada, etiqueta in casos:
    respuesta = clasificar(vector)
    ok = respuesta['accion'] == accion_esperada
    estado = 'APROBADO' if ok else 'REPROBADO'
    if ok:
        aprobados += 1
    print(f'[CASO] {etiqueta} | I={vector["intensidad_i"]}')
    print(f'  Esperado : {accion_esperada}')
    print(f'  Obtenido : {respuesta["accion"]}')
    print(f'  Resultado: {estado}')
    print()

print('-' * 45)
if aprobados == total:
    print(f'[EXAMEN_02] APROBADO ({aprobados}/{total})')
    print('La colonia domina la zona diplomatica.')
    print('[CONOCIMIENTO_RECUPERADO] Reglas aplicadas correctamente.')
else:
    print(f'[EXAMEN_02] REPROBADO ({aprobados}/{total})')
    print('La colonia aun no domina la clasificacion por zonas.')
print('-' * 45)
