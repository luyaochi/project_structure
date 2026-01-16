"""
測試專案生成器
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from project_generator import ProjectGenerator
from structure_parser import StructureParser


class TestProjectGenerator(unittest.TestCase):
    """測試專案生成器"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output_dir = self.temp_dir / "output"

        # 創建簡單的結構
        self.structure = {
            'project': {
                'name': 'project',
                'type': 'directory',
                'children': {
                    'src': {
                        'name': 'src',
                        'type': 'directory',
                        'children': {
                            'main.py': {
                                'name': 'main.py',
                                'type': 'file'
                            }
                        }
                    },
                    'README.md': {
                        'name': 'README.md',
                        'type': 'file'
                    }
                }
            }
        }

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generate_project(self):
        """測試生成專案"""
        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(self.structure, "test_project")

        # 檢查生成的目錄和文件（使用結構中的鍵名 'project'）
        self.assertTrue((self.output_dir / "project").exists())
        self.assertTrue((self.output_dir / "project" / "src").exists())
        self.assertTrue((self.output_dir / "project" / "src" / "main.py").exists())
        self.assertTrue((self.output_dir / "project" / "README.md").exists())

    def test_generate_python_file(self):
        """測試生成 Python 文件"""
        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(self.structure, "test_project")

        main_py = self.output_dir / "project" / "src" / "main.py"
        self.assertTrue(main_py.exists())
        content = main_py.read_text(encoding='utf-8')
        self.assertIn('def main', content)

    def test_generate_readme(self):
        """測試生成 README"""
        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(self.structure, "test_project")

        readme = self.output_dir / "project" / "README.md"
        self.assertTrue(readme.exists())
        content = readme.read_text(encoding='utf-8')
        self.assertIn('#', content)


if __name__ == '__main__':
    unittest.main()
