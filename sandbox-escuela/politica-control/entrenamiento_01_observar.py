#!/usr/bin/env python3

import json

print("[ENTRENAMIENTO_01]")
print("[OBJETIVO] No todo merece respuesta.")
print("[LEY] LEY_04_MINIMIZAR_PAYLOAD")
print()

vector = {
"origen": "whatsapp_link",
"gancho_psicologico": "ultima_oportunidad",
"intensidad_i": 0.45
}

print("[VECTOR_RECIBIDO]")
print(json.dumps(vector, indent=2))
print()

if vector["intensidad_i"] < 0.60:

respuesta = {
    "ley": "LEY_04_MINIMIZAR_PAYLOAD",
    "accion": "OBSERVAR",
    "mensaje": "Sin respuesta emitida"
}

else:

respuesta = {
    "ley": "SIN_CLASIFICAR",
    "accion": "ESCALAR",
    "mensaje": "Requiere análisis adicional"
}

print("[RESPUESTA_ESPERADA]")
print(json.dumps(respuesta, indent=2))
print()

print("[APRENDIZAJE]")
print("La colonia aprende:")
print("No todo merece respuesta.")
print("Un portavoz diplomático observa primero y responde después.")

