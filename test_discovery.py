import json
from pathlib import Path
import unittest

class DiscoveryContract(unittest.TestCase):
    def test_shared_platform_classification(self):
        entries=json.loads(Path('data.json').read_text())
        self.assertEqual(7,sum(e[0]=='switch2' for e in entries))
        self.assertEqual(11,sum(e[0]=='switch' for e in entries))
        self.assertEqual(387,len(entries))

    def test_five_generated_views(self):
        for file in ['README.md','README.zh-CN.md','README.zh-TW.md','README.ja.md','README.ko.md']:
            s=Path(file).read_text()
            with self.subTest(file=file):
                self.assertIn('images/atlas-hero.webp',s)
                self.assertLess(s.index('### Nintendo Switch 2'),s.index('### PC / DOS / PC-98'))
                self.assertEqual(s.count('<details>'),s.count('</details>'))
                self.assertGreater(s.count('<details>'),1)
                # No table exceeds the preview limit unless inside a disclosure.
                import re
                depth=0
                for token in re.findall(r'<details>|</details>|<table>.*?</table>',s,re.S):
                    if token=='<details>': depth+=1
                    elif token=='</details>': depth-=1
                    elif depth==0: self.assertLessEqual(len(re.findall(r'<tr><td(?:\s[^>]*)?>',token)),15)

    def test_unavailable_previews_never_emit_broken_images(self):
        unavailable=json.loads(Path('unavailable-previews.json').read_text())
        self.assertEqual(9,len(unavailable))
        for file in ['README.md','README.zh-CN.md','README.zh-TW.md','README.ja.md','README.ko.md']:
            text=Path(file).read_text()
            for record in unavailable.values():
                self.assertNotIn('src="'+record['original_image']+'"',text)
                self.assertIn('href="'+record['source']+'"',text)

class GamePresentation(unittest.TestCase):
    def test_game_titles_only_reference_catalog_entries(self):
        entries={e[2] for e in json.loads(Path('data.json').read_text())}
        titles=json.loads(Path('game-titles.json').read_text())
        self.assertTrue(set(titles)<=entries)
        self.assertEqual(titles['Dittobyte/Recompia'],'Pokémon Pokopia')

    def test_platform_icons_are_local_safe_svg(self):
        import xml.etree.ElementTree as ET
        for p in Path('images/platforms').glob('*.svg'):
            text=p.read_text()
            ET.fromstring(text)
            self.assertNotIn('http', text.replace('http://www.w3.org/2000/svg',''))
            self.assertNotIn('<script',text)
        for file in Path('.').glob('README*.md'):
            text=file.read_text()
            self.assertIn('images/platforms/switch2.svg',text)
            self.assertIn('<b>Pokémon\u00a0Pokopia</b>',text)
            self.assertIn('images/platforms/n64.svg',text)

    def test_developer_preview_not_misrepresented(self):
        descriptions=json.loads(Path('descriptions.json').read_text())
        self.assertIn('Not playable', descriptions['RealZotto/oot2-native']['en'])
        self.assertIn('尚不可玩', descriptions['RealZotto/oot2-native']['zh-CN'])

class SkillLocalization(unittest.TestCase):
    def test_techniques_localized_in_readme(self):
        skills=json.loads(Path('skill-map.json').read_text())['skills']
        for lang in ['zh-CN','zh-TW','ja','ko']:
            text=Path('README.'+lang+'.md').read_text()
            for skill in skills:
                self.assertIn(skill['techniques_localized'][lang],text)
                self.assertNotIn(', '.join(skill['techniques']),text)

class CompactTable(unittest.TestCase):
    def test_two_columns_without_losing_fields(self):
        import re
        for file in Path('.').glob('README*.md'):
            text=file.read_text()
            for table in re.findall(r'<table>.*?</table>',text,re.S):
                rows=re.findall(r'<tr>(.*?)</tr>',table,re.S)
                self.assertEqual(2,rows[0].count('<th '))
                for row in rows[1:]:
                    self.assertEqual(2,row.count('<td '))
            self.assertIn('images/editorial/README.md',text)
