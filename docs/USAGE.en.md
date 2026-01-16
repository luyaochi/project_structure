好，下面是你這一整段 **「使用指南」的專業英文版本**，語氣偏 **technical documentation / user guide**，可直接放在 `docs/USAGE.md`、`docs/README.en.md` 的 Usage 區塊，或主 README 的下半段。

你可以**原封不動複製使用**。

---

````markdown
# Usage Guide

## Quick Start

### 1. Define the Project Structure

Define your project structure in `README.md`, for example:

```text
system/
└─ project1/
   ├─ README.md
   ├─ core/
   │  └─ src/
   │     └─ main.py
   └─ backend/
      └─ api/
         └─ routes.py
````

### 2. Run the Generator

```bash
python -m src.main
```

### 3. Inspect the Generated Project

The generated project will be created in the `output/` directory.

---

## Advanced Usage

### Custom Templates

You can customize the generated file contents by modifying the template methods in `src/project_generator.py`:

* `_get_python_template()` — Python file template
* `_get_markdown_template()` — Markdown file template
* `_get_pyproject_template()` — `pyproject.toml` template
* `_get_package_json_template()` — `package.json` template

---

### Extending Supported File Types

To support additional file types, register new templates in `ProjectGenerator._load_templates()`:

```python
def _load_templates(self) -> Dict[str, str]:
    templates = {
        # ... existing templates
        '.ts': self._get_typescript_template(),
    }
    return templates
```

---

## FAQ

### Q: How are empty directories handled?

**A:** Empty directories are created automatically, and a `README.md` file is generated inside them.

---

### Q: How can I skip generating certain files?

**A:** Simply omit those files from the structure definition in `README.md`.

---

### Q: Will generated files overwrite existing ones?

**A:** No. The generator checks for existing files and only creates files that do not already exist.

---

### Q: How can I customize the project name?

**A:** Use the `--project-name` option:

```bash
python -m src.main --project-name my_custom_project
```

```

---

### ✅ 小確認（幫你定錨）


