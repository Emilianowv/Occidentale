#!/usr/bin/env python3
"""Measure saved CLDR repertoires against real XKB + Compose, offline.

Enumerates direct keys and one dead key followed by a printable key, including
Shift/AltGr. A missing result means absent from that tested route, not impossible
through Unicode input, a separately configured Compose key or multiple dead keys.
"""
import argparse
import ctypes as C
import json
from pathlib import Path
import sys
import unicodedata as U

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tests'))
from xkb_api import Keyboard, bind, compose_reset, compose_feed, compose_status, compose_utf8

to_unicode = bind('xkb_keysym_to_utf32', C.c_uint32, C.c_uint32)
DEAD_NAMES = {'dead_grave':'grave muerto', 'dead_acute':'agudo muerto',
              'dead_circumflex':'circunflejo muerto', 'dead_diaeresis':'diéresis muerta',
              'dead_tilde':'tilde muerta', 'dead_doubleacute':'doble agudo muerto',
              'dead_caron':'carón muerto', 'dead_abovedot':'punto superior muerto',
              'dead_belowdot':'punto inferior muerto', 'dead_cedilla':'cedilla muerta',
              'dead_ogonek':'ogonek muerto', 'dead_breve':'breve muerta',
              'dead_hook':'gancho muerto', 'dead_horn':'cuerno muerto'}


def key_label(item, level):
    name = item['xkb_key']
    fixed = {'AD11':'tecla de grave', 'AC11':'tecla de agudo', 'AD12':'tecla de breve', 'SPCE':'Espacio', 'LSGT':'tecla ISO <'}
    base = fixed.get(name) or item['levels'][0]['character'] or name
    if len(base) == 1 and base.isalpha():
        base = base.upper()
    return ('Shift+' if level&1 else '') + ('AltGr+' if level&2 else '') + base


def reachable(kb, manifest):
    mapping, strokes, dead = {}, [], {}
    def add(text, steps, modifiers):
        if not text or any(U.category(c).startswith('C') for c in text):
            return
        text = U.normalize('NFC', text)
        recipe = {'steps':steps, 'modifiers':modifiers}
        previous = mapping.get(text)
        if previous is None or (len(steps),modifiers) < (len(previous['steps']),previous['modifiers']):
            mapping[text] = recipe
    for item in manifest['keys']:
        for level in range(4):
            sym = kb.symbol(item['xkb_key'], bool(level&1), bool(level&2))
            name = kb.name(item['xkb_key'], bool(level&1), bool(level&2))
            label, mods = key_label(item, level), int(bool(level&1))+int(bool(level&2))
            cp = to_unicode(sym)
            if cp:
                add(chr(cp), [label], mods)
                strokes.append((sym,label,mods))
            elif name.startswith('dead_'):
                if sym not in dead or mods < dead[sym][1]:
                    dead[sym] = (label,mods,name)
    for accent, (trigger,mods,name) in dead.items():
        for sym,label,secondmods in strokes:
            compose_reset(kb.compose)
            compose_feed(kb.compose, accent)
            compose_feed(kb.compose, sym)
            if compose_status(kb.compose) == 2:
                buf = C.create_string_buffer(128)
                compose_utf8(kb.compose,buf,len(buf))
                add(buf.value.decode(), [trigger,label], mods+secondmods)
    return mapping, sorted({value[2] for value in dead.values()})


def segment(text, mapping):
    text = U.normalize('NFC',text)
    best = {0:[]}
    for i in range(len(text)):
        if i not in best:
            continue
        for j in range(i+1,len(text)+1):
            part = mapping.get(text[i:j])
            if part:
                candidate = best[i] + part['steps']
                if j not in best or len(candidate)<len(best[j]):
                    best[j] = candidate
    return best.get(len(text))


def report(kb, data, manifest):
    mapping, accents = reachable(kb,manifest)
    rows=[]
    for row in data['languages']:
        sets = row['sets']
        required = sorted({U.normalize('NFC',c) for value in sets['main'] for c in (value,value.upper())})
        # Keep multi-character exemplars (e.g. Catalan l·l), and test concatenation.
        special = [x for x in required if any(ord(c)>127 for c in x)]
        missing = [x for x in required if segment(x,mapping) is None]
        auxiliary = sorted({U.normalize('NFC',c) for value in sets.get('auxiliary',[]) for c in (value,value.upper())})
        punctuation = sorted(sets.get('punctuation',[]))
        rows.append({key:row[key] for key in ('locale','name','group','source')} |
                    {'special':special,'missing':missing,
                     'auxiliary_missing':[x for x in auxiliary if segment(x,mapping) is None],
                     'punctuation_missing':[x for x in punctuation if segment(x,mapping) is None],
                     'required_count':len(required), 'covered_count':len(required)-len(missing)})
    return {'layout_version':manifest['version'], 'source':data['tag'],
            'model':'direct or one dead key + printable key; concatenation for multi-character exemplars',
            'compose_locale':'en_US.UTF-8', 'dead_keys':accents,
            'recipes':mapping,'languages':rows, 'unavailable_languages':data.get('unavailable_languages',[])}


def markdown(result):
    lines=['# Cobertura de RomanceScript', '',
           f"RomanceScript {result['layout_version']} · datos Unicode CLDR {result['source']} · Compose en_US.UTF-8.", '',
           'El alcance prioritario es español, portugués, francés, italiano, rumano y catalán. Se conserva ß/ẞ como compatibilidad adicional.', '',
           'Se han probado teclas directas, Shift/AltGr y un acento muerto seguido de una tecla imprimible. Las mayúsculas también se comprueban. Los dígrafos se evalúan como cadenas. “Falta” significa que no apareció en esas rutas; puede existir otra vía con varios acentos, entrada Unicode o una tecla Compose configurada aparte.', '',
           'Los repertorios principales, auxiliares y de puntuación se mantienen separados. Un repertorio principal cubierto no equivale a soporte ortográfico completo ni a pruebas de aplicaciones. CLDR no es una medida de frecuencia de uso.', '']
    groups = list(dict.fromkeys(row['group'] for row in result['languages']))
    for group in groups:
        lines += ['## '+group, '', '| Lengua | Caracteres especiales principales (ambos casos) | Faltan en las rutas probadas |', '|---|---|---|']
        for row in result['languages']:
            if row['group']==group:
                lines.append(f"| {row['name']} | {' '.join(row['special']) or 'Ninguno fuera de ASCII'} | {' '.join(row['missing']) or '—'} |")
        lines.append('')
    lines += ['## Rutas actuales de interés', '', '| Carácter | Cómo se obtiene |', '|---|---|']
    for char in 'ñÑçÇßẞăĂșȘțȚœŒæÆãÃõÕàèìòùáéíóúâêîôûäëïöüÿŸ·¿¡':
        recipe=result['recipes'].get(char)
        lines.append(f"| {char} | {' → '.join(recipe['steps']) if recipe else 'No encontrado'} |")
    lines += ['', '## Auxiliares y puntuación', '',
              'Estos huecos se muestran aparte: incluyen grafías extranjeras, históricas y tipografía que no forman el alfabeto principal.', '',
              '| Lengua | Auxiliares ausentes | Puntuación ausente |', '|---|---|---|']
    for row in result['languages']:
        if row['auxiliary_missing'] or row['punctuation_missing']:
            escape=lambda xs:' '.join(x.replace('|','&#124;') for x in xs) or '—'
            lines.append(f"| {row['name']} | {escape(row['auxiliary_missing'])} | {escape(row['punctuation_missing'])} |")
    lines += ['', '## Datos pendientes', '']
    for row in result.get('unavailable_languages',[]):
        lines.append(f"- {row['name']}: {row['unavailable']}")
    lines += ['', '## Fuentes y reproducción', '',
              '- [CLDR: definición de repertorios principales y auxiliares](https://cldr.unicode.org/translation/core-data/exemplars).',
              '- [Datos CLDR 49](https://github.com/unicode-org/cldr/tree/release-49/common/main). Cada lengua del JSON conserva el URL y SHA256 de su fuente.',
              '- `python3 scripts/language_audit.py --write` regenera este informe usando XKB y Compose reales, sin red.',
              '- `python3 scripts/update_language_data.py` actualiza la instantánea fijada; requiere red e ICU solo para esa tarea.',
              '- Datos de Unicode bajo Unicode-3.0; véase `UNICODE-LICENSE.txt`.', '']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    data=json.loads((ROOT/'docs/language-repertoires.json').read_text())
    manifest=json.loads((ROOT/'docs/layout-manifest.json').read_text())
    kb=Keyboard()
    try:
        result=report(kb,data,manifest)
    finally:
        kb.close()
    if args.write:
        (ROOT/'docs/language-coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        (ROOT/'docs/LENGUAS.md').write_text(markdown(result))
    for row in result['languages']:
        print(f"{row['name']}: {row['covered_count']}/{row['required_count']} · faltan {' '.join(row['missing']) or 'ninguno'}")


if __name__=='__main__':
    main()
