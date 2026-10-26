#!/usr/bin/env python3
"""Static Windows KLC checks; NOT a substitute for building with MSKLC on Windows."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
man = json.loads((root / 'docs/layout-manifest.json').read_text(encoding='utf-8'))
klc = (root / 'windows/Occidentale.klc').read_text(encoding='utf-16')
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
check('AD09', '006f','004f','0153','0152')
check('AC01', '0061','0041','00e6','00c6')
check('AC10', '00f1','00d1','007e@','02dd@')
assert '0063 00e7' in klc and '0043 00c7' in klc and '0073 00df' in klc
print(f'OK: {len(layout_rows)} posizioni Windows, legature e composizioni principali (controllo statico).')
