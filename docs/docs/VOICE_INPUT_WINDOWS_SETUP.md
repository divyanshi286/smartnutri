# Phase 2.1: Voice Input - Windows PowerShell Quick Start

**Platform:** Windows PowerShell  
**Date:** April 7, 2026  
**Status:** Ready to Test

---

## ⚠️ Important: PowerShell Syntax

### Command Chaining in PowerShell
```powershell
# ❌ WRONG (bash syntax)
python main.py && npm run dev

# ✅ RIGHT (PowerShell syntax)
python main.py; npm run dev

# ✅ BETTER: Run in separate terminals (recommended)
# Terminal 1:
python main.py

# Terminal 2:
cd smartnutri-vite
npm run dev
```

---

## 🚀 Setup Option 1: Separate Terminals (RECOMMENDED)

### Terminal 1: Backend
```powershell
# Navigate to project
cd c:\Users\Dell\Downloads\smartnutri-vite
cd smartnutri-backend

# Activate venv
.\..\\.venv\Scripts\Activate.ps1

# Start backend
python main.py
```

**Expected Output:**
```
[OK] Connected to MongoDB
[OK] Database already has N users
INFO:     Uvicorn running on http://127.0.0.1:3001
```

### Terminal 2: Frontend
```powershell
# Navigate to project
cd c:\Users\Dell\Downloads\smartnutri-vite
cd smartnutri-vite

# Install dependencies (if needed)
npm install

# Start dev server
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### Terminal 3: Test Voice (Browser)
```
1. Open browser to http://localhost:5173
2. Register/Login
3. Navigate to Meals section
4. Click "Voice" tab
5. Click "Start Recording"
6. Say: "I had grilled chicken with rice"
7. Click "Stop & Log"
8. Verify meal logged with ~280 calories
```

---

## 🚀 Setup Option 2: Using PowerShell Profiles

Create a startup script that runs both in separate jobs:

### Create Script: `start-dev.ps1`
```powershell
# File: c:\Users\Dell\Downloads\smartnutri-vite\start-dev.ps1

param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$All
)

$projectPath = "c:\Users\Dell\Downloads\smartnutri-vite"

if ($All -or $Backend) {
    Write-Host "Starting Backend..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList {
        cd $projectPath
        cd smartnutri-backend
        .\..\\.venv\Scripts\Activate.ps1
        python main.py
    } -NoNewWindow -PassThru
    
    Start-Sleep -Seconds 2
}

if ($All -or $Frontend) {
    Write-Host "Starting Frontend..." -ForegroundColor Green
    Start-Process powershell -ArgumentList {
        cd $projectPath
        cd smartnutri-vite
        npm run dev
    } -NoNewWindow -PassThru
}

Write-Host "`nServices started!" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "Backend: http://localhost:3001" -ForegroundColor Cyan
```

### Run Both Services
```powershell
# Run from project root
powershell -ExecutionPolicy Bypass -File start-dev.ps1 -All
```

---

## 🧪 Testing Voice Input

### Test in Browser Console

```javascript
// Check browser support
console.log('Speech Recognition:', !!window.SpeechRecognition);

// Check microphone access
navigator.mediaDevices.enumerateDevices()
  .then(devices => console.log('Audio:', devices.filter(d => d.kind === 'audioinput')));

// Manual speech test
const r = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
r.onresult = (e) => console.log('Heard:', e.results[0][0].transcript);
r.start();
```

---

## 📋 Complete Testing Workflow

### Step 1: Start Backend (Terminal 1)
```powershell
cd c:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend
.\..\\.venv\Scripts\Activate.ps1
python main.py
```

Wait for: `INFO:     Uvicorn running on http://127.0.0.1:3001`

### Step 2: Start Frontend (Terminal 2)
```powershell
cd c:\Users\Dell\Downloads\smartnutri-vite\smartnutri-vite
npm run dev
```

Wait for: `Local: http://localhost:5173/`

### Step 3: Open Browser (Terminal 3 - or just use browser)
```
http://localhost:5173
```

### Step 4: Test Voice Feature
```
1. Click "Register" or "Login"
2. Fill in credentials
3. Navigate to "Meals" section
4. Click "Voice" tab
5. Allow microphone permission
6. Click "Start Recording"
7. Say clearly: "Grilled salmon with vegetables"
8. Click "Stop & Log"
9. Verify response: ✅ "Grilled salmon with Vegetables logged! ~280 cal"
```

---

## 🧹 Cleanup

### Stop Services (When Done)
```powershell
# In each Terminal window: Press Ctrl+C

# Or kill all Python/Node processes
Stop-Process -Name python -Force
Stop-Process -Name node -Force
```

### Clean Database (Optional)
```powershell
# Clear test data
cd c:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend
python seed_db.py
```

---

## 🐛 Troubleshooting

### Error: Activation Script Not Found
```powershell
# Try alternative path
.\smartnutri-vite\.venv\Scripts\Activate.ps1
```

### Error: npm: The term 'npm' is not recognized
```powershell
# Install Node.js from https://nodejs.org/
# Or use: npm from the correct path
C:\Program Files\nodejs\npm.cmd install
```

### Error: Python module not found
```powershell
# Reinstall dependencies
cd smartnutri-backend
pip install -r requirements.txt
```

### Error: Port 3001 already in use
```powershell
# Kill process using port 3001
Get-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess | Stop-Process -Force

# Or use different port
python main.py --port 3002
```

### Microphone Permission Denied
```
1. Settings → Privacy & Security → Microphone
2. Enable microphone access
3. Scroll down and find "Google Chrome" or your browser
4. Toggle ON
5. Reload browser page
```

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:3001 (✅ check: visit in browser)
- [ ] Frontend running on http://localhost:5173 (✅ check: see page load)
- [ ] Can register/login (✅ check: create test account)
- [ ] Voice tab visible in Meals section (✅ check: 3 tabs shown)
- [ ] Can click "Start Recording" (✅ check: button responds)
- [ ] Microphone permission granted (✅ check: no permission popup)
- [ ] Can speak and see transcript (✅ check: words appear in real-time)
- [ ] Can stop and submit (✅ check: meal logged)

---

## 📊 Expected Results

### Voice Recording Test
```
Input: "I had chicken and rice"

Expected API Response:
{
  "foodName": "Chicken with Rice",
  "calories": 295,
  "protein": 31,
  "carbs": 28,
  "fat": 4,
  "source": "voice",
  "confidence": 0.95
}

UI Display: ✅ "Chicken with Rice logged! ~295 cal"
```

### Confidence Scoring
| Speech Quality | Expected Confidence |
|---|---|
| Clear speech | 90-99% |
| Normal speech | 70-85% |
| Quiet/Unclear | 30-60% |
| Silence | 0% (error message) |

---

## 🔗 Quick Links

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3001
- **Food Suggestions:** http://localhost:3001/api/voice/food-suggestions?query=chicken
- **Food Info:** http://localhost:3001/api/voice/food-info?food_name=chicken

---

## 📝 Logging Voice Test

### Manual API Test (PowerShell)
```powershell
# Test voice endpoint directly
Invoke-RestMethod -Uri "http://localhost:3001/api/voice/food-suggestions?query=chicken" `
  -Method GET

# Should return:
# suggestions: ["chicken", "chicken sandwich", "chickpea"]
```

### Test Meal Logging (PowerShell)
```powershell
$body = @{
    mealDescription = "grilled chicken with rice"
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
    confidence = 0.95
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer YOUR_TOKEN_HERE"  # Use real token
}

Invoke-RestMethod -Uri "http://localhost:3001/api/voice/log-meal" `
  -Method POST `
  -Body $body `
  -Headers $headers
```

---

## 🎯 What to Expect

✅ **Working Features:**
- Real-time voice transcription
- Food recognition from description
- Automatic nutrition calculation
- Meal logging to database
- Success feedback messages
- Error handling & fallbacks
- Mobile responsive UI
- Clear microphone animations

⚠️ **Known Limitations:**
- First request may take 2-3 seconds
- Requires HTTPS for production microphone
- Some browsers may require special permissions
- Accuracy depends on speech clarity

---

## 📞 Need Help?

Check logs in terminals:
- **Backend:** Shows API requests and errors
- **Frontend:** Open Developer Tools (F12) → Console

Common issues:
1. Microphone permission - check Settings
2. Port in use - kill process and restart
3. Module not found - reinstall with pip/npm
4. CORS errors - check backend CORS config

---

**Ready to test? Open the terminals and follow the steps above!** 🚀
