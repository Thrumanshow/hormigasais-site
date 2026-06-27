#!/usr/bin/env python3
# LBH-Sensor v2.1 | stdout limpio para pipe
import json, time, sys

# Gancho configurable via argv o default
gancho = sys.argv[1] if len(sys.argv) > 1 else 'falsa_recompensa_sprint_final'
intensidad = float(sys.argv[2]) if len(sys.argv) > 2 else 0.98

print('[HORMIGA_SENSOR] Perimetro activo. Escaneando telemetria entrante...')
print(f'[PIR_LOG] Vector detectado (I={intensidad} | Gancho: {gancho})')

payload = {
    'identificador': 'VECTOR-INFO-DETECTED',
    'origen': 'whatsapp_link',
    'gancho_psicologico': gancho,
    'intensidad_i': intensidad,
    'timestamp': time.time()
}

linea = f'[SENSOR_PAYLOAD] -> {json.dumps(payload, ensure_ascii=False)}'
print(linea)
# Flush garantizado para pipe sin buffer
sys.stdout.flush()
