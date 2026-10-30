"""Small typed binding to the real system libxkbcommon, used only by tests."""
import ctypes as C
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lib = C.CDLL('libxkbcommon.so.0')


def bind(name, result, *args):
    fn = getattr(lib, name)
    fn.restype, fn.argtypes = result, list(args)
    return fn


ptr, u32 = C.c_void_p, C.c_uint32
context_new = bind('xkb_context_new', ptr, C.c_int)
context_free = bind('xkb_context_unref', None, ptr)
map_new = bind('xkb_keymap_new_from_string', ptr, ptr, C.c_char_p, C.c_int, C.c_int)
map_free = bind('xkb_keymap_unref', None, ptr)
key_by_name = bind('xkb_keymap_key_by_name', u32, ptr, C.c_char_p)
state_new = bind('xkb_state_new', ptr, ptr)
state_free = bind('xkb_state_unref', None, ptr)
update = bind('xkb_state_update_key', C.c_int, ptr, u32, C.c_int)
one_sym = bind('xkb_state_key_get_one_sym', u32, ptr, u32)
sym_name = bind('xkb_keysym_get_name', C.c_int, u32, C.c_char_p, C.c_size_t)
sym_from_name = bind('xkb_keysym_from_name', u32, C.c_char_p, C.c_int)
mod_active = bind('xkb_state_mod_name_is_active', C.c_int, ptr, C.c_char_p, C.c_int)
compose_table_new = bind('xkb_compose_table_new_from_buffer', ptr, ptr, C.c_char_p, C.c_size_t, C.c_char_p, C.c_int, C.c_int)
compose_table_free = bind('xkb_compose_table_unref', None, ptr)
compose_new = bind('xkb_compose_state_new', ptr, ptr, C.c_int)
compose_free = bind('xkb_compose_state_unref', None, ptr)
compose_reset = bind('xkb_compose_state_reset', None, ptr)
compose_feed = bind('xkb_compose_state_feed', C.c_int, ptr, u32)
compose_status = bind('xkb_compose_state_get_status', C.c_int, ptr)
compose_utf8 = bind('xkb_compose_state_get_utf8', C.c_int, ptr, C.c_char_p, C.c_size_t)


class Keyboard:
    def __init__(self, include=None, layout='rom', compose=None, keymap_bytes=None):
        self.ctx = context_new(0)
        data = keymap_bytes or subprocess.run(['xkbcli', 'compile-keymap', '--include', str(include or ROOT/'xkb'),
                               '--include-defaults', '--layout', layout, '--options', ''],
                              check=True, capture_output=True).stdout
        self.keymap = map_new(self.ctx, data, 1, 0)
        assert self.keymap, 'real libxkbcommon compilation failed'
        self.state = state_new(self.keymap)
        text = compose if compose is not None else 'include "%L"\n' + (ROOT/'compose/Compose').read_text()
        data = text.encode()
        self.table = compose_table_new(self.ctx, data, len(data), b'en_US.UTF-8', 1, 0)
        assert self.table, 'real Compose compilation failed'
        self.compose = compose_new(self.table, 0)

    def code(self, name):
        code = key_by_name(self.keymap, name.encode())
        assert code != 0xffffffff, name
        return code

    def symbol(self, name, shift=False, altgr=False):
        if shift:
            update(self.state, self.code('LFSH'), 1)
        if altgr:
            update(self.state, self.code('RALT'), 1)
        result = one_sym(self.state, self.code(name))
        if altgr:
            update(self.state, self.code('RALT'), 0)
        if shift:
            update(self.state, self.code('LFSH'), 0)
        return result

    def name(self, name, shift=False, altgr=False):
        buf = C.create_string_buffer(128)
        sym_name(self.symbol(name, shift, altgr), buf, len(buf))
        return buf.value.decode()

    def sequence(self, keys):
        compose_reset(self.compose)
        for key in keys:
            compose_feed(self.compose, self.symbol(*key))
        status = compose_status(self.compose)
        assert status == 2, f'compose status {status}, expected COMPOSED'
        buf = C.create_string_buffer(128)
        compose_utf8(self.compose, buf, len(buf))
        return buf.value.decode()

    def close(self):
        compose_free(self.compose)
        compose_table_free(self.table)
        state_free(self.state)
        map_free(self.keymap)
        context_free(self.ctx)
