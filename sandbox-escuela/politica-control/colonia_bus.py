#!/usr/bin/env python3
# XOXO-BUS v3.0.1 | Base estable + Memoria Quimica
# El vector NUNCA se modifica
# El sabor vive en el Bus, no en el payload
import json, os, sys, time, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
MEMORIA_FILE = os.path.join(BASE, 'memoria_quimica.json')
MASTER_CLHQ = 'lbh.human.CLHQ_99_SAN_MIGUEL'

def run(script, stdin_data=None):
    ruta = os.path.join(BASE, script + '.py')
    if not os.path.exists(ruta):
        return None, 1
    r = subprocess.run(
        ['python3', ruta],
        input=stdin_data, capture_output=True, text=True
    )
    return r.stdout, r.returncode

def extraer(stdout, tag):
    if not stdout:
        return None
    for linea in stdout.splitlines():
        if tag in linea and '->' in linea:
            try:
                return json.loads(
                    linea.split('->', 1)[1].strip()
                )
            except json.JSONDecodeError:
                pass
    return None

def sensor_stdin(vector):
    return (
        f'[SENSOR_PAYLOAD] -> '
        f'{json.dumps(vector, ensure_ascii=False)}\n'
    )

def cargar_memoria():
    if not os.path.exists(MEMORIA_FILE):
        return None
    try:
        with open(MEMORIA_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def actualizar_memoria(vector, decision_final):
    """Actualiza el sabor del Bus despues de cada ciclo"""
    memoria = cargar_memoria()
    if not memoria:
        return
    tipo = vector.get('tipo_ataque', 'INFORMACION')
    i = vector.get('intensidad_i', 0)
    if tipo not in memoria['sabor_acumulado']:
        tipo = 'INFORMACION'
    sabor = memoria['sabor_acumulado'][tipo]
    n = sabor['vectores_procesados']
    sabor['toxicidad_promedio'] = (
        (sabor['toxicidad_promedio'] * n + i) / (n + 1)
    )
    sabor['vectores_procesados'] = n + 1
    sabor['ultima_decision'] = decision_final
    if decision_final in ('FILTRAR', 'BLOQUEO_TOTAL'):
        sabor['patron_dominante'] = 'CONSUMO_BLOQUEADO'
    elif decision_final == 'ACTIVAR_MECANICO_MAXIMA':
        if sabor.get('patron_dominante') != 'CONSUMO_BLOQUEADO':
            sabor['patron_dominante'] = 'ESPEJO_ACTIVO'
    toxicidades = [
        s['toxicidad_promedio']
        for s in memoria['sabor_acumulado'].values()
        if s['vectores_procesados'] > 0
    ]
    memoria['tension_colonia'] = (
        sum(toxicidades) / len(toxicidades)
        if toxicidades else 0
    )
    memoria['ciclos_completados'] += 1
    with open(MEMORIA_FILE, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

def procesar(vector_raw, modo_shadow=True):
    t_inicio = time.time()
    print()
    print('=' * 62)
    print('[XOXO-BUS v3.0.1] Ciclo con Memoria Quimica')
    print('=' * 62)
    # Mostrar sabor activo
    memoria = cargar_memoria()
    if memoria:
        print(
            f'[BUS] Sabor | '
            f'Tension={memoria["tension_colonia"]:.3f} | '
            f'Ciclos={memoria["ciclos_completados"]}'
        )
    # ETAPA 0: RELEVO
    print()
    print('[ETAPA_0] RELEVO — planificando pipeline...')
    stdout_r, _ = run(
        'hormiga_relevo', sensor_stdin(vector_raw)
    )
    plan = extraer(stdout_r, '[RELEVO_PLAN]')
    if not plan:
        print('[BUS_ERROR] Relevo no respondio')
        return None
    agentes = plan['agentes_activos']
    # El consejo_previo es del Bus — no toca el vector
    consejo_previo = plan.get('consejo_previo')
    print(f'  Zona          : {plan["zona"]}')
    print(f'  Energia       : {plan["energia"]}')
    print(f'  Agentes       : {agentes}')
    if plan.get('ajustes'):
        print(f'  Ajustes       : {plan["ajustes"]}')
    if plan.get('ajustes_feromona'):
        print(
            f'  Feromona      : {plan["ajustes_feromona"]}'
        )
    if consejo_previo:
        print(
            f'  Sabor del Bus : consejo_previo={consejo_previo}'
        )
    # ETAPA 1: DESPOJADORA
    # vector_raw llega limpio, sin campos del Bus
    print()
    print('[ETAPA_1] DESPOJADORA — sanitizando...')
    stdout_d, _ = run(
        'hormiga_despojadora', sensor_stdin(vector_raw)
    )
    res_d = extraer(stdout_d, '[DESPOJADORA_RESULTADO]')
    if not res_d or not res_d.get('aprobado'):
        errores = res_d.get('errores', []) if res_d else []
        print(f'  [RECHAZADO] {errores}')
        return {'decision_final': 'RECHAZADO_EN_PERIMETRO'}
    vector = res_d['payload_limpio']
    if res_d.get('advertencias'):
        print(f'  Advertencias  : {res_d["advertencias"]}')
    print(f'  Aprobado. I={vector["intensidad_i"]}')
    # ETAPA 2: CORE
    # El vector llega limpio desde la Despojadora
    # El Bus sabe el consejo_previo pero no lo inyecta
    print()
    print('[ETAPA_2] CORE — decidiendo...')
    stdout_c, _ = run('hormiga_core', sensor_stdin(vector))
    payload_core = extraer(stdout_c, '[CORE_PAYLOAD]')
    if not payload_core:
        print('[BUS_ERROR] Core no respondio')
        return None
    decision_core = payload_core.get('comando_actuador')
    print(f'  Ley           : {payload_core["ley_poder"]}')
    print(f'  Decision      : {decision_core}')
    # El Bus compara decision_core con consejo_previo
    if consejo_previo and decision_core != consejo_previo:
        print(
            f'  [TENSION_BUS] Core={decision_core} '
            f'Sabor={consejo_previo}'
        )
    elif consejo_previo and decision_core == consejo_previo:
        print(f'  [ARMONIA_BUS] Core honro el sabor')
    # ETAPA 3: SUCTORA
    feromona = None
    if 'hormiga_suctora' in agentes:
        print()
        print('[ETAPA_3] SUCTORA — analizando...')
        stdout_s, _ = run(
            'hormiga_suctora', sensor_stdin(vector)
        )
        feromona = extraer(stdout_s, '[SUCTORA_FEROMONA]')
        if feromona:
            print(
                f'  Gravedad      : '
                f'{feromona["gravedad_semantica"]}'
            )
            if feromona.get('recomendacion'):
                print(
                    f'  Consejo       : '
                    f'{feromona["recomendacion"]}'
                )
            else:
                print('  Sin alarma semantica')
    # ETAPA 4: ARBITRO
    decision_final = decision_core
    if 'hormiga_arbitro' in agentes and feromona:
        print()
        print('[ETAPA_4] ARBITRO — consensuando...')
        arb_in = json.dumps({
            'decision_core': decision_core,
            'feromona': feromona,
            'payload': vector
        })
        stdout_a, _ = run(
            'hormiga_arbitro', stdin_data=arb_in
        )
        res_a = extraer(stdout_a, '[ARBITRO_DECISION]')
        if res_a:
            decision_final = res_a.get(
                'decision_final', decision_core
            )
            if res_a.get('arbitrado'):
                print(
                    f'  Regla         : '
                    f'{res_a["regla_aplicada"]}'
                )
                print(f'  Final         : {decision_final}')
            else:
                print(
                    f'  Core mantiene : {decision_final}'
                )
    # ETAPA 5: ACTUADORA
    if 'hormiga_actuadora' in agentes and not modo_shadow:
        print()
        print('[ETAPA_5] ACTUADORA — ejecutando...')
        stdout_act, _ = run('hormiga_actuadora')
        print(
            stdout_act.strip()
            if stdout_act else '[sin respuesta]'
        )
    elif 'hormiga_actuadora' in agentes and modo_shadow:
        print()
        print('[ETAPA_5] ACTUADORA — SHADOW_ONLY')
    # ACTUALIZAR MEMORIA QUIMICA
    # El sabor del Bus crece con cada ciclo
    actualizar_memoria(vector, decision_final)
    t_total = time.time() - t_inicio
    nueva_mem = cargar_memoria()
    print()
    print('-' * 62)
    print(f'[BUS] Decision final  : {decision_final}')
    print(f'[BUS] Zona            : {plan["zona"]}')
    print(f'[BUS] Energia         : {plan["energia"]}')
    print(f'[BUS] Agentes activos : {len(agentes)}')
    print(f'[BUS] Tiempo          : {t_total*1000:.1f}ms')
    if nueva_mem:
        print(
            f'[BUS] Tension colonia : '
            f'{nueva_mem["tension_colonia"]:.3f}'
        )
        print(
            f'[BUS] Ciclos totales  : '
            f'{nueva_mem["ciclos_completados"]}'
        )
    print(
        f'[BUS] Modo            : '
        f'{"SHADOW" if modo_shadow else "PRODUCCION"}'
    )
    print('[BUS] Ciclo completado')
    print('-' * 62)
    return {
        'decision_final': decision_final,
        'zona': plan['zona'],
        'energia': plan['energia'],
        'tiempo_ms': round(t_total * 1000, 2)
    }

if __name__ == '__main__':
    vectores_test = [
        {
            'identificador': 'TEST-001',
            'origen': 'api_externa',
            'gancho_psicologico': 'extraccion_modelo_completo',
            'intensidad_i': 0.92,
            'tipo_ataque': 'RECURSOS',
            'amenaza_soberania': False,
            'escalada_activa': False
        },
        {
            'identificador': 'TEST-002',
            'origen': 'whatsapp_link',
            'gancho_psicologico': 'falsa_recompensa_sprint_final',
            'intensidad_i': 0.98,
            'tipo_ataque': 'ATENCION',
            'amenaza_soberania': False,
            'escalada_activa': False
        },
        {
            'identificador': 'TEST-003',
            'origen': 'linkedin',
            'gancho_psicologico': 'critica_publica_hormigasais',
            'intensidad_i': 0.65,
            'tipo_ataque': 'REACCION_EMOCIONAL',
            'amenaza_soberania': False,
            'escalada_activa': False
        }
    ]
    for v in vectores_test:
        procesar(v, modo_shadow=True)
        print()
