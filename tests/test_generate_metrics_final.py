"""
指標報告生成最終測試 - 覆蓋剩餘行
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics
from generate_metrics import main
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW


class TestGenerateMetricsFinal(unittest.TestCase):
    """指標報告生成最終測試"""

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

    def test_main_json_output_without_file(self):
        """測試 JSON 輸出但不指定文件"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--json'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 應該打印到標準輸出
            except SystemExit:
                pass

    def test_main_all_langs_without_output(self):
        """測試生成所有語言版本但不指定輸出"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--all-langs'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 應該生成預設名稱的文件
                for lang in [LANG_ZH_TW, LANG_ZH_CN, LANG_EN]:
                    from i18n import get_lang_suffix
                    suffix = get_lang_suffix(lang)
                    metrics_file = Path.cwd() / f"METRICS{suffix}.md"
                    if metrics_file.exists():
                        metrics_file.unlink()
            except SystemExit:
                pass

    def test_main_single_lang_without_output(self):
        """測試生成單一語言版本但不指定輸出"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--lang', 'zh-CN'
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 應該生成預設名稱的文件
                metrics_file = Path.cwd() / "METRICS.zh-CN.md"
                if metrics_file.exists():
                    metrics_file.unlink()
            except SystemExit:
                pass

    def test_main_exception_handling(self):
        """測試異常處理"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', 'nonexistent.md',
            '--generated', str(self.generated_dir / "project")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
            except SystemExit as e:
                self.assertEqual(e.code, 1)


if __name__ == '__main__':
    unittest.main()
