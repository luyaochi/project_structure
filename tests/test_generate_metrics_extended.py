"""
擴展的指標報告生成測試
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
from generate_metrics import generate_report, main
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW, DEFAULT_LANG


class TestGenerateMetricsExtended(unittest.TestCase):
    """擴展的指標報告生成測試"""

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

    def test_generate_report_without_output_file(self):
        """測試不指定輸出文件"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()

        overall_score = (
            metrics['structure_coverage']['overall_coverage'] * 0.3 +
            metrics['file_coverage']['coverage_rate'] * 0.2 +
            metrics['directory_coverage']['coverage_rate'] * 0.2 +
            metrics['template_accuracy']['accuracy_rate'] * 0.1 +
            metrics['hierarchy_accuracy']['overall_accuracy'] * 0.1 +
            metrics['annotation_preservation']['preservation_rate'] * 0.05 +
            metrics['module_independence']['independence_rate'] * 0.05
        ) * 100
        metrics['overall_score'] = overall_score

        # 不提供輸出文件，應該打印到標準輸出
        report = generate_report(metrics, None, LANG_ZH_TW)
        self.assertIsNotNone(report)
        self.assertIn('專案', report)

    def test_generate_report_with_missing_files(self):
        """測試包含缺失文件的報告"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()

        # 模擬缺失文件
        metrics['file_coverage']['missing_files'] = ['missing1.py', 'missing2.py']
        metrics['file_coverage']['extra_files'] = ['extra1.py']

        overall_score = (
            metrics['structure_coverage']['overall_coverage'] * 0.3 +
            metrics['file_coverage']['coverage_rate'] * 0.2 +
            metrics['directory_coverage']['coverage_rate'] * 0.2 +
            metrics['template_accuracy']['accuracy_rate'] * 0.1 +
            metrics['hierarchy_accuracy']['overall_accuracy'] * 0.1 +
            metrics['annotation_preservation']['preservation_rate'] * 0.05 +
            metrics['module_independence']['independence_rate'] * 0.05
        ) * 100
        metrics['overall_score'] = overall_score

        output_file = self.temp_dir / "metrics.md"
        report = generate_report(metrics, str(output_file), LANG_EN)

        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Missing', content)

    def test_generate_report_different_scores(self):
        """測試不同分數等級的報告"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()

        # 測試優秀分數 (>= 90)
        metrics['structure_coverage']['overall_coverage'] = 1.0
        metrics['file_coverage']['coverage_rate'] = 1.0
        metrics['directory_coverage']['coverage_rate'] = 1.0
        metrics['template_accuracy']['accuracy_rate'] = 1.0
        metrics['hierarchy_accuracy']['overall_accuracy'] = 1.0
        metrics['annotation_preservation']['preservation_rate'] = 1.0
        metrics['module_independence']['independence_rate'] = 1.0

        overall_score = (
            metrics['structure_coverage']['overall_coverage'] * 0.3 +
            metrics['file_coverage']['coverage_rate'] * 0.2 +
            metrics['directory_coverage']['coverage_rate'] * 0.2 +
            metrics['template_accuracy']['accuracy_rate'] * 0.1 +
            metrics['hierarchy_accuracy']['overall_accuracy'] * 0.1 +
            metrics['annotation_preservation']['preservation_rate'] * 0.05 +
            metrics['module_independence']['independence_rate'] * 0.05
        ) * 100
        metrics['overall_score'] = overall_score

        output_file = self.temp_dir / "metrics_excellent.md"
        report = generate_report(metrics, str(output_file), LANG_EN)

        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Excellent', content)

    def test_main_function_json_output(self):
        """測試 main 函數的 JSON 輸出"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--json',
            '--output', str(self.temp_dir / "metrics.json")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                json_file = self.temp_dir / "metrics.json"
                self.assertTrue(json_file.exists())
                import json
                data = json.loads(json_file.read_text(encoding='utf-8'))
                self.assertIn('overall_score', data)
            except SystemExit:
                pass

    def test_main_function_all_langs(self):
        """測試 main 函數生成所有語言版本"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--all-langs',
            '--output', str(self.temp_dir / "METRICS.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                # 檢查是否生成了所有語言版本
                self.assertTrue((self.temp_dir / "METRICS.md").exists())
                self.assertTrue((self.temp_dir / "METRICS.zh-CN.md").exists())
                self.assertTrue((self.temp_dir / "METRICS.en.md").exists())
            except SystemExit:
                pass

    def test_main_function_single_lang(self):
        """測試 main 函數生成單一語言版本"""
        import sys

        test_args = [
            'generate_metrics.py',
            '--structure', str(self.structure_file),
            '--generated', str(self.generated_dir / "project"),
            '--lang', 'zh-CN',
            '--output', str(self.temp_dir / "METRICS.md")
        ]

        with patch.object(sys, 'argv', test_args):
            try:
                main()
                self.assertTrue((self.temp_dir / "METRICS.zh-CN.md").exists())
            except SystemExit:
                pass


if __name__ == '__main__':
    unittest.main()
