"""
生成驗證指標報告
"""
import argparse
import json
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

from verification_metrics import VerificationMetrics


def format_percentage(value: float) -> str:
    """格式化百分比"""
    return f"{value * 100:.2f}%"


def generate_report(metrics: dict, output_file: str = None):
    """生成指標報告"""
    report = []
    report.append("# 專案結構生成對抗指標報告\n")
    report.append("## 📊 總體指標\n\n")

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

    report.append(f"**總體評分**: {overall_score:.2f}/100\n\n")
    report.append("---\n\n")

    # 1. 結構覆蓋率
    report.append("## 1️⃣ 結構覆蓋率指標\n\n")
    sc = metrics['structure_coverage']
    report.append(f"- **預期目錄數**: {sc['expected_directories']}")
    report.append(f"- **實際目錄數**: {sc['actual_directories']}")
    report.append(f"- **目錄覆蓋率**: {format_percentage(sc['directory_coverage_rate'])}")
    report.append(f"- **預期文件數**: {sc['expected_files']}")
    report.append(f"- **實際文件數**: {sc['actual_files']}")
    report.append(f"- **文件覆蓋率**: {format_percentage(sc['file_coverage_rate'])}")
    report.append(f"- **整體覆蓋率**: {format_percentage(sc['overall_coverage'])}\n\n")

    # 2. 文件覆蓋率
    report.append("## 2️⃣ 文件覆蓋率指標\n\n")
    fc = metrics['file_coverage']
    report.append(f"- **預期文件數**: {fc['expected_count']}")
    report.append(f"- **實際文件數**: {fc['actual_count']}")
    report.append(f"- **匹配文件數**: {fc['matched_count']}")
    report.append(f"- **文件覆蓋率**: {format_percentage(fc['coverage_rate'])}")
    report.append(f"- **文件準確率**: {format_percentage(fc['accuracy_rate'])}")
    if fc['missing_files']:
        report.append(f"\n**缺失文件** ({len(fc['missing_files'])} 個):")
        for f in fc['missing_files'][:10]:  # 只顯示前10個
            report.append(f"  - {f}")
        if len(fc['missing_files']) > 10:
            report.append(f"  - ... 還有 {len(fc['missing_files']) - 10} 個")
    if fc['extra_files']:
        report.append(f"\n**額外文件** ({len(fc['extra_files'])} 個):")
        for f in fc['extra_files'][:10]:
            report.append(f"  - {f}")
        if len(fc['extra_files']) > 10:
            report.append(f"  - ... 還有 {len(fc['extra_files']) - 10} 個")
    report.append("\n")

    # 3. 目錄覆蓋率
    report.append("## 3️⃣ 目錄覆蓋率指標\n\n")
    dc = metrics['directory_coverage']
    report.append(f"- **預期目錄數**: {dc['expected_count']}")
    report.append(f"- **實際目錄數**: {dc['actual_count']}")
    report.append(f"- **匹配目錄數**: {dc['matched_count']}")
    report.append(f"- **目錄覆蓋率**: {format_percentage(dc['coverage_rate'])}")
    report.append(f"- **目錄準確率**: {format_percentage(dc['accuracy_rate'])}\n\n")

    # 4. 模板準確性
    report.append("## 4️⃣ 模板準確性指標\n\n")
    ta = metrics['template_accuracy']
    report.append(f"- **總檢查項**: {ta['total_checks']}")
    report.append(f"- **通過檢查**: {ta['passed_checks']}")
    report.append(f"- **準確率**: {format_percentage(ta['accuracy_rate'])}\n\n")

    # 5. 層級準確性
    report.append("## 5️⃣ 層級準確性指標\n\n")
    ha = metrics['hierarchy_accuracy']
    report.append("### 專案層級\n")
    pl = ha['project_level']
    report.append(f"- **通過檢查**: {pl['passed']}/{pl['total']}")
    report.append(f"- **準確率**: {format_percentage(pl['accuracy'])}\n")

    report.append("### 模組層級\n")
    ml = ha['module_level']
    report.append(f"- **通過檢查**: {ml['passed']}/{ml['total']}")
    report.append(f"- **準確率**: {format_percentage(ml['accuracy'])}\n")

    report.append("### 功能層級\n")
    fl = ha['feature_level']
    report.append(f"- **通過檢查**: {fl['passed']}/{fl['total']}")
    report.append(f"- **準確率**: {format_percentage(fl['accuracy'])}\n")

    report.append(f"### 整體層級準確率\n")
    report.append(f"- **整體準確率**: {format_percentage(ha['overall_accuracy'])}\n\n")

    # 6. 註解保留率
    report.append("## 6️⃣ 註解保留率指標\n\n")
    ap = metrics['annotation_preservation']
    report.append(f"- **預期註解數**: {ap['expected_count']}")
    report.append(f"- **保留註解數**: {ap['preserved_count']}")
    report.append(f"- **保留率**: {format_percentage(ap['preservation_rate'])}\n\n")

    # 7. 模組獨立性
    report.append("## 7️⃣ 模組獨立性指標\n\n")
    mi = metrics['module_independence']
    report.append(f"- **總檢查項**: {mi['total_checks']}")
    report.append(f"- **通過檢查**: {mi['passed_checks']}")
    report.append(f"- **獨立性率**: {format_percentage(mi['independence_rate'])}\n\n")

    # 總結
    report.append("---\n\n")
    report.append("## 📈 指標總結\n\n")
    report.append("| 指標類別 | 評分 | 狀態 |\n")
    report.append("|---------|------|------|\n")

    indicators = [
        ('結構覆蓋率', sc['overall_coverage'] * 100, '✅' if sc['overall_coverage'] >= 0.95 else '⚠️' if sc['overall_coverage'] >= 0.8 else '❌'),
        ('文件覆蓋率', fc['coverage_rate'] * 100, '✅' if fc['coverage_rate'] >= 0.95 else '⚠️' if fc['coverage_rate'] >= 0.8 else '❌'),
        ('目錄覆蓋率', dc['coverage_rate'] * 100, '✅' if dc['coverage_rate'] >= 0.95 else '⚠️' if dc['coverage_rate'] >= 0.8 else '❌'),
        ('模板準確性', ta['accuracy_rate'] * 100, '✅' if ta['accuracy_rate'] >= 0.9 else '⚠️' if ta['accuracy_rate'] >= 0.7 else '❌'),
        ('層級準確性', ha['overall_accuracy'] * 100, '✅' if ha['overall_accuracy'] >= 0.9 else '⚠️' if ha['overall_accuracy'] >= 0.7 else '❌'),
        ('註解保留率', ap['preservation_rate'] * 100, '✅' if ap['preservation_rate'] >= 0.8 else '⚠️' if ap['preservation_rate'] >= 0.6 else '❌'),
        ('模組獨立性', mi['independence_rate'] * 100, '✅' if mi['independence_rate'] >= 0.9 else '⚠️' if mi['independence_rate'] >= 0.7 else '❌'),
    ]

    for name, score, status in indicators:
        report.append(f"| {name} | {score:.2f}% | {status} |\n")

    report.append(f"\n**總體評分**: {overall_score:.2f}/100\n")

    if overall_score >= 90:
        report.append("\n✅ **優秀** - 生成器表現優秀，可以投入使用\n")
    elif overall_score >= 80:
        report.append("\n⚠️ **良好** - 生成器表現良好，建議優化部分指標\n")
    elif overall_score >= 70:
        report.append("\n⚠️ **及格** - 生成器基本可用，需要改進\n")
    else:
        report.append("\n❌ **不及格** - 生成器需要重大改進\n")

    report_text = ''.join(report)

    if output_file:
        Path(output_file).write_text(report_text, encoding='utf-8')
        print(f"[OK] 指標報告已生成: {output_file}")
    else:
        print(report_text)

    return report_text


def main():
    parser = argparse.ArgumentParser(description="生成專案結構驗證指標")
    parser.add_argument('--structure', type=str, default='structure_example.md', help='結構定義文件')
    parser.add_argument('--generated', type=str, required=True, help='生成的專案路徑')
    parser.add_argument('--output', type=str, help='輸出報告文件')
    parser.add_argument('--json', action='store_true', help='輸出 JSON 格式')

    args = parser.parse_args()

    try:
        metrics_calculator = VerificationMetrics(args.structure, args.generated)
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

        if args.json:
            output = json.dumps(metrics, indent=2, ensure_ascii=False)
            if args.output:
                Path(args.output).write_text(output, encoding='utf-8')
            else:
                print(output)
        else:
            generate_report(metrics, args.output)

    except Exception as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
