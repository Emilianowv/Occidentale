import json
from pathlib import Path
import sys
import unittest

from xkb_api import Keyboard, ROOT
sys.path.insert(0,str(ROOT/'scripts'))
from language_audit import report, segment


class LanguageCoverageTests(unittest.TestCase):
    def test_saved_report_matches_real_keyboard(self):
        data=json.loads((ROOT/'docs/language-repertoires.json').read_text())
        manifest=json.loads((ROOT/'docs/layout-manifest.json').read_text())
        kb=Keyboard()
        try:
            actual=report(kb,data,manifest)
        finally:
            kb.close()
        saved=json.loads((ROOT/'docs/language-coverage.json').read_text())
        self.assertEqual(actual,saved,'Regenerate the report when changing the layout or Compose')
        rows={row['locale']:row for row in actual['languages']}
        self.assertEqual(rows['ro']['group'],'Romances')
        self.assertEqual(rows['es']['missing'],[])
        for locale in ('es','fr','it','pt','ro','ca'):
            with self.subTest(locale=locale):
                self.assertEqual(rows[locale]['missing'],[])
        self.assertIsNotNone(segment('l·l',actual['recipes']))
        self.assertEqual(set(rows), {'es','pt','fr','it','ro','ca'})
        self.assertEqual(actual['recipes']['ñ']['steps'],['Ñ'])
        self.assertIsNotNone(segment('ßẞ',actual['recipes']))


if __name__=='__main__':
    unittest.main()
