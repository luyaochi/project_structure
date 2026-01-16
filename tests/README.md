# 測試說明

本目錄包含專案結構生成器的測試套件。

## 測試結構

- `test_structure_parser.py` - 測試結構解析器
- `test_project_generator.py` - 測試專案生成器
- `test_verification_metrics.py` - 測試驗證指標計算
- `test_generate_metrics.py` - 測試指標報告生成
- `test_i18n.py` - 測試多語言模組
- `test_main.py` - 測試主程式

## 執行測試

### 執行所有測試
```bash
python -m pytest tests/
```

或使用 unittest:
```bash
python -m unittest discover tests
```

### 執行特定測試
```bash
python -m pytest tests/test_structure_parser.py
```

### 執行特定測試類別
```bash
python -m pytest tests/test_structure_parser.py::TestStructureParser
```

### 執行特定測試方法
```bash
python -m pytest tests/test_structure_parser.py::TestStructureParser::test_parse_simple_structure
```

## 測試覆蓋率

安裝 coverage:
```bash
pip install coverage
```

執行測試並生成覆蓋率報告:
```bash
coverage run -m pytest tests/
coverage report
coverage html  # 生成 HTML 報告
```

## 注意事項

- 測試會創建臨時目錄和文件，測試結束後會自動清理
- 某些測試可能需要特定的文件結構，請確保測試環境正確設置
