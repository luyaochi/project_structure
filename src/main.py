"""
專案結構生成器主程式
"""
import argparse
import sys
import os
from pathlib import Path

# 設置 Windows 控制台編碼支援 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加 src 目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))

from structure_parser import StructureParser
from project_generator import ProjectGenerator


def main():
    parser = argparse.ArgumentParser(
        description="根據 README.md 中的結構描述生成專案目錄和文件"
    )
    parser.add_argument(
        "--readme",
        type=str,
        default="README.md",
        help="README.md 文件路徑（預設: README.md）"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="輸出目錄（預設: output）"
    )
    parser.add_argument(
        "--project-name",
        type=str,
        default="project1",
        help="專案名稱（預設: project1）"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="僅顯示將要生成的結構，不實際創建文件"
    )

    args = parser.parse_args()

    try:
        # 解析結構
        print(f"[*] 讀取結構定義: {args.readme}")
        parser_obj = StructureParser(args.readme)
        structure = parser_obj.parse()

        if not structure:
            print("[X] 無法解析結構，請檢查 README.md 格式")
            sys.exit(1)

        print(f"[OK] 成功解析結構")

        if args.dry_run:
            print("\n將要生成的結構:")
            print_structure(structure)
            return

        # 生成專案
        print(f"\n開始生成專案到: {args.output}")
        generator = ProjectGenerator(args.output)
        generator.generate(structure, args.project_name)

        print("\n完成！")

    except FileNotFoundError as e:
        print(f"[X] 錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[X] 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def print_structure(node: dict, indent: int = 0):
    """遞迴打印結構"""
    prefix = "  " * indent
    for name, info in node.items():
        if isinstance(info, dict):
            node_type = "[DIR]" if info.get('type') == 'directory' else "[FILE]"
            node_name = info.get('name', name)
            comment = f"  <- {info.get('comment', '')}" if info.get('comment') else ""
            print(f"{prefix}{node_type} {node_name}{comment}")

            if 'children' in info and info['children']:
                print_structure(info['children'], indent + 1)


if __name__ == "__main__":
    main()
