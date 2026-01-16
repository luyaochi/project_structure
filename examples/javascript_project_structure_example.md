frontend-app/
├─ README.md                        ← 專案說明
├─ package.json                     ← 前端套件設定
├─ tsconfig.json                    ← TypeScript 設定
├─ vite.config.ts                   ← Vite 設定
├─ public/
│  └─ index.html
│
├─ src/
│  ├─ main.tsx                      ← 應用程式進入點
│  ├─ App.tsx                       ← 根組件
│  │
│  ├─ assets/                       ← 靜態資源
│  │  ├─ images/
│  │  └─ styles/
│  │     └─ global.css
│  │
│  ├─ components/                   ← 共用元件
│  │  ├─ Button.tsx
│  │  └─ Modal.tsx
│  │
│  ├─ pages/                        ← 頁面層（路由單位）
│  │  ├─ Home.tsx
│  │  └─ Settings.tsx
│  │
│  ├─ services/                     ← API / 外部服務
│  │  └─ api.ts
│  │
│  ├─ hooks/                        ← 自訂 Hooks
│  │  └─ useAuth.ts
│  │
│  ├─ store/                        ← 狀態管理
│  │  └─ authStore.ts
│  │
│  ├─ utils/                        ← 工具函式
│  │  └─ format.ts
│  │
│  └─ types/                        ← 型別定義
│     └─ user.ts
│
├─ tests/
│  ├─ components/
│  │  └─ Button.test.tsx
│  └─ pages/
│     └─ Home.test.tsx
│
└─ docs/
   ├─ architecture.md               ← 架構設計說明
   └─ decisions/
      └─ adr_001_frontend_stack.md
