# Project Structure Generator

Automatically generate complete project directories and files based on tree structure descriptions in README.md.

## Features

- 📖 Parse tree structure diagrams in README.md
- 🔨 Automatically generate directory structures
- 📄 Generate templates for different file types (Python, Markdown, config files, etc.)
- 🎯 Support annotations and descriptions
- 🧪 Support dry-run mode for preview
- 🌐 Multi-language report generation (English, Simplified Chinese, Traditional Chinese)

## Installation

```bash
# Install dependencies (if needed)
pip install -e .
```

## Usage

### Basic Usage

```bash
python -m src.main
```

### Specify README File

```bash
python -m src.main --readme my_structure.md
```

### Specify Output Directory

```bash
python -m src.main --output ./my_project
```

### Preview Mode (Dry-run)

```bash
python -m src.main --dry-run
```

### Complete Parameters

```bash
python -m src.main \
  --readme README.md \
  --output output \
  --project-name my_project \
  --dry-run
```

### Generate Project and Auto-generate Reports

```bash
# Generate project and generate English reports (default)
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports

# Generate project and generate all language versions of reports
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --all-langs

# Generate project and generate Simplified Chinese reports
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-lang zh-CN

# Generate project and specify report output directory
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-output reports
```

### Generate Reports Directly (Without Generating Project)

```bash
# Generate all language versions of reports directly
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --all-langs

# Generate English reports directly
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --report-lang en
```

## README.md Format

The generator parses tree structures in README.md, supporting the following format:

```
system/
└─ project1/
   ├─ README.md
   ├─ docs/
   │  ├─ 00_overview.md
   │  └─ decisions/
   │     └─ adr_001.md
   │
   ├─ core/                          ← 🧠 Business Core (standalone package)
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     └─ core/
   │        ├─ id.py
   │        └─ errors.py
```

### Format Rules

1. Use tree symbols: `├─`, `└─`, `│` to represent hierarchy
2. Support annotations: Use `←` symbol to add descriptions
3. Auto-detect file types: Determine files or directories based on extensions
4. Auto-generate templates: Generate initial templates for `.py`, `.md`, `pyproject.toml`, `package.json`, etc.

## Generated File Types

### Python Files (.py)
Generate Python file templates with basic structure.

### Markdown Files (.md)
Generate Markdown files with titles and annotations.

### pyproject.toml
Generate standard `pyproject.toml` configuration files for Python projects.

### package.json
Generate `package.json` configuration files for frontend projects.

### README.md
Automatically generate README.md files for each directory.

## Project Structure

```
.
├── README.md              # This file
├── pyproject.toml         # Python project configuration
├── .gitignore            # Git ignore file
└── src/
    ├── main.py           # Main program entry
    ├── structure_parser.py  # Structure parser
    └── project_generator.py # Project generator
```

## Examples

The project includes a complete example structure file `structure_example.md` that demonstrates complex project structures.

### Quick Test

```bash
# Generate project using example structure file
python -m src.main --readme structure_example.md --output my_project

# Preview structure to be generated (without actually creating files)
python -m src.main --readme structure_example.md --dry-run
```

### Simple Example

If your structure file contains:

```
my_project/
├─ src/
│  └─ main.py
└─ tests/
   └─ test_main.py
```

After running the generator, it will create:

```
output/
└─ my_project/
   ├─ README.md
   ├─ src/
   │  └─ main.py
   └─ tests/
      └─ test_main.py
```

## Verification Metrics

The generator includes a complete verification metrics system to evaluate the quality of generated results:

### Using main.py to Generate Reports

```bash
# Generate project and auto-generate reports
python -m src.main \
  --readme structure_example.md \
  --output my_project \
  --generate-reports \
  --all-langs
```

### Using Standalone Report Generators

```bash
# Generate metrics report (English)
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang en

# Generate metrics report (all language versions)
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --all-langs

# Generate metrics report (Simplified Chinese)
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang zh-CN

# Generate JSON format report
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output metrics.json \
  --json
```

### Generate Verification Report

```bash
# Generate verification report (all language versions)
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --all-langs

# Generate verification report (single language)
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --lang en
```

### Generate Conclusion Report

```bash
# Generate conclusion report (all language versions)
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --all-langs

# Generate conclusion report (single language)
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --lang en
```

### Metric Categories

1. **Structure Coverage** - Evaluate directory and file coverage
2. **File Coverage** - Evaluate expected file generation
3. **Directory Coverage** - Evaluate expected directory generation
4. **Template Accuracy** - Evaluate template quality of generated files
5. **Hierarchy Accuracy** - Evaluate three-level structure (project/module/feature) correctness
6. **Annotation Preservation** - Evaluate annotation retention
7. **Module Independence** - Evaluate independence of each module

Detailed metric reports will be generated in `METRICS.md` files.

### Multi-language Support

All reports support three languages:
- Traditional Chinese (zh-TW) - Default, filename: `METRICS.md`
- Simplified Chinese (zh-CN) - Filename: `METRICS.zh-CN.md`
- English (en) - Filename: `METRICS.en.md`

Reports are generated in the `reports/` directory by default. You can use the `--report-output` parameter to specify a different directory.

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## License

MIT License
