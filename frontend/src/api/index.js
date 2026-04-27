/**
 * api/index.js
 * Real REST API client that calls the SmartNutri backend.
 */

import { useAppStore } from '@store'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:3001'

async function apiCall(method, path, body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include', // Enable for CORS with proper headers
  }

  // Add authorization token if available
  const token = useAppStore.getState().auth.token
  if (token) {
    options.headers.Authorization = `Bearer ${token}`
  }

  if (body) options.body = JSON.stringify(body)

  const res = await fetch(`${API_BASE}${path}`, options)
  const json = await res.json()

  if (!res.ok) throw json.error || { code: 'UNKNOWN_ERROR', message: res.statusText }
  return json.data
}

/* ─── Dashboard ─── */
export const fetchDashboard = async () => {
  try {
    return await apiCall('GET', '/api/dashboard')
  } catch (err) {
    console.error('Dashboard fetch failed:', err)
    throw err
  }
}

/* ─── Meals ─── */
export const fetchMeals = async ({ date } = {}) => {
  try {
    const dateStr = date || new Date().toISOString().split('T')[0]
    return await apiCall('GET', `/api/meals/date/${dateStr}`)
  } catch (err) {
    console.error('Meals fetch failed:', err)
    throw err
  }
}

export const logMeal = async (mealType, food, quantity = 1) => {
  try {
    const mealData = {
      meal_type: mealType.toLowerCase(),
      foods: [
        {
          name: food.name,
          calories: food.calories * quantity,
          protein_g: (food.protein || food.protein_g || 0) * quantity,
          carbs_g: (food.carbs || food.carbs_g || 0) * quantity,
          fats_g: (food.fats || food.fats_g || 0) * quantity,
          fiber_g: (food.fiber || food.fiber_g || 0) * quantity,
          quantity: `${quantity} serving${quantity > 1 ? 's' : ''}`
        }
      ],
      notes: null
    }
    return await apiCall('POST', '/api/meals/log', mealData)
  } catch (err) {
    console.error('Meal logging failed:', err)
    throw err
  }
}

export const fetchWeekMeals = async () => {
  try {
    return await apiCall('GET', '/api/meals/week')
  } catch (err) {
    console.warn('Weekly meals fetch failed:', err)
    return { daily: {} }
  }
}

/* ─── Progress / Stats ─── */
export const fetchProgress = async () => {
  try {
    const [summary, streak, meals, achievements] = await Promise.all([
      apiCall('GET', '/api/progress/summary?days=7'),
      apiCall('GET', '/api/progress/streak').catch(() => ({})),
      apiCall('GET', '/api/meals/week').catch(() => ({ daily: [] })),
      apiCall('GET', '/api/progress/achievements').catch(() => ({})),
    ])
    
    // Extract stats from backend responses
    const summaryStats = summary?.stats || {}
    const currentWeight = summaryStats.currentWeight
    const logs = summary?.logs || []
    
    // Transform to component format
    const stats = [
      {
        label: 'Current Weight',
        value: currentWeight ? `${currentWeight.toFixed(1)}kg` : '—',
        ico: '⚖️',
        bg: '#fef3c7',
        color: '#92400e',
      },
      {
        label: 'Streak',
        value: `${streak.currentStreak || 0} days`,
        ico: '🔥',
        bg: '#fee2e2',
        color: '#991b1b',
      },
      {
        label: 'This Week',
        value: `${logs.length || 0} logs`,
        ico: '📊',
        bg: '#dbeafe',
        color: '#164e63',
      },
      {
        label: 'Avg Mood',
        value: summaryStats.mostCommonMood || '—',
        ico: '😊',
        bg: '#f0fdf4',
        color: '#14532d',
      },
    ]
    
    // Map daily meal data to weekly calories chart
    const today = new Date()
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    const weeklyCalories = []
    const mealsByDate = meals?.daily ? Object.entries(meals.daily).reduce((acc, [date, day]) => {
      acc[date] = day?.totalCalories || 0
      return acc
    }, {}) : {}
    
    for (let i = 6; i >= 0; i--) {
      const d = new Date(today)
      d.setDate(d.getDate() - i)
      const dateStr = d.toISOString().split('T')[0]
      const calories = mealsByDate[dateStr] || 0
      weeklyCalories.push({
        day: days[d.getDay()],
        value: calories,
        today: i === 0,
      })
    }
    
    // Transform badges
    const badges = (achievements.achievements || []).map((a, idx) => ({
      id: a.id || idx,
      emoji: a.icon || '🏆',
      label: a.name || 'Badge',
      earned: a.unlocked || false,
    }))
    
    return {
      stats,
      weeklyCalories,
      badges,
      streak: streak.currentStreak || 0,
      bestStreak: streak.bestStreak || 0,
      summary: summary || {},
    }
  } catch (err) {
    console.error('Progress fetch failed:', err)
    return {
      stats: [],
      weeklyCalories: [],
      badges: [],
      streak: 0,
      bestStreak: 0,
    }
  }
}

export const logProgress = async (progressData) => {
  try {
    return await apiCall('POST', '/api/progress/log', progressData)
  } catch (err) {
    console.error('Progress logging failed:', err)
    throw err
  }
}

/* ─── Nutrition Detail ─── */
export const fetchNutrition = async () => {
  try {
    return await apiCall('GET', '/api/nutrition/today')
  } catch (err) {
    console.error('Nutrition fetch failed:', err)
    throw err
  }
}

/* ─── Cycle ─── */
export const fetchCycle = async () => {
  try {
    const apiResp = await apiCall('GET', '/api/cycle')
    const data = apiResp
    
    // Transform backend data to frontend format
    // Backend returns: phase, label, emoji, cycleDay, description, nutritionTips, symptoms, recommendedActivity
    const phases = [
      { key: 'menstrual', label: 'Menstrual', flex: 1, color: '#e11d48', active: data.phase === 'menstrual' },
      { key: 'follicular', label: 'Follicular', flex: 1.5, color: '#d946ef', active: data.phase === 'follicular' },
      { key: 'ovulation', label: 'Ovulation', flex: 1, color: '#ec4899', active: data.phase === 'ovulation' },
      { key: 'luteal', label: 'Luteal', flex: 1.5, color: '#f43f5e', active: data.phase === 'luteal' },
    ]
    
    // Transform nutrition tips into eat/avoid foods
    const tips = data.nutritionTips || []
    const eatFoods = tips.filter(t => !t.includes('avoid') && !t.includes('❌')).slice(0, 4).map((tip, idx) => {
      const name = tip.replace(/^\s+/, '').split(':')[0] || tip
      return {
        name: name.substring(0, 20),
        reason: tip.substring(0, 40),
        emoji: ['🥗', '🥦', '🥕', '🫐'][idx % 4]
      }
    })
    
    const avoidFoods = []
    
    // Phase tips
    const phaseTips = {
      menstrual: '💡 Focus on iron-rich foods and rest. Your body needs more iron during this phase.',
      follicular: '✨ Eat light & energizing foods. Your energy is rising, try new recipes!',
      ovulation: '💪 Peak energy! Great time for workouts. Eat antioxidant-rich foods.',
      luteal: '🌙 Crave comfort foods? Add magnesium-rich foods. Reduce high-intensity exercise.',
      not_started: '📅 Set up your cycle to get personalized nutrition tips for each phase.',
      unknown: '📅 Set up your cycle to get personalized nutrition tips for each phase.',
    }
    
    // Phase guide
    const phaseGuide = [
      { phase: 'Menstrual', dot: '🔴', tips: 'Iron & Magnesium', current: data.phase === 'menstrual' },
      { phase: 'Follicular', dot: '🟣', tips: 'Light & Energizing', current: data.phase === 'follicular' },
      { phase: 'Ovulation', dot: '🟠', tips: 'Protein & Antioxidants', current: data.phase === 'ovulation' },
      { phase: 'Luteal', dot: '🟡', tips: 'Magnesium & Carbs', current: data.phase === 'luteal' },
    ]
    
    return {
      phase: data.phase,
      phaseLabel: data.label || (data.phase ? data.phase.charAt(0).toUpperCase() + data.phase.slice(1) : 'Not Set'),
      currentDay: data.cycleDay || '—',
      cycleLength: 28,
      phases,
      eatFoods: eatFoods.length > 0 ? eatFoods : generateDefaultFoods(data.phase),
      avoidFoods,
      activities: data.recommendedActivity ? [data.recommendedActivity] : [],
      phaseTip: phaseTips[data.phase] || phaseTips.not_started,
      phaseGuide,
    }
  } catch (err) {
    console.warn('Cycle fetch failed:', err)
    return {
      phase: 'not_started',
      phaseLabel: 'Setup your cycle',
      currentDay: '—',
      cycleLength: 28,
      phases: [
        { key: 'menstrual', label: 'Menstrual', flex: 1, color: '#e11d48', active: false },
        { key: 'follicular', label: 'Follicular', flex: 1.5, color: '#d946ef', active: false },
        { key: 'ovulation', label: 'Ovulation', flex: 1, color: '#ec4899', active: false },
        { key: 'luteal', label: 'Luteal', flex: 1.5, color: '#f43f5e', active: false },
      ],
      eatFoods: [],
      avoidFoods: [],
      activities: [],
      phaseTip: '📅 Set up your cycle to get personalized nutrition tips for each phase.',
      phaseGuide: [
        { phase: 'Menstrual', dot: '🔴', tips: 'Iron & magnesium', current: false },
        { phase: 'Follicular', dot: '🟣', tips: 'Light & energizing', current: false },
        { phase: 'Ovulation', dot: '🟠', tips: 'Protein & antioxidants', current: false },
        { phase: 'Luteal', dot: '🟡', tips: 'Magnesium & complex carbs', current: false },
      ],
    }
  }
}

function generateDefaultFoods(phase) {
  const defaultFoods = {
    menstrual: [
      { name: 'Red Meat', emoji: '🥩', reason: 'Iron-rich for energy' },
      { name: 'Spinach', emoji: '🥬', reason: 'Iron & magnesium' },
      { name: 'Dark Chocolate', emoji: '🍫', reason: 'Magnesium for cramps' },
      { name: 'Lentils', emoji: '🫘', reason: 'Plant-based iron' },
    ],
    follicular: [
      { name: 'Fresh Berries', emoji: '🫐', reason: 'Antioxidants' },
      { name: 'Leafy Greens', emoji: '🥗', reason: 'Light & fresh' },
      { name: 'Eggs', emoji: '🥚', reason: 'Protein for energy' },
      { name: 'Citrus Fruits', emoji: '🍊', reason: 'Vitamin C boost' },
    ],
    ovulation: [
      { name: 'Salmon', emoji: '🐟', reason: 'Omega-3s' },
      { name: 'Almonds', emoji: '🌰', reason: 'Antioxidants' },
      { name: 'Blueberries', emoji: '🫐', reason: 'Peak energy foods' },
      { name: 'Chicken Breast', emoji: '🍗', reason: 'Lean protein' },
    ],
    luteal: [
      { name: 'Avocado', emoji: '🥑', reason: 'Healthy fats' },
      { name: 'Seeds', emoji: '🌰', reason: 'Magnesium rich' },
      { name: 'Nuts', emoji: '🥜', reason: 'Mood-boosting' },
      { name: 'Sweet Potato', emoji: '🍠', reason: 'Complex carbs' },
    ],
  }
  return defaultFoods[phase] || []
}

function transformPhaseNutrition(tips, category) {
  if (!tips || !tips[category]) return []
  return tips[category].map((item, idx) => ({
    name: item.split(' - ')[0] || item,
    reason: item.split(' - ')[1] || '',
    emoji: ['🥗', '🥦', '🥕', '🫐', '🥑', '🍗'][idx % 6],
  }))
}

/* ─── Education ─── */
export const fetchModules = async () => {
  try {
    return await apiCall('GET', '/api/modules')
  } catch (err) {
    console.warn('Modules not available yet')
    return { modules: [] }
  }
}

/* ─── Parent Dashboard ─── */
export const fetchParentDashboard = async ({ child = 'Test User' } = {}) => {
  try {
    return await apiCall('GET', `/api/parent/dashboard?child=${child}`)
  } catch (err) {
    console.warn('Parent dashboard not available yet')
    return {}
  }
}

/* ─── AI Chat ─── */
export const fetchChatSuggestions = async () => {
  try {
    return await apiCall('GET', '/api/chat/suggestions')
  } catch (err) {
    console.warn('Chat suggestions not available')
    return []
  }
}

export const fetchVoiceExamples = async () => {
  try {
    return await apiCall('GET', '/api/voice/examples')
  } catch (err) {
    console.warn('Voice examples not available')
    return []
  }
}

export const sendChatMessage = async (text) => {
  try {
    return await apiCall('POST', '/api/chat/message', { text })
  } catch (err) {
    console.error('Chat message failed:', err)
    return { role: 'ai', content: 'Sorry, I could not process that request.' }
  }
}

/* ─── Food Database ─── */
export const searchFoods = async (query) => {
  try {
    return await apiCall('GET', `/api/foods/search?q=${encodeURIComponent(query)}&limit=10`)
  } catch (err) {
    console.error('Food search failed:', err)
    return []
  }
}

export const getFoodCategories = async () => {
  try {
    return await apiCall('GET', '/api/foods/categories')
  } catch (err) {
    console.error('Failed to fetch categories:', err)
    return []
  }
}

export const browseFoods = async (category) => {
  try {
    const url = category ? `/api/foods/browse?category=${encodeURIComponent(category)}&limit=20` : '/api/foods/browse?limit=20'
    return await apiCall('GET', url)
  } catch (err) {
    console.error('Food browse failed:', err)
    return []
  }
}

export const getFoodDetails = async (foodId) => {
  try {
    return await apiCall('GET', `/api/foods/${foodId}`)
  } catch (err) {
    console.error('Food details failed:', err)
    return null
  }
}

export const addFavoriteFood = async (foodId) => {
  try {
    return await apiCall('POST', `/api/foods/favorite?food_id=${foodId}`)
  } catch (err) {
    console.error('Add favorite failed:', err)
    return false
  }
}

export const getFavoriteFoods = async () => {
  try {
    return await apiCall('GET', '/api/foods/favorites')
  } catch (err) {
    console.error('Favorites fetch failed:', err)
    return []
  }
}

/* ─── Cycle Operations ─── */
export const updateCycleData = async (lastPeriodDate, cycleLength) => {
  try {
    return await apiCall('PUT', '/api/cycle/update', { lastPeriodDate, cycleLength })
  } catch (err) {
    console.error('Cycle update failed:', err)
    throw err
  }
}

export const logCycleMood = async (mood, symptom) => {
  try {
    const params = new URLSearchParams({ mood, symptom }).toString()
    return await apiCall('POST', `/api/cycle/mood?${params}`)
  } catch (err) {
    console.error('Mood logging failed:', err)
    throw err
  }
}

export const getCyclePredictions = async (daysAhead = 30) => {
  try {
    return await apiCall('GET', `/api/cycle/predictions?days_ahead=${daysAhead}`)
  } catch (err) {
    console.error('Cycle predictions failed:', err)
    return []
  }
}

export const getCycleStats = async (days = 90) => {
  try {
    return await apiCall('GET', `/api/cycle/stats?days=${days}`)
  } catch (err) {
    console.error('Cycle stats failed:', err)
    return {}
  }
}
