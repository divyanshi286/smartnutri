# SmartNutri Frontend — Setup & Onboarding

## 🚀 Quick Start

```bash
npm install
npm run dev
# Frontend: http://localhost:5173
# Backend must be running on http://localhost:3001
```

## 🔑 Key Files

### Auth & Onboarding

| File | Purpose |
|------|---------|
| `src/api/auth.js` | Auth API client with error handling |
| `src/store/index.js` | Zustand store (auth + onboarding) |
| `src/router.jsx` | TanStack Router with auth guards |
| `src/components/layout/RootLayout.jsx` | Auth middleware + redirects |
| `src/pages/auth/LoginPage.jsx` | Login form |
| `src/pages/auth/RegisterPage.jsx` | Registration form |
| `src/pages/onboarding/*.jsx` | 6-step onboarding pages |

### Configuration

```env
# .env (frontend uses VITE_ prefix)
VITE_API_URL=http://localhost:3001
```

## 📋 Auth Flow

1. **Register** → POST `/api/auth/register` → Store JWT + navigate to `/onboarding/segment`
2. **Login** → POST `/api/auth/login` → If onboarding complete: `/dashboard`, else: resume step
3. **On App Load** → GET `/api/auth/me` → Hydrate Zustand from server
4. **Logout** → POST `/api/auth/logout` → Clear cookie + redirect to login

## 🛣️ Routes & Guards

```
/auth/login              (public)
/auth/register           (public)
/onboarding/*            (auth required, onboarding incomplete)
/dashboard & others      (auth required, onboarding complete)
```

## 🧩 Zustand Store

Persisted keys:
- `auth.isAuthenticated`
- `auth.userId`
- `onboarding.step`
- `onboarding.complete`
- `theme`, `dark`
- `selectedChild` (parent feature)

Full onboarding data lives in `onboarding.data.*` until step 5, then PATCH sent to backend.

## 🧪 Test Registration Flow

1. Navigate to `http://localhost:5173/auth/register`
2. Fill form (name, email, password, age)
3. Submit → redirects to `/onboarding/segment`
4. Select segment → navigate to `/onboarding/basics`
5. Complete all steps → `/onboarding/complete` calls PATCH
6. On success → redirects to `/dashboard`

## 🔗 Integration Points

- **Backend**: `VITE_API_URL` in .env
- **Cookies**: httpOnly, set automatically by backend
- **State**: Zustand handles all auth + onboarding state
- **Routing**: TanStack Router handles guards

## ⚠️ Notes

- Do NOT store JWT in localStorage — backend sets httpOnly cookie
- Theme changes via `setTheme()` in Zustand — automatically applied to `document.body`
- Onboarding data is NOT sent until step 5 — allows back/forward navigation
- Age in register auto-detects segment (< 18 = teen)

## 📦 Dependencies Added

```json
{
  "react-hook-form": "^7.51.0",
  "zod": "^3.22.0"
}
```

These are ready for form validation schema sharing with backend.

---

**Frontend Ready for Onboarding Testing ✅**
