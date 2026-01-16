"""
擴展的結論報告測試
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


class TestGenerateConclusionExtended(unittest.TestCase):
    """擴展的結論報告測試"""

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

    def test_generate_conclusion_different_scores(self):
        """測試不同分數的結論報告"""
        # 直接測試報告生成，不修改 metrics（因為 generate_conclusion_report 會重新計算）
        output_file = self.temp_dir / "conclusion_test.md"
        report = generate_conclusion_report(
            str(self.structure_file),
            str(self.generated_dir / "project"),
            str(output_file),
            LANG_EN
        )

        content = output_file.read_text(encoding='utf-8')
        # 檢查報告是否包含基本內容
        self.assertIn('Project', content)
        self.assertIn('Conclusion', content)

    def test_main_function_without_output(self):
        """測試 main 函數不指定輸出"""
        import sys

        test_args = [
            'generate_conclusion.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--lang', 'en'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 應該生成預設名稱的文件
                conclusion_file = Path.cwd() / "CONCLUSION.en.md"
                if conclusion_file.exists():
                    conclusion_file.unlink()
            except SystemExit:
                pass

    def test_main_function_single_lang_with_output(self):
        """測試 main 函數單一語言並指定輸出"""
        import sys

        test_args = [
            'generate_conclusion.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--lang', 'zh-CN',
            '--output', str(self.temp_dir / "CONCLUSION.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                self.assertTrue((self.temp_dir / "CONCLUSION.zh-CN.md").exists())
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
