import styles from './Design.module.css'

const DOCS = [
  { title: '🔐 Privacy Principles', items: [["Data Minimization","Collect only what's needed. No passive behavioral tracking."],["Local-First Storage","Cycle, mood, and chat stored on-device by default."],["Teen Data Sovereignty","Teens control what parents see — not the reverse."],["Right to Delete","Any data deleted instantly via Settings → Privacy."],["No Data Selling","Health data is never monetized or used for ads."]] },
  { title: '🚨 Safety Systems', items: [["AI Content Filter","All teen-facing responses screened before display."],["Trigger Detection","Harmful queries → warm intervention + alternatives."],["SOS Button","Always accessible — crisis helplines one tap away."],["Parent Alerts","Nutritional alerts sent without revealing private data."],["Professional Referral","App suggests doctors/dietitians for medical concerns."]] },
  { title: '💚 Empowerment Values', items: [["Never Shame","Missed a day? \"Let's get back on track! 🌱\" Not guilt."],["Celebrate Progress","Streaks, badges, and warm positive reinforcement."],["Body Positivity","No \"ideal weight.\" Focus on health and how you feel."],["Education First","Every recommendation explains the WHY behind it."],["Supportive Friend","AI speaks like a kind, informed, non-judgmental friend."]] },
]

const A11Y = [
  { ico:'👆', title:'Touch Targets', body:'All tappable elements minimum 44×44px. FAB is 54×54px. Phase dots have 32px hit areas despite 14px visual size.' },
  { ico:'🎨', title:'Color Contrast', body:'Text meets WCAG AA (4.5:1). Safety warnings meet AAA (7:1). Charts use color + shape + icon — never color alone.' },
  { ico:'📢', title:'Screen Reader', body:'ARIA labels on all icons and charts. Rings announce "78g of 110g protein goal — 71% complete". Swipe actions have button equivalents.' },
  { ico:'📖', title:'Reading Support', body:'Fraunces chosen for rounded letterforms. Line-height 1.75 throughout. OpenDyslexic font option in Settings. 1.6× text scale supported.' },
]

export default function PrivacyDoc() {
  return (
    <div className={styles.wrap}>
      <div className={styles.docGrid}>
        {DOCS.map((doc) => (
          <div key={doc.title} className={styles.docCard}>
            <div className={styles.docTitle}>{doc.title}</div>
            {doc.items.map(([label, body]) => (
              <div key={label} style={{ marginBottom: 10 }}>
                <div style={{ fontWeight: 700, fontSize: 13, color: 'var(--text)' }}>{label}</div>
                <div style={{ fontSize: 12, color: 'var(--muted)', lineHeight: 1.65, marginTop: 2 }}>{body}</div>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div className={styles.section}>
        <div className={styles.sectionTitle}>♿ Accessibility Annotations</div>
        <div className={styles.a11yGrid}>
          {A11Y.map((a) => (
            <div key={a.title} className={styles.a11yCard}>
              <div style={{ fontSize: 24, marginBottom: 8 }}>{a.ico}</div>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 6 }}>{a.title}</div>
              <div style={{ fontSize: 12, color: 'var(--muted)', lineHeight: 1.65 }}>{a.body}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
