import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import { BtnPrimary, BtnGhost } from '@ui'
import styles from './onboarding.module.css'

export default function OnboardingConditionsPage() {
  const navigate = useNavigate()
  const { updateOnboardingData, setOnboardingStep } = useAppStore()

  const handleNext = () => {
    setOnboardingStep(5)
    navigate({ to: '/onboarding/diet' })
  }

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent}>
        <div className={styles.header}>
          <div className={styles.progress}>Step 4 of 5</div>
          <h1>Health & Fitness Details</h1>
          <p>Help us customize your plan</p>
        </div>

        <div className={styles.placeholder}>
          <p>Conditions/Cycle/Sports selection UI</p>
          <p style={{ fontSize: 12, color: '#999' }}>This page varies by segment</p>
        </div>

        <div className={styles.formActions}>
          <BtnGhost onClick={() => navigate({ to: '/onboarding/goal' })}>Back</BtnGhost>
          <BtnPrimary onClick={handleNext}>Next</BtnPrimary>
        </div>
      </div>
    </div>
  )
}
