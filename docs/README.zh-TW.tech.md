# 專案結構生成器

根據 README.md 中的樹狀結構描述，自動生成完整的專案目錄和文件。

## 功能特色

- 📖 解析 README.md 中的樹狀結構圖
- 🔨 自動生成目錄結構
- 📄 為不同類型的文件生成模板（Python、Markdown、配置文件等）
- 🎯 支援註解和說明
- 🧪 支援乾跑模式（dry-run）預覽
- 🌐 多語言報告生成（英文、簡體中文、繁體中文）

## 安裝

```bash
# 安裝依賴（如果需要）
pip install -e .
```

## 使用方法

### 基本使用

```bash
python -m src.main
```

### 指定 README 文件

```bash
python -m src.main --readme my_structure.md
```

### 指定輸出目錄

```bash
python -m src.main --output ./my_project
```

### 預覽模式（不實際創建文件）

```bash
python -m src.main --dry-run
```

### 完整參數

```bash
python -m src.main \
  --readme README.md \
  --output output \
  --project-name my_project \
  --dry-run
```

### 生成專案並自動生成報告

```bash
# 生成專案並生成繁體中文報告（預設）
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports

# 生成專案並生成所有語言版本的報告
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --all-langs

# 生成專案並生成簡體中文報告
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-lang zh-CN

# 生成專案並指定報告輸出目錄
python -m src.main \
  --readme structure_example.md \
  --output output \
  --generate-reports \
  --report-output reports
```

### 直接生成報告（不生成專案）

```bash
# 直接生成所有語言版本的報告
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --all-langs

# 直接生成英文報告
python -m src.main \
  --structure structure_example.md \
  --generated output \
  --generate-reports \
  --report-lang en
```

## README.md 格式說明

生成器會解析 README.md 中的樹狀結構，支援以下格式：

```
system/
└─ project1/
   ├─ README.md
   ├─ docs/
   │  ├─ 00_overview.md
   │  └─ decisions/
   │     └─ adr_001.md
   │
   ├─ core/                          ← 🧠 商業核心（可獨立套件）
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     └─ core/
   │        ├─ id.py
   │        └─ errors.py
```

### 格式規則

1. 使用樹狀符號：`├─`, `└─`, `│` 表示層級關係
2. 支援註解：使用 `←` 符號添加註解
3. 自動識別文件類型：根據副檔名判斷是文件還是目錄
4. 自動生成模板：為 `.py`, `.md`, `pyproject.toml`, `package.json` 等生成初始模板

## 生成的文件類型

### Python 文件 (.py)
生成包含基本結構的 Python 文件模板。

### Markdown 文件 (.md)
生成包含標題和註解的 Markdown 文件。

### pyproject.toml
為 Python 專案生成標準的 `pyproject.toml` 配置文件。

### package.json
為前端專案生成 `package.json` 配置文件。

### README.md
為每個目錄自動生成 README.md 文件。

## 專案結構

```
.
├── README.md              # 本文件
├── pyproject.toml         # Python 專案配置
├── .gitignore            # Git 忽略文件
└── src/
    ├── main.py           # 主程式入口
    ├── structure_parser.py  # 結構解析器
    └── project_generator.py # 專案生成器
```

## 範例

專案中包含一個完整的範例結構文件 `structure_example.md`，展示了複雜的專案結構。

### 快速測試

```bash
# 使用範例結構文件生成專案
python -m src.main --readme structure_example.md --output my_project

# 預覽將要生成的結構（不實際創建文件）
python -m src.main --readme structure_example.md --dry-run
```

### 簡單範例

假設你的結構文件包含：

```
my_project/
├─ src/
│  └─ main.py
└─ tests/
   └─ test_main.py
```

執行生成器後，會創建：

```
output/
└─ my_project/
   ├─ README.md
   ├─ src/
   │  └─ main.py
   └─ tests/
      └─ test_main.py
```

## 驗證指標

生成器包含完整的驗證指標系統，可以評估生成結果的質量：

### 使用 main.py 生成報告

```bash
# 生成專案並自動生成報告
python -m src.main \
  --readme structure_example.md \
  --output my_project \
  --generate-reports \
  --all-langs
```

### 使用獨立的報告生成器

```bash
# 生成指標報告（繁體中文，預設）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md

# 生成指標報告（所有語言版本）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --all-langs

# 生成指標報告（簡體中文）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang zh-CN

# 生成指標報告（英文）
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output METRICS.md \
  --lang en

# 生成 JSON 格式報告
python -m src.generate_metrics \
  --structure structure_example.md \
  --generated my_project \
  --output metrics.json \
  --json
```

### 生成驗證報告

```bash
# 生成驗證報告（所有語言版本）
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --all-langs

# 生成驗證報告（單一語言）
python -m src.generate_verification \
  --structure structure_example.md \
  --generated my_project \
  --output VERIFICATION.md \
  --lang zh-CN
```

### 生成結論報告

```bash
# 生成結論報告（所有語言版本）
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --all-langs

# 生成結論報告（單一語言）
python -m src.generate_conclusion \
  --structure structure_example.md \
  --generated my_project \
  --output CONCLUSION.md \
  --lang en
```

### 指標類別

1. **結構覆蓋率** - 評估目錄和文件的覆蓋情況
2. **文件覆蓋率** - 評估預期文件的生成情況
3. **目錄覆蓋率** - 評估預期目錄的生成情況
4. **模板準確性** - 評估生成文件的模板質量
5. **層級準確性** - 評估三層級結構（專案/模組/功能）的正確性
6. **註解保留率** - 評估註解的保留情況
7. **模組獨立性** - 評估各模組的獨立性

詳細指標報告會生成在 `METRICS.md` 文件中。

### 多語言支援

所有報告都支援三種語言：
- 繁體中文（zh-TW）- 預設，檔案名為 `METRICS.md`
- 簡體中文（zh-CN）- 檔案名為 `METRICS.zh-CN.md`
- 英文（en）- 檔案名為 `METRICS.en.md`

報告預設會生成到 `reports/` 目錄中，可以使用 `--report-output` 參數指定其他目錄。

## 開發

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest

# 運行測試並生成覆蓋率報告
pytest --cov=src --cov-report=html
```

## 授權

MIT License
