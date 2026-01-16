system/
└─ project1/
   ├─ README.md
   ├─ docs/
   │  ├─ 00_overview.md
   │  ├─ 01_architecture.md
   │  ├─ 02_domain_model.md
   │  ├─ 03_task_flow.md
   │  ├─ 04_api_spec.md
   │  └─ decisions/
   │     ├─ adr_001_task_pool.md
   │     └─ adr_002_goal_project.md
   │
   ├─ core/                          ← 🧠 商業核心（可獨立套件）
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     ├─ core/
   │     │  ├─ id.py
   │     │  ├─ time.py
   │     │  ├─ result.py
   │     │  └─ errors.py
   │     │
   │     └─ domain/
   │        ├─ goal.py
   │        ├─ project.py
   │        └─ task.py
   │
   ├─ backend/                       ← 🔌 API / Orchestration
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     ├─ core/
   │     │  ├─ api_error.py
   │     │  ├─ auth.py
   │     │  └─ config.py
   │     │
   │     ├─ domain/
   │     │  ├─ core/
   │     │  ├─ goal/
   │     │  ├─ project/
   │     │  └─ task/
   │     │
   │     ├─ infra/
   │     │  ├─ core/
   │     │  ├─ db/
   │     │  └─ repositories/
   │     │
   │     ├─ api/
   │     │  ├─ main.py
   │     │  └─ routes/
   │     │
   │     └─ tests/
   │
   ├─ jobs/                          ← ⏱ 背景任務 / 排程（可獨立 worker）
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     ├─ core/                    ← jobs 共用核心（排程 / retry）
   │     │  ├─ job_base.py
   │     │  ├─ scheduler.py
   │     │  └─ retry_policy.py
   │     │
   │     ├─ tasks/
   │     │  ├─ generate_tasks.py     ← 目標 → 任務批次生成
   │     │  ├─ archive_projects.py   ← 專案歸檔
   │     │  ├─ cleanup_tasks.py      ← 清理任務池
   │     │  └─ reminders.py          ← 到期提醒
   │     │
   │     ├─ adapters/
   │     │  ├─ core_adapter.py       ← 呼叫 core domain
   │     │  └─ backend_adapter.py    ← 呼叫 backend API（可選）
   │     │
   │     └─ tests/
   │
   ├─ cli/                           ← 🧰 指令工具（管理 / 開發）
   │  ├─ README.md
   │  ├─ pyproject.toml
   │  └─ src/
   │     ├─ core/
   │     │  ├─ command_base.py
   │     │  └─ output.py
   │     │
   │     ├─ commands/
   │     │  ├─ goal_create.py        ← 建立目標
   │     │  ├─ project_plan.py       ← 規劃專案
   │     │  ├─ task_import.py        ← 匯入任務到任務池
   │     │  └─ status_report.py      ← 狀態總覽
   │     │
   │     ├─ adapters/
   │     │  ├─ core_adapter.py
   │     │  └─ backend_adapter.py
   │     │
   │     └─ main.py                  ← cli 入口
   │
   └─ frontend/                      ← 🖥 前端 App
      ├─ README.md
      ├─ package.json
      └─ src/
         ├─ core/
         ├─ pages/
         ├─ components/
         ├─ services/
         └─ tests/
