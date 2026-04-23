import { useEffect, useCallback } from 'react'
import { useAppStore } from '@store'
import { useQuery } from '@tanstack/react-query'
import authApi from '@api/auth'
import { Outlet, useNavigate, useLocation } from '@tanstack/react-router'
import AppShell from './AppShell'

export default function RootLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { auth, onboarding, setAuth, setUser, setOnboardingStep, completeOnboarding, theme, dark, setTheme } = useAppStore()

  // Fetch current user on app startup (runs once)
  const { data: authData, isLoading, error } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: authApi.getMe,
    retry: false,
    staleTime: 5 * 60_000, // Cache for 5 minutes
  })

  // Hydrate store when auth data loads
  useEffect(() => {
    if (authData) {
      setAuth({
        isAuthenticated: true,
        userId: authData.userId,
        email: authData.email,
      })
      setUser({
        name: authData.name,
        email: authData.email,
        segment: authData.segment,
        initials: authData.name?.charAt(0).toUpperCase(),
      })
      
      if (authData.theme) {
        setTheme(authData.theme)
      }
      
      if (authData.onboardingComplete !== onboarding.complete) {
        completeOnboarding()
      }
    }
  }, [authData, setAuth, setUser, setTheme, onboarding.complete, completeOnboarding])

  // Auth guard: redirect non-authenticated users
  useEffect(() => {
    // Public routes that don't require auth
    const publicRoutes = ['/auth/login', '/auth/register', '/health']
    const isPublicRoute = publicRoutes.some(route => location.pathname.startsWith(route))

    if (!auth.isAuthenticated && !isPublicRoute) {
      // Not logged in and trying to access protected route
      navigate({ to: '/auth/login' })
    }
  }, [auth.isAuthenticated, location.pathname, navigate])

  // Onboarding guard: redirect incomplete onboarding
  useEffect(() => {
    if (!auth.isAuthenticated) return

    const onboardingRoutes = ['/onboarding/segment', '/onboarding/basics', '/onboarding/goal', '/onboarding/conditions', '/onboarding/diet', '/onboarding/complete']
    const dashboardRoutes = ['/dashboard', '/chat', '/meals', '/progress', '/nutrition', '/cycle', '/education', '/safety', '/parent']
    
    const isOnboardingRoute = onboardingRoutes.some(route => location.pathname.startsWith(route))
    const isDashboardRoute = dashboardRoutes.some(route => location.pathname.startsWith(route))

    if (!onboarding.complete && isDashboardRoute) {
      // Onboarding not complete but trying to access dashboard
      navigate({ to: '/onboarding/segment' })
    }

    if (onboarding.complete && isOnboardingRoute) {
      // Onboarding complete but trying to access onboarding routes
      navigate({ to: '/dashboard' })
    }
  }, [auth.isAuthenticated, onboarding.complete, location.pathname, navigate])

  // Apply theme
  useEffect(() => {
    const body = document.body
    body.className = [theme, dark ? 'dark' : ''].filter(Boolean).join(' ')
  }, [theme, dark])

  // If checking auth status, show loading
  if (isLoading && auth.isAuthenticated) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    )
  }

  // If authenticated and onboarding complete, show app shell
  if (auth.isAuthenticated && onboarding.complete) {
    return <AppShell><Outlet /></AppShell>
  }

  // Otherwise show page content (auth or onboarding)
  return <Outlet />
}
