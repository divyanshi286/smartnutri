import { useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import authApi from '@api/auth'
import { BtnPrimary } from '@ui'
import styles from './onboarding.module.css'

export default function OnboardingCompletePage() {
  const navigate = useNavigate()
  const { onboarding, completeOnboarding, setTheme, user } = useAppStore()

  const { mutate: saveOnboarding, isPending, isError, error } = useMutation({
    mutationFn: authApi.saveOnboarding,
    onSuccess: (data) => {
      // Update theme and greeting
      if (data.theme) setTheme(data.theme)

      // Mark onboarding complete
      completeOnboarding()

      // Auto-navigate after celebration
      setTimeout(() => {
        navigate({ to: '/dashboard' })
      }, 2500)
    },
  })

  useEffect(() => {
    // Auto-submit on mount
    saveOnboarding(onboarding.data)
  }, [])

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent} style={{ textAlign: 'center' }}>
        {isPending && (
          <>
            <div className={styles.header}>
              <div className={styles.spinnerEmoji}>🎉</div>
              <h1>Setting up your personalized plan...</h1>
            </div>
          </>
        )}

        {isError && (
          <>
            <div className={styles.header}>
              <div style={{ fontSize: 60 }}>❌</div>
              <h1>Something went wrong</h1>
              <p style={{ color: '#ef4444' }}>{error.message}</p>
            </div>
            <div className={styles.formActions}>
              <BtnPrimary onClick={() => saveOnboarding(onboarding.data)}>
                Try Again
              </BtnPrimary>
            </div>
          </>
        )}

        {!isPending && !isError && (
          <>
            <div className={styles.header}>
              <div style={{ fontSize: 60, animation: 'bounce 0.6s infinite' }}>🌟</div>
              <h1>Welcome to SmartNutri!</h1>
              <p>Your personalized nutrition plan is ready.</p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
