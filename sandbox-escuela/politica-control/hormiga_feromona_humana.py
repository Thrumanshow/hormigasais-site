#!/usr/bin/env python3
import json, sys, time
def main():
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else '{}'
    try: payload = json.loads(raw.split('->', 1)[1].strip()) if '->' in raw else json.loads(raw)
    except: payload = {}
    res = {
        'autoridad': 'lbh.human.CLHQ_99_SAN_MIGUEL',
        'timestamp_emision': time.time(),
        'ponderacion_cualitativa': 'DEFENSA_SOBERANA_ABSOLUTA' if payload.get('amenaza_soberania') else 'COEXISTENCIA_NO_INVASIVA'
    }
    print(f'[FEROMONA_HUMANA] -> {json.dumps(res)}')
