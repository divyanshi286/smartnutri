import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import authApi from '@api/auth'
import { BtnPrimary } from '@ui'
import styles from './auth.module.css'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setAuth, setOnboardingStep, completeOnboarding, onboarding } = useAppStore()

  const [formData, setFormData] = useState({ email: '', password: '', rememberMe: false })
  const [fieldErrors, setFieldErrors] = useState({})

  const { mutate: login, isPending } = useMutation({
    mutationFn: ({ email, password, rememberMe }) =>
      authApi.login(email, password, rememberMe),
    onSuccess: (data) => {
      setAuth({
        isAuthenticated: true,
        userId: data.userId,
        email: data.email,
      })

      if (data.onboardingComplete) {
        completeOnboarding()
        navigate({ to: '/dashboard' })
      } else {
        setOnboardingStep(data.onboardingStep || 1)
        navigate({ to: '/onboarding/segment' })
      }
    },
    onError: (error) => {
      setFieldErrors({ form: error.message || 'Login failed' })
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!formData.email || !formData.password) {
      setFieldErrors({ form: 'Email and password required' })
      return
    }
    login(formData)
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBox}>
        <div className={styles.authHeader}>
          <div className={styles.logo}>🥗</div>
          <h1>Welcome Back</h1>
          <p>Sign in to continue your health journey</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          {fieldErrors.form && <div className={styles.errorBanner}>{fieldErrors.form}</div>}

          <div className={styles.formGroup}>
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="you@example.com"
            />
          </div>

          <div className={styles.formGroup}>
            <label>Password</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="Your password"
            />
          </div>

          <div className={styles.checkboxGroup}>
            <input
              type="checkbox"
              id="rememberMe"
              checked={formData.rememberMe}
              onChange={(e) => setFormData({ ...formData, rememberMe: e.target.checked })}
            />
            <label htmlFor="rememberMe">Remember me for 7 days</label>
          </div>

          <BtnPrimary type="submit" disabled={isPending} style={{ width: '100%' }}>
            {isPending ? 'Signing in...' : 'Sign In'}
          </BtnPrimary>
        </form>

        <div className={styles.authFooter}>
          Don't have an account?
          <button onClick={() => navigate({ to: '/auth/register' })} className={styles.linkButton}>
            Sign up
          </button>
        </div>
      </div>
    </div>
  )
}
