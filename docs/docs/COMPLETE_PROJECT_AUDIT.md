# 🔍 SmartNutri — COMPLETE PROJECT AUDIT

**Project:** Full-stack nutrition app (React Vite frontend + FastAPI backend)  
**Audit Date:** April 28, 2026  
**Status:** Early-stage MVP with 60% backend done, 40% frontend integration complete

---

## 🔍 TASK 1: WORKING vs NON-WORKING FEATURES

### ✅ FULLY WORKING (End-to-End Functional)

| Feature | Frontend | Backend | Status |
|---------|----------|---------|--------|
| **Authentication** | ✅ Login form, register, error handling | ✅ Auth routes, JWT tokens, password hashing | ✅ **WORKING** |
| **Dashboard Overview** | ✅ Data display, skeleton loaders | ✅ Complete aggregation, streak calc | ✅ **WORKING** |
| **Meal Search** | ✅ Search modal, food browsing, categories | ✅ Food database (45+ foods), filtering | ✅ **WORKING** |
| **Meal Logging** | ⚠️ UI exists, not using React Query properly | ✅ Full endpoint, nutrition calc | ⚠️ **PARTIALLY WORKING** |
| **Progress Tracking** | ✅ Stats display, chart visualization | ✅ Streak calc, achievements, logging | ✅ **WORKING** |
| **Chat AI** | ✅ Message UI, history, suggestions | ✅ OpenAI integration, fallback responses | ✅ **WORKING** |
| **Cycle Tracking** | ⚠️ Phase display, but mood logging not wired | ✅ Phase calc, predictions, mood logs | ⚠️ **PARTIALLY WORKING** |
| **Nutrition Today** | ✅ Macro display, micro recommendations | ✅ Aggregation by meal type, PCOS tips | ✅ **WORKING** |

### ⚠️ PARTIALLY WORKING (UI Ready, Backend Incomplete OR Frontend Not Integrated)

| Feature | Frontend | Backend | Issue |
|---------|----------|---------|-------|
| **Meal Logging** | ✅ UI, search, add button | ✅ Endpoint exists | ❌ Not using React Query mutation (manual state) |
| **Cycle Mood Log** | ✅ Emoji selector UI | ✅ Endpoint exists | ❌ UI doesn't call mutation on click |
| **Voice Input** | ✅ FAB button, modal UI | ✅ Voice endpoint exists | ❌ API functions never imported in components |
| **Onboarding Flow** | ✅ 6-step UI, all pages | ✅ Save endpoint works | ⚠️ Auto-submit at end, unclear data validation |

### ❌ NON-FUNCTIONAL (Broken or Stub)

| Feature | Frontend | Backend | Root Cause |
|---------|----------|---------|-----------|
| **Education Modules** | ✅ UI exists | ❌ Returns empty `[]` | No endpoint implemented |
| **Parent Dashboard** | ✅ UI exists, hardcoded kids | ❌ Returns empty `{}` | Endpoint stub only |
| **Delete Meal** | ❌ No UI button at all | ✅ Endpoint implemented | Frontend never added button |
| **Email Reset Password** | ⚠️ Form exists | ❌ No email sending | Backend TODO |
| **Health Conditions Filter** | ✅ UI in onboarding | ⚠️ Saved but unused | Backend doesn't filter recommendations by condition |
| **Water Logging** | ⚠️ Shows on progress charts | ❌ Not actually logged | Water tracking endpoint missing |

---

## 🔍 TASK 2: FEATURE-BY-FEATURE ANALYSIS

### 📱 AUTHENTICATION

**What Frontend Does:**
- Login page: email + password + "remember me" checkbox
- Register page: email + password + name + age + parent toggle
- Token stored in localStorage
- Redirects to onboarding if first time, dashboard otherwise
- Handles logout

**What Backend Supports:**
- Register: creates user + profile, auto-detects segment (teen-girl-h if age < 18), returns JWT
- Login: verifies credentials, returns token + segment + theme + onboardingComplete flag
- Logout: clears cookie
- GET /me: returns full user profile
- Forgot/Reset password: stub implementation (no email sending)

**Missing Connections:**
- ❌ No email verification on signup (backend doesn't send email)
- ❌ Password reset incomplete (no token generation or email)
- ⚠️ Token in localStorage instead of httpOnly cookie (XSS vulnerability)

**Exact Issues:**
- **File:** `backend/app/routes/auth_routes.py` line 208-225 (forgot-password returns 200 always)
- **File:** `backend/app/routes/auth_routes.py` line 234-255 (reset-password no token validation)
- **File:** `frontend/src/pages/auth/LoginPage.jsx` (stores token in localStorage instead of relying on secure cookie)

---

### 🎯 ONBOARDING

**What Frontend Does:**
- Step 1: Segment selection (adult, teen-girl-h, teen-girl-a, teen-boy)
- Step 2: Height + weight
- Step 3: Goals + activity level
- Step 4: Health conditions (PCOS, diabetes, allergies, etc.)
- Step 5: Diet preferences (vegan, keto, gluten-free, etc.)
- Step 6: Auto-submit all data + show "success" screen

**What Backend Supports:**
- Single endpoint: `PATCH /api/auth/onboarding`
- Calculates nutrition targets based on age/weight/height/activity
- Saves conditions and diet preferences
- Returns theme, greeting, profile with onboarding_complete = true

**Missing Connections:**
- ⚠️ No validation that age/weight/height are reasonable before saving
- ⚠️ No UI to modify onboarding after completion (one-time only)
- ⚠️ Auto-submit might submit incomplete data if user navigates back

**Exact Issues:**
- **File:** `frontend/src/pages/onboarding/OnboardingCompletePage.jsx` line 12 (auto-submit on mount, no confirmation)
- **File:** `backend/app/routes/auth_routes.py` line 119 (no validation on numeric fields)

---

### 📊 DASHBOARD

**What Frontend Does:**
- Shows user greeting (morning/afternoon/evening)
- Displays today's calorie + macro totals vs targets
- Shows 7-day streak with emoji (🌱 → 🔥 → 👑)
- Lists AI Coach suggestions
- Shows badges/achievements unlocked
- Displays cycle phase summary (for women)
- Shows today's meals quick-view

**What Backend Supports:**
- `GET /api/dashboard` aggregates:
  - User profile data (name, segment, theme)
  - Today's meals + nutrition totals
  - 30-day progress logs to calculate streak
  - Achievements unlocked
  - Cycle phase (if women)
  - Chat suggestion

**Missing Connections:**
- ⚠️ Cycle phase hardcoded to "luteal" for all users (not calculated)
- ⚠️ AI nudge sometimes empty (depends on chat history)
- ⚠️ Water intake shown but never actually logged

**Exact Issues:**
- **File:** `backend/app/routes/dashboard_routes.py` line 84-88 (cycle phase stub)
- **File:** `backend/app/routes/dashboard_routes.py` line 62 (water hardcoded to 1.5/2.5)

---

### 🍽️ MEALS

**What Frontend Does:**
- Shows date picker + today's meals
- Search modal to find foods by name/category
- Click food to add to meal type (breakfast, lunch, dinner, snack)
- Shows total calories + macros for each meal type
- Displays progress bars vs targets
- No delete button visible

**What Backend Supports:**
- `POST /api/meals/log` → logs meal with foods + quantities, calculates macros
- `GET /api/meals/date/{date}` → returns all meals for a date with totals
- `GET /api/meals/week` → returns 7-day summary
- `DELETE /api/meals/{meal_id}` → deletes meal (but frontend doesn't call it)
- `GET /api/foods/search` → searches 45+ foods in database
- `GET /api/foods/categories` → returns 9 food categories
- `GET /api/foods/browse` → browses foods by category

**Missing Connections:**
- ❌ Meal logging uses manual state management instead of React Query mutation (error handling weak)
- ❌ No delete meal button in UI despite backend endpoint existing
- ❌ Meal quantity selector missing (hardcoded quantity=1)
- ⚠️ Food database small (45 foods) — need to seed more

**Exact Issues:**
- **File:** `frontend/src/components/features/meals/Meals.jsx` line 45-55 (manual logMeal call, not mutation)
- **File:** `frontend/src/components/features/meals/Meals.jsx` (no delete button in UI)
- **File:** `frontend/src/hooks/useQueries.js` (useMealMutation not exported/used)

---

### 💬 CHAT (AI COACH)

**What Frontend Does:**
- Message input + send button
- Shows AI responses with follow-up chips
- Displays 3 suggested questions at top
- Full chat history scrollable

**What Backend Supports:**
- `POST /api/chat/message` → sends message, gets AI response
  - If OpenAI API key configured: uses GPT-3.5-turbo with system prompt
  - Fallback: keyword matching (200+ responses hardcoded)
  - Safety check: blocks harmful keywords
- `GET /api/chat/suggestions` → returns 3 segment-specific suggestions
- `GET /api/chat/history` → returns last 50 messages

**Missing Connections:**
- ⚠️ Suggestions API returns empty if profile not found (UI falls back to hardcoded suggestions)
- ⚠️ No OpenAI API key in most environments (falls back to keyword responses)
- ⚠️ Chat history not persisted across app restarts (stored in Zustand only)
- ⚠️ Chat context doesn't include user's meals/goals (should be personalized)

**Exact Issues:**
- **File:** `backend/app/routes/chat_routes.py` line 42 (API key check, falls back silently)
- **File:** `frontend/src/components/features/chat/Chat.jsx` (hardcoded fallback suggestions)
- **File:** `frontend/src/store/index.js` (chat messages in memory, not persisted)

---

### 🩸 CYCLE TRACKING

**What Frontend Does:**
- Shows current cycle phase (menstrual, follicular, ovulation, luteal) with emoji
- Displays phase-specific nutrition tips
- Shows foods to eat + avoid during phase
- Mood emoji selector (happiness levels)
- Shows recent mood logs
- Phase prediction calendar

**What Backend Supports:**
- `GET /api/cycle` → calculates phase based on lastPeriodDate + cycleLength
- `PUT /api/cycle/update` → saves cycle data (start date, cycle length, symptoms)
- `POST /api/cycle/mood` → logs mood + symptoms for today
- `GET /api/cycle/predictions` → generates phase predictions for next 30 days
- `GET /api/cycle/stats` → mood frequency + common symptoms analysis

**Missing Connections:**
- ❌ Mood emoji selector UI doesn't call `logCycleMood()` mutation (onClick just sets local state)
- ⚠️ Cycle data entered in onboarding but can't be edited afterward
- ⚠️ "Avoid foods" always empty (parsed from tips but not actual data)
- ⚠️ For non-cycle users (men, teens not tracking): shows "not_started" placeholder

**Exact Issues:**
- **File:** `frontend/src/components/features/cycle/Cycle.jsx` line 94 (mood emoji onClick doesn't trigger mutation)
- **File:** `frontend/src/components/features/cycle/Cycle.jsx` (avoidFoods hardcoded empty)
- **File:** `backend/app/routes/cycle_routes.py` line 84-88 (avoid foods not returned)

---

### 📈 PROGRESS TRACKING

**What Frontend Does:**
- Shows daily weight + mood + energy level logger
- Displays 7-day chart with calories burned + meals logged
- Shows streak (days in a row logged)
- Lists unlocked achievements/badges
- Stats: avg weight, total exercises, mood distribution

**What Backend Supports:**
- `POST /api/progress/log` → logs daily: weight, mood, energy, water, exercise, notes
  - Deduplication: only 1 entry per day (upsert)
  - Achievement check: awards badges at 7/14/30/100 day streaks
- `GET /api/progress/summary` → returns last 7 days of logs + stats
- `GET /api/progress/streak` → returns current + best streak
- `GET /api/progress/goals` → today's nutrition goals vs actual
- `GET /api/progress/achievements` → all achievements with unlock status

**Missing Connections:**
- ⚠️ Hardcoded goal values (1800 kcal/day) in frontend chart — should come from backend
- ⚠️ Water logging shown but never actually logged (no water tracking UI)
- ⚠️ No way to edit/delete logged entries
- ⚠️ Day/Week/Month filter buttons show no state change

**Exact Issues:**
- **File:** `frontend/src/components/features/progress/Progress.jsx` line 25 (hardcoded 1800 goal)
- **File:** `frontend/src/components/features/progress/Progress.jsx` (filter buttons don't update query)
- **File:** No water logging form anywhere

---

### 🥗 NUTRITION (DETAILED)

**What Frontend Does:**
- Shows today's macros breakdown (pie chart)
- Shows micronutrient recommendations (bars for PCOS iron boost, calcium, etc.)
- Displays foods rich in recommended micronutrients
- Segment-specific recommendations (PCOS vs athletic vs general)

**What Backend Supports:**
- `GET /api/nutrition/today` → returns today's nutrition aggregated from meals
  - Macros: calories, protein, carbs, fats vs targets
  - Percentages capped at 100%
- `GET /api/nutrition/summary` → returns 7-day nutrition trends

**Missing Connections:**
- ⚠️ Micronutrient recommendations hardcoded for PCOS (not dynamic by condition)
- ⚠️ Frontend has no way to update nutrition targets
- ⚠️ "Iron boost foods" only shown if PCOS; no other condition-specific foods

**Exact Issues:**
- **File:** `frontend/src/components/features/nutrition/Nutrition.jsx` (hardcoded PCOS micronutrients)
- **File:** `backend/app/routes/nutrition_routes.py` (no micronutrient logic, only macros)

---

### 📚 EDUCATION (LEARNING MODULES)

**What Frontend Does:**
- Shows module cards (video + quiz format)
- Module selection opens interactive quiz
- Shows progress (completed/total)

**What Backend Supports:**
- `GET /api/modules` → returns learning modules
  - **ISSUE:** Returns empty array (no modules implemented)

**Missing Connections:**
- ❌ Feature completely non-functional
- No modules in database
- No backend implementation for module creation/delivery
- Frontend UI is polished but displays nothing

**Exact Issues:**
- **File:** `backend/app/routes/education_routes.py` (doesn't exist or incomplete)
- **File:** `frontend/src/components/features/education/Education.jsx` (waits for data that never comes)

---

### 👨‍👩‍👧 PARENT DASHBOARD

**What Frontend Does:**
- Dropdown to select child to monitor
- Shows child's stats: streaks, nutrition, progress
- Shows privacy settings (what parent can/can't see)
- Hardcoded to "Ananya" and "Rohan"

**What Backend Supports:**
- `GET /api/parent/dashboard` → returns child's aggregated stats
  - **ISSUE:** Returns empty object (not fully implemented)

**Missing Connections:**
- ❌ API returns empty `{}`, UI breaks
- ❌ Child list hardcoded in frontend (not fetched from backend)
- ❌ No actual parent-child relationship data in database
- ❌ No endpoint to list children for a parent account

**Exact Issues:**
- **File:** `backend/app/routes/parent_routes.py` (stub implementation)
- **File:** `frontend/src/components/features/parent/Parent.jsx` line 15 (hardcoded children)
- **File:** `frontend/src/api/index.js` line 298 (fetchParentDashboard returns empty on error)

---

### 🎤 VOICE INPUT

**What Frontend Does:**
- FAB button on dashboard opens voice modal
- Shows transcript as user speaks (Web Speech API)
- "Done" button to submit meal

**What Backend Supports:**
- `POST /api/voice/log-meal` → parses meal description, extracts foods, estimates macros
- `GET /api/voice/food-suggestions` → autocomplete food names
- `GET /api/voice/food-info` → returns nutrition for specific food
- `GET /api/voice/examples` → example voice commands

**Missing Connections:**
- ❌ Voice.js functions completely detached from UI components
- ❌ Functions defined in `src/api/voice.js` but never imported in `VoiceInput.jsx`
- ❌ useVoiceInput hook only uses Web Speech API (browser), doesn't call backend
- ❌ No actual meal logging after voice transcript

**Exact Issues:**
- **File:** `frontend/src/api/voice.js` (functions exported but never used)
- **File:** `frontend/src/hooks/useVoiceInput.js` (only handles browser API, not backend calls)
- **File:** `frontend/src/components/features/VoiceInput.jsx` (doesn't import voice API functions)
- **File:** Logic mismatch: `/api/voice/log-meal` vs `/api/meals/log`

---

## 🔍 TASK 3: API MAPPING TABLE

| Feature | Frontend Call | Backend Endpoint | Status | Issue |
|---------|--------------|------------------|--------|-------|
| Register | `authApi.register()` | `POST /api/auth/register` | ✅ Working | — |
| Login | `authApi.login()` | `POST /api/auth/login` | ✅ Working | Token in localStorage |
| Get Me | `authApi.getMe()` | `GET /api/auth/me` | ✅ Working | — |
| Logout | `authApi.logout()` | `POST /api/auth/logout` | ✅ Working | — |
| Save Onboarding | `authApi.saveOnboarding()` | `PATCH /api/auth/onboarding` | ✅ Working | Auto-submit, no confirm |
| Forgot Password | `authApi.forgotPassword()` | `POST /api/auth/forgot-password` | ❌ Broken | No email implementation |
| Reset Password | `authApi.resetPassword()` | `POST /api/auth/reset-password` | ⚠️ Stub | No token logic |
| Get Dashboard | `fetchDashboard()` | `GET /api/dashboard` | ✅ Working | Cycle phase hardcoded |
| Log Meal | `logMeal()` | `POST /api/meals/log` | ⚠️ Bad pattern | Manual state mgmt, not mutation |
| Get Meals by Date | `fetchMeals()` | `GET /api/meals/date/{date}` | ✅ Working | — |
| Get Weekly Meals | (not called) | `GET /api/meals/week` | ✅ Implemented | Unused |
| Delete Meal | (not called) | `DELETE /api/meals/{id}` | ✅ Implemented | No UI button |
| Search Foods | `searchFoods()` | `GET /api/foods/search` | ✅ Working | — |
| Get Categories | `getFoodCategories()` | `GET /api/foods/categories` | ✅ Working | — |
| Browse Foods | `browseFoods()` | `GET /api/foods/browse` | ✅ Working | — |
| Get Food Details | `getFoodDetails()` | `GET /api/foods/{id}` | ✅ Working | — |
| Add Favorite | `addFavoriteFood()` | `POST /api/foods/favorite` | ✅ Implemented | No UI to remove |
| Get Favorites | `getFavoriteFoods()` | `GET /api/foods/favorites` | ✅ Implemented | Not used in UI |
| Get Nutrition Today | `fetchNutrition()` | `GET /api/nutrition/today` | ✅ Working | — |
| Get Cycle | `fetchCycle()` | `GET /api/cycle` | ✅ Working | Mood not saved |
| Update Cycle | `updateCycleData()` | `PUT /api/cycle/update` | ✅ Implemented | Onboarding only |
| Log Cycle Mood | `logCycleMood()` | `POST /api/cycle/mood` | ✅ Implemented | UI doesn't call it |
| Get Cycle Predictions | `getCyclePredictions()` | `GET /api/cycle/predictions` | ✅ Working | Display-only |
| Get Cycle Stats | `getCycleStats()` | `GET /api/cycle/stats` | ✅ Implemented | Not shown in UI |
| Log Progress | `logProgress()` | `POST /api/progress/log` | ✅ Working | — |
| Get Progress Summary | `fetchProgress()` | `GET /api/progress/summary` | ✅ Working | — |
| Get Streak | (in fetchProgress) | `GET /api/progress/streak` | ✅ Working | — |
| Get Goals | (in fetchProgress) | `GET /api/progress/goals` | ✅ Working | — |
| Get Achievements | (in fetchProgress) | `GET /api/progress/achievements` | ✅ Working | — |
| Send Chat Message | `sendChatMessage()` | `POST /api/chat/message` | ✅ Working | Context limited |
| Get Chat Suggestions | `fetchChatSuggestions()` | `GET /api/chat/suggestions` | ⚠️ Unreliable | Falls back to hardcoded |
| Get Chat History | (loaded on mount) | `GET /api/chat/history` | ✅ Working | — |
| Get Education Modules | `fetchModules()` | `GET /api/modules` | ❌ Missing | No implementation |
| Get Parent Dashboard | `fetchParentDashboard()` | `GET /api/parent/dashboard` | ❌ Missing | Stub only |
| Voice Log Meal | (not called) | `POST /api/voice/log-meal` | ✅ Implemented | Not wired to UI |
| Voice Food Suggestions | (not called) | `GET /api/voice/food-suggestions` | ✅ Implemented | Not used |
| Voice Food Info | (not called) | `GET /api/voice/food-info` | ✅ Implemented | Not used |
| Voice Examples | (not called) | `GET /api/voice/examples` | ✅ Implemented | Not called |

---

## 🔍 TASK 4: ROOT CAUSES — WHY FEATURES DON'T WORK

### 1. ❌ **Missing API Endpoints** (4 features)
- **Education Modules** → No `GET /api/modules` implementation
- **Parent Dashboard** → No real `GET /api/parent/dashboard` implementation (stub returns `{}`)
- **Email sending** → `POST /api/auth/forgot-password` has no email integration
- **Password reset tokens** → `POST /api/auth/reset-password` no token generation

### 2. ❌ **Frontend Not Importing Backend Functions** (Voice)
- Voice.js functions exist but never imported in components
- VoiceInput.jsx only uses Web Speech API (browser), never calls backend
- Result: voice transcript never becomes a logged meal

### 3. ❌ **UI Components Not Triggering Mutations** (3 features)
- **Mood logging:** Emoji selector exists but onClick doesn't call `logCycleMood()` mutation
- **Meal logging:** Uses manual state instead of `useMutation` (weak error handling)
- **Delete meal:** Backend endpoint exists but no delete button in UI

### 4. ⚠️ **State Management Issues**
- Chat messages stored in Zustand (memory) → lost on refresh
- Onboarding data split across multiple steps → validation incomplete
- No way to edit settings after onboarding

### 5. ⚠️ **Hardcoded Data Instead of Dynamic**
- Progress chart hardcodes 1800 kcal goal
- Nutrition recommendations hardcoded for PCOS only
- Cycle phase hardcoded to "luteal" in dashboard
- Parent dashboard kids hardcoded to ["Ananya", "Rohan"]
- Chat suggestions fallback is hardcoded list

### 6. ⚠️ **API Base URL Mismatch**
- `.env.local` says `VITE_API_URL=http://localhost:8000` ✅ correct
- `frontend/src/api/auth.js` has fallback to `http://localhost:3001` ❌ wrong port
- If env not loaded, auth calls wrong server

### 7. ⚠️ **React Query Pattern Issues**
- Meal logging uses `apiCall()` directly instead of `useMutation`
- Makes error handling and cache invalidation manual/unreliable
- Should be: `const { mutateAsync } = useMutation(logMeal, { onSuccess: () => queryClient.invalidateQueries() })`

### 8. ⚠️ **Backend Issues**
- Water tracking shown but never logged (no UI form)
- Cycle phase hardcoded in dashboard calculations
- Chat context doesn't include user's actual data
- Voice endpoint uses generic `db` object (connection issues possible)

### 9. ⚠️ **Security Issues**
- JWT token stored in localStorage (XSS vulnerable)
- Should be httpOnly cookie only
- Password reset has no token expiration

### 10. ⚠️ **Database Not Fully Seeded**
- Only 45 foods in database (small for production)
- No education modules created
- No parent-child relationships pre-populated

---

## 🔍 TASK 5: FIX PLAN (PRIORITIZED)

### **PRIORITY 1: Fix Authentication Issues (Est. 1-2 hours)**

**1.1 Move JWT Token to Secure Cookie**
- **File:** `frontend/src/api/auth.js`
- **Issue:** Token in localStorage (XSS vulnerable)
- **Fix:**
  ```javascript
  // REMOVE:
  localStorage.setItem("token", data.token)
  
  // REPLACE WITH: Rely on httpOnly cookie only
  // The backend already sets sn_token cookie, just don't override
  // Use this in API calls:
  options.credentials = 'include' // Already there ✅
  ```
- **Backend:** Already sets httpOnly cookie correctly ✅

**1.2 Implement Email Verification**
- **File:** `backend/app/routes/auth_routes.py` line 48-78
- **Issue:** No email verification after signup
- **Fix:**
  ```python
  # Generate verification token
  verify_token = create_access_token({"userId": user_id, "type": "email_verify"}, expires_hours=24)
  
  # Send email with verification link (use SendGrid or similar)
  send_email(
    to=req.email,
    subject="Verify your SmartNutri email",
    html=f"Click here to verify: https://smartnutri.app/verify?token={verify_token}"
  )
  
  # Mark user as unverified initially
  user_doc["email_verified"] = False
  ```
- **Time:** 1 hour
- **Dependencies:** Email service (SendGrid, Mailgun, or AWS SES)

**1.3 Implement Password Reset**
- **File:** `backend/app/routes/auth_routes.py` line 208-255
- **Issue:** forgot-password stub, no token generation
- **Fix:**
  ```python
  # POST /api/auth/forgot-password
  user = await db.users.find_one({"email": req.email})
  if user:
    reset_token = create_access_token({"userId": str(user["_id"]), "type": "reset"}, expires_hours=1)
    # Send email with reset link
    send_email(to=req.email, link=f"https://smartnutri.app/reset?token={reset_token}")
  return {"success": true}  # Don't reveal if email exists
  ```
- **Time:** 1 hour

---

### **PRIORITY 2: Fix Core Meal Features (Est. 1.5 hours)**

**2.1 Use React Query Mutation for Meal Logging**
- **File:** `frontend/src/components/features/meals/Meals.jsx` line 45-55
- **Issue:** Manual state management, not using React Query
- **Fix:**
  ```javascript
  // In useQueries.js:
  export const useLogMeal = () => {
    const queryClient = useQueryClient()
    return useMutation(logMeal, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: KEYS.meals })
      }
    })
  }
  
  // In Meals.jsx:
  const { mutate: logMealMutation, isPending } = useLogMeal()
  
  const handleAddFood = (food) => {
    logMealMutation({ mealType: selectedMealType, food }, {
      onError: (err) => {
        // Show toast error
      }
    })
  }
  ```
- **Time:** 30 min

**2.2 Add Delete Meal Button**
- **File:** `frontend/src/components/features/meals/Meals.jsx`
- **Issue:** No delete button in UI despite backend endpoint existing
- **Fix:**
  ```javascript
  // Add mutation hook in useQueries.js:
  export const useDeleteMeal = () => {
    const queryClient = useQueryClient()
    return useMutation((mealId) => apiCall('DELETE', `/api/meals/${mealId}`), {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: KEYS.meals })
      }
    })
  }
  
  // In MealCard component, add:
  <BtnSecondary onClick={() => onDelete(meal.id)}>Delete</BtnSecondary>
  ```
- **Time:** 30 min

**2.3 Add Meal Quantity Selector**
- **File:** `frontend/src/components/features/meals/Meals.jsx`
- **Issue:** Quantity hardcoded to 1
- **Fix:**
  ```javascript
  <input type="number" min="0.5" max="5" step="0.5" value={quantity} onChange={setQuantity} />
  
  // Pass to logMeal:
  logMeal(selectedMealType, food, quantity)
  ```
- **Time:** 15 min

---

### **PRIORITY 3: Fix Cycle Tracking (Est. 1 hour)**

**3.1 Wire Mood Logging to Backend**
- **File:** `frontend/src/components/features/cycle/Cycle.jsx` line 94
- **Issue:** Mood emoji selector UI doesn't call mutation
- **Fix:**
  ```javascript
  // Import mutation:
  const { mutate: logMood } = useLogCycleMood()
  
  // In mood emoji click handler:
  const handleMoodClick = (mood) => {
    setMood(mood)
    logMood({ mood, symptom: selectedSymptom }, {
      onSuccess: () => {
        // Refetch cycle data
        queryClient.invalidateQueries({ queryKey: KEYS.cycle })
      }
    })
  }
  ```
- **Time:** 30 min

**3.2 Fix Backend Cycle Phase Calculation**
- **File:** `backend/app/routes/dashboard_routes.py` line 84-88
- **Issue:** Cycle phase hardcoded to "luteal"
- **Fix:**
  ```python
  # Import from cycle_routes:
  from app.routes.cycle_routes import calculate_cycle_phase
  
  # In dashboard endpoint:
  if profile and profile.get("cycle_data") and profile["cycle_data"].get("lastPeriodDate"):
    cycle_phase = calculate_cycle_phase(
      profile["cycle_data"]["lastPeriodDate"],
      profile["cycle_data"].get("cycleLength", 28)
    )
  ```
- **Time:** 15 min

**3.3 Populate Avoid Foods from Backend**
- **File:** `backend/app/routes/cycle_routes.py` (add avoid_foods)
- **Issue:** Avoid foods always empty
- **Fix:**
  ```python
  CYCLE_PHASES = {
    "menstrual": {
      "avoid_foods": ["Caffeine", "High sodium", "Alcohol"]
    },
    # ... etc
  }
  
  # Return in response:
  "avoidFoods": CYCLE_PHASES[phase]["avoid_foods"]
  ```
- **Time:** 15 min

---

### **PRIORITY 4: Wire Voice Input to Components (Est. 45 min)**

**4.1 Import and Connect Voice API Functions**
- **File:** `frontend/src/components/features/VoiceInput.jsx`
- **Issue:** Functions in voice.js but not imported
- **Fix:**
  ```javascript
  import { logMealWithVoice } from '@api/voice'
  
  const handleVoiceSubmit = async (transcript) => {
    const result = await logMealWithVoice(transcript)
    // Show result: "Added 2 eggs, toast, and orange juice"
    queryClient.invalidateQueries({ queryKey: KEYS.meals })
  }
  ```
- **Time:** 15 min

**4.2 Use Voice Endpoint Instead of Manual Parsing**
- **File:** `frontend/src/hooks/useVoiceInput.js`
- **Issue:** Only uses Web Speech API, never calls backend
- **Fix:**
  ```javascript
  // After getting transcript:
  const response = await fetch('/api/voice/log-meal', {
    method: 'POST',
    body: JSON.stringify({ mealDescription: transcript })
  })
  const meals = await response.json()
  // Show confirmation: "Parsed as: 2 eggs (150cal), 1 toast (100cal)"
  ```
- **Time:** 15 min

**4.3 Add Delete from Voice Suggestions**
- **File:** `frontend/src/api/voice.js`
- **Issue:** User might add wrong food via voice
- **Fix:** Allow user to "remove" items before final submit
- **Time:** 15 min

---

### **PRIORITY 5: Implement Missing Endpoints (Est. 2 hours)**

**5.1 Implement Education Modules Endpoint**
- **File:** `backend/app/routes/education_routes.py` (create if missing)
- **Issue:** GET /api/modules returns empty
- **Fix:**
  ```python
  EDUCATION_MODULES = [
    {
      "id": "macro-basics",
      "title": "Macro Basics 101",
      "description": "Learn about proteins, carbs, and fats",
      "video_url": "https://example.com/video1",
      "quiz": [
        {"question": "What is a macronutrient?", "options": [...], "answer": 0}
      ]
    },
    # ... add 5-10 modules
  ]
  
  @router.get("/modules")
  async def get_modules(request: Request):
    return {"success": True, "data": EDUCATION_MODULES}
  ```
- **Time:** 45 min

**5.2 Implement Parent Dashboard Endpoint**
- **File:** `backend/app/routes/parent_routes.py`
- **Issue:** Stub returns empty `{}`
- **Fix:**
  ```python
  @router.get("/parent/dashboard")
  async def get_parent_dashboard(request: Request, child: str = None):
    user = get_current_user(request)
    db = get_db()
    
    # Get children associated with this parent
    # Find child by name
    child_user = await db.users.find_one({"name": child, "parent_id": user["userId"]})
    
    if not child_user:
      raise HTTPException(404, "Child not found")
    
    # Aggregate child's data (meals, progress, cycle)
    return {
      "success": True,
      "data": {
        "childName": child,
        "stats": {...},
        "recentMeals": [...]
      }
    }
  ```
- **Time:** 45 min
- **Note:** Requires parent-child relationship in database first

**5.3 Seed More Foods into Database**
- **File:** `backend/seed_db.py`
- **Issue:** Only 45 foods (too small)
- **Fix:**
  ```python
  # Add 200+ foods from nutrition database
  # Use public food API or import CSV
  DEFAULT_FOODS = [
    # Existing 45 + new 200
  ]
  ```
- **Time:** 30 min (if using import script)

---

### **PRIORITY 6: Fix State Management & Data Flow (Est. 1.5 hours)**

**6.1 Persist Chat History to Backend**
- **File:** `frontend/src/store/index.js` + `backend/app/routes/chat_routes.py`
- **Issue:** Chat messages lost on refresh
- **Fix:**
  ```javascript
  // In Zustand store: load chat history from /api/chat/history on app init
  useEffect(() => {
    const loadChatHistory = async () => {
      const history = await apiCall('GET', '/api/chat/history')
      setChatMessages(history)
    }
    loadChatHistory()
  }, [])
  ```
- **Time:** 30 min

**6.2 Add Nutrition Target Update Endpoint**
- **File:** `backend/app/routes/nutrition_routes.py` (add PUT endpoint)
- **Issue:** No way to change targets after onboarding
- **Fix:**
  ```python
  @router.put("/nutrition/targets")
  async def update_nutrition_targets(request: Request, req: NutritionTargetsRequest):
    user = get_current_user(request)
    db = get_db()
    
    await db.nutrition_targets.update_one(
      {"user_id": user["userId"]},
      {"$set": {
        "calorie_goal": req.calorie_goal,
        "protein_g": req.protein_g,
        "carbs_g": req.carbs_g,
        "fats_g": req.fats_g
      }}
    )
    return {"success": True}
  ```
- **Time:** 20 min

**6.3 Add Water Logging Endpoint**
- **File:** `backend/app/routes/progress_routes.py` (add water tracking)
- **Issue:** Water shown but never logged
- **Fix:**
  ```python
  @router.post("/water/log")
  async def log_water(request: Request, glasses: int):
    user = get_current_user(request)
    db = get_db()
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    await db.water_logs.update_one(
      {"user_id": user["userId"], "date": today},
      {"$set": {"glasses": glasses, "updated_at": datetime.utcnow()}},
      upsert=True
    )
    return {"success": True}
  ```
- **Time:** 15 min

---

### **PRIORITY 7: Hardcoded Data → Dynamic Data (Est. 1.5 hours)**

**7.1 Progress Chart Goals from Backend**
- **File:** `frontend/src/components/features/progress/Progress.jsx` line 25
- **Issue:** Hardcoded 1800 kcal goal
- **Fix:**
  ```javascript
  // Get from backend:
  const { data: goals } = useQuery({
    queryKey: KEYS.progress,
    queryFn: () => apiCall('GET', '/api/progress/goals')
  })
  
  // Use:
  chartMeta.goal = goals?.calories?.goal || 1800
  ```
- **Time:** 15 min

**7.2 Nutrition Recommendations by Condition**
- **File:** `backend/app/routes/nutrition_routes.py` + frontend
- **Issue:** Only PCOS hardcoded
- **Fix:**
  ```python
  # Add to GET /api/nutrition/today:
  user = get_current_user(request)
  profile = await db.profiles.find_one({"user_id": user["userId"]})
  conditions = profile.get("conditions", [])
  
  if "pcos" in conditions:
    micronutrients = {...PCOS_MICROS}
  elif "diabetes" in conditions:
    micronutrients = {...DIABETES_MICROS}
  # etc
  ```
- **Time:** 30 min

**7.3 Parent Dashboard Children from Database**
- **File:** `frontend/src/components/features/parent/Parent.jsx` line 15
- **Issue:** Hardcoded ["Ananya", "Rohan"]
- **Fix:**
  ```javascript
  // Fetch children endpoint (to be added to backend):
  const { data: children } = useQuery({
    queryKey: KEYS.parent,
    queryFn: () => apiCall('GET', '/api/parent/children')
  })
  
  // Then:
  <select value={selectedChild} onChange={setSelectedChild}>
    {children.map(c => <option key={c.id}>{c.name}</option>)}
  </select>
  ```
- **Time:** 30 min

**7.4 Cycle Phase Calculation Logic**
- **File:** `backend/app/routes/cycle_routes.py` (already correct), dashboard needs to use it
- **Issue:** Hardcoded "luteal" in dashboard
- **Already in fix plan above** ✓

---

### **PRIORITY 8: Clean Up API Base URL** (Est. 15 min)

**8.1 Remove Hardcoded Fallback**
- **File:** `frontend/src/api/auth.js` line 1
- **Issue:** Fallback to wrong port `http://localhost:3001`
- **Fix:**
  ```javascript
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  ```
- **Time:** 5 min

**8.2 Ensure All API Files Use Same Base**
- **Files:** `frontend/src/api/index.js`, `frontend/src/api/auth.js`, `frontend/src/api/voice.js`
- **Fix:** Centralize API_BASE
  ```javascript
  // Create frontend/src/api/client.js:
  export const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  
  export async function apiCall(method, path, body = null) { /* ... */ }
  
  // In other files:
  import { apiCall, API_BASE } from './client'
  ```
- **Time:** 10 min

---

## 🔍 TASK 6: QUICK WINS (Features Fixable in <30 minutes)

### ⚡ Quick Win #1: Add Delete Meal Button
- **Component:** `frontend/src/components/ui/MealCard.jsx`
- **Time:** 15 min
- **Effort:** Trivial
- **Impact:** High (users can correct mistakes)
```jsx
// Add to MealCard:
<BtnSecondary onClick={() => onDelete(id)} size="sm">
  Delete
</BtnSecondary>
```

### ⚡ Quick Win #2: Connect Mood Logging UI
- **Component:** `frontend/src/components/features/cycle/Cycle.jsx`
- **Time:** 10 min
- **Effort:** Trivial
- **Impact:** High (enables cycle tracking)
```jsx
// Change mood emoji onClick:
onClick={() => {
  setMood(m)
  logMood({ mood: m, symptom: selectedSymptom })
}}
```

### ⚡ Quick Win #3: Fix API Base URL Fallback
- **File:** `frontend/src/api/auth.js`
- **Time:** 5 min
- **Effort:** Trivial
- **Impact:** Medium (prevents wrong server calls)

### ⚡ Quick Win #4: Add Filter State to Progress Chart
- **Component:** `frontend/src/components/features/progress/Progress.jsx`
- **Time:** 15 min
- **Effort:** Low
- **Impact:** Medium (visual feedback)
```jsx
const [filterPeriod, setFilterPeriod] = useState('7')

// When clicking Day/Week/Month:
const { data } = useProgress(parseInt(filterPeriod))
```

### ⚡ Quick Win #5: Show Water Logging UI
- **Component:** `frontend/src/components/features/progress/Progress.jsx`
- **Time:** 15 min
- **Effort:** Low
- **Impact:** Medium (users can track water)
```jsx
// Add water input:
<input type="number" value={waterGlasses} onChange={setWaterGlasses} />
<button onClick={() => logWater(waterGlasses)}>Log Water</button>
```

### ⚡ Quick Win #6: Use Streaks in Goals Display
- **Component:** Already fetching streak in progress
- **Time:** 5 min
- **Effort:** Trivial
- **Impact:** Low (visual polish)

### ⚡ Quick Win #7: Add Copy-Paste Food Suggestion Links
- **Component:** `frontend/src/components/features/meals/Meals.jsx`
- **Time:** 10 min
- **Effort:** Low
- **Impact:** Medium (UX improvement)

### ⚡ Quick Win #8: Show Error Toast on API Failures
- **Component:** All feature components
- **Time:** 20 min
- **Effort:** Low
- **Impact:** High (better UX)
```jsx
// Instead of silent failures, use:
const { mutate, error } = useMutation(...)
if (error) <Toast message={error.message} type="error" />
```

---

## SUMMARY TABLE — ALL ISSUES & FIXES

| Issue | Category | Priority | Time | Difficulty | Impact |
|-------|----------|----------|------|-----------|--------|
| JWT in localStorage | Security | 1 | 15 min | Trivial | High |
| Email verification missing | Features | 1 | 1 hour | Low | Medium |
| Password reset stub | Features | 1 | 1 hour | Low | Medium |
| Meal logging manual state | Code Quality | 2 | 30 min | Low | High |
| No delete meal button | Features | 2 | 15 min | Trivial | Medium |
| No meal quantity selector | Features | 2 | 15 min | Trivial | Medium |
| Mood logging not wired | Features | 3 | 30 min | Low | High |
| Cycle phase hardcoded | Backend | 3 | 15 min | Trivial | Medium |
| Avoid foods empty | Backend | 3 | 15 min | Trivial | Low |
| Voice not connected | Features | 4 | 45 min | Low | High |
| Education modules missing | Features | 5 | 45 min | Low | High |
| Parent dashboard stub | Features | 5 | 45 min | Low | Medium |
| Chat history not persisted | Features | 6 | 30 min | Low | Medium |
| No nutrition target update | Features | 6 | 20 min | Low | Medium |
| Water logging UI missing | Features | 6 | 15 min | Trivial | Low |
| Progress goals hardcoded | Features | 7 | 15 min | Low | Medium |
| Recommendations hardcoded | Backend | 7 | 30 min | Low | Medium |
| Parent children hardcoded | Features | 7 | 30 min | Low | Medium |
| API base URL fallback | Config | 8 | 5 min | Trivial | Low |

---

## 🎯 EXECUTION ROADMAP

### Week 1: Fix Critical Path (Auth + Core Features)
- [ ] Priority 1: Authentication (2 hours)
- [ ] Priority 2: Meal Features (1.5 hours)
- [ ] Priority 3: Cycle Tracking (1 hour)
- **Total:** ~4.5 hours → 80% of core features working

### Week 2: Connect Missing Parts
- [ ] Priority 4: Voice Input (45 min)
- [ ] Priority 6: State Management (1.5 hours)
- [ ] Quick Wins: 8 features (2 hours)
- **Total:** ~4 hours → UI more polished

### Week 3: Implement Missing Endpoints
- [ ] Priority 5: Education + Parent (2 hours)
- [ ] Priority 7: Dynamic Data (1.5 hours)
- [ ] Testing + bug fixes (2 hours)
- **Total:** ~5.5 hours → Feature complete

### Week 4: Polish & Deploy
- [ ] Code review + cleanup
- [ ] Performance optimization
- [ ] Security audit
- [ ] Production deployment

---

## 📊 FEATURE COMPLETION STATUS

| Feature | Before | After | Effort |
|---------|--------|-------|--------|
| Authentication | 70% | 100% | 2 hrs |
| Meals | 60% | 100% | 1.5 hrs |
| Progress | 85% | 100% | 1 hr |
| Cycle | 50% | 100% | 1.5 hrs |
| Chat | 80% | 90% | 1 hr |
| Nutrition | 60% | 100% | 1 hr |
| Voice | 5% | 80% | 1 hr |
| Education | 0% | 70% | 1 hr |
| Parent | 10% | 70% | 1 hr |
| **OVERALL** | **45%** | **90%** | **~11 hours** |

---

## 🚀 NEXT STEPS

1. **Immediately:** Fix security issue (JWT to cookie)
2. **This sprint:** Implement priorities 1-3 (core features working)
3. **Next sprint:** Connect voice, fix state management
4. **Final sprint:** Implement missing endpoints, polish

You now have a complete roadmap to transform this from 45% → 90% functional product. Start with authentication and meal features for maximum impact.

