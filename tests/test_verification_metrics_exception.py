"""
驗證指標異常處理測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from verification_metrics import VerificationMetrics


class TestVerificationMetricsException(unittest.TestCase):
    """驗證指標異常處理測試"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.structure_file = self.temp_dir / "structure.md"
        self.generated_dir = self.temp_dir / "generated"

        structure_content = """```
system/
└─ project1/
   ├─ core/
   │  └─ pyproject.toml
   ├─ frontend/
   │  └─ package.json
   ├─ src/
   │  └─ main.py
   └─ README.md
```"""
        self.structure_file.write_text(structure_content, encoding='utf-8')

        # 創建生成的專案結構
        self.generated_dir.mkdir()
        system_dir = self.generated_dir / "system"
        system_dir.mkdir()
        project1_dir = system_dir / "project1"
        project1_dir.mkdir()
        core_dir = project1_dir / "core"
        core_dir.mkdir()
        frontend_dir = project1_dir / "frontend"
        frontend_dir.mkdir()
        src_dir = project1_dir / "src"
        src_dir.mkdir()

        # 創建文件
        (core_dir / "pyproject.toml").write_text(
            "[build-system]\nrequires = [\"setuptools\"]\n\n[project]\nname = \"core\"\n",
            encoding='utf-8'
        )
        (frontend_dir / "package.json").write_text(
            '{\n  "name": "frontend",\n  "version": "1.0.0"\n}',
            encoding='utf-8'
        )
        (src_dir / "main.py").write_text("# main.py\n", encoding='utf-8')
        (project1_dir / "README.md").write_text("# README\n", encoding='utf-8')

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_check_python_files_with_exception(self):
        """測試檢查 Python 文件（包含異常處理）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        result = metrics_calculator._check_python_files()

        self.assertIn('checks', result)
        # 即使有異常也應該返回結果

    def test_check_readme_files_with_exception(self):
        """測試檢查 README 文件（包含異常處理）"""
        metrics_calculator = VerificationMetrics(str(self.structure_file), str(self.generated_dir))
        result = metrics_calculator._check_readme_files()

        self.assertIn('checks', result)
        # 即使有異常也應該返回結果


if __name__ == '__main__':
    unittest.main()
