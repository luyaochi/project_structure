"""
擴展的驗證指標測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics


class TestVerificationMetricsExtended(unittest.TestCase):
    """擴展的驗證指標測試"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"

        # 創建更複雜的結構文件
        structure_content = """```
project/
├─ src/
│  ├─ main.py
│  └─ utils.py
├─ tests/
│  └─ test_main.py
└─ README.md
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')

        # 創建生成的專案結構
        self.generated_dir.mkdir()
        project_dir = self.generated_dir / "project"
        project_dir.mkdir()
        (project_dir / "src").mkdir()
        (project_dir / "tests").mkdir()
        (project_dir / "src" / "main.py").write_text("# main.py\n", encoding='utf-8')
        (project_dir / "src" / "utils.py").write_text("# utils.py\n", encoding='utf-8')
        (project_dir / "tests" / "test_main.py").write_text("# test_main.py\n", encoding='utf-8')
        (project_dir / "README.md").write_text("# README\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_template_accuracy(self):
        """測試模板準確性計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        accuracy = metrics_calculator.calculate_template_accuracy()

        self.assertIn('total_checks', accuracy)
        self.assertIn('passed_checks', accuracy)
        self.assertIn('accuracy_rate', accuracy)

    def test_hierarchy_accuracy(self):
        """測試層級準確性計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        accuracy = metrics_calculator.calculate_hierarchy_accuracy()

        self.assertIn('project_level', accuracy)
        self.assertIn('module_level', accuracy)
        self.assertIn('feature_level', accuracy)
        self.assertIn('overall_accuracy', accuracy)

    def test_annotation_preservation(self):
        """測試註解保留率計算"""
        # 創建帶註解的結構
        structure_with_annotations = """```
project/
├─ src/
│  └─ main.py ← 主程式
└─ README.md ← 說明文件
```"""
        annotated_file = self.temp_dir / "annotated_structure.md"
        annotated_file.write_text(structure_with_annotations, encoding='utf-8')

        # 創建帶註解的生成專案
        annotated_project = self.temp_dir / "annotated_project"
        annotated_project.mkdir()
        (annotated_project / "src").mkdir()
        (annotated_project / "src" / "main.py").write_text("# main.py\n# 主程式\n", encoding='utf-8')
        (annotated_project / "README.md").write_text("# README\n# 說明文件\n", encoding='utf-8')

        metrics_calculator = VerificationMetrics(str(annotated_file), str(annotated_project))
        preservation = metrics_calculator.calculate_annotation_preservation()

        self.assertIn('expected_count', preservation)
        self.assertIn('preserved_count', preservation)
        self.assertIn('preservation_rate', preservation)

    def test_module_independence(self):
        """測試模組獨立性計算"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir / "project"))
        independence = metrics_calculator.calculate_module_independence()

        self.assertIn('total_checks', independence)
        self.assertIn('passed_checks', independence)
        self.assertIn('independence_rate', independence)


if __name__ == '__main__':
    unittest.main()
