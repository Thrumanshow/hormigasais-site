#!/usr/bin/env python3
# Shadow Batch v3.0 — Core + Suctora + Arbitro
import json, os, sys, time, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
SHADOW_LOG = os.path.join(BASE, 'capturas_shadow.jsonl')
VECTORES_FILE = os.path.join(BASE, 'vectores_shadow.json')

def run_agente(script, vector=None, stdin_raw=None):
    ruta = os.path.join(BASE, script)
    if stdin_raw is None and vector is not None:
        stdin_raw = (
            f'[SENSOR_PAYLOAD] -> '
            f'{json.dumps(vector, ensure_ascii=False)}\n'
        )
    r = subprocess.run(
        ['python3', ruta],
        input=stdin_raw,
        capture_output=True,
        text=True
    )
    return r.stdout, r.returncode

def extraer(stdout, tag):
    for linea in stdout.splitlines():
        if tag in linea and '->' in linea:
            try:
                return json.loads(linea.split('->', 1)[1].strip())
            except json.JSONDecodeError:
                pass
    return None

if not os.path.exists(VECTORES_FILE):
    print(f'[ERROR] No existe {VECTORES_FILE}')
    sys.exit(1)

with open(VECTORES_FILE, encoding='utf-8') as f:
    vectores = json.load(f)

print(f'[SHADOW_BATCH v3.0] {len(vectores)} vectores')
print('[AGENTES] Core + Suctora + Arbitro')
print()

core_ok = 0
final_ok = 0
arbitrado_ok = 0
total_arbitrados = 0
con_humana = 0

for i, v in enumerate(vectores):
    humana = v.get('respuesta_humana')
    # 1. Core decide
    stdout_core, _ = run_agente('hormiga_core.py', v)
    payload_core = extraer(stdout_core, '[CORE_PAYLOAD]')
    if not payload_core:
        print(f'  [{i+1:03d}] ERROR — core no respondio')
        continue
    decision_core = payload_core.get('comando_actuador', 'ERROR')
    # 2. Suctora aconseja
    stdout_suct, _ = run_agente('hormiga_suctora.py', v)
    feromona = extraer(stdout_suct, '[SUCTORA_FEROMONA]')
    gravedad = feromona.get('gravedad_semantica', '-') if feromona else '-'
    consejo = feromona.get('recomendacion') if feromona else None
    # 3. Arbitro consensua
    arbitro_input = json.dumps({
        'decision_core': decision_core,
        'feromona': feromona,
        'payload': v
    })
    stdout_arb, _ = run_agente(
        'hormiga_arbitro.py', stdin_raw=arbitro_input
    )
    resultado_arb = extraer(stdout_arb, '[ARBITRO_DECISION]')
    decision_final = (
        resultado_arb.get('decision_final', decision_core)
        if resultado_arb else decision_core
    )
    arbitrado = (
        resultado_arb.get('arbitrado', False)
        if resultado_arb else False
    )
    regla = (
        resultado_arb.get('regla_aplicada', '-')
        if resultado_arb else '-'
    )
    # Metricas
    if humana:
        con_humana += 1
        if decision_core == humana:
            core_ok += 1
        if decision_final == humana:
            final_ok += 1
        if arbitrado:
            total_arbitrados += 1
            if decision_final == humana:
                arbitrado_ok += 1
    # Log
    entrada = {
        'timestamp': time.time(),
        'vector': v,
        'decision_core': decision_core,
        'feromona_suctora': feromona,
        'resultado_arbitro': resultado_arb,
        'decision_final': decision_final,
        'arbitrado': arbitrado,
        'regla_aplicada': regla,
        'respuesta_humana': humana,
        'coincidencia_core': decision_core == humana if humana else None,
        'coincidencia_final': decision_final == humana if humana else None,
        'estado': 'SHADOW_ONLY'
    }
    with open(SHADOW_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    # Output
    estado_core = '✓' if decision_core == humana else '✗'
    estado_final = '✓' if decision_final == humana else '✗'
    arb_tag = f'[{regla}]' if arbitrado else ''
    print(
        f'  [{i+1:03d}] I={v["intensidad_i"]} | '
        f'{v["gancho_psicologico"][:24]:24s} | '
        f'Core:{decision_core:25s}{estado_core} | '
        f'Final:{decision_final:25s}{estado_final} | '
        f'Sem:{gravedad:8s} {arb_tag}'
    )

pct_core = (core_ok / con_humana * 100) if con_humana else 0
pct_final = (final_ok / con_humana * 100) if con_humana else 0
ganancia = pct_final - pct_core
print()
print('=' * 80)
print('  REPORTE SHADOW BATCH v3.0')
print('=' * 80)
print(f'  Vectores procesados       : {len(vectores)}')
print(f'  Con referencia humana     : {con_humana}')
print()
print(f'  CORE solo                 : {core_ok}/{con_humana} ({pct_core:.1f}%)')
print(f'  FINAL (Core+Arbitro)      : {final_ok}/{con_humana} ({pct_final:.1f}%)')
print(f'  Ganancia del arbitro      : +{ganancia:.1f}%')
print(f'  Casos arbitrados          : {total_arbitrados}')
print(f'  Arbitrajes correctos      : {arbitrado_ok}/{total_arbitrados}')
print()
if pct_final >= 97:
    print('  EVALUACION: PRODUCCION AUTONOMA — umbral superado')
elif pct_final >= 90:
    print('  EVALUACION: PRODUCCION ASISTIDA — nivel alcanzado')
else:
    print('  EVALUACION: SHADOW — seguir recopilando')
print()
if total_arbitrados > 0:
    pct_arb = arbitrado_ok / total_arbitrados * 100
    print(f'  Precision del arbitro     : {pct_arb:.1f}%')
    if pct_arb >= 80:
        print('  ARBITRO: confiable — reglas bien calibradas')
    else:
        print('  ARBITRO: revisar reglas — precision insuficiente')
print('=' * 80)
