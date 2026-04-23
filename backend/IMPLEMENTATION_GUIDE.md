# SmartNutri — Complete Implementation Guide

## 📋 Overview

SmartNutri is a personalized nutrition coaching app for 4 user segments (Adult, Teen Girl Hormonal, Teen Girl Athletic, Teen Boy). This guide covers:

- **Backend**: FastAPI + MongoDB
- **Frontend**: React + Vite + TanStack Router + Zustand + TanStack Query
- **Auth Flow**: Register → Login → 5-step Onboarding → Dashboard
- **Data**: Dynamic nutrition targets, encrypted cycle data, segment-specific personalization

---

## 🚀 Quick Start

### Backend Setup

```bash
cd smartnutri-backend
pip install -r requirements.txt

# Set up MongoDB locally or via Docker:
# MongoDB: brew install mongodb-community (Mac) or Download from mongodb.com
# Or use Docker: docker run -d -p 27017:27017 --name mongodb mongo

# Edit .env with your MongoDB URL
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=<generate with: openssl rand -hex 32>
FRONTEND_URL=http://localhost:5173

# Run backend
python main.py
# Server runs on http://localhost:3001
```

### Frontend Setup

```bash
cd smartnutri-vite
npm install
npm run dev
# App runs on http://localhost:5173
```

---

## 📁 Project Structure

### Backend (`smartnutri-backend/`)

```
smartnutri-backend/
├── main.py                  # FastAPI app entry
├── requirements.txt         # Python dependencies
├── .env                     # Config (MONGO_URL, SECRET_KEY, etc.)
└── app/
    ├── database.py          # MongoDB connection + indexes
    ├── models.py            # Pydantic request/response schemas
    ├── security.py          # JWT, bcrypt, encryption (Fernet)
    ├── utils.py             # Nutrition math (Harris-Benedict, targets)
    └── routes/
        └── auth_routes.py   # Auth endpoints (register, login, onboarding, forgot-pwd, etc.)
```

### Frontend (`smartnutri-vite/smartnutri-vite/`)

```
src/
├── main.jsx                   # TanStack Query + Router setup
├── router.jsx                 # TanStack Router routes + guards
├── App.jsx                    # (Legacy — now handled by RootLayout)
├── api/
│   └── auth.js               # Auth API client (calls backend)
├── store/
│   └── index.js              # Zustand store (auth + onboarding + UI state)
├── pages/
│   ├── auth/
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   └── auth.module.css
│   ├── onboarding/
│   │   ├── OnboardingSegmentPage.jsx   (Step 1)
│   │   ├── OnboardingBasicsPage.jsx    (Step 2)
│   │   ├── OnboardingGoalPage.jsx      (Step 3)
│   │   ├── OnboardingConditionsPage.jsx (Step 4)
│   │   ├── OnboardingDietPage.jsx      (Step 5)
│   │   ├── OnboardingCompletePage.jsx  (Step 6 — final)
│   │   └── onboarding.module.css
│   └── NotFound.jsx
├── components/
│   ├── layout/
│   │   ├── RootLayout.jsx    # Auth guards + theme injection
│   │   ├── AppShell.jsx
│   │   ├── Sidebar.jsx
│   │   └── Topbar.jsx
│   ├── features/
│   │   └── ... (Dashboard, Chat, Meals, etc.)
│   └── ui/
│       └── ... (BtnPrimary, BtnGhost, etc.)
└── styles/
    └── globals.css
```

---

## 🔐 Auth Flow Diagram

```
┌─ Not Authenticated
│
├─ POST /api/auth/register
│  └─ Validate → Hash password → Create user + profile → Issue JWT
│     └─ Navigate to /onboarding/segment
│
├─ POST /api/auth/login
│  └─ Verify email → Verify password → Fetch profile → Issue JWT
│     └─ If onboardingComplete: go to /dashboard
│        Else: resume at current onboarding step
│
└─ GET /api/auth/me (on app load)
   └─ Hydrate Zustand store with user profile + nutrition targets
```

---

## 🛣️ Route Structure

### Public Routes (No Auth Required)

- `GET /auth/login` → LoginPage
- `GET /auth/register` → RegisterPage

### Onboarding Routes (Auth Required, onboardingComplete = false)

- `GET /onboarding/segment` → Choose segment (adult, teen-girl-h, teen-girl-a, teen-boy)
- `GET /onboarding/basics` → Name, weight, height, activity level
- `GET /onboarding/goal` → Primary goal (segment-specific)
- `GET /onboarding/conditions` → Conditions/cycle/sports (segment-specific)
- `GET /onboarding/diet` → Dietary preferences + allergies
- `GET /onboarding/complete` → Review + PATCH onboarding endpoint

### Dashboard Routes (Auth Required, onboardingComplete = true)

- `GET /dashboard` → Main dashboard
- `GET /chat` → AI coach chat
- `GET /meals` → Meal log
- `GET /progress` → Progress tracking
- `GET /nutrition` → Nutrition breakdown
- `GET /cycle` → Cycle tracker (if teen-girl-h)
- `GET /education` → Learning modules
- `GET /safety` → Safety resources
- `GET /parent` → Parent view (if isParent = true)

---

## 🔧 Backend Endpoints

### Authentication

#### `POST /api/auth/register`

**Request:**
```json
{
  "name": "Priya Sharma",
  "email": "priya@example.com",
  "password": "securepass123",
  "age": 23,
  "isParent": false
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid",
    "email": "priya@example.com",
    "name": "Priya Sharma",
    "segment": "adult",
    "onboardingComplete": false
  }
}
```

Sets `sn_token` cookie (httpOnly, Secure, SameSite=Strict).

---

#### `POST /api/auth/login`

**Request:**
```json
{
  "email": "priya@example.com",
  "password": "securepass123",
  "rememberMe": true
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid",
    "email": "priya@example.com",
    "name": "Priya Sharma",
    "segment": "teen-girl-h",
    "onboardingComplete": true,
    "onboardingStep": 5,
    "theme": "th-girl-h"
  }
}
```

---

#### `PATCH /api/auth/onboarding`

**Auth Required:** JWT in cookie

**Request:**
```json
{
  "segment": "teen-girl-h",
  "displayName": "Priya",
  "weight": 52,
  "height": 162,
  "activityLevel": "moderate",
  "primaryGoal": "hormone-balance",
  "conditions": ["PCOS"],
  "cycleData": {
    "lastPeriodDate": "2026-03-01",
    "cycleLength": 28,
    "symptoms": ["cramps", "fatigue"]
  },
  "dietPreferences": ["vegetarian"],
  "allergies": null,
  "indianCuisine": true
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "profile": { ...all profile fields... },
    "nutritionTargets": {
      "calories": 1750,
      "protein_g": 90,
      "carbs_g": 220,
      "fats_g": 58,
      "water_glasses": 8,
      "iron_mg": 18,
      "magnesium_mg": 310,
      "omega3_mg": 1600,
      "fiber_g": 25
    },
    "theme": "th-girl-h",
    "greeting": "Welcome, Priya! Your hormone-balanced plan is ready."
  }
}
```

**Side Effects:**
- Creates `nutrition_targets` record (server-computed based on Harris-Benedict + segment/goal modifiers)
- If `cycleData` present: creates `cycle_records` with AES-256 encrypted fields
- Sets `onboarding_complete = true`

---

#### `GET /api/auth/me`

**Auth Required:** JWT in cookie

**Response (200):**
```json
{
  "success": true,
  "data": {
    "userId": "uuid",
    "email": "priya@example.com",
    "name": "Priya Sharma",
    "segment": "teen-girl-h",
    "theme": "th-girl-h",
    "onboardingComplete": true,
    "profile": { ...full profile doc... },
    "nutritionTargets": { ...nutrition targets... }
  }
}
```

---

#### `POST /api/auth/logout`

Clears `sn_token` cookie.

---

#### `POST /api/auth/forgot-password`

**Request:**
```json
{
  "email": "priya@example.com"
}
```

Always returns 200 (never reveals user existence).

---

#### `POST /api/auth/reset-password`

**Request:**
```json
{
  "token": "jwt-signed-reset-token",
  "newPassword": "newpass123"
}
```

---

## 📊 Database Schema (MongoDB)

### `users` Collection

```javascript
{
  _id: ObjectId,
  email: "priya@example.com",           // unique
  password_hash: "bcrypt-hash",
  name: "Priya Sharma",
  age: 23,
  is_parent: false,
  last_login_at: ISODate(),
  created_at: ISODate()
}
```

### `profiles` Collection

```javascript
{
  _id: ObjectId,
  user_id: "user-uuid",                 // indexed
  segment: "teen-girl-h",
  display_name: "Priya",
  weight_kg: 52.0,
  height_cm: 162,
  activity_level: "moderate",
  primary_goal: "hormone-balance",
  conditions: ["PCOS"],
  diet_preferences: ["vegetarian"],
  allergies: null,
  indian_cuisine: true,
  sport_type: null,                     // for athletic segments
  training_frequency: null,
  onboarding_complete: true,
  onboarding_step: 5,
  created_at: ISODate(),
  updated_at: ISODate()
}
```

### `nutrition_targets` Collection

```javascript
{
  _id: ObjectId,
  user_id: "user-uuid",                 // unique indexed
  calories: 1750,
  protein_g: 90,
  carbs_g: 220,
  fats_g: 58,
  water_glasses: 8,
  iron_mg: 18.0,
  magnesium_mg: 310,
  omega3_mg: 1600,
  fiber_g: 25,
  updated_at: ISODate()
}
```

### `cycle_records` Collection (Encrypted Fields)

```javascript
{
  _id: ObjectId,
  user_id: "user-uuid",                 // indexed
  last_period_date: "encrypted-string", // AES-256
  cycle_length: 28,
  symptoms_enc: "encrypted-json-array", // AES-256
  created_at: ISODate()
}
```

---

## 🧠 Nutrition Calculation Logic

**Harris-Benedict Formula:**
```
Male:   BMR = 88.362 + (13.397 × weight_kg) + (4.799 × height_cm) - (5.677 × age)
Female: BMR = 447.593 + (9.247 × weight_kg) + (3.098 × height_cm) - (4.330 × age)

TDEE = BMR × activity_multiplier
```

**Activity Multipliers:**
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Active: 1.725
- Very Active: 1.9

**Calorie Modifiers (by goal):**
- Weight loss: TDEE × 0.85
- Weight gain: TDEE × 1.15
- Maintain/Manage condition: TDEE × 1.0
- Athletic goals: TDEE × 1.05–1.1

**Protein (by segment):**
- Athletic teens: 1.6 g/kg
- General teens: 1.2 g/kg minimum
- Athletic adults: 1.8 g/kg
- General adults: 1.6 g/kg

**Micronutrient Modifiers (PCOS example):**
- Iron: 18 mg (vs 8–18 baseline)
- Magnesium: 310 mg (vs 310–400 baseline)
- Omega-3: 1600 mg (vs 1000 baseline)

---

## 🛡️ Security Checklist

- ✅ Passwords: bcrypt cost factor 12
- ✅ Tokens: httpOnly + Secure + SameSite=Strict cookies (no localStorage)
- ✅ Cycle data: AES-256 encrypted at application layer before DB insert
- ✅ Login rate limiting: TODO (implement in FastAPI middleware)
- ✅ CORS: Only allow FRONTEND_URL origin
- ✅ Input validation: Pydantic on backend, react-hook-form + Zod on frontend
- ✅ Parent accounts: API-level enforcement (parent userId cannot access teen endpoints)

---

## 📝 Zustand Store Shape

```javascript
{
  // Theme
  theme: 'th-adult',
  dark: false,
  setTheme: (theme) => void,
  toggleDark: () => void,

  // Auth
  auth: {
    isAuthenticated: boolean,
    userId: string | null,
    email: string | null,
    token: null,
    isParent: boolean,
  },
  setAuth: (payload) => void,
  clearAuth: () => void,

  // User Profile
  user: { name, email, segment, initials } | null,
  setUser: (user) => void,
  updateUser: (patch) => void,

  // Onboarding
  onboarding: {
    step: 0–5,
    complete: boolean,
    data: {
      segment, displayName, weight, height, activityLevel,
      primaryGoal, conditions[], cycleData, sportType,
      trainingFrequency, dietPreferences[], allergies, indianCuisine
    }
  },
  setOnboardingStep: (step) => void,
  updateOnboardingData: (patch) => void,
  completeOnboarding: () => void,
  resetOnboarding: () => void,

  // UI
  activePage: string,
  voiceOpen: boolean,
  sidebarOpen: boolean,
  setActivePage: (page) => void,
  setVoiceOpen: (open) => void,
  setSidebarOpen: (open) => void,

  // Chat
  messages: [],
  addMessage: (msg) => void,

  // Meals
  meals: [],
  addMeal: (meal) => void,
  removeMeal: (id) => void,

  // Cycle
  cycle: null | object,
  setCycle: (cycle) => void,

  // Badges
  badges: [],
  setBadges: (badges) => void,

  // Parent
  selectedChild: string | null,
  setSelectedChild: (name) => void,
}
```

**Persistence:** Only `auth.isAuthenticated`, `auth.userId`, `onboarding.step`, `onboarding.complete`, `theme`, `dark`, `selectedChild` are persisted.

---

## 🚧 Frontend Auth Guards (RootLayout)

```javascript
// Public routes (no auth required)
const publicRoutes = ['/auth/login', '/auth/register']

// Onboarding redirects
if (!onboarding.complete && isDashboardRoute) {
  navigate('/onboarding/segment')
}

if (onboarding.complete && isOnboardingRoute) {
  navigate('/dashboard')
}

// Auth check & hydration
useQuery(['auth', 'me'], authApi.getMe, {
  enabled: auth.isAuthenticated,
  onSuccess: (data) => {
    setAuth(data)
    setUser(data)
    if (data.theme) setTheme(data.theme)
  }
})
```

---

## 🧪 Testing the Flow

### 1. Register
```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "age": 23,
    "isParent": false
  }'
```

### 2. Navigate to /onboarding/segment
Select segment → updates `onboarding.data.segment` in Zustand

### 3. Complete all 5 onboarding steps
Final step calls `PATCH /api/auth/onboarding`

### 4. Redirect to /dashboard
App now shows full AppShell with sidebar, topbar, content

### 5. Refresh page
RootLayout calls `GET /api/auth/me` → hydrates store from server truth

---

## 🔗 Key Integrations

- **TanStack Router**: File-based routing structure in `router.jsx`
- **TanStack Query**: `useMutation` for auth, `useQuery` for hydration
- **Zustand**: Persisted state (auth, onboarding, UI)
- **Fernet (Cryptography)**: AES-256 encryption for cycle data
- **FastAPI**: Async request handling + Pydantic validation
- **MongoDB Motor**: Async driver for MongoDB
- **JWT**: Token-based auth + httpOnly cookies

---

## 🚀 Next Steps (Not Implemented Yet)

1. **Email verification** (register endpoint)
2. **Password reset flow** (forgot-password email template)
3. **Rate limiting** (for login attempts)
4. **Segment/goal-specific oboarding UIs** (conditions, diet preferences)
5. **Meal logging API** → calculate macro targets 6. **Chat AI endpoint** → send messages to LLM
7. **Cycle tracking calculations** → phase prediction, symptom logging
8. **Progress analytics** → weekly trends, badge logic
9. **Parent view endpoints** → child data aggregation
10. **Notification system** → reminders, alerts

---

## 📧 Support

For questions or issues:
- Frontend: Check `src/api/auth.js` for API client
- Backend: Check `app/routes/auth_routes.py` for endpoint logic
- Auth: Check `app/security.py` for JWT/password logic
- State: Check `src/store/index.js` for store shape

---

**SmartNutri Backend v1.0 — Auth & Onboarding Complete ✅**
