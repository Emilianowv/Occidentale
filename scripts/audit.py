#!/usr/bin/env python3
"""Reject personal email addresses and accidental private files in release inputs."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EMAIL = '309815527+Emilianowv@users.noreply.github.com'
TOP = ('romancescript', 'occidentale', 'VERSION', 'README.md', 'COPYRIGHT', 'Makefile', '.gitignore', '.gitattributes',
       'xkb', 'compose', 'docs', 'scripts', 'tests', 'packaging', 'windows', '.github')


def source_files():
    for name in TOP:
        base = ROOT/name
        if base.is_file():
            yield base
        elif base.is_dir():
            yield from (p for p in sorted(base.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')


def audit():
    errors = []
    files = list(source_files())
    for p in files:
        if p.is_symlink():
            errors.append(f'Unexpected source symlink: {p.relative_to(ROOT)}')
            continue
        raw = p.read_bytes()
        text = raw.decode('utf-16') if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else raw.decode('utf-8')
        for mail in re.findall(r'[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text):
            if mail != ALLOWED_EMAIL:
                errors.append(f'Email not allowed in {p.relative_to(ROOT)}')
        if p.name in ('state.json', 'manifest.json', '.XCompose', 'kxkbrc', 'hosts.yml'):
            errors.append(f'Private configuration in source: {p.relative_to(ROOT)}')
    if errors:
        raise RuntimeError('\n'.join(errors))
    print(f'OK: audit privacy di {len(files)} file; solo indirizzo GitHub noreply consentito.')


if __name__ == '__main__':
    try:
        audit()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
