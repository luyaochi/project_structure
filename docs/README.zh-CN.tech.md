# 项目结构生成器

根据 README.md 中的树状结构描述，自动生成完整的项目目录和文件。

---

## 功能特色

- 📖 解析 README.md 中的树状结构图
- 🔨 自动生成目录结构
- 📄 为不同类型的文件生成模板（Python、Markdown、配置文件等）
- 🎯 支持注释和说明
- 🧪 支持预览模式（dry-run）
- 🌐 多语言报告生成（英文、简体中文、繁体中文）

---

## 安装

```bash
# 安装依赖（如有需要）
pip install -e .
```

---

## 使用方法

### 基本使用

```bash
python -m src.main
```

### 指定 README 文件

```bash
python -m src.main --readme my_structure.md
```

### 指定输出目录

```bash
python -m src.main --output ./my_project
```

### 预览模式（不实际创建文件）

```bash
python -m src.main --dry-run
```

### 完整参数示例

```bash
python -m src.main \
  --readme README.md \
  --output output \
  --project-name my_project \
  --dry-run
```

### 生成项目并自动生成报告

```bash
# 生成项目并生成简体中文报告
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-lang zh-CN

# 生成项目并生成所有语言版本的报告
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --all-langs

# 生成项目并指定报告输出目录
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-output reports
```

### 直接生成报告（不生成项目）

```bash
# 直接生成所有语言版本的报告
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --all-langs

# 直接生成英文报告
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --report-lang en
```

---

## README.md 格式说明

生成器会解析 README.md 中的树状结构，支持以下格式：

```text
system/
└─ project1/
   ├─ README.md
   ├─ docs/
   │  ├─ 00_overview.md
   │  └─ decisions/
   │     └─ adr_001.md
   │
   ├─ core/                          ← 🧠 业务核心（可独立为套件）
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     └─ core/
   │        ├─ id.py
   │        └─ errors.py
```

---

## 格式规则

1. 使用树状符号：`├─`, `└─`, `│` 表示层级关系
2. 支持注释：使用 `←` 符号添加说明
3. 自动识别文件类型：根据扩展名判断是文件或目录
4. 自动生成模板：为 `.py`、`.md`、`pyproject.toml`、`package.json` 等生成初始模板

---

## 生成的文件类型

### Python 文件（.py）

生成包含基础结构的 Python 文件模板。

### Markdown 文件（.md）

生成包含标题和注释说明的 Markdown 文件。

### pyproject.toml

为 Python 项目生成标准的 `pyproject.toml` 配置文件。

### package.json

为前端项目生成 `package.json` 配置文件。

### README.md

为每个目录自动生成对应的 README.md 说明文件。

---

## 项目结构

```text
.
├── README.md                 # 本文件
├── pyproject.toml            # Python 项目配置
├── .gitignore                # Git 忽略文件
└── src/
    ├── main.py               # 主程序入口
    ├── structure_parser.py   # 结构解析器
    └── project_generator.py  # 项目生成器
```

---

## 示例

项目中包含一个完整的示例结构文件 `structure_example.md`，用于展示较复杂的项目结构。

### 快速测试

```bash
# 使用示例结构文件生成项目
python -m src.main --readme structure_example.md --output my_project

# 预览将要生成的结构（不实际创建文件）
python -m src.main --readme structure_example.md --dry-run
```

---

### 简单示例

假设你的结构文件包含：

```text
my_project/
├─ src/
│  └─ main.py
└─ tests/
   └─ test_main.py
```

执行生成器后，将创建：

```text
output/
└─ my_project/
   ├─ README.md
   ├─ src/
   │  └─ main.py
   └─ tests/
      └─ test_main.py
```

---

## 验证指标

生成器包含完整的验证指标系统，用于评估生成结果的质量：

### 使用 main.py 生成报告

```bash
# 生成项目并自动生成报告
python -m src.main \
  --readme structure_example.md \
  --output my_project \
  --generate-reports \
  --all-langs
```

### 使用独立的报告生成器

```bash
# 生成指标报告（简体中文）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang zh-CN

# 生成指标报告（所有语言版本）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --all-langs

# 生成指标报告（英文）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang en

# 生成 JSON 格式报告
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output metrics.json \
  --json
```

### 生成验证报告

```bash
# 生成验证报告（所有语言版本）
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --all-langs

# 生成验证报告（单一语言）
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --lang zh-CN
```

### 生成结论报告

```bash
# 生成结论报告（所有语言版本）
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --all-langs

# 生成结论报告（单一语言）
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --lang en
```

---

### 指标类别

1. **结构覆盖率**：评估目录和文件的覆盖情况
2. **文件覆盖率**：评估预期文件的生成情况
3. **目录覆盖率**：评估预期目录的生成情况
4. **模板准确性**：评估生成文件的模板质量
5. **层级准确性**：评估三层结构（项目 / 模块 / 功能）的正确性
6. **注释保留率**：评估注释说明的保留情况
7. **模块独立性**：评估各模块之间的独立程度

详细的指标报告将生成在 `METRICS.md` 文件中。

### 多语言支持

所有报告都支持三种语言：
- 繁体中文（zh-TW）- 默认，文件名为 `METRICS.md`
- 简体中文（zh-CN）- 文件名为 `METRICS.zh-CN.md`
- 英文（en）- 文件名为 `METRICS.en.md`

报告默认会生成到 `reports/` 目录中，可以使用 `--report-output` 参数指定其他目录。

---

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src --cov-report=html
```

---

## 授权

MIT License

