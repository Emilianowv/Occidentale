#!/usr/bin/env python3
"""Exercise actual dpkg install/reinstall/remove/purge in a disposable root.

--live is only for disposable CI containers: it installs into / instead.
"""
import argparse
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def test(root, live):
    version = (ROOT/'VERSION').read_text().strip()
    deb = ROOT/f'dist/occidentale_{version}_all.deb'
    flags = [] if live else ['--root='+str(root), '--log='+str(root/'dpkg.log'),
                             '--force-depends', '--force-script-chrootless']
    command = ['dpkg', *flags]
    symbol = root/'usr/share/X11/xkb/symbols/wst'
    registry = root/'etc/xkb/rules/evdev.xml'
    assert not symbol.exists() and not registry.exists(), 'Only run in a clean disposable system'
    for name in ('postinst', 'prerm'):
        subprocess.run(['sh', '-n', str(ROOT/'packaging'/name)], check=True)
    for _ in range(2):
        subprocess.run([*command, '-i', str(deb)], check=True, capture_output=True)
        assert symbol.read_bytes() == (ROOT/'xkb/symbols/wst').read_bytes()
        assert '<name>wst</name>' in registry.read_text()
        assert '<description>RomanceScript</description>' in registry.read_text()
        for name in ('romancescript', 'occidentale'):
            wrapper = root/'usr/bin'/name
            assert wrapper.is_file() and wrapper.stat().st_mode & 0o111, name
        # In a disposable root, compile using installed native symbols + host base data.
        subprocess.run(['xkbcli', 'compile-keymap', '--include', str(symbol.parent.parent),
                        '--include-defaults', '--layout', 'wst'], check=True, capture_output=True)
    subprocess.run([*command, '-r', 'occidentale'], check=True, capture_output=True)
    assert not symbol.exists() and not registry.exists(), 'Native files must be removed by prerm'
    assert not (root/'usr/bin/romancescript').exists()
    assert not (root/'usr/bin/occidentale').exists()
    subprocess.run([*command, '-P', 'occidentale'], check=True, capture_output=True)
    assert list((root/'var/lib/occidentale/backups').glob('*/manifest.json')), 'Recovery snapshots must survive purge'
    print('OK: dpkg installazione, reinstallazione, rimozione, purge e compilazione del payload installato.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    if not args.live and os.geteuid() != 0:
        if not shutil.which('fakeroot'):
            raise SystemExit('Installa fakeroot per il test dpkg senza privilegi amministrativi.')
        os.execvp('fakeroot', ['fakeroot', sys.executable, __file__])
    os.environ['PATH'] = os.environ.get('PATH', '') + ':/usr/sbin:/sbin'
    try:
        if args.live:
            assert os.geteuid() == 0, '--live requires root in a disposable container'
            test(Path('/'), True)
        else:
            with tempfile.TemporaryDirectory(prefix='occidentale-dpkg-') as t:
                test(Path(t), False)
    except subprocess.CalledProcessError as exc:
        print(exc.stdout.decode() if isinstance(exc.stdout, bytes) else exc.stdout or '')
        print(exc.stderr.decode() if isinstance(exc.stderr, bytes) else exc.stderr or '')
        raise
