"""
Quick MVP Integration Test - Tests core user flows
Focuses on the happy path with minimal setup
"""
import asyncio
import sys
import json
from datetime import datetime, timedelta

# Start the backend
import subprocess
import time

print("\n" + "="*60)
print("MVP INTEGRATION TEST - QUICK VERIFICATION")
print("="*60 + "\n")

# Check if backend is running
print("Starting backend...")
backend_proc = subprocess.Popen(
    [sys.executable, "smartnutri-backend/main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3)  # Wait for backend to start

try:
    import requests
    
    BASE_URL = "http://localhost:3001"
    
    def api_call(method, path, body=None, headers=None):
        """Make API call"""
        h = {"Content-Type": "application/json"}
        if headers:
            h.update(headers)
        
        url = f"{BASE_URL}{path}"
        try:
            if method == "GET":
                res = requests.get(url, headers=h)
            elif method == "POST":
                res = requests.post(url, json=body, headers=h)
            elif method == "PUT":
                res = requests.put(url, json=body, headers=h)
            elif method == "PATCH":
                res = requests.patch(url, json=body, headers=h)
            
            return res.status_code, res.text
        except Exception as e:
            return 999, str(e)
    
    def test(name, method, path, body=None, headers=None, expect_success=True):
        status, response = api_call(method, path, body, headers)
        success = status < 400
        
        # Try to get error message
        try:
            data = json.loads(response)
            if isinstance(data, dict):
                msg = data.get("error", {}).get("message") or data.get("data", {}).get("message") or ""
                if msg:
                    response_preview = msg[:80]
                else:
                    response_preview = str(response)[:80]
            else:
                response_preview = str(response)[:80]
        except:
            response_preview = response[:80]
        
        passed = success == expect_success
        symbol = "✅" if passed else "❌"
        
        print(f"{symbol} {name}")
        if not passed:
            print(f"   Status: {status}, Response: {response_preview}")
        
        return success, response if success else response
    
    #tests
    token = None
    email = f"test_{datetime.now().timestamp()}@test.com"
    headers_with_token = lambda: {"Authorization": f"Bearer {token}"} if token else {}
    
    print("────── AUTH ──────")
    
    # Register
    status, resp = test("Register", "POST", "/api/auth/register", {
        "name": "Test User",
        "email": email,
        "password": "Test@123",
        "age": 25
    }, expect_success=True)
    
    if status < 400:
        try:
            data = json.loads(resp)
            token = data.get("data", {}).get("token")
        except:
            pass
    
    # Food endpoints (public)
    print("\n────── FOOD DATABASE ──────")
    test("Search foods", "GET", "/api/foods/search?q=chicken")
    test("Food categories", "GET", "/api/foods/categories")
    
    # If we have token, test protected endpoints
    if token:
        print("\n────── MEALS ──────")
        test("Log meal", "POST", "/api/meals/log", {
            "meal_type": "breakfast",
            "foods": [{
                "name": "Eggs",
                "calories": 155,
                "protein_g": 13,
                "carbs_g": 1.1,
                "fats_g": 11
            }]
        }, headers_with_token())
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        test("Fetch meals today", "GET", f"/api/meals/date/{today}", headers=headers_with_token())
        
        print("\n────── CYCLE ──────")
        test("Set cycle", "PUT", "/api/cycle/update", {
            "lastPeriodDate": (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "cycleLength": 28
        }, headers_with_token())
        
        test("Get cycle", "GET", "/api/cycle", headers=headers_with_token())
        test("Log mood", "POST", "/api/cycle/mood?mood=happy&symptom=cramps", headers=headers_with_token())
        test("Predictions", "GET", "/api/cycle/predictions", headers=headers_with_token())
        test("Stats", "GET", "/api/cycle/stats", headers=headers_with_token())
        
        print("\n────── PROGRESS ──────")
        test("Log progress", "POST", "/api/progress/log", {
            "weight": 65.5,
            "mood": "happy",
            "energy_level": 4,
            "water_glasses": 8,
            "exercise_minutes": 30
        }, headers_with_token())
        
        test("Summary", "GET", "/api/progress/summary?days=7", headers=headers_with_token())
        test("Streak", "GET", "/api/progress/streak", headers=headers_with_token())
        test("Goals", "GET", "/api/progress/goals", headers=headers_with_token())
        test("Achievements", "GET", "/api/progress/achievements", headers=headers_with_token())
        
        print("\n────── CHAT ──────")
        test("Send message", "POST", "/api/chat/message", {
            "text": "How many calories should I eat?"
        }, headers_with_token())
        
        test("Suggestions", "GET", "/api/chat/suggestions", headers=headers_with_token())
        
        print("\n────── DASHBOARD ──────")
        test("Dashboard", "GET", "/api/dashboard", headers=headers_with_token())
    
    print("\n" + "="*60)
    print("INTEGRATION TEST COMPLETE")
    print("="*60 + "\n")
    
finally:
    # Cleanup
    backend_proc.terminate()
    backend_proc.wait(timeout=5)
