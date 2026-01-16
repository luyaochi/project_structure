"""
根據解析的結構生成專案目錄和文件
"""
import os
from pathlib import Path
from typing import Dict, List
from structure_parser import StructureParser


class ProjectGenerator:
    """專案生成器"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """載入文件模板"""
        return {
            'pyproject.toml': self._get_pyproject_template(),
            'package.json': self._get_package_json_template(),
            'README.md': self._get_readme_template(),
            '.py': self._get_python_template(),
            '.md': self._get_markdown_template(),
        }

    def _get_pyproject_template(self) -> str:
        """pyproject.toml 模板"""
        return """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_backend"

[project]
name = "{name}"
version = "0.1.0"
description = ""
readme = "README.md"
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
    "ruff>=0.1.0",
]
"""

    def _get_package_json_template(self) -> str:
        """package.json 模板"""
        return """{{
  "name": "{name}",
  "version": "0.1.0",
  "description": "",
  "main": "index.js",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{}},
  "devDependencies": {{
    "vite": "^5.0.0"
  }}
}}
"""

    def _get_readme_template(self) -> str:
        """README.md 模板"""
        return """# {name}

{comment}

## 說明

此模組由專案生成器自動建立。

"""

    def _get_python_template(self) -> str:
        """Python 文件模板"""
        return '''"""
{comment}
"""


def main():
    """主函數"""
    pass


if __name__ == "__main__":
    main()
'''

    def _get_markdown_template(self) -> str:
        """Markdown 文件模板"""
        return """# {name}

{comment}

"""

    def generate(self, structure: Dict, project_name: str = "project1"):
        """生成專案結構"""
        self.output_dir.mkdir(parents=True, exist_ok=True)

        def create_structure(node: Dict, parent_path: Path):
            for name, info in node.items():
                if not isinstance(info, dict):
                    continue

                current_path = parent_path / name
                comment = info.get('comment', '')
                node_name = info.get('name', name)

                if info.get('type') == 'directory':
                    # 創建目錄
                    current_path.mkdir(parents=True, exist_ok=True)
                    print(f"[DIR] 創建目錄: {current_path}")

                    # 如果有 README.md，創建它
                    readme_path = current_path / "README.md"
                    if not readme_path.exists():
                        readme_content = self.templates['README.md'].format(
                            name=node_name,
                            comment=comment or f"{node_name} 模組"
                        )
                        readme_path.write_text(readme_content, encoding='utf-8')
                        print(f"  [FILE] 創建: {readme_path.name}")

                    # 遞迴處理子項目
                    if 'children' in info and info['children']:
                        create_structure(info['children'], current_path)

                elif info.get('type') == 'file':
                    # 創建文件
                    if not current_path.exists():
                        file_ext = Path(node_name).suffix
                        template_key = file_ext if file_ext in ['.py', '.md'] else node_name

                        if template_key in self.templates:
                            if node_name == 'pyproject.toml':
                                content = self.templates['pyproject.toml'].format(
                                    name=parent_path.name
                                )
                            elif node_name == 'package.json':
                                content = self.templates['package.json'].format(
                                    name=parent_path.name
                                )
                            elif file_ext == '.py':
                                content = self.templates['.py'].format(
                                    name=node_name.replace(file_ext, ''),
                                    comment=comment or f"{node_name} 模組"
                                )
                            elif file_ext == '.md':
                                content = self.templates['.md'].format(
                                    name=node_name.replace(file_ext, ''),
                                    comment=comment or f"{node_name} 文件"
                                )
                            else:
                                content = f"# {node_name}\n\n{comment or ''}\n"
                        else:
                            # 預設空文件
                            content = f"# {node_name}\n\n{comment or ''}\n"

                        current_path.write_text(content, encoding='utf-8')
                        print(f"[FILE] 創建文件: {current_path}")

        # 從結構中找到根目錄
        root_name = list(structure.keys())[0] if structure else project_name
        root_path = self.output_dir / root_name
        root_path.mkdir(parents=True, exist_ok=True)

        # 生成結構
        create_structure(structure, self.output_dir)

        print(f"\n[OK] 專案已生成到: {self.output_dir}")
        return self.output_dir
