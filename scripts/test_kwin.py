#!/usr/bin/env python3
"""Run a separate headless KWin 6; inspect the keymap it sends over Wayland.

Needs kwin-wayland, dbus, gcc, pkg-config, libwayland-dev and permission to
create Unix sockets. Does not connect to or modify the desktop session.
"""
import json
import os
from pathlib import Path
import signal
import shutil
import select
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tests'))
from xkb_api import Keyboard, sym_from_name


def verify_states(keymap, compose):
    kb = Keyboard(keymap_bytes=keymap, compose=compose)
    manifest = json.loads((ROOT/'docs/layout-manifest.json').read_text())
    try:
        for item in manifest['keys']:
            for i, level in enumerate(item['levels']):
                assert kb.symbol(item['xkb_key'], bool(i&1), bool(i&2)) == sym_from_name(level['xkb_keysym'].encode(), 0), (item['xkb_key'], i)
        assert kb.sequence([('AD11',), ('AB03',)]) == 'ç'
        assert kb.sequence([('AD11',), ('AC02',)]) == 'ß'
        assert kb.sequence([('AD11',), ('AB06',)]) == 'ñ'
        assert kb.sequence([('AD11',), ('AB06', True)]) == 'Ñ'
        for first, second, expected in [
            (('AD12',True),('AC02',),'ș'), (('AD12',True),('AC02',True),'Ș'),
            (('AD12',True),('AD05',),'ț'), (('AD12',True),('AD05',True),'Ț'),
            (('AD12',),('AC01',),'ă'), (('AD12',),('AC01',True),'Ă')]:
            assert kb.sequence([first,second]) == expected, expected
        for first, expected in [(('AD11',),'`'),(('AD11',True),'~')]:
            assert kb.sequence([first,('SPCE',)]) == expected, expected
    finally:
        kb.close()


def verify_x11(base, env, keymap, compose):
    """Load a map into a real independent X server and read it back."""
    readfd, writefd = os.pipe()
    xlog = (base/'xwayland.log').open('w')
    server = subprocess.Popen(['Xwayland', '-rootless', '-nokeymap', '-noreset', '-nolisten', 'tcp',
                               '-displayfd', str(writefd)], pass_fds=(writefd,), env=env,
                              stdout=xlog, stderr=xlog)
    os.close(writefd)
    try:
        if not select.select([readfd], [], [], 8)[0]:
            raise RuntimeError('Xwayland display startup timed out')
        number = os.read(readfd, 64).decode().strip()
        if not number.isdigit():
            raise RuntimeError('Xwayland did not provide a display')
        xenv = dict(env, DISPLAY=':'+number)
        subprocess.run(['xkbcomp', '-w', '0', '-', ':'+number], input=keymap, env=xenv, check=True, capture_output=True)
        actual = subprocess.run(['xkbcomp', '-w', '0', '-xkb', ':'+number, '-'], env=xenv, check=True, capture_output=True).stdout
        verify_states(actual, compose)
        print('OK: mappa caricata e riletta da un server X11 (Xwayland indipendente), 196 stati verificati.')
    except BaseException:
        xlog.flush()
        print((base/'xwayland.log').read_text()[-3000:], file=sys.stderr)
        raise
    finally:
        os.close(readfd)
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()
        xlog.close()


def main():
    with tempfile.TemporaryDirectory(prefix='occidentale-kwin-') as t:
        base = Path(t)
        runtime, home, native = base/'runtime', base/'home', base/'system'
        runtime.mkdir(mode=0o700)
        home.mkdir()
        cli = [str(ROOT/'occidentale'), '--root', str(native), '--home', str(home)]
        for command in ('system-install', 'user-install', 'kde-select'):
            subprocess.run([*cli, command], check=True, capture_output=True)
        binary = base/'read-keymap'
        subprocess.run(['cc', '-Wall', '-Wextra', '-Werror', str(ROOT/'tests/wayland_keymap.c'),
                        '-lwayland-client', '-o', str(binary)], check=True)
        env = dict(os.environ, XDG_RUNTIME_DIR=str(runtime), XDG_CONFIG_HOME=str(home/'.config'),
                   HOME=str(home), XKB_CONFIG_EXTRA_PATH=str(native/'usr/share/X11/xkb'),
                   QT_QPA_PLATFORM='offscreen', KWIN_COMPOSE='Q', LIBGL_ALWAYS_SOFTWARE='true',
                   WAYLAND_DISPLAY='occidentale-test')
        for key in ('DISPLAY', 'DBUS_SESSION_BUS_ADDRESS', 'XKB_DEFAULT_LAYOUT', 'XKB_DEFAULT_VARIANT', 'XCOMPOSEFILE'):
            env.pop(key, None)
        log = base/'kwin.log'
        with log.open('w') as f:
            process = subprocess.Popen(['dbus-run-session', '--', 'kwin_wayland', '--virtual',
                                        '--no-lockscreen', '--no-global-shortcuts', '--no-kactivities',
                                        '--socket', 'occidentale-test'], env=env, stdout=f, stderr=f,
                                       start_new_session=True)
        try:
            for _ in range(100):
                if (runtime/'occidentale-test').exists() or process.poll() is not None:
                    break
                time.sleep(0.05)
            if process.poll() is not None:
                raise RuntimeError('KWin did not start:\n' + log.read_text()[-5000:])
            exported = base/'actual-keymap.xkb'
            subprocess.run([str(binary), str(exported)], env=env, check=True, timeout=12)
            compose = (home/'.XCompose').read_text()
            verify_states(exported.read_bytes(), compose)
            print('OK: KWin carica kxkbrc e invia via Wayland la mappa corretta in tutti i 196 stati; Compose ç/ß verificato.')
            verify_x11(base, env, exported.read_bytes(), compose)
        except BaseException:
            print(log.read_text()[-5000:], file=sys.stderr)
            raise
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            # A portal auto-started on the private bus can leave a disconnected
            # FUSE document mount. Detach only this test's mount before cleanup.
            fusermount = shutil.which('fusermount3') or shutil.which('fusermount')
            if fusermount:
                subprocess.run([fusermount, '-uz', str(runtime/'doc')], capture_output=True)


if __name__ == '__main__':
    main()
