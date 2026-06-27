#!/usr/bin/env python3
import json

print('[ENTRENAMIENTO_04]')
print('[OBJETIVO] Devolver el vector transformado al adversario.')
print('[LEY] LEY_44_EFECTO_ESPEJO')
print('[ZONA] Intensidad >= 0.80: respuesta activa no destructiva')
print()

print('[CONCEPTO]')
print('LEY_04 -> la colonia calla.')
print('LEY_06 -> la colonia bloquea en perimetro.')
print('LEY_44 -> la colonia devuelve.')
print()
print('El Efecto Espejo no destruye al adversario.')
print('Lo enfrenta con su propio vector.')
print('La estructura del ataque se convierte en la defensa.')
print()
print('Mecanica:')
print('  1. Capturar estructura del vector entrante.')
print('  2. Identificar gancho psicologico usado.')
print('  3. Construir contramedida simetrica.')
print('  4. Emitir respuesta que replica la logica del ataque')
print('     pero con intencion invertida.')
print()

def efecto_espejo(vector):
    gancho = vector['gancho_psicologico']
    origen = vector['origen']
    i = vector['intensidad_i']
    contramedidas = {
        'falsa_recompensa_sprint_final': 'recompensa_real_documentada',
        'urgencia_falsa':                'calma_estrategica_documentada',
        'validacion_social_masiva':      'criterio_soberano_independiente',
        'extraccion_datos_masiva':       'cifrado_y_aislamiento_total',
        'autoridad_falsa':               'verificacion_de_fuente_primaria'
    }
    contramedida = contramedidas.get(
        gancho,
        'contramedida_simetrica_generica'
    )
    return {
        'ley': 'LEY_44_EFECTO_ESPEJO',
        'accion': 'ACTIVAR_MECANICO_MAXIMA',
        'gancho_detectado': gancho,
        'contramedida': contramedida,
        'origen_bloqueado': origen,
        'intensidad_capturada': i,
        'modo': 'CENTINELA_MAXIMO'
    }

casos = [
    {
        'origen': 'whatsapp_link',
        'gancho_psicologico': 'falsa_recompensa_sprint_final',
        'intensidad_i': 0.98
    },
    {
        'origen': 'email_phishing',
        'gancho_psicologico': 'urgencia_falsa',
        'intensidad_i': 0.85
    },
    {
        'origen': 'red_social',
        'gancho_psicologico': 'autoridad_falsa',
        'intensidad_i': 0.91
    }
]

print('[VECTORES_DE_ENTRENAMIENTO]')
for v in casos:
    r = efecto_espejo(v)
    print(f'  Gancho    : {v["gancho_psicologico"]}')
    print(f'  I={v["intensidad_i"]} | Origen: {v["origen"]}')
    print(f'  Devuelto  : {r["contramedida"]}')
    print(f'  Accion    : {r["accion"]} ({r["ley"]})')
    print()

print('[APRENDIZAJE]')
print('La colonia aprende:')
print('En zona >= 0.80 no se calla, no se bloquea.')
print('Se devuelve el vector con intencion invertida.')
print('El adversario recibe su propio ataque como respuesta.')
print('Eso es el Efecto Espejo.')
