"""
測試指標報告生成
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics
from generate_metrics import generate_report
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW


class TestGenerateMetrics(unittest.TestCase):
    """測試指標報告生成"""

    def setUp(self):
        """設置測試環境"""
        # 創建臨時目錄結構
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

    def test_generate_report_zh_tw(self):
        """測試生成繁體中文報告"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()

        # 計算總體分數
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

        output_file = self.temp_dir / "metrics_zh_tw.md"
        report = generate_report(metrics, str(output_file), LANG_ZH_TW)

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('專案', content)
        self.assertIn('指標', content)

    def test_generate_report_en(self):
        """測試生成英文報告"""
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

        output_file = self.temp_dir / "metrics_en.md"
        report = generate_report(metrics, str(output_file), LANG_EN)

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Metrics', content)
        self.assertIn('Report', content)

    def test_generate_report_zh_cn(self):
        """測試生成簡體中文報告"""
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

        output_file = self.temp_dir / "metrics_zh_cn.md"
        report = generate_report(metrics, str(output_file), LANG_ZH_CN)

        self.assertIsNotNone(report)
        self.assertTrue(output_file.exists())
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('项目', content)
        self.assertIn('指标', content)


if __name__ == '__main__':
    unittest.main()
