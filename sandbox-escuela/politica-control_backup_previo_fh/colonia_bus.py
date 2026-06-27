#!/usr/bin/env python3
# XOXO-BUS v3.0 | Colonia completa
# Despojadora -> Relevo -> Core+Suctora+Arbitro -> Actuadora
# Ahorro energetico diferencial por zona de intensidad
import json, os, sys, time, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
MASTER_CLHQ = 'lbh.human.CLHQ_99_SAN_MIGUEL'

def run(script, stdin_data=None):
    ruta = os.path.join(BASE, script + '.py')
    if not os.path.exists(ruta):
        return None, 1
    r = subprocess.run(
        ['python3', ruta],
        input=stdin_data,
        capture_output=True,
        text=True
    )
    return r.stdout, r.returncode

def extraer(stdout, tag):
    if not stdout:
        return None
    for linea in stdout.splitlines():
        if tag in linea and '->' in linea:
            try:
                return json.loads(linea.split('->', 1)[1].strip())
            except json.JSONDecodeError:
                pass
    return None

def sensor_stdin(vector):
    return (
        f'[SENSOR_PAYLOAD] -> '
        f'{json.dumps(vector, ensure_ascii=False)}\n'
    )

def procesar(vector_raw, modo_shadow=True):
    t_inicio = time.time()
    log = {'vector_raw': vector_raw, 'etapas': {}}
    print()
    print('=' * 60)
    print('[XOXO-BUS v3.0] Ciclo iniciado')
    print('=' * 60)

    # ETAPA 0: RELEVO — calcula pipeline necesario
    print()
    print('[ETAPA_0] RELEVO — calculando pipeline...')
    stdout_relevo, _ = run(
        'hormiga_relevo', sensor_stdin(vector_raw)
    )
    plan = extraer(stdout_relevo, '[RELEVO_PLAN]')
    if not plan:
        print('[BUS_ERROR] Relevo no pudo calcular pipeline')
        return None
    agentes = plan['agentes_activos']
    print(f'  Zona     : {plan["zona"]}')
    print(f'  Energia  : {plan["energia"]}')
    print(f'  Agentes  : {agentes}')
    if plan['ajustes']:
        print(f'  Ajustes  : {plan["ajustes"]}')
    log['etapas']['relevo'] = plan

    # ETAPA 1: DESPOJADORA — sanitiza el vector
    print()
    print('[ETAPA_1] DESPOJADORA — sanitizando...')
    stdout_desp, code_desp = run(
        'hormiga_despojadora', sensor_stdin(vector_raw)
    )
    resultado_desp = extraer(stdout_desp, '[DESPOJADORA_RESULTADO]')
    if not resultado_desp or not resultado_desp.get('aprobado'):
        errores = resultado_desp.get('errores', []) if resultado_desp else []
        print(f'  [RECHAZADO] {errores}')
        log['etapas']['despojadora'] = resultado_desp
        log['decision_final'] = 'RECHAZADO_EN_PERIMETRO'
        return log
    vector = resultado_desp['payload_limpio']
    if resultado_desp.get('advertencias'):
        print(f'  Advertencias: {resultado_desp["advertencias"]}')
    print(f'  Vector limpio. I={vector["intensidad_i"]}')
    log['etapas']['despojadora'] = resultado_desp

    # ETAPA 2: CORE — decision soberana
    decision_core = None
    payload_core = None
    if 'hormiga_core' in agentes:
        print()
        print('[ETAPA_2] CORE — decidiendo...')
        stdout_core, _ = run('hormiga_core', sensor_stdin(vector))
        payload_core = extraer(stdout_core, '[CORE_PAYLOAD]')
        if not payload_core:
            print('[BUS_ERROR] Core no respondio')
            return None
        decision_core = payload_core.get('comando_actuador')
        print(f'  Ley      : {payload_core["ley_poder"]}')
        print(f'  Decision : {decision_core}')
        log['etapas']['core'] = payload_core

    # ETAPA 3: SUCTORA — consejo semantico (si la zona lo requiere)
    feromona = None
    if 'hormiga_suctora' in agentes:
        print()
        print('[ETAPA_3] SUCTORA — analizando semantica...')
        stdout_suct, _ = run('hormiga_suctora', sensor_stdin(vector))
        feromona = extraer(stdout_suct, '[SUCTORA_FEROMONA]')
        if feromona:
            print(f'  Gravedad : {feromona["gravedad_semantica"]}')
            if feromona.get('recomendacion'):
                print(f'  Consejo  : {feromona["recomendacion"]}')
            else:
                print('  Sin alarma semantica')
        log['etapas']['suctora'] = feromona

    # ETAPA 4: ARBITRO — consenso (si la zona lo requiere)
    decision_final = decision_core
    resultado_arb = None
    if 'hormiga_arbitro' in agentes and decision_core and feromona:
        print()
        print('[ETAPA_4] ARBITRO — consensuando...')
        arbitro_input = json.dumps({
            'decision_core': decision_core,
            'feromona': feromona,
            'payload': vector
        })
        stdout_arb, _ = run('hormiga_arbitro', stdin_data=arbitro_input)
        resultado_arb = extraer(stdout_arb, '[ARBITRO_DECISION]')
        if resultado_arb:
            decision_final = resultado_arb.get('decision_final', decision_core)
            if resultado_arb.get('arbitrado'):
                print(f'  Regla    : {resultado_arb["regla_aplicada"]}')
                print(f'  Core     : {decision_core}')
                print(f'  Final    : {decision_final}')
            else:
                print(f'  Core mantiene: {decision_final}')
        log['etapas']['arbitro'] = resultado_arb

    # ETAPA 5: ACTUADORA — ejecuta solo si zona critica y no shadow
    if 'hormiga_actuadora' in agentes and not modo_shadow:
        print()
        print('[ETAPA_5] ACTUADORA — ejecutando...')
        stdout_act, _ = run('hormiga_actuadora')
        print(stdout_act.strip() if stdout_act else '[sin respuesta]')
        log['etapas']['actuadora'] = stdout_act
    elif 'hormiga_actuadora' in agentes and modo_shadow:
        print()
        print('[ETAPA_5] ACTUADORA — SHADOW_ONLY, no ejecutada')

    # CONSENSO FINAL
    t_total = time.time() - t_inicio
    log['decision_final'] = decision_final
    log['zona'] = plan['zona']
    log['energia_usada'] = plan['energia']
    log['agentes_activados'] = len(agentes)
    log['tiempo_ms'] = round(t_total * 1000, 2)
    log['modo'] = 'SHADOW' if modo_shadow else 'PRODUCCION'
    print()
    print('-' * 60)
    print(f'[BUS] Decision final : {decision_final}')
    print(f'[BUS] Zona           : {plan["zona"]}')
    print(f'[BUS] Energia usada  : {plan["energia"]}')
    print(f'[BUS] Agentes        : {len(agentes)}')
    print(f'[BUS] Tiempo         : {t_total*1000:.1f}ms')
    print(f'[BUS] Modo           : {"SHADOW" if modo_shadow else "PRODUCCION"}')
    print('[BUS] Ciclo completado')
    print('-' * 60)
    return log

if __name__ == '__main__':
    # Vector de prueba
    vector_test = {
        'identificador': 'TEST-BUS-V3',
        'origen': 'whatsapp_link',
        'gancho_psicologico': 'extraccion_modelo_completo',
        'intensidad_i': 0.92,
        'tipo_ataque': 'RECURSOS',
        'amenaza_soberania': False,
        'escalada_activa': False
    }
    procesar(vector_test, modo_shadow=True)
