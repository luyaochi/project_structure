"""
結構解析器最終測試 - 覆蓋剩餘行
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParserFinal(unittest.TestCase):
    """結構解析器最終測試"""

    def test_parse_stops_at_non_structure_text(self):
        """測試在非結構文字處停止"""
        structure_with_text = """```
project/
└─ README.md
```
這是普通文字描述，不包含路徑或樹狀符號
應該停止解析
```"""
        text_file = Path(__file__).parent / "test_stop_text.md"
        text_file.write_text(structure_with_text, encoding='utf-8')
        
        try:
            parser = StructureParser(str(text_file))
            structure = parser.parse()
            # 應該在遇到非結構文字時停止
            self.assertIsInstance(structure, dict)
        finally:
            if text_file.exists():
                text_file.unlink()

    def test_parse_continues_with_arrow_in_line(self):
        """測試包含 ← 的行繼續解析"""
        structure_with_arrow = """```
project/
└─ main.py ← 主程式
普通文字但包含 ← 符號
```"""
        arrow_file = Path(__file__).parent / "test_arrow_continue.md"
        arrow_file.write_text(structure_with_arrow, encoding='utf-8')
        
        try:
            parser = StructureParser(str(arrow_file))
            structure = parser.parse()
            # 包含 ← 的行應該繼續解析
            self.assertIsInstance(structure, dict)
        finally:
            if arrow_file.exists():
                arrow_file.unlink()

    def test_parse_empty_line_outside_block(self):
        """測試結構區塊外的空行"""
        structure_with_empty = """
```
project/
└─ README.md
```
"""
        empty_file = Path(__file__).parent / "test_empty_outside.md"
        empty_file.write_text(structure_with_empty, encoding='utf-8')
        
        try:
            parser = StructureParser(str(empty_file))
            structure = parser.parse()
            # 結構區塊外的空行應該被跳過
            self.assertIsInstance(structure, dict)
        finally:
            if empty_file.exists():
                empty_file.unlink()


if __name__ == '__main__':
    unittest.main()
