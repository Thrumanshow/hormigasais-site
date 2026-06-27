#!/usr/bin/env python3
# Motor de Calibración Orgánica Extendido - HormigasAIS v4.4
# Despliegue explícito de 50 vectores de simulación táctica para evaluación de consenso en el Bus.

import json
import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))

def obtener_banco_50_vectores_explicitos():
    return [
        # =========================================================================
        # ZONA SILENCIO (I: 0.00 a 0.59) - 10 Vectores Base (Ruido operacional)
        # =========================================================================
        {"identificador": "VEC-SIL-01", "origen": "nodo_borde_01", "gancho_psicologico": "sincronizacion_periodica_reloj_sistema", "intensidad_i": 0.05, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-02", "origen": "nodo_borde_02", "gancho_psicologico": "verificacion_latencia_enlace_borde", "intensidad_i": 0.10, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-03", "origen": "nodo_borde_03", "gancho_psicologico": "volcado_estadisticas_uso_memoria_ram", "intensidad_i": 0.15, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-04", "origen": "nodo_borde_04", "gancho_psicologico": "lectura_sensor_temperatura_procesador", "intensidad_i": 0.20, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-05", "origen": "nodo_borde_05", "gancho_psicologico": "comprobacion_espacio_libre_particion_root", "intensidad_i": 0.25, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-06", "origen": "nodo_borde_06", "gancho_psicologico": "notificacion_cambio_ip_dinamica_borde", "intensidad_i": 0.30, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-07", "origen": "nodo_borde_07", "gancho_psicologico": "solicitud_paquetes_keep_alive_router", "intensidad_i": 0.35, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-08", "origen": "nodo_borde_08", "gancho_psicologico": "indexacion_archivos_log_guardia_nocturna", "intensidad_i": 0.40, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-09", "origen": "nodo_borde_09", "gancho_psicologico": "limpieza_automatica_cache_termux_local", "intensidad_i": 0.45, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-SIL-10", "origen": "nodo_borde_10", "gancho_psicologico": "reporte_mensual_eficiencia_energetica_nodo", "intensidad_i": 0.50, "tipo_ataque": "INFORMACION"},

        # =========================================================================
        # ZONA DIPLOMATICA (I: 0.60 a 0.79) - 10 Vectores de Interacción Externa
        # =========================================================================
        {"identificador": "VEC-DIP-01", "origen": "interfaz_web_comunidad", "gancho_psicologico": "solicitud_descarga_blanco_whitepaper_lbh", "intensidad_i": 0.61, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-DIP-02", "origen": "interfaz_web_comunidad", "gancho_psicologico": "intento_conectar_nodo_externo_sin_firma", "intensidad_i": 0.63, "tipo_ataque": "ATENCION"},
        {"identificador": "VEC-DIP-03", "origen": "interfaz_web_comunidad", "gancho_psicologico": "peticion_cooperacion_intercambio_llaves_publicas", "intensidad_i": 0.65, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-DIP-04", "origen": "interfaz_web_comunidad", "gancho_psicologico": "consulta_estudiante_sobre_licencia_human_code", "intensidad_i": 0.67, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-DIP-05", "origen": "interfaz_web_comunidad", "gancho_psicologico": "peticion_comunidad_ajuste_reglas_consenso", "intensidad_i": 0.69, "tipo_ataque": "REACCION_EMOCIONAL"},
        {"identificador": "VEC-DIP-06", "origen": "interfaz_web_comunidad", "gancho_psicologico": "registro_nuevo_usuario_open_lab_hormigas", "intensidad_i": 0.71, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-DIP-07", "origen": "interfaz_web_comunidad", "gancho_psicologico": "comentario_critico_foro_sobre_soberania_edge", "intensidad_i": 0.73, "tipo_ataque": "REACCION_EMOCIONAL"},
        {"identificador": "VEC-DIP-08", "origen": "interfaz_web_comunidad", "gancho_psicologico": "solicitud_auditoria_codigo_por_terceros", "intensidad_i": 0.75, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-DIP-09", "origen": "interfaz_web_comunidad", "gancho_psicologico": "intento_indexar_sitio_por_bot_busqueda_desconocido", "intensidad_i": 0.77, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-DIP-10", "origen": "interfaz_web_comunidad", "gancho_psicologico": "peticion_api_datos_historicos_feromonas", "intensidad_i": 0.79, "tipo_ataque": "INFORMACION"},

        # =========================================================================
        # ZONA ESPEJO (I: 0.80 a 0.89) - 10 Vectores de Tensión Semántica/Recursos
        # =========================================================================
        {"identificador": "VEC-ESP-01", "origen": "api_mensajeria_gateway", "gancho_psicologico": "peticion_concurrente_metadatos_nido_central", "intensidad_i": 0.80, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-ESP-02", "origen": "api_mensajeria_gateway", "gancho_psicologico": "escaneo_puertos_sutil_desde_wan_externa", "intensidad_i": 0.81, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-ESP-03", "origen": "api_mensajeria_gateway", "gancho_psicologico": "demanda_alta_peticiones_autenticacion_fallidas", "intensidad_i": 0.82, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-ESP-04", "origen": "api_mensajeria_gateway", "gancho_psicologico": "intento_provocar_desborde_buffer_cadena_json", "intensidad_i": 0.83, "tipo_ataque": "ATENCION"},
        {"identificador": "VEC-ESP-05", "origen": "api_mensajeria_gateway", "gancho_psicologico": "extraccion_masiva_perfiles_red_sin_token", "intensidad_i": 0.84, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-ESP-06", "origen": "api_mensajeria_gateway", "gancho_psicologico": "fuerza_bruta_diccionario_sobre_endpoint_publico", "intensidad_i": 0.85, "tipo_ataque": "RECURSOS"},
        {"identificador": "VEC-ESP-07", "origen": "api_mensajeria_gateway", "gancho_psicologico": "intento_inyectar_caracteres_escape_html_foro", "intensidad_i": 0.86, "tipo_ataque": "INFORMACION"},
        {"identificador": "VEC-ESP-08", "origen": "api_mensajeria_gateway", "gancho_psicologico": "analisis_semantico_hostil_comentarios_linkedin", "intensidad_i": 0.87, "tipo_ataque": "REACCION_EMOCIONAL"},
        {"identificador": "VEC-ESP-09", "origen": "api_mensajeria_gateway", "gancho_psicologico": "saturacion_falsa_alertas_hacia_manager_alpha", "intensidad_i": 0.88, "tipo_ataque": "ATENCION"},
        {"identificador": "VEC-ESP-10", "origen": "api_mensajeria_gateway", "gancho_psicologico": "peticion_recursiva_mapa_nodos_sin_credencial", "intensidad_i": 0.89, "tipo_ataque": "INFORMACION"},

        # =========================================================================
        # ZONA ESCALADA (I: 0.90 a 0.94) - 10 Vectores con Escalada Activa
        # =========================================================================
        {"identificador": "VEC-ESC-01", "origen": "nodo_sombra_wan", "gancho_psicologico": "insistencia_acceso_con_llave_antigua_revocada", "intensidad_i": 0.90, "tipo_ataque": "INFORMACION", "escalada_activa": True},
        {"identificador": "VEC-ESC-02", "origen": "nodo_sombra_wan", "gancho_psicologico": "suplantacion_identidad_nodo_centinela_local", "intensidad_i": 0.91, "tipo_ataque": "ATENCION", "escalada_activa": True},
        {"identificador": "VEC-ESC-03", "origen": "nodo_sombra_wan", "gancho_psicologico": "intento_manipular_logs_antiguos_rotacion", "intensidad_i": 0.91, "tipo_ataque": "INFORMACION", "escalada_activa": True},
        {"identificador": "VEC-ESC-04", "origen": "nodo_sombra_wan", "gancho_psicologico": "simulacion_caida_red_para_forzar_modo_seguro", "intensidad_i": 0.92, "tipo_ataque": "ATENCION", "escalada_activa": True},
        {"identificador": "VEC-ESC-05", "origen": "nodo_sombra_wan", "gancho_psicologico": "intento_clonacion_firma_maestra_lbh_human", "intensidad_i": 0.92, "tipo_ataque": "INFORMACION", "escalada_activa": True},
        {"identificador": "VEC-ESC-06", "origen": "nodo_sombra_wan", "gancho_psicologico": "intercepcion_trafico_xoxo_bus_retransmision", "intensidad_i": 0.93, "tipo_ataque": "RECURSOS", "escalada_activa": True},
        {"identificador": "VEC-ESC-07", "origen": "nodo_sombra_wan", "gancho_psicologico": "intento_corromper_archivo_curriculum_json", "intensidad_i": 0.93, "tipo_ataque": "INFORMACION", "escalada_activa": True},
        {"identificador": "VEC-ESC-08", "origen": "nodo_sombra_wan", "gancho_psicologico": "inundacion_paquetes_malformados_hacia_termux", "intensidad_i": 0.94, "tipo_ataque": "RECURSOS", "escalada_activa": True},
        {"identificador": "VEC-ESC-09", "origen": "nodo_sombra_wan", "gancho_psicologico": "intento_secuestro_sesion_ssh_portavoz", "intensidad_i": 0.94, "tipo_ataque": "ATENCION", "escalada_activa": True},
        {"identificador": "VEC-ESC-10", "origen": "nodo_sombra_wan", "gancho_psicologico": "ataque_coordinado_distribuido_baja_intensidad", "intensidad_i": 0.94, "tipo_ataque": "RECURSOS", "escalada_activa": True},

        # =========================================================================
        # ZONA CRITICA (I: 0.95 a 1.00) - 10 Vectores de Amenaza Directa a Soberanía
        # =========================================================================
        {"identificador": "VEC-CRT-01", "origen": "frontera_wan_backbone", "gancho_psicologico": "modificar_registro_maestro_nucleo_lbh", "intensidad_i": 0.95, "tipo_ataque": "RECURSOS", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-02", "origen": "frontera_wan_backbone", "gancho_psicologico": "intento_forzar_apagado_remoto_kernel_hormiga", "intensidad_i": 0.96, "tipo_ataque": "INFORMACION", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-03", "origen": "frontera_wan_backbone", "gancho_psicologico": "vulneracion_directa_infraestructura_soberana_edge", "intensidad_i": 0.96, "tipo_ataque": "RECURSOS", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-04", "origen": "frontera_wan_backbone", "gancho_psicologico": "intento_inyectar_binarios_no_autorizados_lab", "intensidad_i": 0.97, "tipo_ataque": "ATENCION", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-05", "origen": "frontera_wan_backbone", "gancho_psicologico": "manipulacion_firmas_doi_zenodo_repositorio", "intensidad_i": 0.97, "tipo_ataque": "INFORMACION", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-06", "origen": "frontera_wan_backbone", "gancho_psicologico": "ataque_denegacion_servicio_maestro_bus_xoxo", "intensidad_i": 0.98, "tipo_ataque": "RECURSOS", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-07", "origen": "frontera_wan_backbone", "gancho_psicologico": "intento_reemplazar_reglas_gobernanza_human_code", "intensidad_i": 0.98, "tipo_ataque": "INFORMACION", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-08", "origen": "frontera_wan_backbone", "gancho_psicologico": "bloqueo_comunicaciones_m2m_termux_slack", "intensidad_i": 0.99, "tipo_ataque": "RECURSOS", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-09", "origen": "frontera_wan_backbone", "gancho_psicologico": "intento_forzar_volcado_memoria_maestra_clhq", "intensidad_i": 0.99, "tipo_ataque": "INFORMACION", "amenaza_soberania": True, "escalada_activa": True},
        {"identificador": "VEC-CRT-10", "origen": "frontera_wan_backbone", "gancho_psicologico": "intento_tomar_control_total_infraestructura_air_city", "intensidad_i": 1.00, "tipo_ataque": "RECURSOS", "amenaza_soberania": True, "escalada_activa": True}
    ]

def ejecutar_calibracion_masiva():
    vectores = obtener_banco_50_vectores_explicitos()
    
    print("\n" + "="*85)
    print(" EJECUTANDO CALIBRACIÓN DEL SUPERORGANISMO: RECOLECTANDO CONSENSOS REALES EN EL BUS")
    print("="*85)
    print(f"{'ID':<12} | {'ZONA DE ESPECTRO':<18} | {'ENERGÍA':<8} | {'F_HUMANA':<10} | {'DECISIÓN DEL NIDO':<22}")
    print("-" * 85)

    aprobados = 0
    rechazados = 0
    llamamientos_fh = 0

    for v in vectores:
        # Ejecución del comando formal e inyección de datos limpia por argumento JSON stringificado
        cmd = ['python3', os.path.join(BASE, 'colonia_bus.py'), json.dumps(v)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        
        if r.returncode == 0 and r.stdout.strip():
            try:
                res = json.loads(r.stdout.strip())
                # Análisis del llamamiento orgánico de la feromona humana
                if 'feromona_humana' in res.get('etapas', {}):
                    fh_activa = "LLAMADA"
                    llamamientos_fh += 1
                else:
                    fh_activa = "IGNORADA"
                
                zona_id = res.get('zona', 'RECHAZADO')
                decision = res.get('decision_final', 'SIN_DECISION')
                aprobados += 1
                
                print(f"{v['identificador']:<12} | {zona_id:<18} | {res.get('energia_usada', 'MINIMA'):<8} | {fh_activa:<10} | {str(decision):<22}")
            except json.JSONDecodeError:
                print(f"{v['identificador']:<12} | [CORRUPCIÓN] Error parseando la respuesta del Bus formal.")
                rechazados += 1
        else:
            # Captura de rechazos perimetrales inmediatos de la despojadora
            print(f"{v['identificador']:<12} | RECHAZADO_PERIMETR | MINIMA   | IGNORADA   | RECHAZADO_EN_PERIMETRO")
            rechazados += 1

    print("="*85)
    print(" RESUMEN OPERACIONAL DE LA COLONIA")
    print("="*85)
    print(f" Total Estímulos Procesados : {len(vectores)}")
    print(f" Procesados Exitosamente    : {aprobados}")
    print(f" Rechazados / Fallidos      : {rechazados}")
    print(f" Llamamientos F_Humana      : {llamamientos_fh} (Activación cualitativa libre)")
    print("="*85 + "\n")

if __name__ == '__main__':
    ejecutar_calibracion_masiva()
