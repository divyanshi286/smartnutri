import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import { BtnPrimary, BtnGhost } from '@ui'
import styles from './onboarding.module.css'

const GOALS = {
  adult: [
    { id: 'weight-loss', emoji: '⚖️', title: 'Lose weight' },
    { id: 'weight-gain', emoji: '📈', title: 'Gain weight' },
    { id: 'manage-condition', emoji: '🩺', title: 'Manage my condition' },
    { id: 'maintain', emoji: '🎯', title: 'Maintain & feel great' },
  ],
  'teen-girl-h': [
    { id: 'hormone-balance', emoji: '🌙', title: 'Balance my hormones' },
    { id: 'manage-pcos', emoji: '🩺', title: 'Manage PCOS' },
    { id: 'weight-management', emoji: '⚖️', title: 'Healthy weight' },
    { id: 'energy', emoji: '⚡', title: 'More energy' },
  ],
  'teen-girl-a': [
    { id: 'performance', emoji: '🏃', title: 'Athletic performance' },
    { id: 'lean-muscle', emoji: '💪', title: 'Build lean muscle' },
    { id: 'endurance', emoji: '🚴', title: 'Improve endurance' },
    { id: 'recover', emoji: '🛌', title: 'Faster recovery' },
  ],
  'teen-boy': [
    { id: 'build-muscle', emoji: '💪', title: 'Build muscle mass' },
    { id: 'performance', emoji: '⚡', title: 'Sports performance' },
    { id: 'lean-bulk', emoji: '📈', title: 'Lean bulk' },
    { id: 'energy', emoji: '🔋', title: 'All-day energy' },
  ],
}

export default function OnboardingGoalPage() {
  const navigate = useNavigate()
  const { onboarding, updateOnboardingData, setOnboardingStep } = useAppStore()
  const segment = onboarding.data.segment
  const goals = GOALS[segment] || GOALS.adult

  const handleSelect = (goalId) => {
    updateOnboardingData({ primaryGoal: goalId })
    setOnboardingStep(4)
    navigate({ to: '/onboarding/conditions' })
  }

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent}>
        <div className={styles.header}>
          <div className={styles.progress}>Step 3 of 5</div>
          <h1>What's your primary goal?</h1>
        </div>

        <div className={styles.goalsGrid}>
          {goals.map((goal) => (
            <button
              key={goal.id}
              className={styles.goalCard}
              onClick={() => handleSelect(goal.id)}
            >
              <div className={styles.cardEmoji}>{goal.emoji}</div>
              <div className={styles.cardTitle}>{goal.title}</div>
            </button>
          ))}
        </div>

        <div className={styles.formActions}>
          <BtnGhost onClick={() => navigate({ to: '/onboarding/basics' })}>Back</BtnGhost>
        </div>
      </div>
    </div>
  )
}
