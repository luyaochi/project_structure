"""
專案結構生成驗證指標計算器
"""
import os
from pathlib import Path
from typing import Dict, List, Tuple
from structure_parser import StructureParser


class VerificationMetrics:
    """驗證指標計算器"""

    def __init__(self, structure_file: str, generated_path: str):
        self.structure_file = Path(structure_file)
        self.generated_path = Path(generated_path)
        self.parser = StructureParser(structure_file)
        self.expected_structure = self.parser.parse()

    def calculate_all_metrics(self) -> Dict:
        """計算所有驗證指標"""
        return {
            'structure_coverage': self.calculate_structure_coverage(),
            'file_coverage': self.calculate_file_coverage(),
            'directory_coverage': self.calculate_directory_coverage(),
            'template_accuracy': self.calculate_template_accuracy(),
            'hierarchy_accuracy': self.calculate_hierarchy_accuracy(),
            'annotation_preservation': self.calculate_annotation_preservation(),
            'module_independence': self.calculate_module_independence(),
            'overall_score': 0.0
        }

    def calculate_structure_coverage(self) -> Dict:
        """計算結構覆蓋率"""
        expected = self._count_expected_items()
        actual = self._count_actual_items()

        coverage = {
            'expected_directories': expected['directories'],
            'actual_directories': actual['directories'],
            'expected_files': expected['files'],
            'actual_files': actual['files'],
            'directory_coverage_rate': actual['directories'] / expected['directories'] if expected['directories'] > 0 else 0.0,
            'file_coverage_rate': actual['files'] / expected['files'] if expected['files'] > 0 else 0.0,
            'overall_coverage': (actual['directories'] + actual['files']) / (expected['directories'] + expected['files']) if (expected['directories'] + expected['files']) > 0 else 0.0
        }

        return coverage

    def calculate_file_coverage(self) -> Dict:
        """計算文件覆蓋率"""
        expected_files = self._get_expected_files()
        actual_files = self._get_actual_files()

        matched = set(actual_files) & set(expected_files)
        missing = set(expected_files) - set(actual_files)
        extra = set(actual_files) - set(expected_files)

        return {
            'expected_count': len(expected_files),
            'actual_count': len(actual_files),
            'matched_count': len(matched),
            'missing_files': list(missing),
            'extra_files': list(extra),
            'coverage_rate': len(matched) / len(expected_files) if expected_files else 0.0,
            'accuracy_rate': len(matched) / len(actual_files) if actual_files else 0.0
        }

    def calculate_directory_coverage(self) -> Dict:
        """計算目錄覆蓋率"""
        expected_dirs = self._get_expected_directories()
        actual_dirs = self._get_actual_directories()

        matched = set(actual_dirs) & set(expected_dirs)
        missing = set(expected_dirs) - set(actual_dirs)
        extra = set(actual_dirs) - set(expected_dirs)

        return {
            'expected_count': len(expected_dirs),
            'actual_count': len(actual_dirs),
            'matched_count': len(matched),
            'missing_directories': list(missing),
            'extra_directories': list(extra),
            'coverage_rate': len(matched) / len(expected_dirs) if expected_dirs else 0.0,
            'accuracy_rate': len(matched) / len(actual_dirs) if actual_dirs else 0.0
        }

    def calculate_template_accuracy(self) -> Dict:
        """計算模板準確性"""
        template_files = {
            'pyproject.toml': self._check_pyproject_toml(),
            'package.json': self._check_package_json(),
            'python_files': self._check_python_files(),
            'readme_files': self._check_readme_files()
        }

        total_checks = sum(len(v.get('checks', [])) for v in template_files.values())
        passed_checks = sum(sum(1 for c in v.get('checks', []) if c.get('passed', False)) for v in template_files.values())

        return {
            'template_files': template_files,
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'accuracy_rate': passed_checks / total_checks if total_checks > 0 else 0.0
        }

    def calculate_hierarchy_accuracy(self) -> Dict:
        """計算層級準確性"""
        # 驗證三層級結構
        project_level = self._verify_project_level()
        module_level = self._verify_module_level()
        feature_level = self._verify_feature_level()

        return {
            'project_level': project_level,
            'module_level': module_level,
            'feature_level': feature_level,
            'overall_accuracy': (project_level['accuracy'] + module_level['accuracy'] + feature_level['accuracy']) / 3
        }

    def calculate_annotation_preservation(self) -> Dict:
        """計算註解保留率"""
        expected_annotations = self._get_expected_annotations()
        preserved_annotations = self._check_annotation_preservation()

        return {
            'expected_count': len(expected_annotations),
            'preserved_count': len(preserved_annotations),
            'preservation_rate': len(preserved_annotations) / len(expected_annotations) if expected_annotations else 0.0,
            'missing_annotations': [a for a in expected_annotations if a not in preserved_annotations]
        }

    def calculate_module_independence(self) -> Dict:
        """計算模組獨立性"""
        modules = ['core', 'backend', 'jobs', 'cli', 'frontend']
        independence_checks = {}

        for module in modules:
            module_path = self.generated_path / 'system' / 'project1' / module
            checks = {
                'has_readme': (module_path / 'README.md').exists(),
                'has_config': False,
                'has_src': (module_path / 'src').exists() if module != 'frontend' else (module_path / 'src').exists()
            }

            if module != 'frontend':
                checks['has_config'] = (module_path / 'pyproject.toml').exists()
            else:
                checks['has_config'] = (module_path / 'package.json').exists()

            independence_checks[module] = checks

        total_checks = sum(len(checks) for checks in independence_checks.values())
        passed_checks = sum(sum(1 for v in checks.values() if v) for checks in independence_checks.values())

        return {
            'module_checks': independence_checks,
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'independence_rate': passed_checks / total_checks if total_checks > 0 else 0.0
        }

    def _count_expected_items(self) -> Dict[str, int]:
        """計算預期項目數量"""
        def count_items(node: Dict, counts: Dict[str, int] = None):
            if counts is None:
                counts = {'directories': 0, 'files': 0}

            for name, info in node.items():
                if isinstance(info, dict):
                    if info.get('type') == 'directory':
                        counts['directories'] += 1
                        if 'children' in info and info['children']:
                            count_items(info['children'], counts)
                    elif info.get('type') == 'file':
                        counts['files'] += 1

            return counts

        return count_items(self.expected_structure)

    def _count_actual_items(self) -> Dict[str, int]:
        """計算實際項目數量"""
        project_path = self.generated_path / 'system' / 'project1'
        if not project_path.exists():
            return {'directories': 0, 'files': 0}

        directories = sum(1 for _ in project_path.rglob('*') if _.is_dir())
        files = sum(1 for _ in project_path.rglob('*') if _.is_file())

        return {'directories': directories, 'files': files}

    def _get_expected_files(self) -> List[str]:
        """獲取預期文件列表"""
        files = []

        def traverse(node: Dict, parent_path: str = ""):
            for name, info in node.items():
                if isinstance(info, dict):
                    # 跳過 system 和 project1 根目錄，從 project1 內部開始
                    if name in ['system', 'project1']:
                        if 'children' in info and info['children']:
                            traverse(info['children'], "")
                        continue

                    current_path = f"{parent_path}/{name}" if parent_path else name
                    if info.get('type') == 'file':
                        files.append(current_path)
                    elif 'children' in info and info['children']:
                        traverse(info['children'], current_path)

        traverse(self.expected_structure)
        return files

    def _get_actual_files(self) -> List[str]:
        """獲取實際文件列表"""
        project_path = self.generated_path / 'system' / 'project1'
        if not project_path.exists():
            return []

        files = []
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(project_path)
                # 標準化路徑格式
                file_str = str(relative_path).replace('\\', '/')
                files.append(file_str)

        return files

    def _get_expected_directories(self) -> List[str]:
        """獲取預期目錄列表"""
        directories = []

        def traverse(node: Dict, parent_path: str = ""):
            for name, info in node.items():
                if isinstance(info, dict):
                    # 跳過 system 和 project1 根目錄，從 project1 內部開始
                    if name in ['system', 'project1']:
                        if 'children' in info and info['children']:
                            traverse(info['children'], "")
                        continue

                    current_path = f"{parent_path}/{name}" if parent_path else name
                    if info.get('type') == 'directory':
                        directories.append(current_path)
                        if 'children' in info and info['children']:
                            traverse(info['children'], current_path)

        traverse(self.expected_structure)
        return directories

    def _get_actual_directories(self) -> List[str]:
        """獲取實際目錄列表"""
        project_path = self.generated_path / 'system' / 'project1'
        if not project_path.exists():
            return []

        directories = []
        for dir_path in project_path.rglob('*'):
            if dir_path.is_dir():
                relative_path = dir_path.relative_to(project_path)
                directories.append(str(relative_path).replace('\\', '/'))

        return directories

    def _get_expected_annotations(self) -> List[str]:
        """獲取預期註解列表"""
        annotations = []

        def traverse(node: Dict):
            for name, info in node.items():
                if isinstance(info, dict):
                    if info.get('comment'):
                        annotations.append(info['comment'])
                    if 'children' in info and info['children']:
                        traverse(info['children'])

        traverse(self.expected_structure)
        return annotations

    def _check_annotation_preservation(self) -> List[str]:
        """檢查註解保留情況"""
        preserved = []
        expected = self._get_expected_annotations()
        project_path = self.generated_path / 'system' / 'project1'

        # 檢查 README 文件中的註解
        for readme_file in project_path.rglob('README.md'):
            try:
                content = readme_file.read_text(encoding='utf-8')
                for annotation in expected:
                    if annotation in content:
                        preserved.append(annotation)
            except:
                pass

        # 檢查 Python 文件中的註解
        for py_file in project_path.rglob('*.py'):
            try:
                content = py_file.read_text(encoding='utf-8')
                for annotation in expected:
                    if annotation in content:
                        preserved.append(annotation)
            except:
                pass

        return list(set(preserved))

    def _check_pyproject_toml(self) -> Dict:
        """檢查 pyproject.toml 文件"""
        checks = []
        project_path = self.generated_path / 'system' / 'project1'

        for toml_file in project_path.rglob('pyproject.toml'):
            try:
                content = toml_file.read_text(encoding='utf-8')
                checks.append({
                    'file': str(toml_file.relative_to(project_path)),
                    'passed': '[project]' in content and 'name =' in content,
                    'has_build_system': '[build-system]' in content,
                    'has_project_section': '[project]' in content
                })
            except:
                checks.append({
                    'file': str(toml_file.relative_to(project_path)),
                    'passed': False
                })

        return {'checks': checks}

    def _check_package_json(self) -> Dict:
        """檢查 package.json 文件"""
        checks = []
        project_path = self.generated_path / 'system' / 'project1'

        for json_file in project_path.rglob('package.json'):
            try:
                content = json_file.read_text(encoding='utf-8')
                checks.append({
                    'file': str(json_file.relative_to(project_path)),
                    'passed': '"name"' in content and '"version"' in content,
                    'has_name': '"name"' in content,
                    'has_version': '"version"' in content
                })
            except:
                checks.append({
                    'file': str(json_file.relative_to(project_path)),
                    'passed': False
                })

        return {'checks': checks}

    def _check_python_files(self) -> Dict:
        """檢查 Python 文件"""
        checks = []
        project_path = self.generated_path / 'system' / 'project1'

        for py_file in project_path.rglob('*.py'):
            try:
                content = py_file.read_text(encoding='utf-8')
                checks.append({
                    'file': str(py_file.relative_to(project_path)),
                    'passed': 'def main()' in content or '"""' in content,
                    'has_docstring': '"""' in content,
                    'has_main': 'def main()' in content
                })
            except:
                checks.append({
                    'file': str(py_file.relative_to(project_path)),
                    'passed': False
                })

        return {'checks': checks}

    def _check_readme_files(self) -> Dict:
        """檢查 README 文件"""
        checks = []
        project_path = self.generated_path / 'system' / 'project1'

        for readme_file in project_path.rglob('README.md'):
            try:
                content = readme_file.read_text(encoding='utf-8')
                checks.append({
                    'file': str(readme_file.relative_to(project_path)),
                    'passed': len(content.strip()) > 0,
                    'has_content': len(content.strip()) > 0
                })
            except:
                checks.append({
                    'file': str(readme_file.relative_to(project_path)),
                    'passed': False
                })

        return {'checks': checks}

    def _verify_project_level(self) -> Dict:
        """驗證專案層級"""
        project_path = self.generated_path / 'system' / 'project1'
        checks = {
            'has_project_root': (project_path).exists(),
            'has_project_readme': (project_path / 'README.md').exists(),
            'has_docs': (project_path / 'docs').exists()
        }

        passed = sum(1 for v in checks.values() if v)
        return {
            'checks': checks,
            'passed': passed,
            'total': len(checks),
            'accuracy': passed / len(checks) if checks else 0.0
        }

    def _verify_module_level(self) -> Dict:
        """驗證模組層級"""
        modules = ['core', 'backend', 'jobs', 'cli', 'frontend']
        project_path = self.generated_path / 'system' / 'project1'

        module_checks = {}
        for module in modules:
            module_path = project_path / module
            module_checks[module] = {
                'exists': module_path.exists(),
                'has_readme': (module_path / 'README.md').exists(),
                'has_config': (module_path / 'pyproject.toml').exists() if module != 'frontend' else (module_path / 'package.json').exists()
            }

        total_checks = sum(len(checks) for checks in module_checks.values())
        passed_checks = sum(sum(1 for v in checks.values() if v) for checks in module_checks.values())

        return {
            'module_checks': module_checks,
            'passed': passed_checks,
            'total': total_checks,
            'accuracy': passed_checks / total_checks if total_checks > 0 else 0.0
        }

    def _verify_feature_level(self) -> Dict:
        """驗證功能層級"""
        project_path = self.generated_path / 'system' / 'project1'

        feature_checks = {
            'core_core': (project_path / 'core' / 'src' / 'core').exists(),
            'core_domain': (project_path / 'core' / 'src' / 'domain').exists(),
            'backend_api': (project_path / 'backend' / 'src' / 'api').exists(),
            'backend_domain': (project_path / 'backend' / 'src' / 'domain').exists(),
            'jobs_tasks': (project_path / 'jobs' / 'src' / 'tasks').exists(),
            'cli_commands': (project_path / 'cli' / 'src' / 'commands').exists(),
            'frontend_components': (project_path / 'frontend' / 'src' / 'components').exists()
        }

        passed = sum(1 for v in feature_checks.values() if v)
        return {
            'checks': feature_checks,
            'passed': passed,
            'total': len(feature_checks),
            'accuracy': passed / len(feature_checks) if feature_checks else 0.0
        }
