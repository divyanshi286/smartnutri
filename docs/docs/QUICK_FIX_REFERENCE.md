# ⚡ QUICK FIX REFERENCE — Exact Files & Line Numbers

## 🔴 CRITICAL (DO FIRST)

### 1️⃣ Security: JWT Token in localStorage
**Status:** 🔴 SECURITY ISSUE  
**Files to edit:**
- `frontend/src/api/auth.js` line 57
- `frontend/src/pages/auth/LoginPage.jsx` (check if relies on localStorage)

**What to do:**
```javascript
// ❌ REMOVE THIS:
localStorage.setItem("token", data.token)

// ✅ KEEP THIS (already working):
options.credentials = 'include' // Use httpOnly cookie instead
```

**Time:** 5 minutes  
**Reason:** XSS attacks can steal token from localStorage

---

### 2️⃣ API Base URL Wrong Fallback
**Status:** 🔴 WILL BREAK if env not loaded  
**File to edit:**
- `frontend/src/api/auth.js` line 1

**What to do:**
```javascript
// ❌ CURRENT:
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001'

// ✅ FIXED:
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

**Time:** 2 minutes

---

## 🟠 HIGH PRIORITY (FIX NEXT)

### 3️⃣ Meal Logging Uses Wrong Pattern
**Status:** ⚠️ Works but fragile  
**File to edit:**
- `frontend/src/components/features/meals/Meals.jsx` line 45-55
- `frontend/src/hooks/useQueries.js` (add new hook)

**What to do:**

In `useQueries.js`, add:
```javascript
export const useLogMeal = () => {
  const queryClient = useQueryClient()
  return useMutation(logMeal, {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: KEYS.meals })
    },
    onError: (error) => {
      console.error('Meal log failed:', error)
    }
  })
}

export const useDeleteMeal = () => {
  const queryClient = useQueryClient()
  return useMutation(
    (mealId) => apiCall('DELETE', `/api/meals/${mealId}`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: KEYS.meals })
      }
    }
  )
}
```

In `Meals.jsx`, replace line 45-55:
```javascript
// ❌ REMOVE:
const handleAddFood = async (food) => {
  if (isLoggingMeal) return
  try {
    setIsLoggingMeal(true)
    await logMeal(selectedMealType, food)  // ← Direct call
    queryClient.invalidateQueries({ queryKey: ['meals', today] })
    setShowFoodSearch(false)
  } catch (err) {
    alert(`Error: ${err.message}`)
  } finally {
    setIsLoggingMeal(false)
  }
}

// ✅ REPLACE WITH:
const { mutate: logMealMutation, isPending } = useLogMeal()
const { mutate: deleteMealMutation } = useDeleteMeal()

const handleAddFood = (food) => {
  logMealMutation(
    { mealType: selectedMealType, food },
    {
      onSuccess: () => {
        setShowFoodSearch(false)
        setSearchQuery('')
      },
      onError: (err) => {
        // Show toast instead of alert
        console.error('Failed to log meal:', err)
      }
    }
  )
}

// Add delete handler:
const handleDeleteMeal = (mealId) => {
  if (confirm('Delete this meal?')) {
    deleteMealMutation(mealId)
  }
}
```

Then add delete button to MealCard:
```javascript
<BtnSecondary onClick={() => handleDeleteMeal(meal.id)}>Delete</BtnSecondary>
```

**Time:** 30 minutes  
**Why:** Proper error handling, cache invalidation, cleaner code

---

### 4️⃣ Cycle Mood Logging Not Connected
**Status:** 🟠 UI ready, backend ready, just not wired  
**Files to edit:**
- `frontend/src/components/features/cycle/Cycle.jsx` line 94

**What to do:**

In `Cycle.jsx`, find mood emoji selector and change onClick:
```javascript
// ❌ CURRENT (line ~94):
<button onClick={() => setMood(m)}>
  {m === mood ? '★' : '☆'} {moodLabels[m]}
</button>

// ✅ FIXED:
const { mutate: logMood } = useLogCycleMood()

<button 
  onClick={() => {
    setMood(m)
    logMood({ mood: m, symptom: selectedSymptom }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: KEYS.cycle })
      }
    })
  }}
>
  {m === mood ? '★' : '☆'} {moodLabels[m]}
</button>
```

**Time:** 10 minutes  
**Why:** Enables cycle mood tracking (user feature request)

---

### 5️⃣ Delete Meal Button Missing
**Status:** 🟠 Backend implemented, UI missing  
**File to edit:**
- `frontend/src/components/ui/MealCard.jsx` (or wherever MealCard renders)

**What to do:**
```javascript
// Add to MealCard component:
<BtnSecondary 
  onClick={() => onDelete(id)} 
  size="sm"
  style={{ color: '#e11d48' }}
>
  Delete
</BtnSecondary>
```

And ensure parent passes `onDelete` prop:
```javascript
<MealCard {...meal} onDelete={handleDeleteMeal} />
```

**Time:** 15 minutes

---

## 🟡 MEDIUM PRIORITY (FIX AFTER)

### 6️⃣ Cycle Phase Hardcoded in Dashboard
**Status:** ⚠️ Shows "luteal" for everyone  
**File to edit:**
- `backend/app/routes/dashboard_routes.py` line 84-88

**What to do:**
```python
# ❌ CURRENT (line 84-88):
cycle_summary = {
    "phase": "luteal",  # ← HARDCODED!
    "label": "Luteal Phase",
    ...
}

# ✅ FIXED:
if profile and profile.get("cycle_data"):
    from app.routes.cycle_routes import calculate_cycle_phase
    phase_info = calculate_cycle_phase(
        profile["cycle_data"].get("lastPeriodDate", "2024-01-01"),
        profile["cycle_data"].get("cycleLength", 28)
    )
    cycle_summary = {
        "phase": phase_info["phase"],
        "label": phase_info["label"],
        "emoji": phase_info["emoji"],
        ...
    }
else:
    cycle_summary = {"phase": "not_started", ...}
```

**Time:** 15 minutes

---

### 7️⃣ Voice Input Functions Never Imported
**Status:** 🟡 Code exists, never used  
**Files to edit:**
- `frontend/src/components/features/VoiceInput.jsx` (or VoiceModal.jsx)
- `frontend/src/hooks/useVoiceInput.js`

**What to do:**

In `VoiceInput.jsx`, add these imports:
```javascript
import { logMealWithVoice } from '@api/voice'
import { useLogMeal } from '@hooks/useQueries'
```

Then add this handler:
```javascript
const { mutate: logMeal } = useLogMeal()

const handleVoiceSubmit = async (transcript) => {
  try {
    const result = await logMealWithVoice(transcript)
    logMeal(result) // Log the parsed meal
    setTranscript('')
    showToast(`Added: ${result.name} (${result.calories} cal)`)
  } catch (err) {
    showToast(`Failed to parse: ${err.message}`, 'error')
  }
}
```

**Time:** 20 minutes  
**Why:** Voice feature currently non-functional

---

### 8️⃣ Chat Suggestions Unreliable
**Status:** 🟡 Falls back to hardcoded  
**File to edit:**
- `frontend/src/components/features/chat/Chat.jsx`
- `backend/app/routes/chat_routes.py` line 180-195

**What to do:**

Backend fix (line 180-195):
```python
# Ensure profile is loaded before generating suggestions
profile = await db.profiles.find_one({"user_id": user_id})

suggestions = []
if profile:
    segment = profile.get("segment", "adult")
    
    base_suggestions = [
        "What should I eat for breakfast?",
        "How many calories should I eat?",
        "What foods help with energy?"
    ]
    
    if "teen-girl-h" in segment or "pcos" in profile.get("conditions", []):
        base_suggestions.append("What foods help with PCOS?")
    
    if "athlete" in segment or "athletic" in profile.get("goals", []):
        base_suggestions.append("Best foods for muscle recovery?")
    
    suggestions = base_suggestions

return {"success": True, "data": suggestions}
```

**Time:** 15 minutes

---

## 🟢 LOW PRIORITY (POLISH)

### 9️⃣ Progress Goals Hardcoded
**Status:** 🟢 Works but not dynamic  
**File to edit:**
- `frontend/src/components/features/progress/Progress.jsx` line 25

**What to do:**
```javascript
// ❌ CURRENT:
const chartMeta = { goal: 1800 }  // ← Hardcoded

// ✅ FIXED:
const { data: goalsData } = useGoals() // If endpoint exists
const chartMeta = { goal: goalsData?.calories?.goal || 1800 }
```

**Time:** 10 minutes

---

### 🔟 Water Logging UI Missing
**Status:** 🟢 Backend ready, no UI  
**File to edit:**
- `frontend/src/components/features/progress/Progress.jsx`

**What to do:**
```javascript
// Add water input near weight input:
const [waterGlasses, setWaterGlasses] = useState(0)
const { mutate: logWater } = useMutation(...)

<div>
  <label>Water Intake (glasses):</label>
  <input 
    type="number" 
    min="0" 
    value={waterGlasses} 
    onChange={(e) => setWaterGlasses(e.target.value)}
  />
  <button onClick={() => logWater({ water_glasses: waterGlasses })}>
    Log Water
  </button>
</div>
```

**Time:** 15 minutes

---

### 1️⃣1️⃣ Add Meal Quantity Selector
**Status:** 🟢 Hardcoded quantity=1  
**File to edit:**
- `frontend/src/components/features/meals/Meals.jsx`

**What to do:**
```javascript
// Add state:
const [quantity, setQuantity] = useState(1)

// Add UI:
<input 
  type="number" 
  min="0.5" 
  max="5" 
  step="0.5"
  value={quantity}
  onChange={(e) => setQuantity(parseFloat(e.target.value))}
/>

// Update call:
logMealMutation({ mealType: selectedMealType, food, quantity })
```

**Time:** 15 minutes

---

## ❌ MISSING ENDPOINTS (Need Backend Work)

### Education Modules
**Status:** ❌ Returns empty array  
**File to create:**
- `backend/app/routes/education_routes.py` (if doesn't exist)

**What to add:**
```python
from fastapi import APIRouter, Request

router = APIRouter()

MODULES = [
    {
        "id": "macro-basics",
        "title": "Macro Basics 101",
        "icon": "📊",
        "description": "Learn about proteins, carbs, and fats",
        "videoUrl": "https://example.com/video1.mp4",
        "duration": 5,
        "quiz": [
            {
                "question": "What is a macronutrient?",
                "options": ["Vitamin", "Mineral", "Protein/Carbs/Fat", "None"],
                "correct": 2
            }
        ]
    },
    # Add 5-10 modules total
]

@router.get("/modules")
async def get_modules(request: Request):
    return {"success": True, "data": MODULES}

@router.post("/modules/{module_id}/complete")
async def complete_module(module_id: str, request: Request):
    # Mark module as complete for user
    user = get_current_user(request)
    db = get_db()
    await db.achievements.update_one(
        {"user_id": user["userId"]},
        {"$addToSet": {"completed_modules": module_id}},
        upsert=True
    )
    return {"success": True}
```

Don't forget to register in `backend/main.py`:
```python
from app.routes import education_routes
app.include_router(education_routes.router, prefix="/api")
```

**Time:** 45 minutes

---

### Parent Dashboard
**Status:** ❌ Returns empty object  
**File to create/fix:**
- `backend/app/routes/parent_routes.py`

**What to add:**
```python
@router.get("/parent/dashboard")
async def get_parent_dashboard(request: Request, child: str = None):
    user = get_current_user(request)
    db = get_db()
    
    if not child:
        # Return list of children
        children = await db.users.find(
            {"parent_id": user["userId"]}
        ).to_list(None)
        return {"success": True, "data": {"children": [c["name"] for c in children]}}
    
    # Get specific child's data
    child_user = await db.users.find_one({
        "name": child,
        "parent_id": user["userId"]
    })
    
    if not child_user:
        raise HTTPException(404, "Child not found")
    
    child_id = str(child_user["_id"])
    
    # Aggregate child's data
    today_meals = await db.meal_logs.find({
        "user_id": child_id,
        "date": datetime.now().strftime("%Y-%m-%d")
    }).to_list(None)
    
    progress = await db.progress_logs.find(
        {"user_id": child_id}
    ).sort("date", -1).limit(30).to_list(None)
    
    return {
        "success": True,
        "data": {
            "childName": child,
            "stats": {
                "todayCalories": sum(m.get("total_calories", 0) for m in today_meals),
                "streak": calculate_streak(progress),
                "lastLogged": progress[0]["date"] if progress else None
            },
            "recentMeals": today_meals[:5]
        }
    }
```

**Time:** 45 minutes

---

## 📋 CHECKLIST — Implementation Order

### Week 1:
- [ ] Security: Remove localStorage token (5 min)
- [ ] Fix API base URL (2 min)
- [ ] Use React Query for meal logging (30 min)
- [ ] Wire mood logging (10 min)
- [ ] Add delete meal button (15 min)
- [ ] Fix cycle phase calculation (15 min)

### Week 2:
- [ ] Import voice functions (20 min)
- [ ] Fix chat suggestions (15 min)
- [ ] Add progress goal update (10 min)
- [ ] Add water logging UI (15 min)
- [ ] Add meal quantity selector (15 min)

### Week 3:
- [ ] Implement education modules (45 min)
- [ ] Implement parent dashboard (45 min)
- [ ] Test all features
- [ ] Deploy to production

---

## 🧪 TESTING AFTER FIXES

Run these tests after each fix:

```bash
# Frontend tests
npm run dev   # Check no build errors
# Then manually:
# 1. Login/Register flow
# 2. Add meal + delete
# 3. Log mood emoji
# 4. Check chat suggestions
# 5. Verify token in cookie (F12 → Application → Cookies)

# Backend tests
pytest backend/  # If tests exist
python -m uvicorn main:app --reload  # Check endpoints respond
curl http://localhost:8000/api/modules  # Check education
```

---

## 📞 SUPPORT

If you get stuck on any fix, check:
1. Console errors (F12 → Console)
2. Network tab (F12 → Network) 
3. Backend logs (terminal where uvicorn running)
4. Compare with working feature (e.g., Meals uses logMeal correctly ✅)

