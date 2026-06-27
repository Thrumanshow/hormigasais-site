#!/usr/bin/env python3

import json
import time

def ejecutar_respuesta(decision_json):

    print("[HORMIGA_ACTUADORA] Módulo portavoz activo...")
    time.sleep(1)

    try:
        decision = json.loads(decision_json)

        ley = decision.get("ley_poder", "DESCONOCIDA")
        comando = decision.get("comando_actuador", "NINGUNO")

    except Exception as e:

        print(f"[ERR_ACTUADORA] Payload inválido: {e}")

        return json.dumps({
            "status": "ERROR",
            "error_code": "ACTUATOR_BAD_PAYLOAD"
        })

    respuesta = {}

    if comando == "ACTIVAR_MECANICO_MAXIMA":

        respuesta = {
            "modo": "CENTINELA_MAXIMO",
            "mensaje": "Interrupción por Agente Centinela (100% EFICACIA)"
        }

    elif comando == "ACTIVAR_MECANICO_MODERADA":

        respuesta = {
            "modo": "PORTAVOZ_MINIMO",
            "mensaje": "Validación mínima emitida. Exposición reducida."
        }

    elif comando == "MANTENER_GRADIENTE_PASIVO":

        respuesta = {
            "modo": "OBSERVACION",
            "mensaje": "Persistencia silenciosa. Sin respuesta emitida."
        }

    else:

        respuesta = {
            "modo": "DESCONOCIDO",
            "mensaje": "Comando no reconocido."
        }

    print(f"[ACTUADOR] Ley aplicada: {ley}")
    print(f"[PORTAVOZ] {respuesta['mensaje']}")

    resultado = {
        "identificador": "ACTUATOR-RESPONSE",
        "ley": ley,
        "modo": respuesta["modo"],
        "mensaje": respuesta["mensaje"],
        "timestamp_actuador": time.time()
    }

    return json.dumps(resultado)


if __name__ == "__main__":

    decision_prueba = json.dumps({
        "identificador": "CORE-DECISION-READY",
        "ley_poder": "LEY_44_EFECTO_ESPEJO",
        "comando_actuador": "ACTIVAR_MECANICO_MAXIMA",
        "fundamento_estrategico": "Contramedida simétrica",
        "origen_vector": "whatsapp_link"
    })

    resultado = ejecutar_respuesta(decision_prueba)

    print(f"[ACTUATOR_PAYLOAD] -> {resultado}")
