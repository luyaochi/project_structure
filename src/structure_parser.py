"""
解析 README.md 中的專案結構樹狀圖
"""
import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class StructureParser:
    """解析目錄樹狀結構"""

    def __init__(self, readme_path: str = "README.md"):
        self.readme_path = Path(readme_path)
        self.structure = {}

    def _calculate_level(self, line: str) -> int:
        """計算縮排層級"""
        # 計算前導空格
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # 檢查是否有樹狀符號
        has_tree_chars = any(char in line for char in ['├', '└', '│'])

        if not has_tree_chars:
            # 沒有樹狀符號，使用空格計算（每3個空格一層）
            return indent // 3

        # 有樹狀符號的情況
        # 計算 ├ 或 └ 的數量（每個表示一個層級）
        # 但需要考慮前面的空格
        level = 0

        # 計算 ├ 或 └ 的數量
        branch_count = line.count('├') + line.count('└')

        # 如果沒有分支符號，可能是純 │ 行（這種情況不應該出現在結構定義中）
        if branch_count == 0:
            # 使用空格計算
            level = indent // 3
        else:
            # 有分支符號，層級 = 分支符號前的空格層級 + 分支符號數量
            # 找到第一個 ├ 或 └ 的位置
            first_branch_pos = -1
            for i, char in enumerate(line):
                if char in ['├', '└']:
                    first_branch_pos = i
                    break

            if first_branch_pos > 0:
                # 分支符號前的空格層級
                space_level = first_branch_pos // 3
                level = space_level + branch_count
            else:
                level = branch_count

        return level

    def _extract_name_and_comment(self, line: str) -> Tuple[Optional[str], Optional[str]]:
        """提取文件名/目錄名和註解"""
        # 移除樹狀符號和空格
        # 匹配開頭的樹狀符號：├─, └─, │, ─, 空格
        cleaned = re.sub(r'^[├└│─\s]+', '', line)

        # 分離路徑和註解
        parts = cleaned.split('←')
        name_part = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else None

        # 移除名稱末尾的斜線（如果有）
        if name_part.endswith('/'):
            name_part = name_part.rstrip('/')

        # 移除註解中的 emoji 和清理
        if comment:
            comment = comment.strip()

        if not name_part:
            return None, None

        return name_part, comment

    def _is_directory(self, name: str) -> bool:
        """判斷是否為目錄"""
        # 有副檔名的通常是文件
        if '.' in name and name.split('.')[-1] in ['py', 'md', 'toml', 'json', 'js', 'ts', 'tsx', 'jsx', 'yml', 'yaml']:
            return False
        return True

    def parse(self) -> Dict:
        """解析 README.md 並返回結構字典"""
        if not self.readme_path.exists():
            raise FileNotFoundError(f"找不到文件: {self.readme_path}")

        with open(self.readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        structure = {}
        path_stack = []  # 追蹤當前路徑層級
        in_structure_block = False  # 是否在結構區塊中

        for line in lines:
            original_line = line
            line = line.rstrip()

            # 跳過空行
            if not line.strip():
                if in_structure_block:
                    continue  # 在結構區塊中的空行可以繼續
                else:
                    continue

            # 檢查是否進入結構區塊（包含樹狀符號或看起來像路徑）
            if not in_structure_block:
                # 檢查是否包含樹狀符號（├, └, │）或看起來像路徑（包含 / 或 .py/.md 等）
                if any(char in line for char in ['├', '└', '│']) or ('/' in line and not line.strip().startswith('#')):
                    in_structure_block = True
                else:
                    continue

            # 如果已經在結構區塊中
            if in_structure_block:
                # 如果遇到明顯的非結構行（如代碼塊、標題等），停止
                stripped = line.strip()
                if stripped.startswith('```'):
                    break
                # 如果是不包含樹狀符號的普通文字行，且不是結構的一部分，停止
                if not any(char in line for char in ['├', '└', '│', '─']) and not stripped.startswith(' ') and len(stripped) > 0:
                    # 但如果是註解行（包含 ←），繼續
                    if '←' not in line:
                        # 檢查是否是純文字描述（沒有縮排）
                        if not line.startswith((' ', '\t')) and stripped and not any(c in stripped for c in ['/', '.py', '.md', '.toml', '.json']):
                            break

            level = self._calculate_level(line)
            name, comment = self._extract_name_and_comment(line)

            if not name:
                continue

            is_dir = self._is_directory(name)

            # 調整路徑堆疊到正確層級
            while len(path_stack) > level:
                path_stack.pop()

            # 建立當前節點
            node = {
                'type': 'directory' if is_dir else 'file',
                'name': name,
                'comment': comment,
                'children': {} if is_dir else None
            }

            # 插入到結構中
            if level == 0:
                # 根節點
                structure[name] = node
                path_stack = [name]
            else:
                # 子節點
                current = structure
                for part in path_stack:
                    if part not in current:
                        current[part] = {
                            'type': 'directory',
                            'name': part,
                            'comment': None,
                            'children': {}
                        }
                    current = current[part]['children']

                current[name] = node

                # 如果是目錄，加入路徑堆疊
                if is_dir:
                    path_stack.append(name)

        self.structure = structure
        return structure

    def get_file_list(self) -> List[Tuple[str, str]]:
        """返回所有文件的列表 (full_path, type)"""
        files = []

        def traverse(node: Dict, parent_path: str = ""):
            for name, info in node.items():
                if isinstance(info, dict):
                    current_path = f"{parent_path}/{name}" if parent_path else name
                    if info.get('type') == 'file':
                        files.append((current_path, name))
                    elif 'children' in info and info['children']:
                        traverse(info['children'], current_path)

        traverse(self.structure)
        return files

    def get_directory_list(self) -> List[str]:
        """返回所有目錄的列表"""
        directories = []

        def traverse(node: Dict, parent_path: str = ""):
            for name, info in node.items():
                if isinstance(info, dict):
                    current_path = f"{parent_path}/{name}" if parent_path else name
                    if info.get('type') == 'directory':
                        directories.append(current_path)
                    if 'children' in info and info['children']:
                        traverse(info['children'], current_path)

        traverse(self.structure)
        return directories
