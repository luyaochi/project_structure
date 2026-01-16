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
from verification_metrics import VerificationMetrics
from generate_metrics import generate_report as generate_metrics_report
from generate_verification import generate_verification_report
from generate_conclusion import generate_conclusion_report as _generate_conclusion_report
from i18n import LANG_EN, LANG_ZH_CN, LANG_ZH_TW, DEFAULT_LANG, get_lang_suffix


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
    parser.add_argument(
        "--structure",
        type=str,
        help="結構定義文件（用於生成報告，預設: structure_example.md）"
    )
    parser.add_argument(
        "--generated",
        type=str,
        help="生成的專案路徑（用於生成報告）"
    )
    parser.add_argument(
        "--generate-reports",
        action="store_true",
        help="生成專案後自動生成驗證報告，或直接生成報告（需提供 --structure 和 --generated）"
    )
    parser.add_argument(
        "--report-lang",
        type=str,
        default=DEFAULT_LANG,
        choices=[LANG_EN, LANG_ZH_CN, LANG_ZH_TW],
        help="報告語言選擇: en, zh-CN, zh-TW (預設: zh-TW)"
    )
    parser.add_argument(
        "--all-langs",
        action="store_true",
        help="生成所有語言版本的報告（僅在 --generate-reports 時有效）"
    )
    parser.add_argument(
        "--report-output",
        type=str,
        help="報告輸出目錄（預設: 專案根目錄）"
    )

    args = parser.parse_args()

    try:
        # 如果只生成報告（提供了 --structure 和 --generated）
        if args.generate_reports and args.structure and args.generated:
            print(f"[*] 直接生成報告模式")
            print(f"[*] 結構定義: {args.structure}")
            print(f"[*] 生成專案路徑: {args.generated}")

            # 確定報告輸出目錄
            if args.report_output:
                report_dir = Path(args.report_output)
            else:
                report_dir = Path.cwd() / "reports"

            report_dir.mkdir(parents=True, exist_ok=True)
            print(f"[*] 報告輸出目錄: {report_dir}")

            # 生成報告
            if args.all_langs:
                languages = [LANG_ZH_TW, LANG_ZH_CN, LANG_EN]
                for lang in languages:
                    suffix = get_lang_suffix(lang)
                    print(f"\n[*] 生成 {lang} 版本報告...")

                    # 指標報告
                    metrics_file = report_dir / f"METRICS{suffix}.md"
                    generate_metrics_report_file(args.structure, args.generated, str(metrics_file), lang)

                    # 驗證報告
                    verification_file = report_dir / f"VERIFICATION{suffix}.md"
                    generate_verification_report(args.structure, args.generated, str(verification_file), lang)

                    # 結論報告
                    conclusion_file = report_dir / f"CONCLUSION{suffix}.md"
                    _generate_conclusion_report(args.structure, args.generated, str(conclusion_file), lang)
            else:
                suffix = get_lang_suffix(args.report_lang)
                print(f"\n[*] 生成 {args.report_lang} 版本報告...")

                # 指標報告
                metrics_file = report_dir / f"METRICS{suffix}.md"
                generate_metrics_report_file(args.structure, args.generated, str(metrics_file), args.report_lang)

                # 驗證報告
                verification_file = report_dir / f"VERIFICATION{suffix}.md"
                generate_verification_report(args.structure, args.generated, str(verification_file), args.report_lang)

                # 結論報告
                conclusion_file = report_dir / f"CONCLUSION{suffix}.md"
                _generate_conclusion_report(args.structure, args.generated, str(conclusion_file), args.report_lang)

            print("\n[OK] 所有報告生成完成！")
            return

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

        print("\n[OK] 專案生成完成！")

        # 生成報告
        if args.generate_reports:
            print("\n[*] 開始生成驗證報告...")
            generated_path = Path(args.output)

            # 確定報告輸出目錄
            if args.report_output:
                report_dir = Path(args.report_output)
            else:
                report_dir = Path.cwd() / "reports"

            report_dir.mkdir(parents=True, exist_ok=True)
            print(f"[*] 報告輸出目錄: {report_dir}")

            # 確定結構文件路徑
            if args.structure:
                structure_file = args.structure
            else:
                structure_file = args.readme

            # 生成報告
            if args.all_langs:
                languages = [LANG_ZH_TW, LANG_ZH_CN, LANG_EN]
                for lang in languages:
                    suffix = get_lang_suffix(lang)
                    print(f"\n[*] 生成 {lang} 版本報告...")

                    # 指標報告
                    metrics_file = report_dir / f"METRICS{suffix}.md"
                    generate_metrics_report_file(structure_file, str(generated_path), str(metrics_file), lang)

                    # 驗證報告
                    verification_file = report_dir / f"VERIFICATION{suffix}.md"
                    generate_verification_report(structure_file, str(generated_path), str(verification_file), lang)

                    # 結論報告
                    conclusion_file = report_dir / f"CONCLUSION{suffix}.md"
                    _generate_conclusion_report(structure_file, str(generated_path), str(conclusion_file), lang)
            else:
                suffix = get_lang_suffix(args.report_lang)
                print(f"\n[*] 生成 {args.report_lang} 版本報告...")

                # 指標報告
                metrics_file = report_dir / f"METRICS{suffix}.md"
                generate_metrics_report_file(structure_file, str(generated_path), str(metrics_file), args.report_lang)

                # 驗證報告
                verification_file = report_dir / f"VERIFICATION{suffix}.md"
                generate_verification_report(structure_file, str(generated_path), str(verification_file), args.report_lang)

                # 結論報告
                conclusion_file = report_dir / f"CONCLUSION{suffix}.md"
                _generate_conclusion_report(structure_file, str(generated_path), str(conclusion_file), args.report_lang)

            print("\n[OK] 所有報告生成完成！")

    except FileNotFoundError as e:
        print(f"[X] 錯誤: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[X] 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def generate_metrics_report_file(structure_file: str, generated_path: str,
                                  output_file: str, lang: str):
    """生成指標報告文件"""
    try:
        metrics_calculator = VerificationMetrics(structure_file, generated_path)
        metrics = metrics_calculator.calculate_all_metrics()

        # 計算總體分數
        overall_score = (
            metrics['structure_coverage']['overall_coverage'] * 0.3 +
            metrics['file_coverage']['coverage_rate'] * 0.2 +
            metrics['directory_coverage']['coverage_rate'] * 0.2 +
            metrics['template_accuracy']['accuracy_rate'] * 0.1 +
            metrics['hierarchy_accuracy']['overall_accuracy'] * 0.1 +
            metrics['annotation_preservation']['preservation_rate'] * 0.05 +
            metrics['module_independence']['independence_rate'] * 0.05
        ) * 100
        metrics['overall_score'] = overall_score

        generate_metrics_report(metrics, output_file, lang)
    except Exception as e:
        print(f"[!] 生成指標報告時發生錯誤: {e}")




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
