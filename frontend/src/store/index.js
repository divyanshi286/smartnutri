import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const initialAuthState = {
  isAuthenticated: false,
  userId: null,
  email: null,
  isParent: false,
}

const initialOnboardingState = {
  step: 0,
  complete: false,
  data: {
    segment: null,
    displayName: null,
    weight: null,
    height: null,
    activityLevel: null,
    primaryGoal: null,
    conditions: [],
    cycleData: null,
    sportType: null,
    trainingFrequency: null,
    dietPreferences: [],
    allergies: null,
    indianCuisine: true,
  },
}

export const useAppStore = create(
  persist(
    (set, get) => ({
      /* ── Theme ── */
      theme: 'th-adult',
      dark: false,
      setTheme: (theme) => set({ theme }),
      toggleDark: () => set((s) => ({ dark: !s.dark })),

      /* ── Auth ── */
      auth: initialAuthState,
      setAuth: (payload) => set((s) => ({ auth: { ...s.auth, ...payload } })),
      clearAuth: () => set({ auth: initialAuthState }),

      /* ── User Profile ── */
      user: null,
      setUser: (user) => set({ user }),
      updateUser: (patch) => set((s) => ({ user: { ...s.user, ...patch } })),

      /* ── Onboarding ── */
      onboarding: initialOnboardingState,
      setOnboardingStep: (step) => set((s) => ({ onboarding: { ...s.onboarding, step } })),
      updateOnboardingData: (patch) => set((s) => ({
        onboarding: { ...s.onboarding, data: { ...s.onboarding.data, ...patch } }
      })),
      completeOnboarding: () => set((s) => ({
        onboarding: { ...s.onboarding, complete: true, step: 5 }
      })),
      resetOnboarding: () => set({ onboarding: initialOnboardingState }),

      /* ── UI State ── */
      activePage: 'dashboard',
      setActivePage: (page) => set({ activePage: page }),
      voiceOpen: false,
      setVoiceOpen: (open) => set({ voiceOpen: open }),
      sidebarOpen: false,
      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      /* ── Chat ── */
      messages: [],
      setMessages: (messages) => set({ messages }),
      addMessage: (message) => set((s) => ({ messages: [...s.messages, { id: `msg-${Date.now()}`, ...message }] })),
      clearMessages: () => set({ messages: [] }),

      /* ── Meals ── */
      meals: [],
      setMeals: (meals) => set({ meals }),
      addMeal: (meal) => set((s) => ({ meals: [...s.meals, { ...meal, id: meal?.id || `m${Date.now()}` }] })),
      removeMeal: (id) => set((s) => ({ meals: s.meals.filter((item) => item.id !== id) })),

      /* ── Cycle ── */
      cycle: null,
      setCycle: (cycle) => set({ cycle }),
      setCycleMood: (mood) => set((s) => ({ cycle: { ...s.cycle, mood } })),

      /* ── Badges ── */
      badges: [],
      setBadges: (badges) => set({ badges }),

      /* ── Parent ── */
      selectedChild: null,
      setSelectedChild: (name) => set({ selectedChild: name }),
    }),
    {
      name: 'smartnutri-store',
      partialize: (state) => ({
        theme: state.theme,
        dark: state.dark,
        auth: {
          isAuthenticated: state.auth.isAuthenticated,
          userId: state.auth.userId,
          email: state.auth.email,
          token: state.auth.token,
          isParent: state.auth.isParent,
        },
        onboarding: {
          step: state.onboarding.step,
          complete: state.onboarding.complete,
        },
        selectedChild: state.selectedChild,
      }),
    }
  )
)
