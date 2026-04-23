"""
Simple Cycle Data Test
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:3001"
session = requests.Session()

test_email = f"ct_{int(datetime.now().timestamp())}@test.com"

# 1. Register
print("1. Register...")
r1 = session.post(f"{BASE_URL}/api/auth/register", json={
    "name": "Cycle Test", "email": test_email,
    "password": "Test123!", "age": 28, "isParent": False
})
print(f"   Status: {r1.status_code}")

# 2. Login
print("2. Login...")
r2 = session.post(f"{BASE_URL}/api/auth/login", json={
    "email": test_email, "password": "Test123!"
})
print(f"   Status: {r2.status_code}")

# 3. Onboard
print("3. Onboard...")
r3 = session.patch(f"{BASE_URL}/api/auth/onboarding", json={
    "segment": "adult", "displayName": "Test", "weight": 70, "height": 170,
    "activityLevel": "moderate", "primaryGoal": "weight_loss", "conditions": [],
    "dietPreferences": ["balanced"],
})
print(f"   Status: {r3.status_code}")

# 4. Update cycle
print("4. Update cycle...")
r4 = session.put(f"{BASE_URL}/api/cycle/update", json={
    "lastPeriodDate": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
    "cycleLength": 28
})
print(f"   Status: {r4.status_code}")
if r4.status_code == 200:
    print(f"   ✅ Cycle updated")
else:
    print(f"   ❌ Error: {r4.json()}")

# 5. Get cycle
print("5. Get cycle...")
r5 = session.get(f"{BASE_URL}/api/cycle")
print(f"   Status: {r5.status_code}")
data = r5.json()
print(f"   Response: {json.dumps(data, indent=2)[:500]}")
