#!/usr/bin/env python3
"""
Backend API Testing Script
Tests all SmartNutri endpoints to verify functionality
"""

import json
import subprocess
import time
import os

BASE_URL = "http://localhost:3001"

# Test credentials from seed data
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def run_curl(method, path, body=None, headers=None, cookies=None):
    """Execute curl command and return response"""
    cmd = ['curl', '-s', '-X', method]
    
    # Add headers
    if headers:
        for key, val in headers.items():
            cmd.extend(['-H', f'{key}: {val}'])
    else:
        cmd.extend(['-H', 'Content-Type: application/json'])
    
    # Add body
    if body:
        cmd.extend(['-d', json.dumps(body)])
    
    # Add cookies
    if cookies:
        for key, val in cookies.items():
            cmd.extend(['-b', f'{key}={val}'])
    
    cmd.append(f'{BASE_URL}{path}')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw": result.stdout}
    except Exception as e:
        return {"error": str(e)}

def test_endpoint(name, method, path, body=None, cookies=None, should_succeed=True):
    """Test an endpoint and report results"""
    print(f"\nTesting: {name}")
    print(f"  {method} {path}")
    
    response = run_curl(method, path, body, cookies=cookies)
    
    if "error" in response and "raw" not in response:
        status = f"{RED}FAIL{RESET}"
        print(f"  {status}: {response['error']}")
        return None
    
    success = response.get("success", True)
    if success == should_succeed:
        status = f"{GREEN}PASS{RESET}"
        print(f"  {status}")
        return response
    else:
        status = f"{RED}FAIL{RESET}"
        print(f"  {status}: Unexpected response")
        print(f"  Response: {json.dumps(response, indent=2)}")
        return None

print(f"\n{YELLOW}=== SmartNutri Backend API Test Suite ==={RESET}\n")

# 1. Health Check
print(f"\n{YELLOW}[1] HEALTH CHECK{RESET}")
test_endpoint("Health", "GET", "/health")

# 2. Authentication Tests
print(f"\n{YELLOW}[2] AUTHENTICATION ENDPOINTS{RESET}")

# Register
print("\n  Registering new user...")
register_resp = test_endpoint(
    "Register",
    "POST",
    "/api/auth/register",
    {
        "name": "Test User 2",
        "email": "test2@example.com",
        "password": "password123",
        "age": 25
    }
)

# Login
login_resp = test_endpoint(
    "Login",
    "POST", 
    "/api/auth/login",
    {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
)

# Extract token from response if available (stored in cookies)
jwt_token = None
if login_resp and 'data' in login_resp:
    print(f"  Login successful!")
    # We'll need to capture cookie from curl properly
    # For now, we'll use a basic test

# 3. Chat Endpoints
print(f"\n{YELLOW}[3] AI CHAT ENDPOINTS{RESET}")

test_endpoint("Chat - Get Suggestions", "GET", "/api/chat/suggestions")

# 4. Food Database Endpoints
print(f"\n{YELLOW}[4] FOOD DATABASE ENDPOINTS{RESET}")

test_endpoint("Food - Search", "GET", "/api/foods/search?q=chicken&limit=5")
test_endpoint("Food - Categories", "GET", "/api/foods/categories")
test_endpoint("Food - Browse (Grains)", "GET", "/api/foods/browse?category=grains&limit=10")

# 5. Meals Endpoints
print(f"\n{YELLOW}[5] MEALS ENDPOINTS{RESET}")

test_endpoint("Meals - Get by Date", "GET", f"/api/meals/date/{time.strftime('%Y-%m-%d')}")
test_endpoint("Meals - Weekly", "GET", "/api/meals/week")

# 6. Nutrition Endpoints
print(f"\n{YELLOW}[6] NUTRITION ENDPOINTS{RESET}")

test_endpoint("Nutrition - Today", "GET", "/api/nutrition/today")

# 7. Dashboard Endpoints
print(f"\n{YELLOW}[7] DASHBOARD ENDPOINTS{RESET}")

test_endpoint("Dashboard", "GET", "/api/dashboard")

# 8. Progress Endpoints
print(f"\n{YELLOW}[8] PROGRESS ENDPOINTS{RESET}")

test_endpoint("Progress - Summary", "GET", "/api/progress/summary?days=7")

print(f"\n{YELLOW}=== Test Suite Complete ==={RESET}\n")
print(f"Note: Some tests require authentication. Install 'requests' for full testing:")
print(f"  pip install requests")
print(f"  python test_backend_complete.py")
