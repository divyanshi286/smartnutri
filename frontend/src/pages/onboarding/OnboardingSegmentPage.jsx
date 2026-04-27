import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import { BtnPrimary } from '@ui'
import { Leaf, Heart, Zap, Dumbbell } from 'lucide-react'
import styles from './onboarding.module.css'

const SEGMENTS = [
  { id: 'adult', icon: Leaf, title: 'Adult (20+)', sub: 'Manage health conditions, weight, energy' },
  { id: 'teen-girl-h', icon: Heart, title: 'Teen — Hormonal Health', sub: 'Cycle tracking, PCOS-aware, hormone balance' },
  { id: 'teen-girl-a', icon: Zap, title: 'Teen — Athletic', sub: 'Performance nutrition, muscle & endurance' },
  { id: 'teen-boy', icon: Dumbbell, title: 'Teen Boy', sub: 'Muscle building, sports performance, growth' },
]

const SEGMENT_THEME_MAP = {
  adult: 'th-adult',
  'teen-girl-h': 'th-girl-h',
  'teen-girl-a': 'th-girl-a',
  'teen-boy': 'th-boy',
}

export default function OnboardingSegmentPage() {
  const navigate = useNavigate()
  const { onboarding, updateOnboardingData, setTheme, setOnboardingStep } = useAppStore()

  const handleSelect = (segmentId) => {
    updateOnboardingData({ segment: segmentId })
    setTheme(SEGMENT_THEME_MAP[segmentId])
    setOnboardingStep(2)
    navigate({ to: '/onboarding/basics' })
  }

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent}>
        <div className={styles.header}>
          <div className={styles.progress}>Step 1 of 5</div>
          <h1>Who are you?</h1>
          <p>We'll personalize nutrition advice based on your segment</p>
        </div>

        <div className={styles.segmentCards}>
          {SEGMENTS.map((seg) => {
            const IconComponent = seg.icon
            return (
              <button key={seg.id} className={styles.segmentCard} onClick={() => handleSelect(seg.id)}>
                <div className={styles.cardEmoji}><IconComponent size={48} strokeWidth={1.5} /></div>
                <div className={styles.cardTitle}>{seg.title}</div>
                <div className={styles.cardSub}>{seg.sub}</div>
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
