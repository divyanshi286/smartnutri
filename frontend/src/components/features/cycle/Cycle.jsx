import { useState } from 'react'
import { useCycle } from '@hooks/useQueries'
import { Card, CardHeader, CardBody, Skeleton } from '@ui'
import styles from './Cycle.module.css'

export default function Cycle() {
  const { data, isLoading } = useCycle()
  const [mood, setMood] = useState(null)

  return (
    <div className={styles.wrap}>
      {/* Phase Hero */}
      <div className={styles.phaseBanner}>
        <div style={{ position: 'absolute', width: 200, height: 200, background: 'rgba(232,121,160,.1)', borderRadius: '50%', top: -60, right: -40 }}/>
        <span className={styles.privPill}>🔒 Private · Only you can see this</span>
        <div className={styles.phaseTitle}>🌸 Cycle Dashboard</div>
        <div className={styles.phaseLabel}>Day {data?.currentDay} of {data?.cycleLength} · {data?.phaseLabel}</div>

        {!isLoading && data?.phases && (
          <div style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', gap: 2, borderRadius: 8, overflow: 'hidden', height: 18 }}>
              {data.phases.map((p) => (
                <div key={p.key} style={{ flex: p.flex, background: p.color, position: 'relative' }}>
                  {p.active && <div style={{ position: 'absolute', top: '50%', right: -9, transform: 'translateY(-50%)', width: 18, height: 18, borderRadius: '50%', background: '#2563eb', border: '2px solid white' }}/>}
                </div>
              ))}
            </div>
            <div style={{ display: 'flex', marginTop: 8 }}>
              {data.phases.map((p) => <span key={p.key} style={{ flex: p.flex, fontSize: 11, fontWeight: 700, color: 'rgba(255,255,255,.8)', textAlign: 'center' }}>{p.label}</span>)}
            </div>
          </div>
        )}
      </div>

      <div className={styles.grid}>
        <div>
          <Card style={{ marginBottom: 16 }}>
            <CardHeader title="✨ Phase Foods — Ovulation"/>
            <CardBody>
              {isLoading ? <Skeleton h={120} radius={12}/> : (
                <>
                  <div style={{ fontWeight: 700, fontSize: 13, color: '#065f46', marginBottom: 8 }}>✅ Eat these</div>
                  <div className={styles.foodGrid}>
                    {data?.eatFoods?.map((f) => (
                      <div key={f.name} className={styles.foodCard} style={{ background: 'linear-gradient(135deg,#fce4ec,#fff)', borderColor: '#f9a8d4' }}>
                        <div style={{ fontSize: 24 }}>{f.emoji}</div>
                        <div style={{ fontWeight: 700, fontSize: 12, marginTop: 6 }}>{f.name}</div>
                        <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 2 }}>{f.reason}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ fontWeight: 700, fontSize: 13, color: '#9f1239', margin: '14px 0 8px' }}>❌ Avoid these</div>
                  <div className={styles.foodGrid}>
                    {data?.avoidFoods?.map((f) => (
                      <div key={f.name} className={styles.foodCard} style={{ background: '#fff5f5', borderColor: '#fecaca' }}>
                        <div style={{ fontSize: 24 }}>{f.emoji}</div>
                        <div style={{ fontWeight: 700, fontSize: 12, color: '#9f1239', marginTop: 6 }}>{f.name}</div>
                        <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 2 }}>{f.reason}</div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </CardBody>
          </Card>
        </div>

        <div>
          <Card style={{ marginBottom: 16 }}>
            <CardHeader title="😊 How are you feeling?"/>
            <CardBody>
              <div style={{ display: 'flex', gap: 10, marginBottom: 16 }}>
                {['😊','😴','😤','🤢'].map((m) => (
                  <button key={m} onClick={() => setMood(m)} style={{ flex: 1, padding: 14, borderRadius: 14, border: `2px solid ${mood===m?'var(--p1)':'var(--border)'}`, background: mood===m?'color-mix(in srgb,var(--p1) 10%,var(--card))':'var(--card)', cursor: 'pointer', fontSize: 26, transition: '.15s' }}>
                    {m}
                  </button>
                ))}
              </div>
              {data?.phaseTip && (
                <div style={{ background: '#f0fdf4', border: '1.5px solid #86efac', borderRadius: 13, padding: 12, fontSize: 13, color: '#14532d', lineHeight: 1.65 }}>
                  {data.phaseTip}
                </div>
              )}
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="📋 Phase Nutrition Guide"/>
            <CardBody>
              {isLoading ? <Skeleton h={100} radius={8}/> : (
                <div style={{ fontSize: 13, lineHeight: 2 }}>
                  {data?.phaseGuide?.map((p) => (
                    <div key={p.phase} style={{ fontWeight: p.current ? 700 : 400, color: p.current ? 'var(--p1)' : 'var(--text)' }}>
                      {p.dot} <strong>{p.phase}</strong> → {p.tips}{p.current ? ' ← You are here' : ''}
                    </div>
                  ))}
                </div>
              )}
            </CardBody>
          </Card>
        </div>
      </div>
    </div>
  )
}
