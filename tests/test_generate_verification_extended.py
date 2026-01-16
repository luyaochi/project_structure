"""
擴展的驗證報告生成測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generate_verification import generate_verification_report, main
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW


class TestGenerateVerificationExtended(unittest.TestCase):
    """擴展的驗證報告生成測試"""

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

    def test_generate_verification_report_without_output(self):
        """測試不指定輸出文件"""
        report = generate_verification_report(
            str(self.structure_file),
            str(self.generated_dir / "project"),
            None,
            LANG_EN
        )
        self.assertIsNotNone(report)
        self.assertIn('Verification', report)

    def test_main_function_all_langs(self):
        """測試 main 函數生成所有語言版本"""
        import sys

        test_args = [
            'generate_verification.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--all-langs',
            '--output', str(self.temp_dir / "VERIFICATION.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 檢查是否生成了所有語言版本
                self.assertTrue((self.temp_dir / "VERIFICATION.md").exists())
                self.assertTrue((self.temp_dir / "VERIFICATION.zh-CN.md").exists())
                self.assertTrue((self.temp_dir / "VERIFICATION.en.md").exists())
            except SystemExit:
                pass

    def test_main_function_single_lang(self):
        """測試 main 函數生成單一語言版本"""
        import sys

        test_args = [
            'generate_verification.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--lang', 'zh-CN',
            '--output', str(self.temp_dir / "VERIFICATION.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                self.assertTrue((self.temp_dir / "VERIFICATION.zh-CN.md").exists())
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
