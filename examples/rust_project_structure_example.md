rust-app/
├─ README.md                         ← 專案說明
├─ Cargo.toml                        ← Cargo 專案設定
├─ Cargo.lock
├─ .gitignore
│
├─ src/
│  ├─ main.rs                        ← 程式進入點（binary）
│  ├─ lib.rs                         ← Library root
│  │
│  ├─ app/                           ← 應用層（use cases）
│  │  ├─ mod.rs
│  │  └─ run.rs
│  │
│  ├─ domain/                        ← 核心領域模型
│  │  ├─ mod.rs
│  │  ├─ entity.rs
│  │  └─ error.rs
│  │
│  ├─ infra/                         ← 基礎設施層
│  │  ├─ mod.rs
│  │  └─ repository.rs
│  │
│  └─ utils/
│     ├─ mod.rs
│     └─ logger.rs
│
├─ tests/
│  └─ integration_test.rs
│
└─ docs/
   ├─ architecture.md                ← 架構說明
   └─ decisions/
      └─ adr_001_initial_design.md
