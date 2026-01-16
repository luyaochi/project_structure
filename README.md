---

# 🚀 Project Structure Generator

> **Turn AI-designed architectures into real-world project skeletons in seconds.**
<sub>
讓 AI 負責設計架構，讓本工具負責落地執行。
让 AI 负责设计架构，让本工具负责落地执行。
</sub>

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

### 💡 這樣調整的好處：

1. **資訊對稱**：不管使用者講什麼語言，他們都能在主頁看到表格（Feature）和代碼塊（Quick Start），這在全球通用的開發者圈子裡是非常直觀的。
2. **SEO 與 關鍵字**：在主頁保留一些英文關鍵字（如 Smart Templates, AI Powered）有助於 GitHub 的搜尋排名。
3. **引流效果**：簡單的快速預覽會讓使用者更有動力點進去 `docs/README.zh-TW.md` 看詳細說明。

