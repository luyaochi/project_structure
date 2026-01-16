好，下面是你**剛剛那一整份內容的「完整、等價、可直接使用」簡體中文版本**。
你可以**直接整段複製**，存成：

```
docs/README.zh-CN.md
```

即可。

---

````markdown
# 项目结构生成器

根据 README.md 中的树状结构描述，自动生成完整的项目目录和文件。

---

## 功能特色

- 📖 解析 README.md 中的树状结构图
- 🔨 自动生成目录结构
- 📄 为不同类型的文件生成模板（Python、Markdown、配置文件等）
- 🎯 支持注释和说明
- 🧪 支持预览模式（dry-run）

---

## 安装

```bash
# 安装依赖（如有需要）
pip install -e .
````

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

```bash
# 生成项目
python -m src.main --readme structure_example.md --output my_project

# 生成验证指标报告
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md
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

---

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试（如有）
pytest
```

---

## 授权

MIT License

```

---

