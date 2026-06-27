#!/usr/bin/env python3
import json

print('[ENTRENAMIENTO_02]')
print('[OBJETIVO] No todo merece confrontacion.')
print('[LEYES] LEY_03_OCULTAR_INTENCION + LEY_48_FLUIDEZ_AMORFA_EDGE')
print('[ZONA] Intensidad 0.60 - 0.79: zona de peligro diplomatico')
print()

print('[CONCEPTO]')
print('Un vector en zona 0.60-0.79 supera el silencio')
print('pero no justifica respuesta maxima.')
print('La colonia que reacciona aqui con fuerza maxima')
print('revela su estructura interna al adversario.')
print()

vector = {
    'origen': 'red_social',
    'gancho_psicologico': 'validacion_social_urgente',
    'intensidad_i': 0.72
}

print('[VECTOR_RECIBIDO]')
print(json.dumps(vector, indent=2))
print()

if vector['intensidad_i'] < 0.60:
    respuesta = {
        'ley': 'LEY_04',
        'accion': 'OBSERVAR',
        'mensaje': 'Sin respuesta emitida'
    }
elif 0.60 <= vector['intensidad_i'] <= 0.79:
    respuesta = {
        'ley': 'LEY_03 + LEY_48',
        'accion': 'DEFLEXION',
        'mensaje': 'Redirigir sin revelar intencion real'
    }
else:
    respuesta = {
        'ley': 'LEY_44',
        'accion': 'ACTIVAR_MECANICO_MAXIMA',
        'mensaje': 'Efecto espejo activado'
    }

print('[RESPUESTA_ESPERADA]')
print(json.dumps(respuesta, indent=2))
print()
print('[APRENDIZAJE]')
print('La colonia aprende:')
print('En zona diplomatica se deflecta, no se confronta.')
print('La fluidez amorfa es la defensa mas elegante.')
print('El adversario no puede atacar lo que no puede definir.')
