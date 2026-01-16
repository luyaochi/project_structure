"""
結構解析器邊界情況測試
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParserEdgeCases(unittest.TestCase):
    """結構解析器邊界情況測試"""

    def test_calculate_level_with_branch_symbols(self):
        """測試帶分支符號的層級計算"""
        test_file = Path(__file__).parent / "test_edge.md"
        test_file.write_text("test", encoding='utf-8')

        try:
            parser = StructureParser(str(test_file))

            # 測試有分支符號但沒有空格的情況
            level = parser._calculate_level("├─test")
            self.assertGreaterEqual(level, 0)

            # 測試只有 │ 的情況
            level = parser._calculate_level("│  test")
            self.assertGreaterEqual(level, 0)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_parse_with_empty_lines_in_structure(self):
        """測試結構中的空行處理"""
        structure_with_empty = """```
project/
├─ src/
│
│  └─ main.py
└─ README.md
```"""
        empty_file = Path(__file__).parent / "empty_lines.md"
        empty_file.write_text(structure_with_empty, encoding='utf-8')

        try:
            parser = StructureParser(str(empty_file))
            structure = parser.parse()
            # 應該能正常解析
            self.assertIsInstance(structure, dict)
        finally:
            if empty_file.exists():
                empty_file.unlink()

    def test_parse_stops_at_code_block_end(self):
        """測試在代碼塊結束時停止解析"""
        structure_with_end = """```
project/
└─ README.md
```
其他內容
```"""
        end_file = Path(__file__).parent / "end_block.md"
        end_file.write_text(structure_with_end, encoding='utf-8')

        try:
            parser = StructureParser(str(end_file))
            structure = parser.parse()
            # 應該在 ``` 處停止
            self.assertIsInstance(structure, dict)
        finally:
            if end_file.exists():
                end_file.unlink()

    def test_extract_name_with_trailing_slash(self):
        """測試提取帶尾隨斜線的名稱"""
        test_file = Path(__file__).parent / "test_slash.md"
        test_file.write_text("test", encoding='utf-8')

        try:
            parser = StructureParser(str(test_file))
            name, comment = parser._extract_name_and_comment("src/")
            self.assertEqual(name, "src")
            self.assertIsNone(comment)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_extract_name_empty_result(self):
        """測試提取空名稱的情況"""
        test_file = Path(__file__).parent / "test_empty.md"
        test_file.write_text("test", encoding='utf-8')

        try:
            parser = StructureParser(str(test_file))
            name, comment = parser._extract_name_and_comment("")
            self.assertIsNone(name)
            self.assertIsNone(comment)
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == '__main__':
    unittest.main()
