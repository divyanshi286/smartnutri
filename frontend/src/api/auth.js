const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001'

/**
 * Unified API client with error handling
 * Credentials included for httpOnly cookie authentication
 */
async function apiCall(method, path, body = null) {
  const token = localStorage.getItem("token")

  const headers = {
    'Content-Type': 'application/json',
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const options = {
    method,
    headers,
    credentials: 'include', // Enable credentials for CORS
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  const res = await fetch(`${API_BASE}${path}`, options)

  let json = {}
  try {
    json = await res.json()
  } catch {
    throw { message: "Invalid backend response" }
  }

  if (!res.ok) {
    throw json.error || { message: res.statusText }
  }

  return json.data
}

export const authApi = {
  // POST /api/auth/register
  register: async (payload) => {
    return apiCall('POST', '/api/auth/register', {
      name: payload.name,
      email: payload.email,
      password: payload.password,
      age: payload.age,
      isParent: payload.isParent || false,
    })
  },

  // POST /api/auth/login
  login: async (email, password, rememberMe = false) => {
  const data = await apiCall('POST', '/api/auth/login', { email, password, rememberMe })

  localStorage.setItem("token", data.token)   // 

  return data
},

  // POST /api/auth/logout
  logout: async () => {
    return apiCall('POST', '/api/auth/logout')
  },

  // GET /api/auth/me
  getMe: async () => {
    return apiCall('GET', '/api/auth/me')
  },

  // PATCH /api/auth/onboarding
  saveOnboarding: async (payload) => {
    return apiCall('PATCH', '/api/auth/onboarding', {
      segment: payload.segment,
      displayName: payload.displayName,
      weight: payload.weight,
      height: payload.height,
      activityLevel: payload.activityLevel,
      primaryGoal: payload.primaryGoal,
      conditions: payload.conditions || [],
      cycleData: payload.cycleData || null,
      sportType: payload.sportType || null,
      trainingFrequency: payload.trainingFrequency || null,
      dietPreferences: payload.dietPreferences || [],
      allergies: payload.allergies || null,
      indianCuisine: payload.indianCuisine !== false,
    })
  },

  // POST /api/auth/forgot-password
  forgotPassword: async (email) => {
    return apiCall('POST', '/api/auth/forgot-password', { email })
  },

  // POST /api/auth/reset-password
  resetPassword: async (token, newPassword) => {
    return apiCall('POST', '/api/auth/reset-password', { token, newPassword })
  },
}

export default authApi
