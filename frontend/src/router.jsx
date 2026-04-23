import { RootRoute, Route, Router } from '@tanstack/react-router'
import RootLayout from '@layout/RootLayout'
import NotFound from '@pages/NotFound'

// Auth pages
import LoginPage from '@pages/auth/LoginPage'
import RegisterPage from '@pages/auth/RegisterPage'

// Onboarding pages
import OnboardingSegmentPage from '@pages/onboarding/OnboardingSegmentPage'
import OnboardingBasicsPage from '@pages/onboarding/OnboardingBasicsPage'
import OnboardingGoalPage from '@pages/onboarding/OnboardingGoalPage'
import OnboardingConditionsPage from '@pages/onboarding/OnboardingConditionsPage'
import OnboardingDietPage from '@pages/onboarding/OnboardingDietPage'
import OnboardingCompletePage from '@pages/onboarding/OnboardingCompletePage'

// Dashboard pages
import Dashboard from '@features/dashboard/Dashboard'
import Chat from '@features/chat/Chat'
import Meals from '@features/meals/Meals'
import Progress from '@features/progress/Progress'
import Nutrition from '@features/nutrition/Nutrition'
import Cycle from '@features/cycle/Cycle'
import Education from '@features/education/Education'
import Safety from '@features/safety/Safety'
import Parent from '@features/parent/Parent'

// Root route with layout
const rootRoute = new RootRoute({
  component: RootLayout,
  notFoundComponent: NotFound,
})

// Auth routes (no auth required)
const loginRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/auth/login',
  component: LoginPage,
})

const registerRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/auth/register',
  component: RegisterPage,
})

// Onboarding routes (requires auth, not onboarding complete)
const onboardingSegmentRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/segment',
  component: OnboardingSegmentPage,
})

const onboardingBasicsRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/basics',
  component: OnboardingBasicsPage,
})

const onboardingGoalRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/goal',
  component: OnboardingGoalPage,
})

const onboardingConditionsRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/conditions',
  component: OnboardingConditionsPage,
})

const onboardingDietRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/diet',
  component: OnboardingDietPage,
})

const onboardingCompleteRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/onboarding/complete',
  component: OnboardingCompletePage,
})

// Dashboard routes (requires auth + onboarding complete)
const dashboardRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: Dashboard,
})

const chatRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/chat',
  component: Chat,
})

const mealsRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/meals',
  component: Meals,
})

const progressRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/progress',
  component: Progress,
})

const nutritionRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/nutrition',
  component: Nutrition,
})

const cycleRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/cycle',
  component: Cycle,
})

const educationRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/education',
  component: Education,
})

const safetyRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/safety',
  component: Safety,
})

const parentRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/parent',
  component: Parent,
})

// 404 route
const notFoundRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '*',
  component: NotFound,
})

// Create route tree
const routeTree = rootRoute.addChildren([
  loginRoute,
  registerRoute,
  onboardingSegmentRoute,
  onboardingBasicsRoute,
  onboardingGoalRoute,
  onboardingConditionsRoute,
  onboardingDietRoute,
  onboardingCompleteRoute,
  dashboardRoute,
  chatRoute,
  mealsRoute,
  progressRoute,
  nutritionRoute,
  cycleRoute,
  educationRoute,
  safetyRoute,
  parentRoute,
  notFoundRoute,
])

// Create router
export const router = new Router({ routeTree })
