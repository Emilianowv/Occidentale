#!/usr/bin/env python3
"""Refresh a pinned CLDR exemplar snapshot. Optional: network + ICU C library.

No dependency is added to the keyboard installer. Normal audits use the saved
JSON offline. ICU interprets UnicodeSet ranges, escapes and strings correctly.
"""
import ctypes as C
import ctypes.util
from concurrent.futures import ThreadPoolExecutor
import hashlib
from functools import lru_cache
import json
from pathlib import Path
import re
import tempfile
from urllib.request import urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TAG = 'release-49'
BASE = f'https://raw.githubusercontent.com/unicode-org/cldr/{TAG}'
PARENTS = {}
CACHE = Path(tempfile.gettempdir()) / ('romancescript-cldr-'+TAG)
GROUPS = {'Romances': {'es':'Español', 'pt':'Portugués', 'fr':'Francés', 'it':'Italiano', 'ro':'Rumano', 'ca':'Catalán'}}


class UnicodeSet:
    def __init__(self):
        soname = ctypes.util.find_library('icuuc')
        if not soname:
            raise RuntimeError('ICU is needed only to refresh CLDR data')
        self.lib = C.CDLL(soname)
        match = re.search(r'\.so\.(\d+)', soname)
        suffix = '_'+match.group(1) if match else ''
        def bind(name, result, *args):
            fn = getattr(self.lib, name+suffix)
            fn.restype, fn.argtypes = result, list(args)
            return fn
        self.open = bind('uset_openPattern', C.c_void_p, C.POINTER(C.c_uint16), C.c_int32, C.POINTER(C.c_int32))
        self.count = bind('uset_getItemCount', C.c_int32, C.c_void_p)
        self.item = bind('uset_getItem', C.c_int32, C.c_void_p, C.c_int32,
                         C.POINTER(C.c_int32), C.POINTER(C.c_int32), C.POINTER(C.c_uint16), C.c_int32, C.POINTER(C.c_int32))
        self.close = bind('uset_close', None, C.c_void_p)

    def parse(self, pattern):
        raw = pattern.encode('utf-16-le')
        buf = (C.c_uint16*(len(raw)//2)).from_buffer_copy(raw)
        error = C.c_int32(0)
        obj = self.open(buf, len(buf), C.byref(error))
        if not obj or error.value > 0:
            raise RuntimeError(f'Invalid UnicodeSet ({error.value}): {pattern}')
        chars = []
        try:
            for i in range(self.count(obj)):
                first, last, error = C.c_int32(), C.c_int32(), C.c_int32(0)
                text = (C.c_uint16*256)()
                length = self.item(obj, i, C.byref(first), C.byref(last), text, 256, C.byref(error))
                if error.value > 0:
                    raise RuntimeError(f'UnicodeSet item error {error.value}')
                if length:
                    chars.append(C.string_at(text, length*2).decode('utf-16-le'))
                else:
                    chars.extend(chr(x) for x in range(first.value, last.value+1))
        finally:
            self.close(obj)
        return sorted(set(chars))


@lru_cache(maxsize=None)
def fetch(relative):
    cached=CACHE/relative
    if cached.exists():
        return cached.read_bytes()
    url=f'{BASE}/{relative}'
    try:
        data=urlopen(url, timeout=30).read()
        cached.parent.mkdir(parents=True,exist_ok=True)
        cached.write_bytes(data)
        return data
    except HTTPError as exc:
        raise RuntimeError(f'HTTP {exc.code}: {url}') from exc


def download(item):
    locale, name, group = item
    url = f'{BASE}/common/main/{locale}.xml'
    patterns, sources = {}, []
    current = locale
    seen = set()
    while current not in seen:
        seen.add(current)
        raw = None
        for directory in ('common/main','seed/main','exemplars/main'):
            relative=f'{directory}/{current}.xml'
            try:
                raw=fetch(relative)
                break
            except RuntimeError as exc:
                if not isinstance(exc.__cause__,HTTPError) or exc.__cause__.code != 404:
                    raise
        if raw is None:
            return {'locale':locale, 'name':name, 'group':group,
                    'unavailable':f'No se encontró un repertorio CLDR en los tres directorios para {current}.'}
        node = ET.fromstring(raw).find('characters')
        sources.append({'locale':current, 'url':f'{BASE}/{relative}',
                        'sha256':hashlib.sha256(raw).hexdigest()})
        if node is not None:
            if node.find('alias') is not None:
                raise RuntimeError(f'{current}: characters alias requires explicit review')
            for field in ('main', 'auxiliary', 'punctuation'):
                el = node.find('exemplarCharacters' if field == 'main' else f'exemplarCharacters[@type="{field}"]')
                if field not in patterns and el is not None and el.text and el.text != '↑↑↑':
                    patterns[field] = el.text
        if current=='root' or len(patterns)==3:
            break
        current = PARENTS.get(current, current.rsplit('_',1)[0] if '_' in current else 'root')
    if not patterns.get('main') or patterns['main']=='[]':
        return {'locale':locale, 'name':name, 'group':group,
                'unavailable':'No contiene un repertorio principal específico; requiere otra fuente.'}
    return {'locale':locale, 'name':name, 'group':group, 'source':sources[0]['url'],
            'sources':sources, 'patterns':patterns}


def main():
    parser = UnicodeSet()
    supplemental = fetch('common/supplemental/supplementalData.xml')
    for group in ET.fromstring(supplemental).findall('parentLocales'):
        if 'component' not in group.attrib:
            for node in group.findall('parentLocale'):
                for locale in node.attrib.get('locales','').split():
                    PARENTS[locale] = node.attrib['parent']
    items = [(locale, name, group) for group, locales in GROUPS.items() for locale, name in locales.items()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(download, items))
    unavailable=[row for row in rows if 'unavailable' in row]
    rows=[row for row in rows if 'unavailable' not in row]
    for row in rows:
        row['sets'] = {key:parser.parse(value) for key, value in row.pop('patterns').items()}
    data = {'source':'Unicode CLDR', 'tag':TAG, 'license':'Unicode-3.0',
            'parent_locales_source':{'url':f'{BASE}/common/supplemental/supplementalData.xml',
                                     'sha256':hashlib.sha256(supplemental).hexdigest()},
            'note':'Seis lenguas prioritarias de RomanceScript. Repertorios principales, auxiliares y puntuación separados.',
            'languages':rows, 'unavailable_languages':unavailable}
    path = ROOT/'docs/language-repertoires.json'
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    # This is the upstream data license, not the separately restricted LDML specification.
    license_text = fetch('LICENSE').decode()
    license_text = 'Copyright © 2001–2026 Unicode, Inc.\n\n' + license_text[license_text.index('NOTICE TO USER:'):]
    (ROOT/'docs/UNICODE-LICENSE.txt').write_text(license_text)
    print(f'CLDR snapshot: {len(rows)} lenguas, {TAG}')


if __name__ == '__main__':
    main()
