# 🚀 SmartNutri Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 16+
- MongoDB running locally (or mock)

## Part 1: Start the Backend

### 1. Install Dependencies
```bash
cd smartnutri-backend
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Backend is ready at: `http://localhost:8000`

### 3. API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Part 2: Start the Frontend

### 1. Install Dependencies
```bash
cd smartnutri-vite
npm install
```

### 2. Run the App
```bash
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

Frontend is ready at: `http://localhost:5173`

## Part 3: First Time Use

### Step 1: Register
1. Open http://localhost:5173
2. Click "Sign Up"
3. Enter:
   - Email: `test@example.com`
   - Password: `Test123!@#`
4. Click "Register"

### Step 2: Onboarding (5 Steps)
1. **Basics**: Age 20, Female
2. **Conditions**: Select any relevant conditions (optional)
3. **Diet**: Select diet preferences
4. **Cycle**: Set menstrual cycle start date
5. **Goals**: Select fitness goals

### Step 3: Explore Features

#### 📱 Log Your First Meal
1. Navigate to "Meals"
2. Click "Add Meal"
3. Search: "chicken"
4. Select "Grilled Chicken Breast"
5. See nutrition: 165 cal, 31g protein

#### 💬 Chat with NutriAI
1. Navigate to "Chat"
2. Ask: "How many calories should I eat?"
3. Get AI response

#### 🔄 Track Your Cycle
1. Navigate to "Cycle"
2. Click "Set Cycle"
3. Select start date
4. Log mood for today
5. View 30-day predictions

#### 📊 Log Your Progress
1. Navigate to "Progress"
2. Log today:
   - Weight: 65
   - Mood: 4/5
   - Energy: 3/5
   - Water: 2L
   - Exercise: 30 min
3. View trends and streaks

#### 📈 Check Dashboard
1. Navigate to "Dashboard"
2. See all your data in one place

## Testing

### Run Backend Tests
```bash
cd smartnutri-backend
pytest test_mvp_complete.py -v
```

**Expected:** 54/54 tests pass ✅

### Run Frontend Tests
```bash
pytest test_e2e.py -v
```

**Expected:** 9/9 tests pass ✅

## Common Issues

### Issue: Can't connect to MongoDB
**Solution:** Tests use MockMongo. If you see connection errors, make sure you're running from the right directory.

### Issue: CORS errors in browser console
**Solution:** The backend serves on 8000, frontend on 5173. Both configured in CORS settings.

### Issue: 401 Unauthorized
**Solution:** Token expired. Register again or login.

### Issue: AI responses not working
**Solution:** Normal - OpenAI API key not configured. App falls back to smart responses. ✅

## API Quick Reference

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!@#"}'
```

### Log Meal
```bash
curl -X POST http://localhost:8000/api/meals/log \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "food_id":"chickenbreast",
    "quantity":100,
    "date":"2024-01-15"
  }'
```

### Get Cycle
```bash
curl -X GET http://localhost:8000/api/cycle \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Log Progress
```bash
curl -X POST http://localhost:8000/api/progress/log \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "weight":65,
    "mood":4,
    "energy":3,
    "water":2000,
    "exercise":30,
    "date":"2024-01-15"
  }'
```

## Project Structure

```
smartnutri-backend/
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── app/
│   ├── models.py       # Database models
│   ├── database.py     # MongoDB connection
│   ├── security.py     # JWT auth
│   ├── utils.py        # Helpers
│   └── routes/         # API endpoints

smartnutri-vite/
├── index.html          # HTML entry point
├── package.json        # Node dependencies
├── vite.config.js      # Vite configuration
└── src/
    ├── App.jsx         # Root component
    ├── main.jsx        # React entry
    ├── router.jsx      # Routes
    ├── api/            # API calls
    ├── components/     # React components
    ├── pages/          # Page components
    └── styles/         # Global styles
```

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
JWT_SECRET=your-secret-key
JWT_EXPIRATION=86400
OPENAI_API_KEY=optional
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Commands Reference

```bash
# Backend
python main.py                 # Start server
pytest test_mvp_complete.py   # Run tests
pip install -r requirements.txt # Install deps

# Frontend
npm run dev                    # Start dev server
npm run build                  # Build for production
npm run preview               # Preview production build
npm install                   # Install dependencies
```

## Performance Tips

1. **First Load**: ~3-5 seconds (Vite build time)
2. **API Calls**: <200ms typical
3. **Page Transitions**: Instant with React Query caching
4. **Meal Search**: <500ms for 42 foods

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` then kill process |
| Port 5173 in use | `lsof -i :5173` then kill process |
| Node modules issue | `rm -rf node_modules` then `npm install` |
| Python venv issue | Create fresh venv: `python -m venv venv` |
| Bad tokens | Login again to refresh |
| Can't find food | Try partial search (e.g., "chicken" not "Grilled Chicken Breast") |

## Next Steps

1. ✅ Get backend running
2. ✅ Get frontend running
3. ✅ Register an account
4. ✅ Complete onboarding
5. ✅ Test each feature
6. ✅ Run the test suites
7. 🚀 Ready to deploy!

---

**Questions?** Check the docs in `smartnutri-backend/IMPLEMENTATION_GUIDE.md` and `smartnutri-vite/FRONTEND_GUIDE.md`

**All systems GO!** ✅
