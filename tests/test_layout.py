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
        for key, lower, upper in [('AB03', 'ç', 'Ç'), ('AC02', 'ß', 'ẞ'), ('AB06', 'ñ', 'Ñ')]:
            for shift, expected in [(False, lower), (True, upper)]:
                with self.subTest(expected=expected):
                    self.assertEqual(self.kb.sequence([('AD11',), (key, shift)]), expected)

    def test_semicolon_colon_and_retained_dead_keys(self):
        self.assertEqual(self.kb.name('AC10'), 'ntilde')
        self.assertEqual(self.kb.name('AC10', shift=True), 'Ntilde')
        self.assertEqual(self.kb.name('AC10', altgr=True), 'dead_tilde')
        self.assertEqual(self.kb.name('AC10', shift=True, altgr=True), 'dead_doubleacute')
        self.assertEqual(self.kb.sequence([('AC10', False, True), ('AC01',)]), 'ã')
        self.assertEqual(self.kb.sequence([('AC10', True, True), ('AD09',)]), 'ő')
        self.assertEqual(self.kb.name('AB08', shift=True), 'semicolon')
        self.assertEqual(self.kb.name('AB09', shift=True), 'colon')

    def test_opening_punctuation_below_escape(self):
        self.assertEqual(self.kb.name('TLDE'), 'questiondown')
        self.assertEqual(self.kb.name('TLDE', shift=True), 'exclamdown')
        self.assertEqual(self.kb.name('TLDE', altgr=True), 'backslash')
        self.assertEqual(self.kb.name('TLDE', shift=True, altgr=True), 'backslash')
        # Existing alternative routes and closing punctuation are retained.
        self.assertEqual(self.kb.name('AE01', shift=True), 'exclam')
        self.assertEqual(self.kb.name('AB10', shift=True), 'question')
        self.assertEqual(self.kb.name('AE01', shift=True, altgr=True), 'exclamdown')
        self.assertEqual(self.kb.name('AE11', shift=True, altgr=True), 'questiondown')

    def test_punctuation_and_braces_keep_altgr_levels(self):
        self.assertEqual(self.kb.name('AB09'), 'period')
        self.assertEqual(self.kb.name('AB09', shift=True), 'colon')
        self.assertEqual(self.kb.name('AB09', altgr=True), 'periodcentered')
        self.assertEqual(self.kb.name('AB09', shift=True, altgr=True), 'division')
        self.assertEqual(self.kb.name('AD12', altgr=True), 'bracketright')
        self.assertEqual(self.kb.name('AD12', shift=True, altgr=True), 'braceright')
        self.assertEqual(self.kb.name('AE12', shift=True), 'plus')
        self.assertEqual(self.kb.name('AE08', shift=True), 'asterisk')

    def test_romanian_breve_and_comma_below_both_cases(self):
        self.assertEqual(self.kb.name('AD12'), 'dead_breve')
        self.assertEqual(self.kb.name('AD12', shift=True), 'dead_belowcomma')
        for key, lower, upper in [('AC02','ș','Ș'), ('AD05','ț','Ț')]:
            for shift, expected in [(False,lower), (True,upper)]:
                with self.subTest(expected=expected):
                    self.assertEqual(self.kb.sequence([('AD12',True),(key,shift)]),expected)
        for shift, expected in [(False,'ă'), (True,'Ă')]:
            self.assertEqual(self.kb.sequence([('AD12',),( 'AC01',shift)]),expected)
        # The acute prefix no longer selects the Romanian comma-below letters.
        self.assertEqual(self.kb.sequence([('AC11',),('AC02',)]),'ś')

    def test_french_ligatures_diaeresis_and_german_extra(self):
        for key, lower, upper in [('AC01','ae','AE'), ('AD09','oe','OE'), ('AC02','ssharp','U1E9E')]:
            self.assertEqual(self.kb.name(key,altgr=True),lower)
            self.assertEqual(self.kb.name(key,shift=True,altgr=True),upper)
        for shift, expected in [(False,'ÿ'),(True,'Ÿ')]:
            self.assertEqual(self.kb.sequence([('AC11',True),('AD06',shift)]),expected)

    def test_accents_both_cases_from_physical_keys(self):
        for dead, shift_dead, combining in [('AD11', False, '\u0300'), ('AE06', True, '\u0302'),
                                             ('AC11', False, '\u0301'), ('AC11', True, '\u0308')]:
            for key, letter in [('AC01', 'a'), ('AD03', 'e'), ('AD08', 'i'), ('AD09', 'o'), ('AD07', 'u')]:
                for shift in (False, True):
                    expected = unicodedata.normalize('NFC', (letter.upper() if shift else letter) + combining)
                    with self.subTest(expected=expected):
                        self.assertEqual(self.kb.sequence([(dead, shift_dead), (key, shift)]), expected)

    def test_dead_keys_then_space(self):
        for key, shift, expected in [('AD11', False, '`'), ('AD11', True, '~'), ('AE06', True, '^'),
                                     ('AC11', False, "'"), ('AC11', True, '"'), ('AD12', False, '˘')]:
            with self.subTest(key=key, shift=shift):
                self.assertEqual(self.kb.sequence([(key, shift), ('SPCE',)]), expected)

    def test_portuguese_tilde_on_shift_grave(self):
        self.assertEqual(self.kb.name('AD11', shift=True), 'dead_tilde')
        self.assertEqual(self.kb.name('AE06', shift=True), 'dead_circumflex')
        for key, lower, upper in [('AC01', 'ã', 'Ã'), ('AD09', 'õ', 'Õ'), ('AB06', 'ñ', 'Ñ')]:
            for shift, expected in [(False,lower),(True,upper)]:
                with self.subTest(expected=expected):
                    self.assertEqual(self.kb.sequence([('AD11',True),(key,shift)]),expected)

    def test_caps_lock_and_shortcut_modifiers(self):
        update(self.kb.state, self.kb.code('CAPS'), 1)
        update(self.kb.state, self.kb.code('CAPS'), 0)
        try:
            self.assertEqual(self.kb.name('AC01'), 'A')
            self.assertEqual(self.kb.name('AD09', altgr=True), 'OE')
            self.assertEqual(self.kb.name('AC10'), 'Ntilde')
            self.assertEqual(self.kb.name('AC10', shift=True), 'ntilde')
            self.assertEqual(self.kb.sequence([('AD11',), ('AB06',)]), 'Ñ')
            self.assertEqual(self.kb.name('TLDE'), 'questiondown')
            self.assertEqual(self.kb.name('TLDE', shift=True), 'exclamdown')
            self.assertEqual(self.kb.sequence([('AD12',True), ('AC02',)]), 'Ș')
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
                                     '--include-defaults', '--layout', 'rom'], check=True, capture_output=True)
            source.write_bytes(result.stdout)
            subprocess.run(['xkbcomp', '-w', '0', str(source), str(binary)], check=True, capture_output=True)
            self.assertGreater(binary.stat().st_size, 1000)
            dumped = subprocess.run(['xkbcomp', '-w', '0', '-xkb', str(binary), '-'], check=True, capture_output=True).stdout
            self.assertIn(b'RomanceScript', dumped)


if __name__ == '__main__':
    unittest.main()
