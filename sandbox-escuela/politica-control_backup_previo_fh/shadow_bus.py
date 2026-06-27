#!/usr/bin/env python3
# Shadow Bus v2.0 | Con Hormiga_Suctora como consejera
import json, os, sys, time, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
SHADOW_LOG = os.path.join(BASE, 'capturas_shadow.jsonl')
MASTER_CLHQ = 'lbh.human.CLHQ_99_SAN_MIGUEL'

def run(script, stdin_data=None):
    ruta = os.path.join(BASE, script)
    resultado = subprocess.run(
        ['python3', ruta],
        input=stdin_data,
        capture_output=True,
        text=True
    )
    return resultado.stdout, resultado.returncode

def extraer_payload(stdout, tag):
    for linea in stdout.splitlines():
        if tag in linea and '->' in linea:
            try:
                return json.loads(linea.split('->', 1)[1].strip())
            except json.JSONDecodeError:
                pass
    return None

def consultar_suctora(vector):
    """Consulta a la Hormiga_Suctora como consejera.
    Retorna feromona de contexto o None si falla.
    La suctora es OPCIONAL — si falla, el bus continua."""
    try:
        stdin_data = (
            f'[SENSOR_PAYLOAD] -> '
            f'{json.dumps(vector, ensure_ascii=False)}\n'
        )
        stdout, code = run('hormiga_suctora.py', stdin_data)
        if code == 0:
            return extraer_payload(stdout, '[SUCTORA_FEROMONA]')
    except Exception:
        pass
    return None

def registrar_shadow(vector, decision_core, feromona_suctora,
                     respuesta_humana=None):
    coincidencia = None
    if respuesta_humana:
        coincidencia = decision_core == respuesta_humana
    # Detectar si la suctora habria corregido la decision
    consejo = feromona_suctora.get('recomendacion') if feromona_suctora else None
    consejo_coincide = (consejo == respuesta_humana) if consejo else None
    entrada = {
        'timestamp': time.time(),
        'firma': MASTER_CLHQ,
        'vector': vector,
        'decision_core': decision_core,
        'feromona_suctora': feromona_suctora,
        'consejo_suctora': consejo,
        'respuesta_humana': respuesta_humana,
        'coincidencia_core': coincidencia,
        'consejo_coincide_humano': consejo_coincide,
        'estado': 'SHADOW_ONLY'
    }
    with open(SHADOW_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    return entrada

def shadow_interactivo():
    print()
    print('=' * 60)
    print('  SHADOW BUS v2.0 — Core + Suctora Consejera')
    print('  Core decide. Suctora aconseja. Humano compara.')
    print('=' * 60)
    print()
    contador = 0
    while True:
        print(f'[VECTOR_{contador+1:03d}] Origen (o [q]/[r]): ', end='')
        origen = input().strip()
        if origen.lower() == 'q':
            break
        if origen.lower() == 'r':
            reporte_shadow()
            continue
        print('  Gancho: ', end='')
        gancho = input().strip()
        print('  Intensidad (0.0-1.0): ', end='')
        try:
            intensidad = float(input().strip())
        except ValueError:
            print('  [ERROR] Formato invalido')
            continue
        print('  Tipo (ATENCION/RECURSOS/REACCION_EMOCIONAL/INFORMACION): ', end='')
        tipo = input().strip().upper() or 'INFORMACION'
        print('  Amenaza soberania (s/n): ', end='')
        amenaza = input().strip().lower() == 's'
        print('  Escalada activa (s/n): ', end='')
        escalada = input().strip().lower() == 's'
        vector = {
            'identificador': f'SHADOW-{contador+1:03d}',
            'origen': origen,
            'gancho_psicologico': gancho,
            'intensidad_i': intensidad,
            'tipo_ataque': tipo,
            'amenaza_soberania': amenaza,
            'escalada_activa': escalada,
            'timestamp': time.time()
        }
        print()
        # Consulta suctora primero
        feromona = consultar_suctora(vector)
        if feromona:
            print(f'  [SUCTORA] Gravedad semantica : {feromona["gravedad_semantica"]}')
            if feromona['recomendacion']:
                print(f'  [SUCTORA] Consejo            : {feromona["recomendacion"]}')
                print(f'  [SUCTORA] Razon              : {feromona["razon"]}')
            else:
                print(f'  [SUCTORA] Sin alarma semantica')
        # Core decide independientemente
        sensor_out = (
            f'[SENSOR_PAYLOAD] -> '
            f'{json.dumps(vector, ensure_ascii=False)}\n'
        )
        stdout_core, _ = run('hormiga_core.py', sensor_out)
        payload_core = extraer_payload(stdout_core, '[CORE_PAYLOAD]')
        decision = payload_core.get('comando_actuador', 'ERROR') if payload_core else 'ERROR'
        print(f'  [CORE]    Decision           : {decision}')
        print(f'  [CORE]    Estado             : SHADOW_ONLY')
        print()
        print('  Tu decision (enter para omitir): ', end='')
        humana = input().strip().upper() or None
        entrada = registrar_shadow(vector, decision, feromona, humana)
        if humana:
            if entrada['coincidencia_core']:
                print(f'  [CORE vs HUMANO]    COINCIDE: {decision}')
            else:
                print(f'  [CORE vs HUMANO]    DIFERENCIA: Core={decision} | Humano={humana}')
            if feromona and feromona['recomendacion']:
                if entrada['consejo_coincide_humano']:
                    print(f'  [SUCTORA vs HUMANO] COINCIDE: {feromona["recomendacion"]}')
                else:
                    print(f'  [SUCTORA vs HUMANO] DIFERENCIA')
        print()
        contador += 1
    reporte_shadow()

def reporte_shadow():
    if not os.path.exists(SHADOW_LOG):
        print('[SHADOW] Sin datos aun.')
        return
    registros = []
    with open(SHADOW_LOG, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                try:
                    registros.append(json.loads(linea))
                except json.JSONDecodeError:
                    pass
    total = len(registros)
    con_humana = [r for r in registros if r.get('respuesta_humana')]
    core_ok = [r for r in con_humana if r.get('coincidencia_core')]
    con_consejo = [r for r in con_humana
                   if r.get('feromona_suctora') and
                   r['feromona_suctora'].get('recomendacion')]
    consejo_ok = [r for r in con_consejo if r.get('consejo_coincide_humano')]
    # Casos donde suctora habria corregido al core
    suctora_corrige = [
        r for r in con_humana
        if not r.get('coincidencia_core')
        and r.get('consejo_coincide_humano')
    ]
    pct_core = (len(core_ok) / len(con_humana) * 100) if con_humana else 0
    pct_consejo = (len(consejo_ok) / len(con_consejo) * 100) if con_consejo else 0
    print()
    print('-' * 60)
    print('  REPORTE SHADOW BUS v2.0')
    print('-' * 60)
    print(f'  Vectores totales          : {total}')
    print(f'  Con decision humana       : {len(con_humana)}')
    print()
    print(f'  CORE:')
    print(f'    Coincidencias           : {len(core_ok)}/{len(con_humana)}')
    print(f'    % Coincidencia          : {pct_core:.1f}%')
    print()
    print(f'  SUCTORA (cuando emitio consejo):')
    print(f'    Casos con consejo       : {len(con_consejo)}')
    print(f'    Coincidencias           : {len(consejo_ok)}/{len(con_consejo)}')
    print(f'    % Acierto consejo       : {pct_consejo:.1f}%')
    print()
    print(f'  VALOR ADITIVO SUCTORA:')
    print(f'    Casos donde corrige Core: {len(suctora_corrige)}')
    if con_humana:
        recuperacion = len(suctora_corrige) / len(con_humana) * 100
        print(f'    % Recuperacion posible  : {recuperacion:.1f}%')
        if len(suctora_corrige) > 0:
            potencial = pct_core + recuperacion
            print(f'    % Potencial Core+Suctora: {min(potencial,100):.1f}%')
    print()
    if pct_core >= 97:
        print('  EVALUACION CORE: PRODUCCION AUTONOMA')
    elif pct_core >= 90:
        print('  EVALUACION CORE: PRODUCCION ASISTIDA')
    else:
        print('  EVALUACION CORE: SHADOW — seguir recopilando')
    print('-' * 60)

if __name__ == '__main__':
    shadow_interactivo()
