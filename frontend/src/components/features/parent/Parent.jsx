import { useAppStore } from '@store'
import { useParentDashboard } from '@hooks/useQueries'
import { StatCard, BtnPrimary, Skeleton } from '@ui'
import styles from './Parent.module.css'

export default function Parent() {
  const { selectedChild, setSelectedChild } = useAppStore()
  const { data, isLoading } = useParentDashboard(selectedChild)

  return (
    <div className={styles.wrap}>
      {/* Hero */}
      <div className={styles.hero}>
        <div style={{ position: 'absolute', width: 200, height: 200, background: 'rgba(255,255,255,.05)', borderRadius: '50%', top: -60, right: -40 }}/>
        <div style={{ fontSize: 11, opacity: .7, textTransform: 'uppercase', letterSpacing: '.6px', fontWeight: 700, marginBottom: 4 }}>Parent View</div>
        <div style={{ fontFamily: 'var(--ff-display)', fontWeight: 700, fontSize: 28 }}>Family Dashboard</div>
        <div style={{ display: 'flex', gap: 8, marginTop: 14, flexWrap: 'wrap' }}>
          {['Ananya', 'Rohan'].map((child) => (
            <button key={child} className={`${styles.childChip} ${selectedChild === child ? styles.chipOn : ''}`} onClick={() => setSelectedChild(child)}>
              {child === 'Ananya' ? '👧' : '👦'} {child}
            </button>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className={styles.statsGrid}>
        {isLoading
          ? [1,2,3,4].map(i => <Skeleton key={i} h={72} radius={16}/>)
          : data?.stats?.map((s) => <StatCard key={s.label} ico={s.ico} bg={s.bg} label={s.label} value={s.value}/>)
        }
      </div>

      <div className={styles.grid}>
        <div>
          {data?.alert && (
            <div className={styles.alertCard}>
              <div style={{ fontSize: 13, fontWeight: 700, color: '#c2410c', marginBottom: 6 }}>⚠️ {data.alert.title}</div>
              <div style={{ fontSize: 13, color: '#9a3412', lineHeight: 1.65 }}>{data.alert.body}</div>
              <BtnPrimary style={{ marginTop: 12, padding: '8px 16px', fontSize: 13 }}>See Meal Suggestion →</BtnPrimary>
            </div>
          )}
          {!data?.alert && !isLoading && (
            <div className={styles.okCard}>✅ All nutrition targets on track for {selectedChild} today!</div>
          )}
        </div>

        <div className={styles.privCard}>
          <div style={{ fontSize: 13, fontWeight: 700, color: '#1d4ed8', marginBottom: 10 }}>🔒 What you can & can't see</div>
          <div style={{ fontSize: 13, color: '#1e40af', lineHeight: 2 }}>
            ✅ Nutrition summary & alerts<br/>
            ✅ Meal log names only<br/>
            ✅ Streak & hydration stats<br/>
            ❌ Cycle / period data<br/>
            ❌ AI chat history<br/>
            ❌ Mood logs
          </div>
          <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 12, fontStyle: 'italic' }}>Teen controls all sharing. They can revoke access anytime.</div>
        </div>
      </div>
    </div>
  )
}
