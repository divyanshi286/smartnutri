import { useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { useAppStore } from '@store'
import { BtnPrimary, BtnGhost } from '@ui'
import styles from './onboarding.module.css'

export default function OnboardingBasicsPage() {
  const navigate = useNavigate()
  const { onboarding, updateOnboardingData, setOnboardingStep } = useAppStore()
  const [form, setForm] = useState(onboarding.data)

  const handleNext = () => {
    updateOnboardingData({
      displayName: form.displayName,
      weight: parseFloat(form.weight),
      height: parseInt(form.height),
      activityLevel: form.activityLevel,
    })
    setOnboardingStep(3)
    navigate({ to: '/onboarding/goal' })
  }

  const isFormValid = form.displayName && form.weight && form.height && form.activityLevel

  return (
    <div className={styles.onboardingContainer}>
      <div className={styles.onboardingContent}>
        <div className={styles.header}>
          <div className={styles.progress}>Step 2 of 5</div>
          <h1>Basic Info</h1>
          <p>Let's get to know you better</p>
        </div>

        <div className={styles.form}>
          <div className={styles.formGroup}>
            <label>Display Name</label>
            <input
              type="text"
              value={form.displayName || ''}
              onChange={(e) => setForm({ ...form, displayName: e.target.value })}
              placeholder="Priya"
            />
          </div>

          <div className={styles.formRow}>
            <div className={styles.formGroup}>
              <label>Weight (kg)</label>
              <input
                type="number"
                min="30"
                max="200"
                step="0.1"
                value={form.weight || ''}
                onChange={(e) => setForm({ ...form, weight: parseFloat(e.target.value) })}
                placeholder="52"
              />
            </div>
            <div className={styles.formGroup}>
              <label>Height (cm)</label>
              <input
                type="number"
                min="100"
                max="250"
                value={form.height || ''}
                onChange={(e) => setForm({ ...form, height: parseInt(e.target.value) })}
                placeholder="162"
              />
            </div>
          </div>

          <div className={styles.formGroup}>
            <label>Activity Level</label>
            <select
              value={form.activityLevel || ''}
              onChange={(e) => setForm({ ...form, activityLevel: e.target.value })}
            >
              <option value="">Select...</option>
              <option value="sedentary">Sedentary (little exercise)</option>
              <option value="light">Light (1–3 days/week)</option>
              <option value="moderate">Moderate (3–4 days/week)</option>
              <option value="active">Active (5–6 days/week)</option>
              <option value="very_active">Very Active (daily)</option>
            </select>
          </div>
        </div>

        <div className={styles.formActions}>
          <BtnGhost onClick={() => navigate({ to: '/onboarding/segment' })}>Back</BtnGhost>
          <BtnPrimary onClick={handleNext} disabled={!isFormValid}>
            Next
          </BtnPrimary>
        </div>
      </div>
    </div>
  )
}
