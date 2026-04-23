import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import { BtnPrimary, BtnGhost } from '@ui'
import styles from './onboarding.module.css'

export default function OnboardingDietPage() {
  const navigate = useNavigate()
  const { updateOnboardingData, setOnboardingStep } = useAppStore()

  const handleNext = () => {
    setOnboardingStep(6)
    navigate({ to: '/onboarding/complete' })
  }

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent}>
        <div className={styles.header}>
          <div className={styles.progress}>Step 5 of 5</div>
          <h1>Diet Preferences</h1>
          <p>Any allergies or dietary restrictions?</p>
        </div>

        <div className={styles.placeholder}>
          <p>Diet preferences & allergies UI</p>
          <p style={{ fontSize: 12, color: '#999' }}>Multi-select + text input</p>
        </div>

        <div className={styles.formActions}>
          <BtnGhost onClick={() => navigate({ to: '/onboarding/conditions' })}>Back</BtnGhost>
          <BtnPrimary onClick={handleNext}>Review & Complete</BtnPrimary>
        </div>
      </div>
    </div>
  )
}
