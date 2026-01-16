"""
Pytest 配置和共用 fixtures
"""
import pytest
import sys
from pathlib import Path

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_structure_file(tmp_path):
    """創建臨時結構文件"""
    structure_content = """```
project/
├─ src/
│  ├─ main.py
│  └─ utils.py
├─ tests/
│  └─ test_main.py
└─ README.md
```"""
    structure_file = tmp_path / "structure.md"
    structure_file.write_text(structure_content, encoding='utf-8')
    return structure_file


@pytest.fixture
def temp_generated_project(tmp_path):
    """創建臨時生成的專案結構"""
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    # 創建目錄結構
    (project_dir / "src").mkdir()
    (project_dir / "tests").mkdir()

    # 創建文件
    (project_dir / "src" / "main.py").write_text("# main.py\n", encoding='utf-8')
    (project_dir / "src" / "utils.py").write_text("# utils.py\n", encoding='utf-8')
    (project_dir / "tests" / "test_main.py").write_text("# test_main.py\n", encoding='utf-8')
    (project_dir / "README.md").write_text("# README\n", encoding='utf-8')

    return project_dir
