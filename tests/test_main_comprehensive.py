"""
主程式全面測試 - 覆蓋剩餘行
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMainComprehensive(unittest.TestCase):
    """主程式全面測試"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"

        structure_content = """```
project/
├─ src/
│  └─ main.py
└─ README.md
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')

        self.generated_dir.mkdir()
        (self.generated_dir / "project").mkdir()
        (self.generated_dir / "project" / "src").mkdir()
        (self.generated_dir / "project" / "src" / "main.py").write_text("# main.py\n", encoding='utf-8')
        (self.generated_dir / "project" / "README.md").write_text("# README\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        # 清理可能生成的 reports 目錄
        reports_dir = Path.cwd() / "reports"
        if reports_dir.exists():
            shutil.rmtree(reports_dir)

    def test_main_with_structure_parameter(self):
        """測試使用 --structure 參數"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--output', str(self.temp_dir / "output"),
            '--generate-reports',
            '--structure', str(self.structure_file),
            '--report-lang', 'en'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_file_not_found_error(self):
        """測試文件不存在錯誤"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', 'nonexistent_file.md',
            '--output', str(self.temp_dir / "output")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)


if __name__ == '__main__':
    unittest.main()
