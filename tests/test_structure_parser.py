"""
測試結構解析器
"""
import unittest
from pathlib import Path
import sys
import os

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParser(unittest.TestCase):
    """測試結構解析器"""

    def setUp(self):
        """設置測試環境"""
        self.test_structure = """```
system/
├─ project1/
│  ├─ core/
│  │  ├─ src/
│  │  │  ├─ core/
│  │  │  │  └─ __init__.py
│  │  │  └─ domain/
│  │  │     └─ __init__.py
│  │  └─ pyproject.toml ← Python 專案配置
│  └─ README.md
└─ README.md
```"""
        self.test_file = Path(__file__).parent / "test_structure.md"
        self.test_file.write_text(self.test_structure, encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.test_file.exists():
            self.test_file.unlink()

    def test_parse_simple_structure(self):
        """測試解析簡單結構"""
        parser = StructureParser(str(self.test_file))
        structure = parser.parse()

        self.assertIsNotNone(structure)
        self.assertIn('system', structure)
        self.assertIn('project1', structure['system']['children'])

    def test_parse_with_comments(self):
        """測試解析帶註解的結構"""
        parser = StructureParser(str(self.test_file))
        structure = parser.parse()

        # 檢查註解是否被保留
        project1 = structure['system']['children']['project1']
        core = project1['children']['core']
        pyproject = core['children']['pyproject.toml']

        self.assertIn('comment', pyproject)
        self.assertIn('Python 專案配置', pyproject['comment'])

    def test_calculate_level(self):
        """測試層級計算"""
        parser = StructureParser(str(self.test_file))

        # 測試不同層級的計算
        self.assertEqual(parser._calculate_level("system/"), 0)
        self.assertEqual(parser._calculate_level("├─ project1/"), 1)
        self.assertEqual(parser._calculate_level("│  ├─ core/"), 2)

    def test_parse_empty_file(self):
        """測試解析空文件"""
        empty_file = Path(__file__).parent / "empty_structure.md"
        empty_file.write_text("", encoding='utf-8')

        try:
            parser = StructureParser(str(empty_file))
            structure = parser.parse()
            self.assertEqual(structure, {})
        finally:
            if empty_file.exists():
                empty_file.unlink()

    def test_parse_invalid_structure(self):
        """測試解析無效結構"""
        invalid_file = Path(__file__).parent / "invalid_structure.md"
        invalid_file.write_text("這不是有效的結構", encoding='utf-8')

        try:
            parser = StructureParser(str(invalid_file))
            structure = parser.parse()
            # 應該返回空字典或處理錯誤
            self.assertIsInstance(structure, dict)
        finally:
            if invalid_file.exists():
                invalid_file.unlink()


if __name__ == '__main__':
    unittest.main()
