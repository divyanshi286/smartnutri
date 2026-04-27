import { useState, useEffect } from 'react'
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
  const [validationErrors, setValidationErrors] = useState({})
  const [showPassword, setShowPassword] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const [focused, setFocused] = useState({})
  const [touched, setTouched] = useState({})

  const validateEmail = (email) => {
    if (!email) return 'Email is required'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Enter a valid email'
    return ''
  }

  const validatePassword = (password) => {
    if (!password) return 'Password is required'
    if (password.length < 6) return 'Password must be at least 6 characters'
    return ''
  }

  const handleFieldChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
    // Real-time validation
    if (touched[field]) {
      if (field === 'email') {
        const error = validateEmail(value)
        setValidationErrors(prev => ({ ...prev, email: error }))
      } else if (field === 'password') {
        const error = validatePassword(value)
        setValidationErrors(prev => ({ ...prev, password: error }))
      }
    }
  }

  const handleFieldBlur = (field) => {
    setTouched(prev => ({ ...prev, [field]: true }))
    if (field === 'email') {
      const error = validateEmail(formData.email)
      setValidationErrors(prev => ({ ...prev, email: error }))
    } else if (field === 'password') {
      const error = validatePassword(formData.password)
      setValidationErrors(prev => ({ ...prev, password: error }))
    }
  }

  const { mutate: login, isPending } = useMutation({
    mutationFn: ({ email, password, rememberMe }) =>
      authApi.login(email, password, rememberMe),
    onSuccess: (data) => {
      setSuccessMessage('Welcome! Redirecting...')
      setAuth({
        isAuthenticated: true,
        userId: data.userId,
        email: data.email,
      })

      // Immediately redirect (don't wait) - let onboarding guard handle routing
      if (data.onboardingComplete) {
        completeOnboarding()
        navigate({ to: '/dashboard' })
      } else {
        setOnboardingStep(data.onboardingStep || 1)
        navigate({ to: '/onboarding/segment' })
      }
    },
    onError: (error) => {
      setFieldErrors({ form: error.message || 'Login failed. Please try again.' })
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    // Validate all fields
    const emailError = validateEmail(formData.email)
    const passwordError = validatePassword(formData.password)
    
    setTouched({ email: true, password: true })
    setValidationErrors({ email: emailError, password: passwordError })
    
    if (emailError || passwordError) return
    
    setFieldErrors({})
    login(formData)
  }

  useEffect(() => {
    if (fieldErrors.form) {
      const timer = setTimeout(() => setFieldErrors({}), 5000)
      return () => clearTimeout(timer)
    }
  }, [fieldErrors.form])

  const isFormValid = formData.email && formData.password && !validationErrors.email && !validationErrors.password

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBox}>
        <div className={styles.authHeader}>
          <div className={styles.logoBounce}>🌱</div>
          <h1>Welcome Back</h1>
          <p>Sign in to continue your health journey</p>
        </div>

        {fieldErrors.form && (
          <div className={`${styles.errorBanner} ${styles.slideIn}`}>
            <span className={styles.errorIcon}>⚠</span>
            <span>{fieldErrors.form}</span>
          </div>
        )}

        {successMessage && (
          <div className={`${styles.successBanner} ${styles.slideIn}`}>
            <span className={styles.successIcon}>✓</span>
            <span>{successMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className={styles.authForm}>
          <div className={styles.formGroup}>
            <label className={styles.labelAnimated}>Email Address</label>
            <div className={styles.inputWrapper}>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => handleFieldChange('email', e.target.value)}
                onFocus={() => setFocused(prev => ({ ...prev, email: true }))}
                onBlur={() => {
                  setFocused(prev => ({ ...prev, email: false }))
                  handleFieldBlur('email')
                }}
                placeholder="you@example.com"
                className={validationErrors.email && touched.email ? styles.inputError : ''}
              />
              {focused.email && <div className={styles.focusUnderline}></div>}
            </div>
            {validationErrors.email && touched.email && (
              <span className={`${styles.fieldError} ${styles.fadeIn}`}>{validationErrors.email}</span>
            )}
          </div>

          <div className={styles.formGroup}>
            <label className={styles.labelAnimated}>Password</label>
            <div className={styles.passwordInputWrapper}>
              <input
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handleFieldChange('password', e.target.value)}
                onFocus={() => setFocused(prev => ({ ...prev, password: true }))}
                onBlur={() => {
                  setFocused(prev => ({ ...prev, password: false }))
                  handleFieldBlur('password')
                }}
                placeholder="Your password"
                className={validationErrors.password && touched.password ? styles.inputError : ''}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className={styles.togglePasswordBtn}
                tabIndex="-1"
              >
                {showPassword ? '👁' : '👁‍🗨'}
              </button>
              {focused.password && <div className={styles.focusUnderline}></div>}
            </div>
            {validationErrors.password && touched.password && (
              <span className={`${styles.fieldError} ${styles.fadeIn}`}>{validationErrors.password}</span>
            )}
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

          <BtnPrimary 
            type="submit" 
            disabled={isPending || !formData.email || !formData.password}
            className={`${styles.submitBtn} ${isPending ? styles.submitting : ''} ${isFormValid ? styles.ready : ''}`}
          >
            <span className={styles.btnContent}>
              {isPending ? (
                <>
                  <span className={styles.spinner}></span>
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </span>
          </BtnPrimary>
        </form>

        <div className={styles.authFooter}>
          <p>Don't have an account?</p>
          <button onClick={() => navigate({ to: '/auth/register' })} className={styles.linkButton}>
            Create one now
          </button>
        </div>
      </div>
    </div>
  )
}
