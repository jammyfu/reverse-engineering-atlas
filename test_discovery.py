import json
from pathlib import Path
import unittest

class DiscoveryContract(unittest.TestCase):
    def test_shared_platform_classification(self):
        entries=json.loads(Path('data.json').read_text())
        self.assertEqual(7,sum(e[0]=='switch2' for e in entries))
        self.assertEqual(7,sum(e[0]=='switch' for e in entries))
        self.assertEqual(382,len(entries))

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
