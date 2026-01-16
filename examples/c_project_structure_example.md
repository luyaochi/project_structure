c-app/
├─ README.md                         ← 專案說明
├─ Makefile                          ← 建置腳本
├─ .gitignore
│
├─ include/                          ← 公開 Header（API）
│  ├─ app.h
│  ├─ core.h
│  └─ utils.h
│
├─ src/
│  ├─ main.c                         ← 程式進入點
│  │
│  ├─ app/                           ← 應用層（流程 / use case）
│  │  ├─ app.c
│  │  └─ app.h
│  │
│  ├─ core/                          ← 核心邏輯
│  │  ├─ core.c
│  │  └─ core.h
│  │
│  ├─ infra/                         ← 平台 / IO / OS
│  │  ├─ infra.c
│  │  └─ infra.h
│  │
│  └─ utils/                         ← 工具函式
│     ├─ logger.c
│     └─ logger.h
│
├─ tests/
│  ├─ test_core.c
│  └─ test_utils.c
│
├─ build/                            ← 編譯輸出（ignored）
│
└─ docs/
   ├─ architecture.md                ← 架構說明
   └─ decisions/
      └─ adr_001_initial_design.md
