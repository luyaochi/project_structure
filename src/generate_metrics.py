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
from i18n import get_text, get_lang_suffix, LANG_EN, LANG_ZH_CN, LANG_ZH_TW, DEFAULT_LANG


def format_percentage(value: float) -> str:
    """格式化百分比"""
    return f"{value * 100:.2f}%"


def generate_report(metrics: dict, output_file: str = None, lang: str = DEFAULT_LANG):
    """生成指標報告"""
    t = lambda key: get_text(key, lang)

    report = []
    report.append(f"# {t('metrics_title')}\n")
    report.append(f"## 📊 {t('overall_metrics')}\n\n")

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

    report.append(f"**{t('overall_score')}**: {overall_score:.2f}/100\n\n")
    report.append("---\n\n")

    # 1. 結構覆蓋率
    report.append(f"## 1️⃣ {t('structure_coverage_title')}\n\n")
    sc = metrics['structure_coverage']
    report.append(f"- **{t('expected_directories')}**: {sc['expected_directories']}")
    report.append(f"- **{t('actual_directories')}**: {sc['actual_directories']}")
    report.append(f"- **{t('directory_coverage_rate')}**: {format_percentage(sc['directory_coverage_rate'])}")
    report.append(f"- **{t('expected_files')}**: {sc['expected_files']}")
    report.append(f"- **{t('actual_files')}**: {sc['actual_files']}")
    report.append(f"- **{t('file_coverage_rate')}**: {format_percentage(sc['file_coverage_rate'])}")
    report.append(f"- **{t('overall_coverage')}**: {format_percentage(sc['overall_coverage'])}\n\n")

    # 2. 文件覆蓋率
    report.append(f"## 2️⃣ {t('file_coverage_title')}\n\n")
    fc = metrics['file_coverage']
    report.append(f"- **{t('expected_files')}**: {fc['expected_count']}")
    report.append(f"- **{t('actual_files')}**: {fc['actual_count']}")
    report.append(f"- **{t('matched_count')}**: {fc['matched_count']}")
    report.append(f"- **{t('file_coverage_rate')}**: {format_percentage(fc['coverage_rate'])}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(fc['accuracy_rate'])}")
    if fc['missing_files']:
        report.append(f"\n**{t('missing_files')}** ({len(fc['missing_files'])} {t('items')}):")
        for f in fc['missing_files'][:10]:  # 只顯示前10個
            report.append(f"  - {f}")
        if len(fc['missing_files']) > 10:
            report.append(f"  - ... {t('more')} {len(fc['missing_files']) - 10} {t('items')}")
    if fc['extra_files']:
        report.append(f"\n**{t('extra_files')}** ({len(fc['extra_files'])} {t('items')}):")
        for f in fc['extra_files'][:10]:
            report.append(f"  - {f}")
        if len(fc['extra_files']) > 10:
            report.append(f"  - ... {t('more')} {len(fc['extra_files']) - 10} {t('items')}")
    report.append("\n")

    # 3. 目錄覆蓋率
    report.append(f"## 3️⃣ {t('directory_coverage_title')}\n\n")
    dc = metrics['directory_coverage']
    report.append(f"- **{t('expected_directories')}**: {dc['expected_count']}")
    report.append(f"- **{t('actual_directories')}**: {dc['actual_count']}")
    report.append(f"- **{t('matched_count')}**: {dc['matched_count']}")
    report.append(f"- **{t('directory_coverage_rate')}**: {format_percentage(dc['coverage_rate'])}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(dc['accuracy_rate'])}\n\n")

    # 4. 模板準確性
    report.append(f"## 4️⃣ {t('template_accuracy_title')}\n\n")
    ta = metrics['template_accuracy']
    report.append(f"- **{t('total_checks')}**: {ta['total_checks']}")
    report.append(f"- **{t('passed_checks')}**: {ta['passed_checks']}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(ta['accuracy_rate'])}\n\n")

    # 5. 層級準確性
    report.append(f"## 5️⃣ {t('hierarchy_accuracy_title')}\n\n")
    ha = metrics['hierarchy_accuracy']
    report.append(f"### {t('project_level')}\n")
    pl = ha['project_level']
    report.append(f"- **{t('passed_checks')}**: {pl['passed']}/{pl['total']}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(pl['accuracy'])}\n")

    report.append(f"### {t('module_level')}\n")
    ml = ha['module_level']
    report.append(f"- **{t('passed_checks')}**: {ml['passed']}/{ml['total']}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(ml['accuracy'])}\n")

    report.append(f"### {t('feature_level')}\n")
    fl = ha['feature_level']
    report.append(f"- **{t('passed_checks')}**: {fl['passed']}/{fl['total']}")
    report.append(f"- **{t('accuracy_rate')}**: {format_percentage(fl['accuracy'])}\n")

    report.append(f"### {t('overall_accuracy')}\n")
    report.append(f"- **{t('overall_accuracy')}**: {format_percentage(ha['overall_accuracy'])}\n\n")

    # 6. 註解保留率
    report.append(f"## 6️⃣ {t('annotation_preservation_title')}\n\n")
    ap = metrics['annotation_preservation']
    report.append(f"- **{t('expected_annotations')}**: {ap['expected_count']}")
    report.append(f"- **{t('preserved_annotations')}**: {ap['preserved_count']}")
    report.append(f"- **{t('preservation_rate')}**: {format_percentage(ap['preservation_rate'])}\n\n")

    # 7. 模組獨立性
    report.append(f"## 7️⃣ {t('module_independence_title')}\n\n")
    mi = metrics['module_independence']
    report.append(f"- **{t('total_checks')}**: {mi['total_checks']}")
    report.append(f"- **{t('passed_checks')}**: {mi['passed_checks']}")
    report.append(f"- **{t('independence_rate')}**: {format_percentage(mi['independence_rate'])}\n\n")

    # 總結
    report.append("---\n\n")
    report.append(f"## 📈 {t('metrics_summary')}\n\n")
    report.append(f"| {t('metric_category')} | {t('score')} | {t('status')} |\n")
    report.append("|---------|------|------|\n")

    indicators = [
        (t('structure_coverage'), sc['overall_coverage'] * 100, '✅' if sc['overall_coverage'] >= 0.95 else '⚠️' if sc['overall_coverage'] >= 0.8 else '❌'),
        (t('file_coverage'), fc['coverage_rate'] * 100, '✅' if fc['coverage_rate'] >= 0.95 else '⚠️' if fc['coverage_rate'] >= 0.8 else '❌'),
        (t('directory_coverage'), dc['coverage_rate'] * 100, '✅' if dc['coverage_rate'] >= 0.95 else '⚠️' if dc['coverage_rate'] >= 0.8 else '❌'),
        (t('template_accuracy'), ta['accuracy_rate'] * 100, '✅' if ta['accuracy_rate'] >= 0.9 else '⚠️' if ta['accuracy_rate'] >= 0.7 else '❌'),
        (t('hierarchy_accuracy'), ha['overall_accuracy'] * 100, '✅' if ha['overall_accuracy'] >= 0.9 else '⚠️' if ha['overall_accuracy'] >= 0.7 else '❌'),
        (t('annotation_preservation'), ap['preservation_rate'] * 100, '✅' if ap['preservation_rate'] >= 0.8 else '⚠️' if ap['preservation_rate'] >= 0.6 else '❌'),
        (t('module_independence'), mi['independence_rate'] * 100, '✅' if mi['independence_rate'] >= 0.9 else '⚠️' if mi['independence_rate'] >= 0.7 else '❌'),
    ]

    for name, score, status in indicators:
        report.append(f"| {name} | {score:.2f}% | {status} |\n")

    report.append(f"\n**{t('overall_score')}**: {overall_score:.2f}/100\n")

    if overall_score >= 90:
        report.append(f"\n✅ **{t('excellent')}** - {t('excellent_desc')}\n")
    elif overall_score >= 80:
        report.append(f"\n⚠️ **{t('good')}** - {t('good_desc')}\n")
    elif overall_score >= 70:
        report.append(f"\n⚠️ **{t('pass')}** - {t('pass_desc')}\n")
    else:
        report.append(f"\n❌ **{t('fail')}** - {t('fail_desc')}\n")

    report_text = ''.join(report)

    if output_file:
        Path(output_file).write_text(report_text, encoding='utf-8')
        print(f"[OK] {t('report_generated')}: {output_file}")
    else:
        print(report_text)

    return report_text


def main():
    parser = argparse.ArgumentParser(description="生成專案結構驗證指標")
    parser.add_argument('--structure', type=str, default='structure_example.md', help='結構定義文件')
    parser.add_argument('--generated', type=str, required=True, help='生成的專案路徑')
    parser.add_argument('--output', type=str, help='輸出報告文件（不含語言後綴）')
    parser.add_argument('--json', action='store_true', help='輸出 JSON 格式')
    parser.add_argument('--lang', type=str, default=DEFAULT_LANG,
                       choices=[LANG_EN, LANG_ZH_CN, LANG_ZH_TW],
                       help='語言選擇: en, zh-CN, zh-TW (預設: zh-TW)')
    parser.add_argument('--all-langs', action='store_true',
                       help='生成所有語言版本的報告')

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
            if args.all_langs:
                # 生成所有語言版本
                languages = [LANG_ZH_TW, LANG_ZH_CN, LANG_EN]
                for lang in languages:
                    if args.output:
                        output_file = args.output.replace('.md', '') + get_lang_suffix(lang) + '.md'
                    else:
                        output_file = f"METRICS{get_lang_suffix(lang)}.md"
                    generate_report(metrics, output_file, lang)
            else:
                # 生成單一語言版本
                if args.output:
                    output_file = args.output.replace('.md', '') + get_lang_suffix(args.lang) + '.md'
                else:
                    output_file = f"METRICS{get_lang_suffix(args.lang)}.md"
                generate_report(metrics, output_file, args.lang)

    except Exception as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
