"""
複雜的驗證指標測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics


class TestVerificationMetricsComplex(unittest.TestCase):
    """複雜的驗證指標測試"""

    def setUp(self):
        """設置測試環境 - 創建完整的 system/project1 結構"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"

        # 創建符合 system/project1 結構的文件
        structure_content = """```
system/
└─ project1/
   ├─ src/
   │  └─ main.py
   └─ README.md
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')

        # 創建生成的專案結構（符合 system/project1 格式）
        self.generated_dir.mkdir()
        system_dir = self.generated_dir / "system"
        system_dir.mkdir()
        project1_dir = system_dir / "project1"
        project1_dir.mkdir()
        (project1_dir / "src").mkdir()
        (project1_dir / "src" / "main.py").write_text("# main.py\n", encoding='utf-8')
        (project1_dir / "README.md").write_text("# README\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_count_actual_items_with_system_project1(self):
        """測試計算實際項目數量（system/project1 結構）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        items = metrics_calculator._count_actual_items()

        self.assertIn('directories', items)
        self.assertIn('files', items)
        self.assertGreaterEqual(items['directories'], 0)
        self.assertGreaterEqual(items['files'], 0)

    def test_get_expected_files_with_system_project1(self):
        """測試獲取預期文件列表（system/project1 結構）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        files = metrics_calculator._get_expected_files()

        self.assertIsInstance(files, list)
        # 應該包含 project1 內部的文件，但不包含 system 和 project1 本身

    def test_get_expected_directories_with_system_project1(self):
        """測試獲取預期目錄列表（system/project1 結構）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        directories = metrics_calculator._get_expected_directories()

        self.assertIsInstance(directories, list)
        # 應該包含 project1 內部的目錄

    def test_structure_coverage_with_system_project1(self):
        """測試結構覆蓋率計算（system/project1 結構）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        coverage = metrics_calculator.calculate_structure_coverage()

        self.assertIn('expected_directories', coverage)
        self.assertIn('actual_directories', coverage)
        self.assertIn('expected_files', coverage)
        self.assertIn('actual_files', coverage)
        self.assertIn('overall_coverage', coverage)


if __name__ == '__main__':
    unittest.main()
