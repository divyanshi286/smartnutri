import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  fetchDashboard,
  fetchMeals,
  fetchProgress,
  fetchNutrition,
  fetchCycle,
  fetchModules,
  fetchParentDashboard,
  fetchChatSuggestions,
  fetchVoiceExamples,
  sendChatMessage,
  searchFoods,
  getFoodCategories,
  browseFoods,
  getFoodDetails,
  getFavoriteFoods,
  updateCycleData,
  logCycleMood,
  getCyclePredictions,
  getCycleStats,
  logProgress,
} from '@api'

/* ── Query Keys ── */
export const KEYS = {
  dashboard:  ['dashboard'],
  meals:      (date) => ['meals', date],
  progress:   ['progress'],
  nutrition:  ['nutrition'],
  cycle:      ['cycle'],
  modules:    ['modules'],
  parent:     (child) => ['parent', child],
}

/* ── Dashboard ── */
export const useDashboard = () =>
  useQuery({ queryKey: KEYS.dashboard, queryFn: fetchDashboard, staleTime: 5 * 60_000 })

/* ── Meals ── */
export const useMeals = (date) =>
  useQuery({ queryKey: KEYS.meals(date), queryFn: () => fetchMeals({ date }), staleTime: 2 * 60_000 })

/* ── Progress ── */
export const useProgress = () =>
  useQuery({ queryKey: KEYS.progress, queryFn: fetchProgress, staleTime: 5 * 60_000 })

/* ── Nutrition ── */
export const useNutrition = () =>
  useQuery({ queryKey: KEYS.nutrition, queryFn: fetchNutrition, staleTime: 5 * 60_000 })

/* ── Cycle ── */
export const useCycle = () =>
  useQuery({ queryKey: KEYS.cycle, queryFn: fetchCycle, staleTime: 10 * 60_000 })

/* ── Education Modules ── */
export const useModules = () =>
  useQuery({ queryKey: KEYS.modules, queryFn: fetchModules, staleTime: 30 * 60_000 })

/* ── Parent Dashboard ── */
export const useParentDashboard = (child) =>
  useQuery({ queryKey: KEYS.parent(child), queryFn: () => fetchParentDashboard({ child }), staleTime: 5 * 60_000 })

/* ── Chat Suggestions ── */
export const useChatSuggestions = () =>
  useQuery({ queryKey: ['chat', 'suggestions'], queryFn: fetchChatSuggestions, staleTime: 15 * 60_000 })

/* ── Voice Examples ── */
export const useVoiceExamples = () =>
  useQuery({ queryKey: ['voice', 'examples'], queryFn: fetchVoiceExamples, staleTime: 60 * 60_000 })

/* ── Chat Mutation ── */
export const useSendChat = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: sendChatMessage,
    onSuccess: () => qc.invalidateQueries({ queryKey: KEYS.nutrition }),
  })
}

/* ── Cycle Mutations ── */
export const useUpdateCycle = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ lastPeriodDate, cycleLength }) => updateCycleData(lastPeriodDate, cycleLength),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.cycle })
    },
  })
}

export const useLogCycleMood = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ mood, symptom }) => logCycleMood(mood, symptom),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.cycle })
    },
  })
}

/* ── Progress Mutation ── */
export const useLogProgress = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: logProgress,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: KEYS.progress })
    },
  })
}

/* ── Food Database ── */
export const useSearchFoods = (query) =>
  useQuery({
    queryKey: ['foods', 'search', query],
    queryFn: () => searchFoods(query),
    enabled: !!(query && query.length > 1),
    staleTime: 5 * 60_000
  })

export const useFoodCategories = () =>
  useQuery({
    queryKey: ['foods', 'categories'],
    queryFn: getFoodCategories,
    staleTime: 30 * 60_000
  })

export const useBrowseFoods = (category) =>
  useQuery({
    queryKey: ['foods', 'browse', category],
    queryFn: () => browseFoods(category),
    staleTime: 10 * 60_000
  })

export const useFoodDetails = (foodId) =>
  useQuery({
    queryKey: ['foods', foodId],
    queryFn: () => getFoodDetails(foodId),
    enabled: !!foodId,
    staleTime: 30 * 60_000
  })

export const useFavoriteFoods = () =>
  useQuery({
    queryKey: ['foods', 'favorites'],
    queryFn: getFavoriteFoods,
    staleTime: 10 * 60_000
  })
