"""
擴展的專案生成器測試
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from project_generator import ProjectGenerator


class TestProjectGeneratorExtended(unittest.TestCase):
    """擴展的專案生成器測試"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output_dir = self.temp_dir / "output"

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generate_pyproject_toml(self):
        """測試生成 pyproject.toml"""
        structure = {
            'core': {
                'name': 'core',
                'type': 'directory',
                'children': {
                    'pyproject.toml': {
                        'name': 'pyproject.toml',
                        'type': 'file'
                    }
                }
            }
        }

        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")

        pyproject_file = self.output_dir / "core" / "pyproject.toml"
        self.assertTrue(pyproject_file.exists())
        content = pyproject_file.read_text(encoding='utf-8')
        self.assertIn('[project]', content)
        self.assertIn('name =', content)

    def test_generate_package_json(self):
        """測試生成 package.json"""
        structure = {
            'frontend': {
                'name': 'frontend',
                'type': 'directory',
                'children': {
                    'package.json': {
                        'name': 'package.json',
                        'type': 'file'
                    }
                }
            }
        }

        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")

        package_file = self.output_dir / "frontend" / "package.json"
        self.assertTrue(package_file.exists())
        content = package_file.read_text(encoding='utf-8')
        self.assertIn('"name"', content)

    def test_generate_unknown_file_type(self):
        """測試生成未知文件類型"""
        structure = {
            'project': {
                'name': 'project',
                'type': 'directory',
                'children': {
                    'config.txt': {
                        'name': 'config.txt',
                        'type': 'file',
                        'comment': '配置文件'
                    }
                }
            }
        }

        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")

        config_file = self.output_dir / "project" / "config.txt"
        self.assertTrue(config_file.exists())
        content = config_file.read_text(encoding='utf-8')
        self.assertIn('config.txt', content)

    def test_generate_file_with_comment(self):
        """測試生成帶註解的文件"""
        structure = {
            'project': {
                'name': 'project',
                'type': 'directory',
                'children': {
                    'main.py': {
                        'name': 'main.py',
                        'type': 'file',
                        'comment': '主程式文件'
                    }
                }
            }
        }

        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")

        main_file = self.output_dir / "project" / "main.py"
        self.assertTrue(main_file.exists())
        content = main_file.read_text(encoding='utf-8')
        self.assertIn('主程式文件', content)


if __name__ == '__main__':
    unittest.main()
