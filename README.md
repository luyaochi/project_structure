---

# 🚀 Project Structure Generator

> **Turn AI-designed architectures into real-world project skeletons in seconds.**
> **讓 AI 負責設計架構，讓本工具負責落地執行。**
> **让 AI 负责设计架构，让本工具负责落地执行。**


---

## 🌍 Language / 語言選擇

* [🇺🇸 English Documentation](./docs/README.en.md)
* [🇹🇼 繁體中文說明文件](./docs/README.zh-TW.md)
* [🇨🇳 简体中文说明文档](./docs/README.zh-CN.md)

---

## 🔥 Quick Start / 快速開始

### 1. Define Structure (README.md)

只需要在 Markdown 中寫下你想要的樹狀結構：

```text
my_project/
├─ src/
│  └─ main.py
└─ tests/
   └─ test_main.py

```

### 2. Run Generator

執行一行指令，直接生成實體檔案：

```bash
python -m src.main --readme README.md --output ./output

```

### 3. Result
```text
output/
└─ my_project/
   ├─ src/
   │  └─ main.py
   └─ tests/
      └─ test_main.py
---

## ✨ Why This Project? / 為什麼選擇本專案？

| Feature / 功能 | Description / 說明 |
| --- | --- |
| **AI Powered** | Designed for AI-generated architecture maps. (專為 AI 設計圖打造) |
| **Smart Templates** | Auto-fill boilerplate for `.py`, `.json`, `.md`. (自動填充代碼模板) |
| **Architecture Metrics** | Verify the integrity of the generated project. (獨家架構完整性驗證) |
| **Dry-run Support** | Preview before creating files. (支援乾跑模式，安全預覽) |

---

## 🛠️ Installation / 安裝

```bash
pip install -e .

```

## 📄 License

MIT License

---



