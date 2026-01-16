# 使用指南

## 快速開始

1. **準備結構定義文件**

   在你的 README.md 中定義專案結構，例如：

   ```
   system/
   └─ project1/
      ├─ README.md
      ├─ core/
      │  └─ src/
      │     └─ main.py
      └─ backend/
         └─ api/
            └─ routes.py
   ```

2. **運行生成器**

   ```bash
   python -m src.main
   ```

3. **查看生成的專案**

   生成的專案會在 `output/` 目錄中。

## 進階用法

### 自訂模板

你可以修改 `src/project_generator.py` 中的模板方法來自訂生成的文件內容：

- `_get_python_template()` - Python 文件模板
- `_get_markdown_template()` - Markdown 文件模板
- `_get_pyproject_template()` - pyproject.toml 模板
- `_get_package_json_template()` - package.json 模板

### 擴展文件類型

在 `ProjectGenerator._load_templates()` 中添加新的模板：

```python
def _load_templates(self) -> Dict[str, str]:
    templates = {
        # ... 現有模板
        '.ts': self._get_typescript_template(),
    }
    return templates
```

## 常見問題

### Q: 如何處理空目錄？

A: 空目錄會自動創建，並生成一個 README.md 文件。

### Q: 如何跳過某些文件？

A: 在 README.md 中不要包含這些文件即可。

### Q: 生成的文件會覆蓋現有文件嗎？

A: 不會。生成器會檢查文件是否存在，只有不存在的文件才會創建。

### Q: 如何自訂專案名稱？

A: 使用 `--project-name` 參數：

```bash
python -m src.main --project-name my_custom_project
```
