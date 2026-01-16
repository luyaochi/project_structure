# 🚀 Project Structure Generator（專案結構生成器）

**讓 AI 負責設計架構，讓本工具負責落地執行。**

你是否也曾遇過這樣的情況：
AI 幫你設計出一個近乎完美的專案架構，但接下來卻得花上半小時，手動建立資料夾、初始化檔案與樣板程式碼？

**Project Structure Generator** 是一個專為
**文檔驅動開發（Documentation-Driven Development, DDD）**
所設計的工具，能將 `README.md` 中的樹狀結構描述，瞬間轉化為**真實、可執行的專案骨架**。

---

## ✨ 核心亮點

- **📖 文檔即架構**
  直接解析 Markdown 樹狀符號（如 `├─`、`└─`）。

- **🤖 AI 友善工作流**
  與 ChatGPT、Claude 等大型語言模型生成的架構設計無縫銜接。

- **📄 智慧模板生成**
  自動辨識副檔名，並為以下檔案生成具備實務意義的初始內容：
  `.py`、`.md`、`pyproject.toml`、`package.json`。

- **🛡️ 內建品質保證機制**
  提供 **Dry-run 預覽模式** 與 **架構驗證指標（Metrics）**，
  確保實體結構與原始設計高度一致。

- **🧠 設計意圖保留**
  自動提取 `← 註解`，並轉化為檔案層級說明或 README 標題，
  避免架構意圖在落地過程中流失。

---

## 🛠️ AI 協作工作流（建議使用）

1. **與 AI 設計架構**
   向大型語言模型提問，例如：
   >「請幫我設計一個【專案類型】的專案架構，並使用樹狀結構表示。」

2. **貼上結構描述**
   將 AI 產出的架構貼入 `structure.md`。

3. **生成專案**
   ```bash
   python -m src.main --readme structure.md --output ./my_new_project
   ```

### 📂 內建最佳實踐範例（Built-in Best Practices）

本工具內建多種語言與場景的**標準化參考架構**，
你可以直接將下列結構複製到 `README.md` 中使用：

* **C++ 企業級結構**
  遵循 Header / Source 分離與現代 CMake 專案慣例。

* **Rust 標準 Library / Binary 架構**
  完全符合 Cargo 生態系的最佳實踐。

* **現代前端（Vite）架構**
  清楚劃分 Services / Stores / Components。

* **大型分層系統架構**
  適用於 Monorepo 或複雜業務邏輯系統。

4. **驗證結果**
   產生架構指標報告，確保結構完整性與一致性。

---

## 🚀 快速開始

### 安裝

```bash
git clone https://github.com/luyaochi/project_structure.git
cd project_structure
pip install -e .
```

### 常用指令

| 功能說明            | 指令                                                                                 |
| --------------- | ---------------------------------------------------------------------------------- |
| **預覽結構（不建立檔案）** | `python -m src.main --dry-run`                                                     |
| **從指定文件生成**     | `python -m src.main --readme my_design.md`                                         |
| **自訂輸出路徑**      | `python -m src.main --output ./dist`                                               |
| **生成驗證報告**      | `python -m src.generate_metrics --structure structure.md --generated ./my_project` |

---

## 📊 架構驗證指標（Metrics）

這不僅僅是一個生成器，
它同時協助你在開發過程中避免**架構腐化（Architectural Drift）**：

* **結構覆蓋率**
  評估目錄與檔案是否完整生成。

* **層級準確性**
  驗證「專案 / 模組 / 功能」三層結構是否合理。

* **註解保留率**
  確保設計階段的意圖被成功保留至程式碼與文件中。

---

## 🗺️ 路線圖（Roadmap）

* [ ] **多語言支援**
  內建更多語言模板（Go、Rust、TypeScript 等）。

* [ ] **AI API 整合**
  直接於 CLI 中透過 LLM 生成架構建議。

* [ ] **GitHub Actions**
  自動檢查 PR 是否破壞既定的專案結構規範。

---

## 📄 授權

本專案採用 **MIT License**。
歡迎 Fork 與貢獻！


