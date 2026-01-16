"""
測試多語言模組
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from i18n import get_text, get_lang_suffix, LANG_EN, LANG_ZH_CN, LANG_ZH_TW, DEFAULT_LANG


class TestI18n(unittest.TestCase):
    """測試多語言模組"""

    def test_get_text_default(self):
        """測試預設語言（繁體中文）"""
        text = get_text('metrics_title')
        self.assertIsInstance(text, str)
        self.assertIn('專案', text or '指標')

    def test_get_text_english(self):
        """測試英文"""
        text = get_text('metrics_title', LANG_EN)
        self.assertIsInstance(text, str)
        self.assertIn('Metrics', text or 'Report')

    def test_get_text_simplified_chinese(self):
        """測試簡體中文"""
        text = get_text('metrics_title', LANG_ZH_CN)
        self.assertIsInstance(text, str)
        self.assertIn('项目', text or '指标')

    def test_get_text_traditional_chinese(self):
        """測試繁體中文"""
        text = get_text('metrics_title', LANG_ZH_TW)
        self.assertIsInstance(text, str)
        self.assertIn('專案', text or '指標')

    def test_get_lang_suffix(self):
        """測試語言後綴"""
        self.assertEqual(get_lang_suffix(LANG_ZH_TW), '')
        self.assertEqual(get_lang_suffix(LANG_ZH_CN), '.zh-CN')
        self.assertEqual(get_lang_suffix(LANG_EN), '.en')

    def test_get_text_missing_key(self):
        """測試缺失的鍵"""
        text = get_text('nonexistent_key')
        # 應該返回鍵本身
        self.assertEqual(text, 'nonexistent_key')

    def test_all_languages_have_same_keys(self):
        """測試所有語言都有相同的鍵"""
        # 獲取英文的所有鍵
        from i18n import TRANSLATIONS
        en_keys = set(TRANSLATIONS[LANG_EN].keys())
        zh_cn_keys = set(TRANSLATIONS[LANG_ZH_CN].keys())
        zh_tw_keys = set(TRANSLATIONS[LANG_ZH_TW].keys())

        self.assertEqual(en_keys, zh_cn_keys, "英文和簡體中文的鍵不一致")
        self.assertEqual(en_keys, zh_tw_keys, "英文和繁體中文的鍵不一致")


if __name__ == '__main__':
    unittest.main()
