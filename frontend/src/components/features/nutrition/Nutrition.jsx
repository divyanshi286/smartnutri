// Nutrition.jsx
import { useNutrition } from '@hooks/useQueries'
import { Card, CardHeader, CardBody, ProgressBar, Skeleton } from '@ui'
import styles from './Nutrition.module.css'

export default function Nutrition() {
  const { data, isLoading } = useNutrition()

  const conicParts = data?.macros?.reduce((acc, m, i) => {
    const prev = acc.prev
    const deg = m.pct * 3.6
    acc.parts.push(`${m.color} ${prev}deg ${prev + deg}deg`)
    acc.prev = prev + deg
    return acc
  }, { parts: [], prev: 0 })

  return (
    <div className={styles.wrap}>
      <div className={styles.grid}>
        <Card>
          <CardHeader title="🥗 Macro Breakdown" sub={`${data?.totalCalories || 980} kcal logged today`}/>
          <CardBody>
            {isLoading ? <Skeleton h={100} radius={12}/> : (
              <div style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                <div style={{ position: 'relative', width: 100, height: 100, borderRadius: '50%', background: `conic-gradient(${conicParts?.parts?.join(',')}, var(--border) ${(conicParts?.prev || 76)}deg 360deg)`, flexShrink: 0 }}>
                  <div style={{ position: 'absolute', inset: 14, background: 'var(--card)', borderRadius: '50%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    <span style={{ fontFamily: 'var(--ff-display)', fontWeight: 700, fontSize: 15 }}>{data?.totalCalories}</span>
                    <span style={{ fontSize: 9, color: 'var(--muted)' }}>kcal</span>
                  </div>
                </div>
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 9 }}>
                  {data?.macros?.map((m) => (
                    <div key={m.name} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      <div style={{ width: 11, height: 11, borderRadius: 3, background: m.color, flexShrink: 0 }}/>
                      <span style={{ flex: 1, fontSize: 13 }}>{m.name}</span>
                      <strong>{m.value}{m.unit} / {m.goal}{m.unit}</strong>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="🩺 PCOS Micronutrients"/>
          <CardBody>
            {isLoading
              ? [1,2,3].map(i => <Skeleton key={i} h={28} radius={4} style={{ marginBottom: 12 }}/>)
              : data?.micronutrients?.map((m) => (
                <ProgressBar key={m.label} label={m.label} current={m.current} goal={m.goal} unit={m.unit} color={m.color} valueColor={m.valueColor} warn={m.warn}/>
              ))
            }
            {!isLoading && data?.ironBoostFoods && (
              <>
                <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 10, marginTop: 4 }}>💡 Boost iron today — eat these:</div>
                <div style={{ display: 'flex', gap: 8 }}>
                  {data.ironBoostFoods.map((f) => (
                    <div key={f.name} style={{ flex: 1, background: 'var(--p3)', borderRadius: 13, padding: 10, textAlign: 'center' }}>
                      <div style={{ fontSize: 22 }}>{f.emoji}</div>
                      <div style={{ fontSize: 11, fontWeight: 700, marginTop: 4 }}>{f.name}</div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
