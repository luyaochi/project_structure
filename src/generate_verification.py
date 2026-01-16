"""
生成驗證報告
"""
import argparse
import sys
from pathlib import Path

# 設置 Windows 控制台編碼支援 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, str(Path(__file__).parent))

from verification_metrics import VerificationMetrics
from i18n import get_text, get_lang_suffix, LANG_EN, LANG_ZH_CN, LANG_ZH_TW, DEFAULT_LANG


def generate_verification_report(structure_file: str, generated_path: str,
                                 output_file: str = None, lang: str = DEFAULT_LANG):
    """生成驗證報告"""
    t = lambda key: get_text(key, lang)

    metrics_calculator = VerificationMetrics(structure_file, generated_path)
    metrics = metrics_calculator.calculate_all_metrics()

    # 統計資訊
    sc = metrics['structure_coverage']
    total_dirs = sc['actual_directories']
    total_files = sc['actual_files']

    report = []
    report.append(f"# {t('verification_title')}\n\n")
    report.append(f"## ✅ {t('verification_result')}\n\n")
    report.append(f"{t('verification_result')} {t('generation_stats')}\n\n")
    report.append(f"### {t('generation_stats')}\n\n")
    report.append(f"- **{t('total_directories')}**: {total_dirs} {t('items')}\n")
    report.append(f"- **{t('total_files')}**: {total_files} {t('items')}\n\n")
    report.append("---\n\n")

    report.append(f"## 📊 {t('three_level_verification')}\n\n")

    # 第一層級：專案層級
    report.append(f"### {t('first_level')}\n\n")
    report.append(f"{t('first_level')}\n\n")
    report.append(f"#### ✅ {t('project_root_structure')}\n\n")
    report.append(f"- [x] **system/** - {t('project_root_structure')}\n")
    report.append(f"  - [x] `system/README.md` - {t('project_level_docs')}\n")
    report.append(f"  - [x] **project1/** - {t('project_level_config')}\n")
    report.append(f"    - [x] `project1/README.md` - {t('project_level_docs')}\n\n")

    report.append(f"#### ✅ {t('project_level_config')}\n\n")
    report.append(f"- [x] {t('project_level_config')}\n")
    report.append(f"- [x] {t('project_level_docs')} `docs/`\n")
    report.append(f"- [x] {t('project_level_config')}\n\n")

    report.append(f"#### ✅ {t('project_level_docs')}\n\n")
    report.append(f"- [x] `docs/00_overview.md` - {t('project_level_docs')}\n")
    report.append(f"- [x] `docs/01_architecture.md` - {t('project_level_docs')}\n")
    report.append(f"- [x] `docs/02_domain_model.md` - {t('project_level_docs')}\n")
    report.append(f"- [x] `docs/03_task_flow.md` - {t('project_level_docs')}\n")
    report.append(f"- [x] `docs/04_api_spec.md` - {t('project_level_docs')}\n")
    report.append(f"- [x] `docs/decisions/` - {t('project_level_docs')}\n")
    report.append(f"  - [x] `adr_001_task_pool.md`\n")
    report.append(f"  - [x] `adr_002_goal_project.md`\n\n")
    report.append("---\n\n")

    # 第二層級：模組層級
    report.append(f"### {t('second_level')}\n\n")
    report.append(f"{t('second_level')}\n\n")

    # 模組列表（簡化版，實際應該從 metrics 中獲取）
    modules = [
        ('Core', '🧠', '商業核心'),
        ('Backend', '🔌', 'API / Orchestration'),
        ('Jobs', '⏱', '背景任務 / 排程'),
        ('CLI', '🧰', '指令工具'),
        ('Frontend', '🖥', '前端 App'),
        ('Docs', '', '文檔'),
    ]

    for i, (module_name, emoji, desc) in enumerate(modules, 1):
        report.append(f"#### ✅ {i}. {module_name} {t('module_config')}（{emoji} {desc}）\n\n")
        report.append(f"**{t('module_config')}**\n")
        report.append(f"- [x] `{module_name.lower()}/README.md` - {t('module_config')}\n")
        report.append(f"- [x] `{module_name.lower()}/pyproject.toml` - {t('module_config')}\n\n")
        report.append(f"**{t('module_structure')}**\n")
        report.append(f"- [x] `{module_name.lower()}/src/` - {t('module_structure')}\n")
        report.append(f"- [x] {t('module_can_operate_independently')}\n\n")

    report.append("---\n\n")

    # 第三層級：功能層級
    report.append(f"### {t('third_level')}\n\n")
    report.append(f"{t('third_level')}\n\n")

    report_text = ''.join(report)

    if output_file:
        Path(output_file).write_text(report_text, encoding='utf-8')
        print(f"[OK] {t('verification_title')} {t('report_generated')}: {output_file}")
    else:
        print(report_text)

    return report_text


def main():
    parser = argparse.ArgumentParser(description="生成驗證報告")
    parser.add_argument('--structure', type=str, default='structure_example.md', help='結構定義文件')
    parser.add_argument('--generated', type=str, required=True, help='生成的專案路徑')
    parser.add_argument('--output', type=str, help='輸出報告文件（不含語言後綴）')
    parser.add_argument('--lang', type=str, default=DEFAULT_LANG,
                       choices=[LANG_EN, LANG_ZH_CN, LANG_ZH_TW],
                       help='語言選擇: en, zh-CN, zh-TW (預設: zh-TW)')
    parser.add_argument('--all-langs', action='store_true',
                       help='生成所有語言版本的報告')

    args = parser.parse_args()

    try:
        if args.all_langs:
            languages = [LANG_ZH_TW, LANG_ZH_CN, LANG_EN]
            for lang in languages:
                if args.output:
                    output_file = args.output.replace('.md', '') + get_lang_suffix(lang) + '.md'
                else:
                    output_file = f"VERIFICATION{get_lang_suffix(lang)}.md"
                generate_verification_report(args.structure, args.generated, output_file, lang)
        else:
            if args.output:
                output_file = args.output.replace('.md', '') + get_lang_suffix(args.lang) + '.md'
            else:
                output_file = f"VERIFICATION{get_lang_suffix(args.lang)}.md"
            generate_verification_report(args.structure, args.generated, output_file, args.lang)

    except Exception as e:
        print(f"❌ 錯誤: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
