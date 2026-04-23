import { useState } from 'react'
import { useModules } from '@hooks/useQueries'
import { Card, CardHeader, CardBody, Skeleton } from '@ui'
import styles from './Education.module.css'

export default function Education() {
  const { data, isLoading } = useModules()
  const [answered, setAnswered] = useState(null)

  const STATUS_ICO = { done: { emoji: '✅', bg: '#d1fae5' }, active: { emoji: '📖', bg: 'var(--grad)', color: '#fff' }, locked: { emoji: '🔒', bg: 'var(--border)' } }

  return (
    <div className={styles.wrap}>
      <div className={styles.grid}>
        <div>
          {isLoading ? <Skeleton h={280} radius={20}/> : (
            <div className={styles.eduModule}>
              <div className={styles.eduHeader}>
                <div>
                  <div className={styles.eduTitle}>{data?.activeModule?.title}</div>
                  <div className={styles.eduSub}>{data?.activeModule?.subtitle}</div>
                </div>
                <div style={{ display: 'flex', gap: 5, marginTop: 8 }}>
                  {Array.from({ length: data?.activeModule?.total || 5 }).map((_, i) => (
                    <div key={i} style={{ width: 7, height: 7, borderRadius: '50%', background: i < (data?.activeModule?.progress || 2) ? '#fff' : 'rgba(255,255,255,.3)' }}/>
                  ))}
                </div>
              </div>
              <div className={styles.eduBody}>
                <div dangerouslySetInnerHTML={{ __html: data?.activeModule?.body }}/>
                {data?.activeModule?.quiz && (
                  <div className={styles.quizArea}>
                    <div className={styles.quizQ}>{data.activeModule.quiz.question}</div>
                    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      {data.activeModule.quiz.options.map((opt, i) => (
                        <button
                          key={i}
                          className={`${styles.quizOpt} ${answered !== null ? (opt.correct ? styles.correct : (answered === i ? styles.wrong : '')) : ''}`}
                          onClick={() => answered === null && setAnswered(i)}
                        >
                          {opt.label}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <Card>
          <CardHeader title="📚 Module Library"/>
          <CardBody>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {isLoading
                ? [1,2,3,4].map(i => <Skeleton key={i} h={56} radius={14}/>)
                : data?.modules?.map((m) => {
                  const s = STATUS_ICO[m.status]
                  return (
                    <div key={m.id} className={`${styles.moduleRow} ${m.status === 'active' ? styles.modActive : ''} ${m.status === 'locked' ? styles.modLocked : ''}`}>
                      <div style={{ width: 40, height: 40, borderRadius: 12, background: s.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 19, flexShrink: 0, color: s.color || 'inherit' }}>{s.emoji}</div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 700, fontSize: 14 }}>{m.title}</div>
                        <div style={{ fontSize: 11, color: m.status === 'active' ? 'var(--p1)' : 'var(--muted)', marginTop: 2, fontWeight: m.status === 'active' ? 600 : 400 }}>{m.meta}</div>
                      </div>
                      {m.status !== 'locked' && <span style={{ color: 'var(--p1)', fontSize: m.status === 'active' ? 14 : 12, fontWeight: 700 }}>{m.status === 'done' ? 'Done' : '→'}</span>}
                    </div>
                  )
                })
              }
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
