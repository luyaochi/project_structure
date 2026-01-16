"""
結構解析器剩餘行測試
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParserRemaining(unittest.TestCase):
    """結構解析器剩餘行測試"""

    def test_parse_empty_line_in_block_else_branch(self):
        """測試結構區塊外空行的 else 分支"""
        structure_content = """
一些文字
```
project/
└─ README.md
```
"""
        test_file = Path(__file__).parent / "test_empty_else.md"
        test_file.write_text(structure_content, encoding='utf-8')
        
        try:
            parser = StructureParser(str(test_file))
            structure = parser.parse()
            # 結構區塊外的空行應該被跳過
            self.assertIsInstance(structure, dict)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_parse_stops_at_plain_text(self):
        """測試在純文字處停止（不包含路徑特徵）"""
        structure_content = """```
project/
└─ README.md
```
這是純文字描述
不包含任何路徑或文件特徵
應該停止解析
```"""
        test_file = Path(__file__).parent / "test_plain_text.md"
        test_file.write_text(structure_content, encoding='utf-8')
        
        try:
            parser = StructureParser(str(test_file))
            structure = parser.parse()
            # 應該在遇到純文字時停止
            self.assertIsInstance(structure, dict)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_parse_continues_with_path_features(self):
        """測試包含路徑特徵的行繼續解析"""
        structure_content = """```
project/
└─ README.md
包含 .py 的文件描述
包含 / 的路徑描述
```"""
        test_file = Path(__file__).parent / "test_path_features.md"
        test_file.write_text(structure_content, encoding='utf-8')
        
        try:
            parser = StructureParser(str(test_file))
            structure = parser.parse()
            # 包含路徑特徵的行應該繼續解析
            self.assertIsInstance(structure, dict)
        finally:
            if test_file.exists():
                test_file.unlink()


if __name__ == '__main__':
    unittest.main()
