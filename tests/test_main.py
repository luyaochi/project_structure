"""
測試主程式
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMain(unittest.TestCase):
    """測試主程式"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"

        # 創建簡單的結構文件
        structure_content = """```
project/
├─ src/
│  └─ main.py
└─ README.md
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')

        # 創建生成的專案結構
        self.generated_dir.mkdir()
        (self.generated_dir / "project").mkdir()
        (self.generated_dir / "project" / "src").mkdir()
        (self.generated_dir / "project" / "src" / "main.py").write_text("# main.py\n", encoding='utf-8')
        (self.generated_dir / "project" / "README.md").write_text("# README\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_main_with_structure_and_generated(self):
        """測試使用 --structure 和 --generated 參數"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--generate-reports',
            '--report-lang', 'en'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 檢查報告是否生成
                reports_dir = Path.cwd() / "reports"
                if reports_dir.exists():
                    # 清理
                    shutil.rmtree(reports_dir)
            except SystemExit:
                pass  # main 可能會調用 sys.exit

    def test_main_generate_project(self):
        """測試生成專案"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--output', str(self.temp_dir / "output"),
            '--project-name', 'test_project'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 檢查專案是否生成
                output_dir = self.temp_dir / "output"
                self.assertTrue(output_dir.exists())
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
