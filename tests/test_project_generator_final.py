"""
專案生成器最終測試 - 覆蓋剩餘行
"""
import unittest
import sys
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from project_generator import ProjectGenerator


class TestProjectGeneratorFinal(unittest.TestCase):
    """專案生成器最終測試"""

    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output_dir = self.temp_dir / "output"

    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_generate_file_not_in_templates(self):
        """測試生成不在模板中的文件"""
        structure = {
            'project': {
                'name': 'project',
                'type': 'directory',
                'children': {
                    'config.yaml': {
                        'name': 'config.yaml',
                        'type': 'file',
                        'comment': '配置文件'
                    }
                }
            }
        }
        
        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")
        
        config_file = self.output_dir / "project" / "config.yaml"
        self.assertTrue(config_file.exists())
        # 應該使用預設模板
        content = config_file.read_text(encoding='utf-8')
        self.assertIn('config.yaml', content)

    def test_generate_file_without_template_key(self):
        """測試生成沒有模板鍵的文件"""
        structure = {
            'project': {
                'name': 'project',
                'type': 'directory',
                'children': {
                    'unknown.xyz': {
                        'name': 'unknown.xyz',
                        'type': 'file'
                    }
                }
            }
        }
        
        generator = ProjectGenerator(str(self.output_dir))
        generator.generate(structure, "test_project")
        
        unknown_file = self.output_dir / "project" / "unknown.xyz"
        self.assertTrue(unknown_file.exists())
        # 應該使用預設內容
        content = unknown_file.read_text(encoding='utf-8')
        self.assertIn('unknown.xyz', content)


if __name__ == '__main__':
    unittest.main()
