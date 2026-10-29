#!/usr/bin/env python3
"""Build deterministic source archives and a Debian all-architecture package."""
import gzip
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

from audit import ROOT, audit, source_files


def main():
    audit()
    subprocess.run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT, check=True)
    subprocess.run(['python3', 'scripts/check_windows_klc.py'], cwd=ROOT, check=True)
    subprocess.run([str(ROOT/'occidentale'), 'test'], cwd=ROOT, check=True)
    version = (ROOT/'VERSION').read_text().strip()
    epoch = int(os.environ.get('SOURCE_DATE_EPOCH', '0'))
    out = ROOT/'dist'
    out.mkdir(exist_ok=True)
    files = list(source_files())
    prefix = f'RomanceScript-{version}'
    with zipfile.ZipFile(out/f'{prefix}.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in files:
            item = zipfile.ZipInfo(f'{prefix}/{p.relative_to(ROOT).as_posix()}', (1980, 1, 1, 0, 0, 0))
            item.external_attr = (0o100755 if p.stat().st_mode & 0o111 else 0o100644) << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, p.read_bytes())
    with (out/f'{prefix}.tar.gz').open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=epoch, compresslevel=9) as gz:
            with tarfile.open(fileobj=gz, mode='w', format=tarfile.PAX_FORMAT) as tar:
                for p in files:
                    data = p.read_bytes()
                    info = tarfile.TarInfo(f'{prefix}/{p.relative_to(ROOT).as_posix()}')
                    info.size, info.mtime = len(data), epoch
                    info.mode = 0o755 if p.stat().st_mode & 0o111 else 0o644
                    tar.addfile(info, io.BytesIO(data))
    with tempfile.TemporaryDirectory(prefix='occidentale-package-') as t:
        stage = Path(t)/'package'
        payload = stage/'usr/share/occidentale'
        for p in files:
            target = payload/p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, target)
            target.chmod(0o755 if p.stat().st_mode & 0o111 else 0o644)
        for command in ('romancescript', 'occidentale'):
            binpath = stage/'usr/bin'/command
            binpath.parent.mkdir(parents=True, exist_ok=True)
            binpath.write_text('#!/bin/sh\nexec python3 /usr/share/occidentale/occidentale "$@"\n')
            binpath.chmod(0o755)
        meta = stage/'DEBIAN'
        meta.mkdir()
        size = sum(p.stat().st_size for p in stage.rglob('*') if p.is_file())//1024+1
        (meta/'control').write_text(f'''Package: occidentale
Version: {version}
Section: x11
Priority: optional
Architecture: all
Maintainer: Emilianowv <309815527+Emilianowv@users.noreply.github.com>
Depends: python3 (>= 3.11), xkb-data, libxkbcommon0, libxkbcommon-tools
Recommends: x11-xkb-utils
Homepage: https://github.com/Emilianowv/RomanceScript
Installed-Size: {size}
Description: RomanceScript keyboard layout for Romance languages (wst)
 XKB layout for Spanish, Portuguese, French, Italian, Romanian and Catalan.
 Includes Compose rules, KDE configuration, backups and removal tools.
''')
        for name in ('postinst', 'prerm'):
            dest = meta/name
            shutil.copyfile(ROOT/'packaging'/name, dest)
            dest.chmod(0o755)
        doc = stage/'usr/share/doc/occidentale'
        doc.mkdir(parents=True)
        shutil.copyfile(ROOT/'COPYRIGHT', doc/'copyright')
        env = dict(os.environ, SOURCE_DATE_EPOCH=str(epoch))
        subprocess.run(['dpkg-deb', '--root-owner-group', '--threads-max=1', '-Zxz', '--build',
                        str(stage), str(out/f'occidentale_{version}_all.deb')], check=True, env=env)
    artifacts = [out/f'{prefix}.zip', out/f'{prefix}.tar.gz', out/f'occidentale_{version}_all.deb']
    (out/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in artifacts))
    print('Pacchetti verificati e creati in dist/.')


if __name__ == '__main__':
    main()
