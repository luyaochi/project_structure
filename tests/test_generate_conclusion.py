"""
測試結論報告生成
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generate_conclusion import generate_conclusion_report, main
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW


class TestGenerateConclusion(unittest.TestCase):
    """測試結論報告生成"""

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

    def test_generate_conclusion_report_zh_tw(self):
        """測試生成繁體中文結論報告"""
        output_file = self.temp_dir / "conclusion.md"
        report = generate_conclusion_report(
            str(self.structure_file),
            str(self.generated_dir / "project"),
            str(output_file),
            LANG_ZH_TW
        )

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('專案', content)

    def test_generate_conclusion_report_en(self):
        """測試生成英文結論報告"""
        output_file = self.temp_dir / "conclusion_en.md"
        report = generate_conclusion_report(
            str(self.structure_file),
            str(self.generated_dir / "project"),
            str(output_file),
            LANG_EN
        )

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Project', content)

    def test_generate_conclusion_report_zh_cn(self):
        """測試生成簡體中文結論報告"""
        output_file = self.temp_dir / "conclusion_zh_cn.md"
        report = generate_conclusion_report(
            str(self.structure_file),
            str(self.generated_dir / "project"),
            str(output_file),
            LANG_ZH_CN
        )

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('项目', content)

    def test_main_function_all_langs(self):
        """測試 main 函數生成所有語言版本"""
        import sys

        test_args = [
            'generate_conclusion.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--all-langs',
            '--output', str(self.temp_dir / "CONCLUSION.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 檢查是否生成了所有語言版本
                self.assertTrue((self.temp_dir / "CONCLUSION.md").exists())
                self.assertTrue((self.temp_dir / "CONCLUSION.zh-CN.md").exists())
                self.assertTrue((self.temp_dir / "CONCLUSION.en.md").exists())
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
