import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from xkb_api import Keyboard, ROOT


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='occidentale test à ')
        self.base = Path(self.temp.name)
        self.root, self.home = self.base/'root', self.base/'home'
        self.home.mkdir()
        self.config = self.home/'.config'
        self.kde = self.config/'kxkbrc'
        self.compose = self.home/'.XCompose'
        self.symbol = self.root/'usr/share/X11/xkb/symbols/wst'
        self.registry = self.root/'etc/xkb/rules/evdev.xml'
        self.state = self.home/'.local/state/occidentale'

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, success=True, cli=None):
        env = dict(os.environ)
        env.pop('XCOMPOSEFILE', None)
        proc = subprocess.run([str(cli or ROOT/'romancescript'), '--root', str(self.root), '--home', str(self.home), *args],
                              env=env, text=True, capture_output=True)
        if success:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def seed(self, layouts='es,us', variants=','):
        self.config.mkdir()
        self.kde.write_text(f'# personal comment\n[Layout]\nLayoutList={layouts}\nVariantList={variants}\nDisplayNames=ES,US\nOptions=grp:alt_shift_toggle\nModel=pc105\nUse=false\n\n[Other]\nKeep=untouched\n')
        self.compose.write_text('include "%L"\n<Multi_key> <q> <q> : "custom"\n')

    def test_full_lifecycle_idempotence_registry_and_real_compose(self):
        self.seed()
        kde_before, compose_before = self.kde.read_bytes(), self.compose.read_bytes()
        self.run_cli('system-install')
        self.run_cli('user-install')
        self.run_cli('kde-select')
        before = [p.read_bytes() for p in (self.symbol, self.registry, self.compose, self.kde)]
        count = len(list(self.state.glob('backups/*')))
        for cmd in ('system-install', 'user-install', 'kde-select'):
            self.run_cli(cmd)
        self.assertEqual(before, [p.read_bytes() for p in (self.symbol, self.registry, self.compose, self.kde)])
        self.assertEqual(count, len(list(self.state.glob('backups/*'))))
        self.assertIn('LayoutList=wst,es,us', self.kde.read_text())
        self.assertIn('Options=grp:alt_shift_toggle', self.kde.read_text())
        self.assertIn('# personal comment', self.kde.read_text())
        self.assertIn('[Other]\nKeep=untouched', self.kde.read_text())
        kb = Keyboard(include=self.symbol.parent.parent, compose=self.compose.read_text())
        try:
            self.assertEqual(kb.sequence([('AD11',), ('AC02',)]), 'ß')
            self.assertEqual(kb.sequence([('AD11',), ('AB03',)]), 'ç')
            for first, second, expected in [
                (('AD12',True),('AC02',),'ș'), (('AD12',True),('AD05',True),'Ț'),
                (('AD12',),('AC01',),'ă'), (('AD12',),('AC01',True),'Ă')]:
                self.assertEqual(kb.sequence([first,second]),expected)
        finally:
            kb.close()
        registry = subprocess.run(['xkbcli', 'list', '--skip-default-paths', '/usr/share/X11/xkb', str(self.root/'etc/xkb')],
                                  check=True, capture_output=True, text=True).stdout
        self.assertIn("layout: 'wst'", registry)
        self.assertIn('description: RomanceScript', registry)
        self.run_cli('doctor')
        self.run_cli('user-remove')
        self.assertEqual(self.kde.read_bytes(), kde_before)
        self.assertEqual(self.compose.read_bytes(), compose_before)
        self.run_cli('system-remove')
        self.assertFalse(self.symbol.exists())
        self.assertFalse(self.registry.exists())
        self.run_cli('user-remove')
        self.run_cli('system-remove')

    def test_registry_coexists_with_other_layouts_and_later_changes(self):
        self.registry.parent.mkdir(parents=True)
        original = '<?xml version="1.0"?><xkbConfigRegistry version="1.1"><layoutList><!-- keep --><layout><configItem><name>other</name><description>Other</description></configItem></layout></layoutList></xkbConfigRegistry>'
        self.registry.write_text(original)
        self.run_cli('system-install')
        self.registry.write_text(self.registry.read_text().replace('</layoutList>', '<!-- later change --></layoutList>'))
        self.run_cli('system-remove')
        self.assertIn('<!-- keep -->', self.registry.read_text())
        self.assertIn('<!-- later change -->', self.registry.read_text())
        self.assertIn('<name>other</name>', self.registry.read_text())
        self.assertNotIn('<name>wst</name>', self.registry.read_text())

    def test_compose_preserves_later_additions(self):
        self.seed()
        self.run_cli('user-install')
        with self.compose.open('a') as f:
            f.write('<Multi_key> <x> <x> : "later"\n')
        self.run_cli('user-remove')
        self.assertIn('custom', self.compose.read_text())
        self.assertIn('later', self.compose.read_text())
        self.assertNotIn('OCCIDENTALE', self.compose.read_text())

    def test_upgrade_replaces_previous_compose_block(self):
        original = 'include "%L"\n# BEGIN OCCIDENTALE WST\n<dead_grave> <c> : "ç" ccedilla\n<dead_acute> <s> : "ș" U0219\n<dead_acute> <t> : "ț" U021B\n# END OCCIDENTALE WST\n# personal rule below\n'
        self.compose.write_text(original)
        self.run_cli('user-install')
        self.assertEqual(self.compose.read_text().count('# BEGIN OCCIDENTALE WST'),1)
        self.assertIn('# personal rule below',self.compose.read_text())
        kb=Keyboard(compose=self.compose.read_text())
        try:
            self.assertEqual(kb.sequence([('AD12',True),('AC02',)]),'ș')
            self.assertEqual(kb.sequence([('AC11',),('AC02',)]),'ś')
        finally:
            kb.close()
        self.run_cli('user-remove')
        self.assertEqual(self.compose.read_text(),original)

    def test_new_files_removed_on_uninstall(self):
        self.run_cli('system-install')
        self.run_cli('user-install')
        self.run_cli('kde-select')
        self.run_cli('user-remove')
        self.assertFalse(self.compose.exists())
        self.assertFalse(self.kde.exists())

    def test_restore_last_user_transaction(self):
        self.seed()
        kde_before = self.kde.read_bytes()
        self.run_cli('system-install')
        self.run_cli('user-install')
        self.run_cli('kde-select')
        self.run_cli('restore')
        self.assertEqual(self.kde.read_bytes(), kde_before)
        self.assertIn('OCCIDENTALE', self.compose.read_text())
        self.run_cli('restore')
        self.assertNotIn('OCCIDENTALE', self.compose.read_text())

    def test_restore_conflict_leaves_all_files_unchanged(self):
        self.run_cli('user-install')
        self.compose.write_text(self.compose.read_text() + '# later\n')
        before = self.compose.read_bytes()
        self.run_cli('restore', success=False)
        self.assertEqual(self.compose.read_bytes(), before)

    def test_symbol_conflict_prevents_install_and_remove(self):
        self.symbol.parent.mkdir(parents=True)
        self.symbol.write_text('foreign layout')
        self.run_cli('system-install', success=False)
        self.assertEqual(self.symbol.read_text(), 'foreign layout')
        self.assertFalse(self.registry.exists())
        self.symbol.unlink()
        self.run_cli('system-install')
        self.symbol.write_text('foreign edit')
        before = self.registry.read_bytes()
        self.run_cli('system-remove', success=False)
        self.assertEqual(self.registry.read_bytes(), before)

    def test_incomplete_compose_and_symlinks_are_not_overwritten(self):
        self.compose.write_text('# BEGIN OCCIDENTALE WST\n')
        before = self.compose.read_bytes()
        self.run_cli('user-install', success=False)
        self.assertEqual(self.compose.read_bytes(), before)
        self.compose.unlink()
        target = self.home/'target'
        target.write_text('unchanged')
        self.compose.symlink_to(target)
        self.run_cli('user-install', success=False)
        self.assertEqual(target.read_text(), 'unchanged')

    def test_four_layout_limit_and_explicit_migration(self):
        self.seed('es,us,fr,de', ',,,')
        self.run_cli('system-install')
        before = self.kde.read_bytes()
        self.run_cli('kde-select', success=False)
        self.assertEqual(self.kde.read_bytes(), before)
        self.run_cli('kde-select', '--replace', 'de')
        self.assertIn('LayoutList=wst,es,us,fr', self.kde.read_text())

    def test_external_kde_changes_keep_new_layouts_and_options(self):
        self.seed()
        self.run_cli('system-install')
        self.run_cli('kde-select')
        self.kde.write_text(self.kde.read_text().replace('LayoutList=wst,es,us', 'LayoutList=wst,es,fr').replace('grp:alt_shift_toggle', 'grp:win_space_toggle'))
        self.run_cli('user-remove')
        self.assertIn('LayoutList=es,fr', self.kde.read_text())
        self.assertIn('Options=grp:win_space_toggle', self.kde.read_text())

    def test_user_shadow_blocks_selection(self):
        self.run_cli('system-install')
        shadow = self.config/'xkb/symbols/wst'
        shadow.parent.mkdir(parents=True)
        shadow.write_text('foreign')
        self.run_cli('kde-select', success=False)
        self.assertFalse(self.kde.exists())

    def test_remove_remembers_kde_path_when_config_home_changes(self):
        self.seed()
        self.run_cli('system-install')
        self.run_cli('kde-select')
        self.kde.write_text(self.kde.read_text() + '# later edit\n')
        self.run_cli('--config-home', str(self.home/'other-config'), 'user-remove')
        self.assertIn('LayoutList=es,us', self.kde.read_text())
        self.assertIn('# later edit', self.kde.read_text())

    def test_upgrade_and_system_rollback(self):
        self.run_cli('system-install')
        original = self.symbol.read_bytes()
        payload = self.base/'updated'
        shutil.copytree(ROOT, payload, ignore=shutil.ignore_patterns('.git', '__pycache__', 'dist'))
        source = payload/'xkb/symbols/wst'
        source.write_text(source.read_text().replace('name[Group1] = "RomanceScript"', 'name[Group1] = "RomanceScript Update"'))
        self.run_cli('system-install', cli=payload/'occidentale')
        self.assertIn('RomanceScript Update', self.symbol.read_text())
        self.run_cli('restore', '--scope', 'system')
        self.assertEqual(self.symbol.read_bytes(), original)
        self.run_cli('system-remove')
        self.assertFalse(self.symbol.exists())

    def test_immutable_kde_configuration_is_preserved(self):
        self.run_cli('system-install')
        self.config.mkdir()
        for text in ('[Layout][$i]\nLayoutList=es\n', '[Layout]\nLayoutList[$i]=es\n', '[Layout]\nLayoutList[$e]=$LAYOUT\n'):
            with self.subTest(text=text):
                self.kde.write_text(text)
                self.run_cli('kde-select', success=False)
                self.assertEqual(self.kde.read_text(), text)

    def test_transaction_rolls_back_on_write_failure(self):
        loader = importlib.machinery.SourceFileLoader('occidentale_test', str(ROOT/'occidentale'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        a, b = self.home/'a', self.home/'b'
        a.write_text('before')
        real = module.atomic
        failed = False

        def faulty(path, snap):
            nonlocal failed
            if Path(path) == b and not failed:
                failed = True
                raise OSError('injected write failure')
            return real(path, snap)

        with module.locked(self.state), patch.object(module, 'atomic', side_effect=faulty):
            with self.assertRaises(OSError):
                module.change(self.state, 'failure-test', {a: module.encoded(b'after'), b: module.encoded(b'new')}, {})
        self.assertEqual(a.read_text(), 'before')
        self.assertFalse(b.exists())
        manifests = [json.loads(p.read_text()) for p in self.state.glob('backups/*/manifest.json')]
        self.assertEqual(manifests[0]['status'], 'rolled-back')


if __name__ == '__main__':
    unittest.main()
