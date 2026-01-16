"""
測試驗證指標計算
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics


class TestVerificationMetrics(unittest.TestCase):
    """測試驗證指標計算"""

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

    def test_calculate_all_metrics(self):
        """測試計算所有指標"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        metrics = metrics_calculator.calculate_all_metrics()

        self.assertIn('structure_coverage', metrics)
        self.assertIn('file_coverage', metrics)
        self.assertIn('directory_coverage', metrics)
        self.assertIn('template_accuracy', metrics)
        self.assertIn('hierarchy_accuracy', metrics)
        self.assertIn('annotation_preservation', metrics)
        self.assertIn('module_independence', metrics)

    def test_structure_coverage(self):
        """測試結構覆蓋率計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        coverage = metrics_calculator.calculate_structure_coverage()

        self.assertIn('expected_directories', coverage)
        self.assertIn('actual_directories', coverage)
        self.assertIn('expected_files', coverage)
        self.assertIn('actual_files', coverage)
        self.assertIn('overall_coverage', coverage)

    def test_file_coverage(self):
        """測試文件覆蓋率計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        coverage = metrics_calculator.calculate_file_coverage()

        self.assertIn('expected_count', coverage)
        self.assertIn('actual_count', coverage)
        self.assertIn('matched_count', coverage)
        self.assertIn('coverage_rate', coverage)

    def test_directory_coverage(self):
        """測試目錄覆蓋率計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        coverage = metrics_calculator.calculate_directory_coverage()

        self.assertIn('expected_count', coverage)
        self.assertIn('actual_count', coverage)
        self.assertIn('matched_count', coverage)
        self.assertIn('coverage_rate', coverage)


if __name__ == '__main__':
    unittest.main()
