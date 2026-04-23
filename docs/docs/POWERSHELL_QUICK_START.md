# PowerShell Quick Command Reference

## ❌ Don't Use This (Bash Syntax)
```bash
python main.py && npm run dev
```

## ✅ Use This Instead (PowerShell)

### Option A: Two Separate Terminals (BEST)

**Terminal 1 - Backend:**
```powershell
cd C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend
..\..\smartnutri-vite\.venv\Scripts\Activate.ps1
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-vite
npm run dev
```

### Option B: Single Terminal (Sequential)
```powershell
# Run backend, wait for it to start (takes 3 seconds)
cd C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend; .\..\smartnutri-vite\.venv\Scripts\Activate.ps1; python main.py

# Wait for "Uvicorn running" message, then Ctrl+C and run:
cd ..\smartnutri-vite; npm run dev
```

### Option C: PowerShell Semicolon (Sequential)
```powershell
cd C:\Users\Dell\Downloads\smartnutri-vite; python main.py; npm run dev
```

---

## PowerShell Syntax Reference

| Task | Bash | PowerShell |
|------|------|-----------|
| Chain commands | `cmd1 && cmd2` | `cmd1; cmd2` |
| Stop on error | `set -e` | `$ErrorActionPreference = "Stop"` |
| Run if success | `cmd1 && cmd2` | `if ($?) { cmd2 }` |
| Find port | `lsof -i :3001` | `Get-NetTCPConnection -LocalPort 3001` |
| Kill process | `pkill python` | `Stop-Process -Name python` |
| Set var | `export VAR=val` | `$env:VAR="val"` |

---

## Current Setup Status

### Backend
```
Location: C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend
Port: 3001
Status: ✅ Ready to start
```

### Frontend
```
Location: C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-vite
Port: 5173
Status: ✅ Ready to start
```

### Virtual Environment
```
Location: C:\Users\Dell\Downloads\smartnutri-vite\.venv
Status: ✅ Created and activated
```

---

## Start Testing in 3 Steps

### Step 1: Open First PowerShell Window
```powershell
cd C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-backend
.\..\smartnutri-vite\.venv\Scripts\Activate.ps1
python main.py

# Wait for: "Uvicorn running on http://127.0.0.1:3001"
```

### Step 2: Open Second PowerShell Window
```powershell
cd C:\Users\Dell\Downloads\smartnutri-vite\smartnutri-vite
npm run dev

# Wait for: "Local: http://localhost:5173/"
```

### Step 3: Open Browser
```
http://localhost:5173
```

**Done!** Now test the voice feature:
1. Login/Register
2. Go to Meals → Voice tab
3. Say: "I had grilled chicken with rice"
4. Click Stop & Log
5. See: ✅ "Chicken with Rice logged! ~295 cal"

---

## Troubleshooting

### "Script cannot be loaded"
```powershell
# Run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv:
.\.venv\Scripts\Activate.ps1
```

### "'npm' is not recognized"
```powershell
# Check if Node is installed:
node --version

# If not, install from: https://nodejs.org/
# Then close and reopen PowerShell
```

### "Port 3001 already in use"
```powershell
# Kill the process using port 3001:
Get-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess | Stop-Process -Force

# Then try again
```

---

## ✅ Voice Input is Ready!

All files created and integrated:
- ✅ Frontend hook (useVoiceInput.js)
- ✅ Frontend component (VoiceInput.jsx)
- ✅ Backend endpoint (voice_routes.py)
- ✅ API integration (voice.js)
- ✅ 100+ food database
- ✅ Testing guide

**Just start the services and test!** 🚀
