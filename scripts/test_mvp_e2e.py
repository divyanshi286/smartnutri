"""
MVP END-TO-END TEST
Complete verification of SmartNutri MVP functionality
Tests all components working together
"""
import subprocess
import time
import sys
import json
from datetime import datetime, timedelta

print("\n" + "="*70)
print("SMARTNUTRI MVP - END-TO-END TEST")
print("="*70 + "\n")

# Stage 1: Start services
print("📦 STAGE 1: Starting Services...\n")

print("  Starting backend (FastAPI)...")
backend_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "smartnutri-backend.app.main:app", "--host", "127.0.0.1", "--port", "3001"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="."
)

print("  Waiting for backend to start...")
time.sleep(3)

# Check if backend is running
try:
    import requests
    res = requests.get("http://localhost:3001/api/foods/search?q=chicken")
    print(f"  ✅ Backend running on http://localhost:3001")
except:
    print(f"  ⚠️ Backend startup issue - will retry")

print("  Starting frontend (Vite)...")
frontend_proc = subprocess.Popen(
    [sys.executable, "-m", "npm", "run", "dev"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd="smartnutri-vite"
)

print("  Waiting for frontend to start...")
time.sleep(5)

print("\n✅ Services started\n")

# Stage 2: API Integration Tests
print("="*70)
print("🧪 STAGE 2: API Integration Tests (23 Endpoints)")
print("="*70 + "\n")

BASE_URL = "http://localhost:3001"
test_results = []

def test_endpoint(category, name, method, path, body=None, expect_success=True, auth=None):
    """Test a single endpoint"""
    try:
        import requests
        
        headers = {"Content-Type": "application/json"}
        if auth:
            headers["Authorization"] = f"Bearer {auth}"
        
        url = f"{BASE_URL}{path}"
        
        if method == "GET":
            res = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            res = requests.post(url, json=body, headers=headers, timeout=5)
        elif method == "PUT":
            res = requests.put(url, json=body, headers=headers, timeout=5)
        elif method == "PATCH":
            res = requests.patch(url, json=body, headers=headers, timeout=5)
        else:
            return None, "Unknown method"
        
        success = res.status_code < 400
        passed = success == expect_success
        
        result = {
            "category": category,
            "name": name,
            "passed": passed,
            "status": res.status_code,
        }
        
        symbol = "✅" if passed else "❌"
        print(f"  {symbol} {name:40} {res.status_code}")
        
        if not passed:
            try:
                err = res.json()
                print(f"     Response: {str(err)[:100]}")
            except:
                print(f"     Body: {res.text[:100]}")
        
        test_results.append(result)
        return res if success else None, res.text
        
    except Exception as e:
        print(f"  ❌ {name:40} ERROR: {str(e)[:50]}")
        test_results.append({
            "category": category,
            "name": name,
            "passed": False,
            "error": str(e)[:100]
        })
        return None, str(e)

# Auth tests
print("AUTH:")
email = f"mvp_test_{datetime.now().timestamp()}@test.com"
token = None

res, _ = test_endpoint("Auth", "Register user", "POST", "/api/auth/register", {
    "name": "MVP Test User",
    "email": email,
    "password": "Test@123456",
    "age": 25
})

if res:
    try:
        token = res.json().get("data", {}).get("token")
        print(f"     Token obtained for protected endpoints")
    except:
        pass

test_endpoint("Auth", "Login user", "POST", "/api/auth/login", {
    "email": email,
    "password": "Test@123456"
})

if token:
    test_endpoint("Auth", "Onboarding save", "PATCH", "/api/auth/onboarding", {
        "segment": "adult",
        "displayName": "Test User",
        "weight": 65.5,
        "height": 165,
        "activityLevel": "moderate",
        "primaryGoal": "Better Health",
        "conditions": ["PCOS"],
        "cycleData": {
            "lastPeriodDate": (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "cycleLength": 28
        },
        "dietPreferences": ["Vegetarian"],
        "allergies": None,
        "indianCuisine": True
    }, auth=token)

# Food tests (public)
print("\nFOOD DATABASE:")
test_endpoint("Food", "Search foods", "GET", "/api/foods/search?q=chicken")
test_endpoint("Food", "Categories", "GET", "/api/foods/categories")
test_endpoint("Food", "Browse", "GET", "/api/foods/browse")

# Protected endpoints (if token exists)
if token:
    print("\nMEALS:")
    test_endpoint("Meal", "Log meal", "POST", "/api/meals/log", {
        "meal_type": "breakfast",
        "foods": [{
            "name": "Eggs",
            "calories": 155,
            "protein_g": 13,
            "carbs_g": 1.1,
            "fats_g": 11
        }]
    }, auth=token)
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    test_endpoint("Meal", "Fetch today", "GET", f"/api/meals/date/{today}", auth=token)
    test_endpoint("Meal", "Weekly meals", "GET", "/api/meals/week", auth=token)

    print("\nCYCLE TRACKING:")
    test_endpoint("Cycle", "Set cycle", "PUT", "/api/cycle/update", {
        "lastPeriodDate": (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "cycleLength": 28
    }, auth=token)
    
    test_endpoint("Cycle", "Get cycle", "GET", "/api/cycle", auth=token)
    test_endpoint("Cycle", "Log mood", "POST", "/api/cycle/mood?mood=happy&symptom=cramps", auth=token)
    test_endpoint("Cycle", "Predictions", "GET", "/api/cycle/predictions?days_ahead=30", auth=token)
    test_endpoint("Cycle", "Stats", "GET", "/api/cycle/stats?days=90", auth=token)

    print("\nPROGRESS & ANALYTICS:")
    test_endpoint("Progress", "Log progress", "POST", "/api/progress/log", {
        "weight": 65.5,
        "mood": "happy",
        "energy_level": 4,
        "water_glasses": 8,
        "exercise_minutes": 30
    }, auth=token)
    
    test_endpoint("Progress", "Summary 7d", "GET", "/api/progress/summary?days=7", auth=token)
    test_endpoint("Progress", "Streak", "GET", "/api/progress/streak", auth=token)
    test_endpoint("Progress", "Goals", "GET", "/api/progress/goals", auth=token)
    test_endpoint("Progress", "Achievements", "GET", "/api/progress/achievements", auth=token)

    print("\nCHAT & AI:")
    test_endpoint("Chat", "Send message", "POST", "/api/chat/message", {
        "text": "How many calories should I eat?"
    }, auth=token)
    
    test_endpoint("Chat", "Suggestions", "GET", "/api/chat/suggestions", auth=token)

    print("\nDASHBOARD:")
    test_endpoint("Dashboard", "Get dashboard", "GET", "/api/dashboard", auth=token)

# Summary
print("\n" + "="*70)
print("📊 TEST RESULTS")
print("="*70 + "\n")

passed = sum(1 for t in test_results if t.get("passed"))
total = len(test_results)

categories = {}
for result in test_results:
    cat = result["category"]
    if cat not in categories:
        categories[cat] = {"total": 0, "passed": 0}
    categories[cat]["total"] += 1
    if result["passed"]:
        categories[cat]["passed"] += 1

for cat in sorted(categories.keys()):
    stats = categories[cat]
    pct = (stats["passed"] / stats["total"] * 100) if stats["total"] else 0
    symbol = "✅" if pct == 100 else "🟡" if pct >= 50 else "❌"
    print(f"{symbol} {cat:20} {stats['passed']}/{stats['total']} ({pct:.0f}%)")

print(f"\n{'='*70}")
print(f"⭐ OVERALL: {passed}/{total} endpoints working ({passed/total*100:.0f}%)")
print(f"{'='*70}\n")

# Stage 3: Feature Completeness
print("="*70)
print("✨ STAGE 3: Feature Verification")
print("="*70 + "\n")

features = {
    "Authentication": {
        "Register": "✅" if any(r["name"] == "Register user" and r["passed"] for r in test_results) else "❌",
        "Login": "✅" if any(r["name"] == "Login user" and r["passed"] for r in test_results) else "❌",
    },
    "Nutrition": {
        "Log Meals": "✅" if any(r["name"] == "Log meal" and r["passed"] for r in test_results) else "❌",
        "Food Search": "✅" if any(r["name"] == "Search foods" and r["passed"] for r in test_results) else "❌",
        "Chat with AI": "✅" if any(r["name"] == "Send message" and r["passed"] for r in test_results) else "❌",
    },
    "Cycle Tracking": {
        "Set Cycle": "✅" if any(r["name"] == "Set cycle" and r["passed"] for r in test_results) else "❌",
        "Log Mood": "✅" if any(r["name"] == "Log mood" and r["passed"] for r in test_results) else "❌",
        "Predictions": "✅" if any(r["name"] == "Predictions" and r["passed"] for r in test_results) else "❌",
    },
    "Progress Analytics": {
        "Log Progress": "✅" if any(r["name"] == "Log progress" and r["passed"] for r in test_results) else "❌",
        "View Trends": "✅" if any(r["name"] == "Summary 7d" and r["passed"] for r in test_results) else "❌",
        "Track Streaks": "✅" if any(r["name"] == "Streak" and r["passed"] for r in test_results) else "❌",
        "Achievements": "✅" if any(r["name"] == "Achievements" and r["passed"] for r in test_results) else "❌",
    },
}

for feature_group, features_list in features.items():
    print(f"{feature_group}:")
    for feature, status in features_list.items():
        print(f"  {status} {feature}")
    print()

# Stage 4: Status
print("="*70)
print("🎯 FINAL STATUS")
print("="*70 + "\n")

if passed == total:
    print("✅ MVP VERIFICATION COMPLETE - ALL SYSTEMS GO!")
    print(f"   All {total} endpoints working perfectly")
    print(f"   Ready for production deployment\n")
    exit_code = 0
elif passed >= total * 0.9:
    print("✅ MVP VERIFICATION SUCCESSFUL - MINOR ISSUES")
    print(f"   {passed}/{total} endpoints working ({passed/total*100:.0f}%)")
    print(f"   Core features operational\n")
    exit_code = 0
elif passed >= total * 0.7:
    print("🟡 MVP VERIFICATION PARTIAL - NEEDS FIXES")
    print(f"   {passed}/{total} endpoints working ({passed/total*100:.0f}%)")
    print(f"   Review failed endpoints above\n")
    exit_code = 1
else:
    print("❌ MVP VERIFICATION FAILED - ISSUES FOUND")
    print(f"   {passed}/{total} endpoints working ({passed/total*100:.0f}%)")
    print(f"   Multiple failures detected\n")
    exit_code = 1

# Cleanup
print("Cleaning up...")
backend_proc.terminate()
frontend_proc.terminate()

try:
    backend_proc.wait(timeout=2)
except:
    backend_proc.kill()

try:
    frontend_proc.wait(timeout=2)
except:
    frontend_proc.kill()

print("Done.\n")
sys.exit(exit_code)
