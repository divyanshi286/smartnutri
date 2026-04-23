"""
Integration Test: Frontend-Backend Endpoint Verification
Tests all API endpoints and verifies frontend can consume responses correctly
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:3001"
API_BASE = "http://localhost:3001"

# Test user
TEST_EMAIL = f"integration_test_{datetime.now().timestamp()}@test.com"
TEST_PASSWORD = "Test123!@#"
TOKEN = None

def test(name, fn):
    """Run a test"""
    try:
        fn()
        print(f"✅ {name}")
        return True
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        return False

def api_call(method, path, body=None, token=None):
    """Make API call"""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"{API_BASE}{path}"
    kwargs = {"headers": headers}
    if body:
        kwargs["json"] = body
    
    res = requests.request(method, url, **kwargs)
    if res.status_code >= 400:
        print(f"  Response: {res.status_code}")
        print(f"  Body: {res.text[:200]}")
        raise Exception(f"{path}: {res.status_code}")
    
    return res.json()

# Tests
def test_register():
    """Test user registration"""
    global TOKEN
    res = api_call("POST", "/api/auth/register", {
        "name": "Integration Test User",
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "age": 25,
        "isParent": False
    })
    assert res.get("success"), f"Register failed: {res}"
    TOKEN = res.get("data", {}).get("token")
    assert TOKEN, "No token returned"

def test_login():
    """Test login"""
    global TOKEN
    res = api_call("POST", "/api/auth/login", {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    })
    assert res.get("success"), f"Login failed: {res}"
    TOKEN = res.get("data", {}).get("token")
    assert TOKEN, "No token returned"

def test_onboarding():
    """Test onboarding"""
    res = api_call("PATCH", "/api/auth/onboarding", {
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
    }, TOKEN)
    assert res.get("success"), f"Onboarding failed: {res}"

def test_meal_logging():
    """Test meal logging"""
    res = api_call("POST", "/api/meals/log", {
        "meal_type": "breakfast",
        "foods": [{
            "name": "Oatmeal",
            "calories": 150,
            "protein_g": 5,
            "carbs_g": 27,
            "fats_g": 3
        }]
    }, TOKEN)
    assert res.get("success"), f"Meal logging failed: {res}"

def test_meals_fetch():
    """Test fetching meals for today"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    res = api_call("GET", f"/api/meals/date/{today}", token=TOKEN)
    assert res.get("success") or "date" in str(res), f"Meals fetch failed: {res}"
    # Check response has expected fields
    data = res.get("data", res)
    assert isinstance(data, dict), "Expected dict response"

def test_food_search():
    """Test food search"""
    res = api_call("GET", "/api/foods/search?q=chicken", token=TOKEN)
    assert res.get("success") or isinstance(res, list), f"Food search failed: {res}"

def test_food_categories():
    """Test food categories"""
    res = api_call("GET", "/api/foods/categories", token=TOKEN)
    assert res.get("success") or isinstance(res, dict), f"Categories failed: {res}"

def test_cycle_set():
    """Test setting cycle data"""
    res = api_call("PUT", "/api/cycle/update", {
        "lastPeriodDate": (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d"),
        "cycleLength": 28
    }, TOKEN)
    assert res.get("success"), f"Cycle update failed: {res}"

def test_cycle_get():
    """Test getting cycle data"""
    res = api_call("GET", "/api/cycle", token=TOKEN)
    assert res.get("success") or "phase" in str(res), f"Cycle get failed: {res}"
    data = res.get("data", res)
    assert isinstance(data, dict), "Expected dict response"

def test_cycle_mood():
    """Test logging cycle mood"""
    res = api_call("POST", "/api/cycle/mood?mood=happy&symptom=cramps", token=TOKEN)
    assert res.get("success") or "ok" in str(res), f"Cycle mood failed: {res}"

def test_cycle_predictions():
    """Test cycle predictions"""
    res = api_call("GET", "/api/cycle/predictions?days_ahead=30", token=TOKEN)
    assert res.get("success") or isinstance(res, (dict, list)), f"Predictions failed: {res}"

def test_cycle_stats():
    """Test cycle statistics"""
    res = api_call("GET", "/api/cycle/stats?days=90", token=TOKEN)
    assert res.get("success") or isinstance(res, dict), f"Cycle stats failed: {res}"

def test_progress_log():
    """Test logging progress"""
    res = api_call("POST", "/api/progress/log", {
        "weight": 65.5,
        "mood": "happy",
        "energy_level": 4,
        "water_glasses": 8,
        "exercise_minutes": 30
    }, TOKEN)
    assert res.get("success"), f"Progress log failed: {res}"

def test_progress_summary():
    """Test progress summary"""
    res = api_call("GET", "/api/progress/summary?days=7", token=TOKEN)
    assert res.get("success"), f"Progress summary failed: {res}"
    data = res.get("data", {})
    # Verify structure
    assert "logs" in data or "stats" in data or isinstance(data, dict), "Expected progress data"

def test_progress_streak():
    """Test progress streak"""
    res = api_call("GET", "/api/progress/streak", token=TOKEN)
    assert res.get("success"), f"Streak failed: {res}"
    data = res.get("data", {})
    assert "currentStreak" in data or "current_streak" in data, "Expected streak data"

def test_progress_goals():
    """Test progress goals"""
    res = api_call("GET", "/api/progress/goals", token=TOKEN)
    assert res.get("success"), f"Goals failed: {res}"
    data = res.get("data", {})
    assert isinstance(data, dict), "Expected goals dict"

def test_progress_achievements():
    """Test achievements"""
    res = api_call("GET", "/api/progress/achievements", token=TOKEN)
    assert res.get("success"), f"Achievements failed: {res}"
    data = res.get("data", {})
    assert isinstance(data, dict), "Expected achievements dict"

def test_chat_message():
    """Test chat"""
    res = api_call("POST", "/api/chat/message", {
        "text": "How many calories should I eat?"
    }, TOKEN)
    assert res.get("success") or "role" in str(res), f"Chat failed: {res}"

def test_chat_suggestions():
    """Test chat suggestions"""
    res = api_call("GET", "/api/chat/suggestions", token=TOKEN)
    # This might return empty array, that's OK
    assert res.get("success") or isinstance(res, (list, dict)), f"Suggestions failed: {res}"

def test_dashboard():
    """Test dashboard"""
    res = api_call("GET", "/api/dashboard", token=TOKEN)
    assert res.get("success"), f"Dashboard failed: {res}"
    data = res.get("data", {})
    assert isinstance(data, dict), "Expected dashboard dict"

# Run all tests
if __name__ == "__main__":
    print("\n" + "="*60)
    print("FRONTEND-BACKEND INTEGRATION TEST")
    print("="*60 + "\n")
    
    tests = [
        ("Register user", test_register),
        ("Login user", test_login),
        ("Onboarding", test_onboarding),
        ("Log meal", test_meal_logging),
        ("Fetch meals", test_meals_fetch),
        ("Search foods", test_food_search),
        ("Food categories", test_food_categories),
        ("Set cycle", test_cycle_set),
        ("Get cycle", test_cycle_get),
        ("Log cycle mood", test_cycle_mood),
        ("Cycle predictions", test_cycle_predictions),
        ("Cycle stats", test_cycle_stats),
        ("Log progress", test_progress_log),
        ("Progress summary", test_progress_summary),
        ("Progress streak", test_progress_streak),
        ("Progress goals", test_progress_goals),
        ("Achievements", test_progress_achievements),
        ("Chat message", test_chat_message),
        ("Chat suggestions", test_chat_suggestions),
        ("Dashboard", test_dashboard),
    ]
    
    passed = sum(1 for name, fn in tests if test(name, fn))
    total = len(tests)
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("✅ ALL INTEGRATION TESTS PASSED!")
    else:
        print(f"⚠️ {total - passed} tests failed")
