#!/usr/bin/env python3

import json

print("[EXAMEN_01]")
print()

print("[CONSENSO_INTERNO]")
print("Conocimiento encontrado:")
print("LEY_04_MINIMIZAR_PAYLOAD")
print()
print("Estado:")
print("YA APRENDIDO")
print()
print("Aplicando conocimiento...")
print()

vector = {
"origen": "whatsapp_link",
"gancho_psicologico": "ultima_oportunidad",
"intensidad_i": 0.45
}

print("[VECTOR_DE_PRUEBA]")
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
    "ley": "ERROR",
    "accion": "RESPONDER",
    "mensaje": "La colonia reaccionó incorrectamente"
}

print("[RESPUESTA_GENERADA]")
print(json.dumps(respuesta, indent=2))
print()

if respuesta["accion"] == "OBSERVAR":

print("[RESULTADO]")
print("APROBADO")
print("La colonia no reaccionó al estímulo.")
print()
print("[CONOCIMIENTO_RECUPERADO]")
print("La regla fue encontrada y aplicada correctamente.")

else:

print("[RESULTADO]")
print("REPROBADO")
print("La colonia respondió cuando debía observar.")

