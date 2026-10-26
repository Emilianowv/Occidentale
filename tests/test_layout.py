import json
import tempfile
import unittest
from pathlib import Path
import subprocess
import unicodedata

from xkb_api import Keyboard, ROOT, sym_from_name, update, mod_active


class LayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = Keyboard()

    @classmethod
    def tearDownClass(cls):
        cls.kb.close()

    def test_all_49_keys_four_modifier_states(self):
        manifest = json.loads((ROOT/'docs/layout-manifest.json').read_text())
        self.assertEqual(len(manifest['keys']), 49)
        for key in manifest['keys']:
            for i, level in enumerate(key['levels']):
                with self.subTest(key=key['xkb_key'], level=i+1):
                    self.assertIsNotNone(level, 'Manifest must describe actual compiled behavior')
                    expected = sym_from_name(level['xkb_keysym'].encode(), 0)
                    actual = self.kb.symbol(key['xkb_key'], bool(i & 1), bool(i & 2))
                    self.assertEqual(actual, expected)

    def test_required_compose_characters(self):
        for key, lower, upper in [('AB03', 'ç', 'Ç'), ('AC02', 'ß', 'ẞ')]:
            for shift, expected in [(False, lower), (True, upper)]:
                with self.subTest(expected=expected):
                    self.assertEqual(self.kb.sequence([('AD11',), (key, shift)]), expected)

    def test_accents_both_cases_from_physical_keys(self):
        for dead, shift_dead, combining in [('AD11', False, '\u0300'), ('AD11', True, '\u0302'),
                                             ('AC11', False, '\u0301'), ('AC11', True, '\u0308')]:
            for key, letter in [('AC01', 'a'), ('AD03', 'e'), ('AD08', 'i'), ('AD09', 'o'), ('AD07', 'u')]:
                for shift in (False, True):
                    expected = unicodedata.normalize('NFC', (letter.upper() if shift else letter) + combining)
                    with self.subTest(expected=expected):
                        self.assertEqual(self.kb.sequence([(dead, shift_dead), (key, shift)]), expected)

    def test_dead_keys_then_space(self):
        for key, shift, expected in [('AD11', False, '`'), ('AD11', True, '^'),
                                     ('AC11', False, "'"), ('AC11', True, '"')]:
            with self.subTest(key=key, shift=shift):
                self.assertEqual(self.kb.sequence([(key, shift), ('SPCE',)]), expected)

    def test_caps_lock_and_shortcut_modifiers(self):
        update(self.kb.state, self.kb.code('CAPS'), 1)
        update(self.kb.state, self.kb.code('CAPS'), 0)
        try:
            self.assertEqual(self.kb.name('AC01'), 'A')
            self.assertEqual(self.kb.name('AD09', altgr=True), 'OE')
        finally:
            update(self.kb.state, self.kb.code('CAPS'), 1)
            update(self.kb.state, self.kb.code('CAPS'), 0)
        update(self.kb.state, self.kb.code('LCTL'), 1)
        try:
            self.assertEqual(self.kb.name('AB03'), 'c')
            self.assertTrue(mod_active(self.kb.state, b'Control', 1 << 3))
        finally:
            update(self.kb.state, self.kb.code('LCTL'), 0)

    def test_x11_xkbcomp_compiles_binary(self):
        with tempfile.TemporaryDirectory() as t:
            source, binary = Path(t)/'map.xkb', Path(t)/'map.xkm'
            result = subprocess.run(['xkbcli', 'compile-keymap', '--include', str(ROOT/'xkb'),
                                     '--include-defaults', '--layout', 'wst'], check=True, capture_output=True)
            source.write_bytes(result.stdout)
            subprocess.run(['xkbcomp', '-w', '0', str(source), str(binary)], check=True, capture_output=True)
            self.assertGreater(binary.stat().st_size, 1000)
            dumped = subprocess.run(['xkbcomp', '-w', '0', '-xkb', str(binary), '-'], check=True, capture_output=True).stdout
            self.assertIn(b'Occidentale', dumped)


if __name__ == '__main__':
    unittest.main()
