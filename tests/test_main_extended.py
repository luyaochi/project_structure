"""
擴展的主程式測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestMainExtended(unittest.TestCase):
    """擴展的主程式測試"""

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
        # 清理可能生成的 reports 目錄
        reports_dir = Path.cwd() / "reports"
        if reports_dir.exists():
            shutil.rmtree(reports_dir)

    def test_main_dry_run(self):
        """測試乾跑模式"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--dry-run'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_generate_with_reports_all_langs(self):
        """測試生成專案並生成所有語言報告"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--output', str(self.temp_dir / "output"),
            '--project-name', 'test_project',
            '--generate-reports',
            '--all-langs'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_generate_with_reports_single_lang(self):
        """測試生成專案並生成單一語言報告"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--output', str(self.temp_dir / "output"),
            '--project-name', 'test_project',
            '--generate-reports',
            '--report-lang', 'zh-CN'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_generate_with_custom_report_output(self):
        """測試生成專案並指定報告輸出目錄"""
        from main import main
        import sys

        custom_report_dir = self.temp_dir / "custom_reports"
        test_args = [
            'main.py',
            '--readme', str(self.structure_file),
            '--output', str(self.temp_dir / "output"),
            '--project-name', 'test_project',
            '--generate-reports',
            '--report-output', str(custom_report_dir)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_with_structure_and_generated_all_langs(self):
        """測試直接生成所有語言報告"""
        from main import main
        import sys

        test_args = [
            'main.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--generate-reports',
            '--all-langs'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_with_structure_and_generated_custom_output(self):
        """測試直接生成報告到自定義目錄"""
        from main import main
        import sys

        custom_report_dir = self.temp_dir / "custom_reports"
        test_args = [
            'main.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--generate-reports',
            '--report-output', str(custom_report_dir)
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit:
                pass

    def test_main_invalid_structure(self):
        """測試無效結構文件"""
        from main import main
        import sys

        invalid_file = self.temp_dir / "invalid.md"
        invalid_file.write_text("無效內容", encoding='utf-8')

        test_args = [
            'main.py',
            '--readme', str(invalid_file),
            '--output', str(self.temp_dir / "output")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)


if __name__ == '__main__':
    unittest.main()
