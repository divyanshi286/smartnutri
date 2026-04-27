import requests

# First login
login_r = requests.post('http://localhost:3001/api/auth/login', json={
    'email': 'test@example.com',
    'password': 'password123'
})
token = login_r.json().get('data', {}).get('token')
print(f'Login status: {login_r.status_code}')
print(f'Token: {token[:30]}...')

# Test GET request
headers = {'Authorization': f'Bearer {token}'}
get_r = requests.get('http://localhost:3001/api/meals/date/2026-04-25', headers=headers)
print(f'GET status: {get_r.status_code}')
print(f'CORS header: {get_r.headers.get("access-control-allow-origin")}')
meals = get_r.json().get('data', [])
print(f'Meals count: {len(meals)}')
if meals:
    print(f'First meal: {meals[0].get("name")}')

