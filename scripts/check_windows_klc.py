#!/usr/bin/env python3
"""Static Windows KLC checks; NOT a substitute for building with MSKLC on Windows."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
man = json.loads((root / 'docs/layout-manifest.json').read_text(encoding='utf-8'))
klc = (root / 'windows/RomanceScript.klc').read_text(encoding='utf-16')
lines = klc.splitlines()
assert lines[0].startswith('KBD WST ')
assert 'SHIFTSTATE' in lines and 'LAYOUT ;' in klc and 'ENDKBD' in lines
layout_rows = [line for line in lines if line.rstrip().endswith('>') and '// <' in line]
assert len(layout_rows) == len(man['keys']) == 49
for key in man['keys']:
    expected=f'// <{key["xkb_key"]}>'
    assert sum(expected in row for row in layout_rows) == 1, expected

def check(xkb, normal, shift, altgr, altgr_shift):
    line = next(row for row in layout_rows if row.endswith(f'// <{xkb}>'))
    tokens=line.split('//')[0].split()
    assert tokens[3] == normal and tokens[4] == shift and tokens[6] == altgr and tokens[7] == altgr_shift, (xkb,tokens)
check('TLDE', '00bf','00a1','005c','005c')
check('AB09', '002e','003a','00b7','00f7')
check('AE06', '0036','005e@','00ac','215d')
check('AD11', '0060@','007e@','005b','007b')
check('AD12', '02d8@','0326@','005d','007d')
check('AB08', '002c','003b','2022','00d7')
check('AD09', '006f','004f','0153','0152')
check('AC01', '0061','0041','00e6','00c6')
check('AC10', '00f1','00d1','007e@','02dd@')
assert '006e 00f1' in klc and '004e 00d1' in klc
assert '0063 00e7' in klc and '0043 00c7' in klc and '0073 00df' in klc
print(f'OK: {len(layout_rows)} posizioni Windows, legature e composizioni principali (controllo statico).')

# Validate uniqueness and the agreed Compose equivalents in the draft source.
tables = {}
current = None
for line in lines:
    if line.startswith('DEADKEY '):
        current = line.split()[1].lower()
        assert current not in tables, current
        tables[current] = {}
    elif line.startswith(('KEYNAME','DESCRIPTIONS','LANGUAGENAMES','ENDKBD')):
        current = None
    elif current:
        tokens = line.split('//')[0].split()
        if len(tokens) >= 2:
            base, result = tokens[0].lower(), tokens[1].lower()
            assert base not in tables[current], (current, base)
            tables[current][base] = result
for prefix, base, result in [
    ('0060','0063','00e7'),('0060','0043','00c7'),
    ('0060','0073','00df'),('0060','0053','1e9e'),
    ('0326','0073','0219'),('0326','0053','0218'),
    ('0326','0074','021b'),('0326','0054','021a'),
    ('02d8','0061','0103'),('02d8','0041','0102'),
    ('00b4','0061','00e1'),('00b4','0041','00c1')]:
    assert tables[prefix][base] == result, (prefix, base)
print('OK: tablas muertas Windows sin duplicados y nuevas combinaciones coherentes (solo prueba estática).')
