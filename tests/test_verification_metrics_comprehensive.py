"""
驗證指標全面測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics


class TestVerificationMetricsComprehensive(unittest.TestCase):
    """驗證指標全面測試"""

    def setUp(self):
        """設置測試環境 - 創建完整的 system/project1 結構"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"
        
        # 創建符合 system/project1 結構的文件，包含註解
        structure_content = """```
system/
└─ project1/
   ├─ core/
   │  ├─ src/
   │  │  └─ main.py ← 主程式
   │  └─ pyproject.toml
   └─ README.md ← 說明文件
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')
        
        # 創建生成的專案結構（符合 system/project1 格式）
        self.generated_dir.mkdir()
        system_dir = self.generated_dir / "system"
        system_dir.mkdir()
        project1_dir = system_dir / "project1"
        project1_dir.mkdir()
        core_dir = project1_dir / "core"
        core_dir.mkdir()
        src_dir = core_dir / "src"
        src_dir.mkdir()
        
        # 創建文件，包含註解
        (src_dir / "main.py").write_text("# main.py\n# 主程式\n", encoding='utf-8')
        (core_dir / "pyproject.toml").write_text(
            "[build-system]\nrequires = [\"setuptools\"]\n\n[project]\nname = \"core\"\n",
            encoding='utf-8'
        )
        (project1_dir / "README.md").write_text("# README\n# 說明文件\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_get_actual_files(self):
        """測試獲取實際文件列表"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        files = metrics_calculator._get_actual_files()
        
        self.assertIsInstance(files, list)
        # 應該包含生成的文件
        self.assertGreater(len(files), 0)
        # 檢查路徑格式（應該是正斜線）
        for file_path in files:
            self.assertNotIn('\\', file_path)

    def test_get_actual_directories(self):
        """測試獲取實際目錄列表"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        directories = metrics_calculator._get_actual_directories()
        
        self.assertIsInstance(directories, list)
        # 應該包含生成的目錄
        self.assertGreater(len(directories), 0)

    def test_check_pyproject_toml(self):
        """測試檢查 pyproject.toml 文件"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        result = metrics_calculator._check_pyproject_toml()
        
        self.assertIn('checks', result)
        self.assertIsInstance(result['checks'], list)
        # 應該有檢查結果
        if result['checks']:
            check = result['checks'][0]
            self.assertIn('file', check)
            self.assertIn('passed', check)

    def test_check_package_json(self):
        """測試檢查 package.json 文件"""
        # 創建包含 package.json 的結構
        structure_with_package = """```
system/
└─ project1/
   ├─ frontend/
   │  └─ package.json
   └─ README.md
```"""
        package_structure = self.temp_dir / "package_structure.md"
        package_structure.write_text(structure_with_package, encoding='utf-8')
        
        # 創建包含 package.json 的專案
        package_project = self.temp_dir / "package_project"
        package_project.mkdir()
        system_dir = package_project / "system"
        system_dir.mkdir()
        project1_dir = system_dir / "project1"
        project1_dir.mkdir()
        frontend_dir = project1_dir / "frontend"
        frontend_dir.mkdir()
        (frontend_dir / "package.json").write_text(
            '{\n  "name": "frontend",\n  "version": "1.0.0"\n}',
            encoding='utf-8'
        )
        
        metrics_calculator = VerificationMetrics(str(package_structure), str(package_project))
        result = metrics_calculator._check_package_json()
        
        self.assertIn('checks', result)
        self.assertIsInstance(result['checks'], list)

    def test_annotation_preservation_with_exceptions(self):
        """測試註解保留（包含異常處理）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        preservation = metrics_calculator.calculate_annotation_preservation()
        
        self.assertIn('expected_count', preservation)
        self.assertIn('preserved_count', preservation)
        self.assertIn('preservation_rate', preservation)

    def test_get_actual_files_nonexistent_path(self):
        """測試獲取實際文件（路徑不存在）"""
        nonexistent_dir = self.temp_dir / "nonexistent"
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(nonexistent_dir))
        files = metrics_calculator._get_actual_files()
        
        # 路徑不存在時應該返回空列表
        self.assertEqual(files, [])

    def test_get_actual_directories_nonexistent_path(self):
        """測試獲取實際目錄（路徑不存在）"""
        nonexistent_dir = self.temp_dir / "nonexistent"
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(nonexistent_dir))
        directories = metrics_calculator._get_actual_directories()
        
        # 路徑不存在時應該返回空列表
        self.assertEqual(directories, [])


if __name__ == '__main__':
    unittest.main()
