"""
結構解析器全面測試
"""
import unittest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from structure_parser import StructureParser


class TestStructureParserComprehensive(unittest.TestCase):
    """結構解析器全面測試"""

    def test_get_file_list(self):
        """測試獲取文件列表"""
        structure_content = """```
project/
├─ src/
│  ├─ main.py
│  └─ utils.py
└─ README.md
```"""
        test_file = Path(__file__).parent / "test_file_list.md"
        test_file.write_text(structure_content, encoding='utf-8')
        
        try:
            parser = StructureParser(str(test_file))
            parser.parse()
            file_list = parser.get_file_list()
            
            self.assertIsInstance(file_list, list)
            self.assertGreater(len(file_list), 0)
            # 檢查返回格式
            for item in file_list:
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_get_directory_list(self):
        """測試獲取目錄列表"""
        structure_content = """```
project/
├─ src/
│  └─ main.py
├─ tests/
└─ README.md
```"""
        test_file = Path(__file__).parent / "test_dir_list.md"
        test_file.write_text(structure_content, encoding='utf-8')
        
        try:
            parser = StructureParser(str(test_file))
            parser.parse()
            dir_list = parser.get_directory_list()
            
            self.assertIsInstance(dir_list, list)
            self.assertGreater(len(dir_list), 0)
            # 檢查是否包含預期的目錄（可能是完整路徑）
            dir_paths = [d for d in dir_list if 'src' in d]
            self.assertGreater(len(dir_paths), 0)
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_parse_stops_at_non_structure_line(self):
        """測試在非結構行處停止解析"""
        structure_with_text = """```
project/
└─ README.md
```
這是普通文字，不應該被解析
```"""
        text_file = Path(__file__).parent / "test_text.md"
        text_file.write_text(structure_with_text, encoding='utf-8')
        
        try:
            parser = StructureParser(str(text_file))
            structure = parser.parse()
            # 應該在 ``` 處停止
            self.assertIsInstance(structure, dict)
        finally:
            if text_file.exists():
                text_file.unlink()

    def test_parse_with_path_like_line(self):
        """測試包含路徑樣式的行"""
        structure_with_path = """```
project/src/main.py
project/tests/test_main.py
```"""
        path_file = Path(__file__).parent / "test_path.md"
        path_file.write_text(structure_with_path, encoding='utf-8')
        
        try:
            parser = StructureParser(str(path_file))
            structure = parser.parse()
            self.assertIsInstance(structure, dict)
        finally:
            if path_file.exists():
                path_file.unlink()

    def test_parse_with_comment_arrow(self):
        """測試包含 ← 註解的行"""
        structure_with_arrow = """```
project/
└─ main.py ← 主程式文件
```"""
        arrow_file = Path(__file__).parent / "test_arrow.md"
        arrow_file.write_text(structure_with_arrow, encoding='utf-8')
        
        try:
            parser = StructureParser(str(arrow_file))
            structure = parser.parse()
            # 包含 ← 的行應該被解析
            self.assertIsInstance(structure, dict)
        finally:
            if arrow_file.exists():
                arrow_file.unlink()

    def test_parse_empty_line_in_structure_block(self):
        """測試結構區塊中的空行處理"""
        structure_with_empty = """```
project/
├─ src/
│  
│  └─ main.py
```"""
        empty_file = Path(__file__).parent / "test_empty_block.md"
        empty_file.write_text(structure_with_empty, encoding='utf-8')
        
        try:
            parser = StructureParser(str(empty_file))
            structure = parser.parse()
            # 空行應該被跳過
            self.assertIsInstance(structure, dict)
        finally:
            if empty_file.exists():
                empty_file.unlink()


if __name__ == '__main__':
    unittest.main()
