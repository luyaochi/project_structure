cpp-app/
├─ README.md                         ← 專案說明
├─ CMakeLists.txt                    ← CMake 設定
├─ .gitignore
│
├─ include/                          ← 公開 Header（API）
│  └─ cpp_app/
│     ├─ app.hpp
│     ├─ domain.hpp
│     └─ utils.hpp
│
├─ src/
│  ├─ main.cpp                       ← 程式進入點
│  │
│  ├─ app/                           ← 應用層（use cases）
│  │  ├─ app.cpp
│  │  └─ app.hpp
│  │
│  ├─ domain/                        ← 核心領域邏輯
│  │  ├─ entity.cpp
│  │  └─ entity.hpp
│  │
│  ├─ infra/                         ← 基礎設施 / 平台
│  │  ├─ repository.cpp
│  │  └─ repository.hpp
│  │
│  └─ utils/                         ← 共用工具
│     ├─ logger.cpp
│     └─ logger.hpp
│
├─ tests/
│  ├─ CMakeLists.txt
│  ├─ test_app.cpp
│  └─ test_domain.cpp
│
├─ build/                            ← 建置輸出（ignored）
│
└─ docs/
   ├─ architecture.md                ← 架構說明
   └─ decisions/
      └─ adr_001_initial_design.md
