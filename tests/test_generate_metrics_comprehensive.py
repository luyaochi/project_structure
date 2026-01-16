"""
指標報告生成全面測試
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
from generate_metrics import generate_report
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW


class TestGenerateMetricsComprehensive(unittest.TestCase):
    """指標報告生成全面測試"""

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

    def test_generate_report_with_many_missing_files(self):
        """測試包含大量缺失文件的報告"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()
        
        # 模擬大量缺失文件（超過10個）
        metrics['file_coverage']['missing_files'] = [f'missing{i}.py' for i in range(15)]
        metrics['file_coverage']['extra_files'] = [f'extra{i}.py' for i in range(15)]
        
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
        
        content = output_file.read_text(encoding='utf-8')
        # 應該顯示 "... 還有 X 個"
        self.assertIn('more', content)

    def test_generate_report_score_ranges(self):
        """測試不同分數範圍的報告"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        base_metrics = metrics_calculator.calculate_all_metrics()
        
        # 測試良好分數 (80-89)
        metrics = base_metrics.copy()
        metrics['structure_coverage']['overall_coverage'] = 0.85
        metrics['file_coverage']['coverage_rate'] = 0.85
        metrics['directory_coverage']['coverage_rate'] = 0.85
        metrics['template_accuracy']['accuracy_rate'] = 0.75
        metrics['hierarchy_accuracy']['overall_accuracy'] = 0.75
        metrics['annotation_preservation']['preservation_rate'] = 0.75
        metrics['module_independence']['independence_rate'] = 0.75
        
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
        
        output_file = self.temp_dir / "metrics_good.md"
        report = generate_report(metrics, str(output_file), LANG_EN)
        
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Good', content)
        
        # 測試及格分數 (70-79)
        metrics = base_metrics.copy()
        metrics['structure_coverage']['overall_coverage'] = 0.75
        metrics['file_coverage']['coverage_rate'] = 0.75
        metrics['directory_coverage']['coverage_rate'] = 0.75
        metrics['template_accuracy']['accuracy_rate'] = 0.65
        metrics['hierarchy_accuracy']['overall_accuracy'] = 0.65
        metrics['annotation_preservation']['preservation_rate'] = 0.65
        metrics['module_independence']['independence_rate'] = 0.65
        
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
        
        output_file = self.temp_dir / "metrics_pass.md"
        report = generate_report(metrics, str(output_file), LANG_EN)
        
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Pass', content)
        
        # 測試不及格分數 (< 70)
        metrics = base_metrics.copy()
        metrics['structure_coverage']['overall_coverage'] = 0.5
        metrics['file_coverage']['coverage_rate'] = 0.5
        metrics['directory_coverage']['coverage_rate'] = 0.5
        metrics['template_accuracy']['accuracy_rate'] = 0.5
        metrics['hierarchy_accuracy']['overall_accuracy'] = 0.5
        metrics['annotation_preservation']['preservation_rate'] = 0.5
        metrics['module_independence']['independence_rate'] = 0.5
        
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
        
        output_file = self.temp_dir / "metrics_fail.md"
        report = generate_report(metrics, str(output_file), LANG_EN)
        
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('Fail', content)


if __name__ == '__main__':
    unittest.main()
