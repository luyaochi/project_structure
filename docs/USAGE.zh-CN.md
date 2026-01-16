好，下面是你這一整段 **「使用指南」的完整、專業、可直接使用的簡體中文版本**。
語氣是**技术文档 / 使用说明**，不是直译腔，适合放在：

* `docs/USAGE.zh-CN.md`
* 或 `docs/README.zh-CN.md` 的 Usage 部分

你可以**原封不动复制使用**。

---

````markdown
# 使用指南

## 快速开始

### 1. 定义项目结构

在你的 `README.md` 中定义项目结构，例如：

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

### 2. 运行生成器

```bash
python -m src.main
```

### 3. 查看生成结果

生成的项目将会创建在 `output/` 目录中。

---

## 进阶用法

### 自定义模板

你可以通过修改 `src/project_generator.py` 中的模板方法，自定义生成的文件内容：

* `_get_python_template()` —— Python 文件模板
* `_get_markdown_template()` —— Markdown 文件模板
* `_get_pyproject_template()` —— `pyproject.toml` 模板
* `_get_package_json_template()` —— `package.json` 模板

---

### 扩展支持的文件类型

如需支持新的文件类型，可在 `ProjectGenerator._load_templates()` 中注册新的模板：

```python
def _load_templates(self) -> Dict[str, str]:
    templates = {
        # ... 现有模板
        '.ts': self._get_typescript_template(),
    }
    return templates
```

---

## 常见问题（FAQ）

### Q：如何处理空目录？

**A：** 空目录会自动创建，并在目录中生成一个 `README.md` 文件。

---

### Q：如何跳过生成某些文件？

**A：** 只需在 `README.md` 的结构定义中不包含这些文件即可。

---

### Q：生成的文件会覆盖已有文件吗？

**A：** 不会。生成器会检查文件是否已存在，仅在文件不存在时才会创建。

---

### Q：如何自定义项目名称？

**A：** 使用 `--project-name` 参数：

```bash
python -m src.main --project-name my_custom_project
```

```

---


