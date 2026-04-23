"""
Debug Cycle Endpoint
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:3001"
session = requests.Session()

# Create and login user
test_email = f"debug_{int(datetime.now().timestamp())}@example.com"

resp = session.post(f"{BASE_URL}/api/auth/register", json={
    "name": "Debug User",
    "email": test_email,
    "password": "Test123!",
    "age": 28,
    "isParent": False
})

session.post(f"{BASE_URL}/api/auth/login", json={
    "email": test_email,
    "password": "Test123!"
})

# Try to fetch cycle
resp = session.get(f"{BASE_URL}/api/cycle")
print(f"Status: {resp.status_code}")
print(f"Response:")
print(json.dumps(resp.json(), indent=2))
