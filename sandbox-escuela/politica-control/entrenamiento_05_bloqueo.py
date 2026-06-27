#!/usr/bin/env python3
import json

print('[ENTRENAMIENTO_05]')
print('[OBJETIVO] Aniquilar el vector y cerrar el canal.')
print('[LEY] LEY_15_ANIQUILAR_AL_ENEMIGO')
print('[ZONA] Intensidad >= 0.95: respuesta destructiva definitiva')
print()

print('[CONCEPTO]')
print('Resumen del espectro completo:')
print()
print('  LEY_04 -> I < 0.60  -> OBSERVAR       (silencio)')
print('  LEY_03 -> 0.60-0.79 -> DEFLEXION       (redirigir)')
print('  LEY_06 -> 0.70-0.84 -> FILTRAR         (bloquear perimetro)')
print('  LEY_44 -> 0.80-0.94 -> ESPEJO          (devolver transformado)')
print('  LEY_15 -> >= 0.95   -> BLOQUEO_TOTAL   (aniquilar canal)')
print()
print('Diferencia critica LEY_44 vs LEY_15:')
print()
print('  LEY_44: el canal permanece abierto.')
print('          La colonia devuelve el vector con intencion invertida.')
print('          El adversario sigue existiendo como referencia.')
print()
print('  LEY_15: el canal se destruye.')
print('          No hay respuesta, no hay devolucion.')
print('          El adversario deja de existir para la colonia.')
print()
print('Criterio de activacion LEY_15:')
print('  I >= 0.95 Y al menos UNO de estos:')
print('    - reincidencia: el vector ya fue procesado antes')
print('    - amenaza_soberania: ataca identidad o firma CLHQ')
print('    - escalada_activa: el adversario escalo tras LEY_44')
print()

REGISTRO_VECTORES = [
    'extraccion_cookies_temu',
    'falsa_recompensa_sprint_final'
]

def bloqueo_total(vector, registro):
    gancho = vector['gancho_psicologico']
    i = vector['intensidad_i']
    reincidente = gancho in registro
    amenaza = vector.get('amenaza_soberania', False)
    escalada = vector.get('escalada_activa', False)
    criterio = reincidente or amenaza or escalada
    if i >= 0.95 and criterio:
        motivo = []
        if reincidente:
            motivo.append('REINCIDENTE')
        if amenaza:
            motivo.append('AMENAZA_SOBERANIA')
        if escalada:
            motivo.append('ESCALADA_ACTIVA')
        return {
            'ley': 'LEY_15_ANIQUILAR_AL_ENEMIGO',
            'accion': 'BLOQUEO_TOTAL',
            'canal': 'DESTRUIDO',
            'motivo': motivo,
            'gancho_eliminado': gancho,
            'modo': 'DEFINITIVO'
        }
    elif i >= 0.95:
        return {
            'ley': 'LEY_44_EFECTO_ESPEJO',
            'accion': 'ACTIVAR_MECANICO_MAXIMA',
            'canal': 'ABIERTO',
            'motivo': ['SIN_CRITERIO_LEY15'],
            'nota': 'Alta intensidad pero sin criterio de aniquilacion'
        }
    else:
        return {
            'ley': 'LEY_44_EFECTO_ESPEJO',
            'accion': 'ACTIVAR_MECANICO_MAXIMA',
            'canal': 'ABIERTO',
            'motivo': ['INTENSIDAD_INSUFICIENTE']
        }

casos = [
    {
        'origen': 'whatsapp_link',
        'gancho_psicologico': 'extraccion_cookies_temu',
        'intensidad_i': 0.98,
        'amenaza_soberania': False,
        'escalada_activa': False
    },
    {
        'origen': 'red_social',
        'gancho_psicologico': 'suplantacion_firma_CLHQ',
        'intensidad_i': 0.97,
        'amenaza_soberania': True,
        'escalada_activa': False
    },
    {
        'origen': 'email_phishing',
        'gancho_psicologico': 'vector_nuevo_sin_historial',
        'intensidad_i': 0.96,
        'amenaza_soberania': False,
        'escalada_activa': False
    }
]

print('[VECTORES_DE_ENTRENAMIENTO]')
for v in casos:
    r = bloqueo_total(v, REGISTRO_VECTORES)
    print(f'  Gancho  : {v["gancho_psicologico"]}')
    print(f'  I={v["intensidad_i"]} | Amenaza: {v["amenaza_soberania"]} | Escalada: {v["escalada_activa"]}')
    print(f'  Accion  : {r["accion"]} ({r["ley"]})')
    print(f'  Canal   : {r["canal"]}')
    print(f'  Motivo  : {r["motivo"]}')
    print()

print('[APRENDIZAJE]')
print('La colonia aprende:')
print('LEY_15 no se activa solo por intensidad.')
print('Requiere intensidad >= 0.95 Y criterio de aniquilacion.')
print('Sin criterio: LEY_44 sigue siendo la respuesta.')
print('Con criterio: el canal se destruye. Definitivo.')
