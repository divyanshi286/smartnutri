import { useEffect, useCallback, useState } from 'react'
import { useAppStore } from '@store'
import { useQuery } from '@tanstack/react-query'
import authApi from '@api/auth'
import { Outlet, useNavigate, useLocation } from '@tanstack/react-router'
import AppShell from './AppShell'

export default function RootLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { auth, onboarding, setAuth, setUser, setOnboardingStep, completeOnboarding, theme, dark, setTheme } = useAppStore()
  const [authCheckAttempted, setAuthCheckAttempted] = useState(false)

  // Fetch current user on app startup (always try, even if not authenticated)
  // This allows cookie-based auth to work on page refresh
  const { data: authData, isLoading, error, refetch } = useQuery({
    queryKey: ['auth', 'me'],
    queryFn: authApi.getMe,
    retry: false,
    staleTime: 5 * 60_000, // Cache for 5 minutes
    enabled: !!localStorage.getItem("token"), // Run once on startup
    refetchOnWindowFocus: false,
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
      
      if (authData.onboardingComplete && !onboarding.complete) {
        completeOnboarding()
      }
    }
    
    // Mark auth check as attempted when query finishes
    if (!isLoading) {
      setAuthCheckAttempted(true)
    }
  }, [authData, setAuth, setUser, setTheme, onboarding.complete, completeOnboarding, isLoading])

  // Auth guard: redirect non-authenticated users
  useEffect(() => {
    // Public routes that don't require auth
    const publicRoutes = ['/auth/login', '/auth/register', '/health']
    const isPublicRoute = publicRoutes.some(route => location.pathname.startsWith(route))

    // If on public route, no need to check auth
    if (isPublicRoute) return

    // If still loading auth and user set isAuthenticated in store, allow the navigation
    if (isLoading && auth.isAuthenticated) return

    // If auth check failed (error) but user manually set isAuthenticated, trust it
    if (error && auth.isAuthenticated && localStorage.getItem("token")) return

    // If auth check failed and user is not on public route, redirect to login
    if (error && !auth.isAuthenticated && !isPublicRoute) {
      navigate({ to: '/auth/login' })
      return
    }

    // Not authenticated and trying to access protected route
    if (!auth.isAuthenticated && !isPublicRoute) {
      navigate({ to: '/auth/login' })
    }
  }, [auth.isAuthenticated, isLoading, error, location.pathname, navigate, setAuth])

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

  // If authenticated and onboarding complete, show app shell (even if auth/me is loading)
  if (auth.isAuthenticated && onboarding.complete) {
    return <AppShell><Outlet /></AppShell>
  }

  // If checking auth status but not authenticated, show loading
  if (isLoading && !auth.isAuthenticated) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
        <div>Loading...</div>
      </div>
    )
  }

  // Otherwise show page content (auth or onboarding)
  return <Outlet />
}
