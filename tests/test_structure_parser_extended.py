"""
擴展的結構解析器測試
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParserExtended(unittest.TestCase):
    """擴展的結構解析器測試"""

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

    def test_parse_file_not_found(self):
        """測試文件不存在的情況"""
        parser = StructureParser("nonexistent_file.md")
        with self.assertRaises(FileNotFoundError):
            parser.parse()

    def test_parse_with_complex_structure(self):
        """測試解析複雜結構"""
        complex_structure = """```
project/
├─ src/
│  ├─ main.py
│  ├─ utils.py
│  └─ config/
│     └─ settings.py
├─ tests/
│  └─ test_main.py
├─ docs/
│  └─ README.md
└─ README.md
```"""
        complex_file = Path(__file__).parent / "complex_structure.md"
        complex_file.write_text(complex_structure, encoding='utf-8')

        try:
            parser = StructureParser(str(complex_file))
            structure = parser.parse()

            self.assertIsNotNone(structure)
            self.assertIn('project', structure)
            self.assertIn('src', structure['project']['children'])
            self.assertIn('tests', structure['project']['children'])
        finally:
            if complex_file.exists():
                complex_file.unlink()

    def test_parse_with_multiple_comments(self):
        """測試解析多個註解"""
        structure_with_comments = """```
project/
├─ src/
│  └─ main.py ← 主程式
├─ config.py ← 配置檔案
└─ README.md ← 說明文件
```"""
        comments_file = Path(__file__).parent / "comments_structure.md"
        comments_file.write_text(structure_with_comments, encoding='utf-8')

        try:
            parser = StructureParser(str(comments_file))
            structure = parser.parse()

            self.assertIsNotNone(structure)
            project = structure['project']
            main_py = project['children']['src']['children']['main.py']
            self.assertIn('comment', main_py)
            self.assertIn('主程式', main_py['comment'])
        finally:
            if comments_file.exists():
                comments_file.unlink()

    def test_calculate_level_edge_cases(self):
        """測試層級計算的邊界情況"""
        parser = StructureParser(str(self.test_file))

        # 測試不同格式的行
        self.assertEqual(parser._calculate_level("system/"), 0)
        self.assertEqual(parser._calculate_level("  system/"), 0)  # 2個空格
        self.assertEqual(parser._calculate_level("    system/"), 1)  # 4個空格
        self.assertEqual(parser._calculate_level("├─ project/"), 1)
        self.assertEqual(parser._calculate_level("│  ├─ src/"), 2)

    def test_parse_name_and_comment(self):
        """測試解析名稱和註解"""
        parser = StructureParser(str(self.test_file))

        # 測試不同格式
        name, comment = parser._extract_name_and_comment("main.py ← 主程式")
        self.assertEqual(name, "main.py")
        self.assertEqual(comment, "主程式")

        name, comment = parser._extract_name_and_comment("README.md")
        self.assertEqual(name, "README.md")
        self.assertIsNone(comment)

        # 注意：_extract_name_and_comment 只會提取第一個 ← 後面的內容
        name, comment = parser._extract_name_and_comment("config.py ← 配置檔案")
        self.assertEqual(name, "config.py")
        self.assertEqual(comment, "配置檔案")

    def test_is_directory(self):
        """測試目錄判斷"""
        parser = StructureParser(str(self.test_file))

        # 測試文件
        self.assertFalse(parser._is_directory("main.py"))
        self.assertFalse(parser._is_directory("README.md"))
        self.assertFalse(parser._is_directory("config.toml"))
        self.assertFalse(parser._is_directory("package.json"))

        # 測試目錄
        self.assertTrue(parser._is_directory("src"))
        self.assertTrue(parser._is_directory("tests"))
        self.assertTrue(parser._is_directory("docs"))


if __name__ == '__main__':
    unittest.main()
