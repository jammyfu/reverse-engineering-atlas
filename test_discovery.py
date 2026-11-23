import json
from pathlib import Path
import unittest

# Must stay aligned with render.py: game platforms, topic sections, and renderable game subsections.
PLATS = ['switch2', 'switch', 'nes', 'snes', 'md', 'saturn', 'gb', 'gba', 'n64', 'gc', 'wii', 'ds', '3ds', 'ps1', 'ps2', 'xbox', 'pc']
TOPICS = ['app', 'protocol', 'firmware', 'security', 'tooling', 'official']
GAME_SUBS = {'decomp', 'remake', 'tools'}
EN_HEAD = {
    'switch2': 'Nintendo Switch 2',
    'switch': 'Nintendo Switch',
    'nes': 'NES / Famicom',
    'snes': 'Super Famicom / SNES',
    'md': 'Mega Drive / Genesis',
    'saturn': 'Sega Saturn',
    'gb': 'Game Boy',
    'gba': 'Game Boy Advance',
    'n64': 'Nintendo 64',
    'gc': 'GameCube',
    'wii': 'Wii',
    'ds': 'Nintendo DS',
    '3ds': 'Nintendo 3DS',
    'ps1': 'PlayStation',
    'ps2': 'PlayStation 2',
    'xbox': 'Xbox / Xbox 360',
    'pc': 'PC / DOS / PC-98',
}

class DiscoveryContract(unittest.TestCase):
    def test_shared_platform_classification(self):
        entries = json.loads(Path('data.json').read_text())
        known = set(PLATS) | set(TOPICS)
        by_plat = {p: [] for p in PLATS}
        for e in entries:
            self.assertIn(e[0], known, f'unknown section: {e[2]}')
            if e[0] in by_plat:
                self.assertIn(e[1], GAME_SUBS, f'{e[2]} uses {e[1]!r}; game rows need decomp/remake/tools to render')
                by_plat[e[0]].append(e)

        switch2 = {e[2] for e in by_plat['switch2']}
        switch = {e[2] for e in by_plat['switch']}
        pc = {e[2] for e in by_plat['pc']}
        self.assertTrue(switch2, 'Switch 2 source-platform group must stay non-empty')
        self.assertTrue(switch, 'Switch source-platform group must stay non-empty')
        self.assertFalse(switch2 & switch, 'Switch 2 and Switch must remain distinct')
        self.assertFalse(switch2 & pc, 'Switch 2 games must not be filed under PC')
        self.assertFalse(switch & pc, 'Switch games must not be filed under PC')

        readme = Path('README.md').read_text()
        self.assertLess(readme.index('### Nintendo Switch 2\n'), readme.index('### Nintendo Switch\n'))
        self.assertLess(readme.index('### Nintendo Switch\n'), readme.index('### PC / DOS / PC-98\n'))
        self.assertRegex(readme, rf'\*\*{len(entries)} catalog entries · ')
        for p, rows in by_plat.items():
            if not rows:
                continue
            heading = f'### {EN_HEAD[p]}\n'
            self.assertIn(heading, readme, f'missing {p} heading')
            start = readme.index(heading)
            cuts = [i for i in (readme.find('\n### ', start + 1), readme.find('\n## ', start + 1)) if i >= 0]
            chunk = readme[start:min(cuts)] if cuts else readme[start:]
            for e in rows:
                self.assertIn(f'href="{e[3]}"', chunk, f'{e[2]} not listed under {EN_HEAD[p]}')

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
                    elif depth==0: self.assertLessEqual(token.count('<tr><td>'),15)

    def test_unavailable_previews_never_emit_broken_images(self):
        unavailable=json.loads(Path('unavailable-previews.json').read_text())
        self.assertEqual(9,len(unavailable))
        for file in ['README.md','README.zh-CN.md','README.zh-TW.md','README.ja.md','README.ko.md']:
            text=Path(file).read_text()
            for record in unavailable.values():
                self.assertNotIn('src="'+record['original_image']+'"',text)
                self.assertIn('href="'+record['source']+'"',text)
