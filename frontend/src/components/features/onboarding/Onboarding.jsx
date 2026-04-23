import { useAppStore } from '@store'
import { Card, CardBody, BtnPrimary, BtnSecondary } from '@ui'
import styles from './Onboarding.module.css'

const GOALS = [
  { id: 'manage-weight', ico: '⚖️', title: 'Manage Weight',      sub: 'Sustainable, science-backed approach'         },
  { id: 'build-muscle',  ico: '💪', title: 'Build Muscle',        sub: 'High protein, strength-focused nutrition'     },
  { id: 'condition',     ico: '🩺', title: 'Manage a Condition',  sub: 'PCOS, Diabetes, Thyroid & more'               },
  { id: 'energy',        ico: '⚡', title: 'Boost Daily Energy',   sub: 'Feel alert and energized all day'             },
]

export default function Onboarding() {
  const { onboarding, setOnboardingGoal } = useAppStore()
  const { step, selectedGoal } = onboarding

  return (
    <div className={styles.wrap}>
      <Card style={{ maxWidth: 680, margin: '0 auto' }}>
        <CardBody style={{ padding: 32 }}>
          {/* Progress steps */}
          <div style={{ display: 'flex', gap: 6, marginBottom: 24 }}>
            {[1,2,3,4,5].map((n) => (
              <div key={n} style={{ width: 28, height: 6, borderRadius: 3, background: n <= step ? 'var(--p1)' : 'var(--border)' }}/>
            ))}
          </div>

          <div style={{ fontSize: 40, marginBottom: 16 }}>🎯</div>
          <div style={{ fontFamily: 'var(--ff-display)', fontWeight: 700, fontSize: 26, marginBottom: 8 }}>What's your main goal?</div>
          <div style={{ fontSize: 15, color: 'var(--muted)', marginBottom: 24 }}>Tell us what you're working towards — we'll build a plan just for you. You can always change this later.</div>

          {GOALS.map((g) => (
            <div
              key={g.id}
              className={`${styles.choice} ${selectedGoal === g.id ? styles.sel : ''}`}
              onClick={() => setOnboardingGoal(g.id)}
            >
              <div className={styles.choiceIco}>{g.ico}</div>
              <div>
                <div style={{ fontWeight: 700, fontSize: 14 }}>{g.title}</div>
                <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 2 }}>{g.sub}</div>
              </div>
              {selectedGoal === g.id && (
                <div style={{ width: 22, height: 22, borderRadius: '50%', background: 'var(--p1)', color: '#fff', fontSize: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', marginLeft: 'auto', flexShrink: 0 }}>✓</div>
              )}
            </div>
          ))}

          <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
            <BtnPrimary style={{ flex: 1, justifyContent: 'center', padding: 13 }}>Continue →</BtnPrimary>
            <BtnSecondary>Skip for now</BtnSecondary>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}
