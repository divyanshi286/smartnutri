# SmartNutri v3 — Vite + React Frontend

A complete, production-grade React web app built from the SmartNutri HTML design system.
Uses **TanStack Query** for server state, **Zustand** for client state, and **CSS Modules** for scoped styling.

---

## 🚀 Quick Start

```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # production build
npm run preview    # preview production build
```

---

## 📁 Folder Structure

```
smartnutri-vite/
├── index.html                          # Vite entry with Google Fonts
├── vite.config.js                      # Path aliases (@, @components, @ui, etc.)
├── package.json
│
└── src/
    ├── main.jsx                        # ReactDOM root + QueryClientProvider
    ├── App.jsx                         # Theme/dark class application
    │
    ├── styles/
    │   └── globals.css                 # All CSS tokens, themes, dark mode, resets
    │
    ├── api/
    │   └── index.js                    # Mock API layer (swap for real endpoints)
    │                                   # fetchDashboard, fetchMeals, fetchProgress,
    │                                   # fetchNutrition, fetchCycle, fetchModules,
    │                                   # fetchParentDashboard, sendChatMessage
    │
    ├── hooks/
    │   └── useQueries.js               # All TanStack Query hooks
    │                                   # useDashboard, useMeals, useProgress,
    │                                   # useNutrition, useCycle, useModules,
    │                                   # useParentDashboard, useSendChat (mutation)
    │
    ├── store/
    │   └── index.js                    # Zustand store (persisted to localStorage)
    │                                   # theme, dark, user, nutrition, meals,
    │                                   # cycle, chat messages, badges, onboarding
    │
    └── components/
        ├── ui/
        │   ├── index.jsx               # All shared UI primitives (barrel export)
        │   │                           # Card, CardHeader, CardBody
        │   │                           # BtnPrimary, BtnSecondary, BtnGhost, IconBtn
        │   │                           # GoalRing, ProgressBar, Badge, StatCard
        │   │                           # Chip, AiNote, MealCard, Skeleton, Tag
        │   └── ui.module.css
        │
        ├── layout/
        │   ├── AppShell.jsx            # Root layout: Sidebar + Topbar + Page router
        │   ├── AppShell.module.css
        │   ├── Sidebar.jsx             # Fixed sidebar: nav, user, theme switcher, dark toggle
        │   ├── Sidebar.module.css
        │   ├── Topbar.jsx              # Sticky topbar with title and actions
        │   └── Topbar.module.css
        │
        └── features/
            ├── VoiceModal.jsx          # Shared voice input overlay
            ├── VoiceModal.module.css
            │
            ├── dashboard/
            │   ├── Dashboard.jsx       # Hero, goal rings, AI nudge, meal list, progress
            │   └── Dashboard.module.css
            │
            ├── chat/
            │   ├── Chat.jsx            # AI chat with TanStack mutation, safety detection
            │   └── Chat.module.css
            │
            ├── meals/
            │   ├── Meals.jsx           # Meal timeline with swipe, daily targets
            │   └── Meals.module.css
            │
            ├── progress/
            │   ├── Progress.jsx        # Weekly bar chart, stats grid, achievements
            │   └── Progress.module.css
            │
            ├── nutrition/
            │   ├── Nutrition.jsx       # Macro donut, PCOS micronutrients, food boosts
            │   └── Nutrition.module.css
            │
            ├── cycle/
            │   ├── Cycle.jsx           # Phase banner, eat/avoid foods, mood picker
            │   └── Cycle.module.css
            │
            ├── education/
            │   ├── Education.jsx       # Active module, quiz with feedback, module list
            │   └── Education.module.css
            │
            ├── safety/
            │   ├── Safety.jsx          # Safety intervention demo, SOS resources
            │   └── Safety.module.css
            │
            ├── onboarding/
            │   ├── Onboarding.jsx      # Step progress, goal selection (persisted)
            │   └── Onboarding.module.css
            │
            ├── parent/
            │   ├── Parent.jsx          # Family dashboard, child switcher, privacy bounds
            │   └── Parent.module.css
            │
            └── design/                 # Design system documentation pages
                ├── Components.jsx      # Component library showcase
                ├── StyleGuide.jsx      # Theme palettes + typography scale
                ├── Gestures.jsx        # Interactive gesture demos
                ├── PrivacyDoc.jsx      # Privacy principles + accessibility annotations
                └── Design.module.css   # Shared CSS for all design pages
```

---

## 🎨 Design System

### 4 Themes (toggled via Sidebar)
| Theme         | Key Color | For          |
|---------------|-----------|--------------|
| 🌿 Miso Sage   | `#3d7a5c` | Adults       |
| 💪 Neon Slate  | `#0ea5e9` | Teen Boys    |
| 🌸 Petal Aurora| `#e879a0` | Teen Girls (Hormonal) |
| ⚡ Ember Reef  | `#f97316` | Teen Girls (Athletic) |

All themes + dark mode via CSS custom properties on `<body>`.

### Fonts
- **Fraunces** — display/headings (variable weight + optical size)
- **Geist** — body text (300–800)
- **Caveat** — handwriting annotations

---

## ⚡ TanStack Query — Data Layer

### Query Hooks (src/hooks/useQueries.js)
```js
const { data, isLoading } = useDashboard()
const { data, isLoading } = useMeals(date)
const { data, isLoading } = useProgress()
const { data, isLoading } = useNutrition()
const { data, isLoading } = useCycle()
const { data, isLoading } = useModules()
const { data, isLoading } = useParentDashboard(childName)
const { mutateAsync, isPending } = useSendChat()
```

### Swap for Real API
All fetch functions are in `src/api/index.js`. Replace the `delay()` mock with real `fetch()` calls:
```js
export const fetchDashboard = async () => {
  const res = await fetch('/api/dashboard')
  return res.json()
}
```

---

## 🗂 Zustand Store (src/store/index.js)

Persisted keys: `theme`, `dark`, `user`, `nutrition`, `meals`, `cycle`, `badges`, `onboarding`

```js
const { theme, setTheme, dark, toggleDark } = useAppStore()
const { activePage, setActivePage } = useAppStore()
const { messages, addMessage } = useAppStore()
const { cycle, setMood } = useAppStore()
```

---

## 🔐 Path Aliases

Configured in `vite.config.js`:

| Alias           | Path                           |
|-----------------|--------------------------------|
| `@`             | `src/`                         |
| `@components`   | `src/components/`              |
| `@ui`           | `src/components/ui/`           |
| `@layout`       | `src/components/layout/`       |
| `@features`     | `src/components/features/`     |
| `@hooks`        | `src/hooks/`                   |
| `@store`        | `src/store/`                   |
| `@lib`          | `src/lib/`                     |
| `@styles`       | `src/styles/`                  |
| `@data`         | `src/data/`                    |
| `@api`          | `src/api/`                     |
