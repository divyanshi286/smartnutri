import { useProgress } from '@hooks/useQueries'
import { Card, CardHeader, CardBody, StatCard, Badge, BtnGhost, Skeleton } from '@ui'
import styles from './Progress.module.css'

export default function Progress() {
  const { data, isLoading } = useProgress()

  const MAX_HEIGHT = 100
  const maxVal = Math.max(...(data?.weeklyCalories?.filter(d => d.value).map(d => d.value) || [1800]))

  return (
    <div className={styles.wrap}>
      {/* Stats */}
      <div className={styles.statsGrid}>
        {isLoading
          ? [1,2,3,4].map(i => <Skeleton key={i} h={72} radius={16}/>)
          : data?.stats?.map((s) => <StatCard key={s.label} ico={s.ico} bg={s.bg} label={s.label} value={s.value} color={s.color}/>)
        }
      </div>

      <div className={styles.grid}>
        <Card>
          <CardHeader
            title="📈 Weekly Calories"
            sub="Goal: 1800 kcal/day"
            action={
              <div style={{ display: 'flex', gap: 4 }}>
                <BtnGhost>Day</BtnGhost>
                <BtnGhost active>Week</BtnGhost>
                <BtnGhost>Month</BtnGhost>
              </div>
            }
          />
          <CardBody>
            {isLoading ? <Skeleton h={140} radius={8}/> : (
              <>
                <div className={styles.barChart}>
                  {data?.weeklyCalories?.map((d) => {
                    const h = d.value ? Math.round((d.value / maxVal) * MAX_HEIGHT) : 4
                    return (
                      <div key={d.day} className={`${styles.barCol} ${d.today ? styles.barToday : ''}`}>
                        <div className={styles.bar} style={{ height: h, background: d.value ? 'var(--grad)' : 'var(--border)', opacity: d.today ? 1 : (d.value ? 0.6 : 1) }}/>
                        <div className={styles.barDay}>{d.day}{d.value ? <><br/><span>{d.value}</span></> : null}</div>
                      </div>
                    )
                  })}
                </div>
                <div className={styles.chartMeta}>
                  <span>📅 Mon–Thu average: <strong>1537 kcal</strong></span>
                  <span>🎯 Goal: <strong>1800 kcal</strong></span>
                  <span>📈 vs last week: <strong style={{ color: 'var(--p1)' }}>↑ 8%</strong></span>
                </div>
              </>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="🏅 Achievements"/>
          <CardBody>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              {isLoading
                ? [1,2,3].map(i => <Skeleton key={i} w={70} h={70} radius={14}/>)
                : data?.badges?.map((b) => <Badge key={b.id} emoji={b.emoji} label={b.label} earned={b.earned}/>)
              }
            </div>
            <div style={{ marginTop: 16, fontFamily: 'var(--ff-hand)', fontSize: 15, color: 'var(--p1)' }}>
              Keep going! 3 more days for the "Fortnight Force" badge 🎯
            </div>
          </CardBody>
        </Card>
      </div>
    </div>
  )
}
