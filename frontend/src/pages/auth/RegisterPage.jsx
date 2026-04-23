import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import authApi from '@api/auth'
import { BtnPrimary, BtnGhost } from '@ui'
import styles from './auth.module.css'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { setAuth, setOnboardingStep, updateOnboardingData } = useAppStore()
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    age: '',
    isParent: false,
    showPassword: false,
  })

  const [fieldErrors, setFieldErrors] = useState({})

  const { mutate: register, isPending } = useMutation({
    mutationFn: authApi.register,
    onSuccess: (data) => {
      // Store auth in Zustand
      setAuth({
        isAuthenticated: true,
        userId: data.userId,
        email: data.email,
      })

      // Initialize onboarding data
      updateOnboardingData({ segment: data.segment })
      setOnboardingStep(1)

      // Navigate to segment selection
      navigate({ to: '/onboarding/segment' })
    },
    onError: (error) => {
      if (error.fields) {
        setFieldErrors(error.fields)
      } else {
        setFieldErrors({ form: error.message || 'Registration failed' })
      }
    },
  })

  const validateForm = () => {
    const errors = {}

    if (!formData.name.trim()) errors.name = 'Name is required'
    if (!formData.email.trim()) errors.email = 'Email is required'
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) errors.email = 'Invalid email'
    if (formData.password.length < 8) errors.password = 'Min 8 characters'
    if (formData.password !== formData.confirmPassword) errors.confirmPassword = 'Passwords do not match'
    if (!formData.age || formData.age < 10 || formData.age > 100) errors.age = 'Valid age required (10–100)'

    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validateForm()) return

    register({
      name: formData.name,
      email: formData.email,
      password: formData.password,
      age: parseInt(formData.age),
      isParent: formData.isParent,
    })
  }

  return (
    <div className={styles.authContainer}>
      <div className={styles.authBox}>
        <div className={styles.authHeader}>
          <div className={styles.logo}>🥗</div>
          <h1>Create Account</h1>
          <p>Join SmartNutri for personalized nutrition</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          {fieldErrors.form && <div className={styles.errorBanner}>{fieldErrors.form}</div>}

          <div className={styles.formGroup}>
            <label>Full Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className={fieldErrors.name ? styles.inputError : ''}
              placeholder="Priya Sharma"
            />
            {fieldErrors.name && <span className={styles.fieldError}>{fieldErrors.name}</span>}
          </div>

          <div className={styles.formGroup}>
            <label>Email</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className={fieldErrors.email ? styles.inputError : ''}
              placeholder="you@example.com"
            />
            {fieldErrors.email && <span className={styles.fieldError}>{fieldErrors.email}</span>}
          </div>

          <div className={styles.formGroup}>
            <label>Password</label>
            <div className={styles.passwordInput}>
              <input
                type={formData.showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className={fieldErrors.password ? styles.inputError : ''}
                placeholder="Min 8 characters"
              />
              <button
                type="button"
                className={styles.togglePassword}
                onClick={() => setFormData({ ...formData, showPassword: !formData.showPassword })}
              >
                {formData.showPassword ? '👁' : '👁‍🗨'}
              </button>
            </div>
            {fieldErrors.password && <span className={styles.fieldError}>{fieldErrors.password}</span>}
          </div>

          <div className={styles.formGroup}>
            <label>Confirm Password</label>
            <input
              type={formData.showPassword ? 'text' : 'password'}
              value={formData.confirmPassword}
              onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
              className={fieldErrors.confirmPassword ? styles.inputError : ''}
              placeholder="Confirm password"
            />
            {fieldErrors.confirmPassword && <span className={styles.fieldError}>{fieldErrors.confirmPassword}</span>}
          </div>

          <div className={styles.formGroup}>
            <label>Age</label>
            <input
              type="number"
              min="10"
              max="100"
              value={formData.age}
              onChange={(e) => setFormData({ ...formData, age: e.target.value })}
              className={fieldErrors.age ? styles.inputError : ''}
              placeholder="23"
            />
            {fieldErrors.age && <span className={styles.fieldError}>{fieldErrors.age}</span>}
          </div>

          <div className={styles.checkboxGroup}>
            <input
              type="checkbox"
              id="isParent"
              checked={formData.isParent}
              onChange={(e) => setFormData({ ...formData, isParent: e.target.checked })}
            />
            <label htmlFor="isParent">I am a parent creating an account for my child</label>
          </div>

          <BtnPrimary type="submit" disabled={isPending} style={{ width: '100%', marginTop: 16 }}>
            {isPending ? 'Creating account...' : 'Create Account'}
          </BtnPrimary>
        </form>

        <div className={styles.authFooter}>
          Already have an account?
          <button
            onClick={() => navigate({ to: '/auth/login' })}
            className={styles.linkButton}
          >
            Log in
          </button>
        </div>
      </div>
    </div>
  )
}
