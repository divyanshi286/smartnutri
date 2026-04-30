import { useEffect } from 'react'
import { useDashboard, useMeals } from '@hooks/useQueries'
import { useAppStore } from '@store'
import { useNavigate } from '@tanstack/react-router'
import { Card, CardHeader, CardBody, GoalRing, AiNote, MealCard, ProgressBar, Badge, BtnPrimary, BtnGhost, Skeleton } from '@ui'
import styles from './Dashboard.module.css'

export default function Dashboard() {
  const { data: dash, isLoading: dashLoading } = useDashboard()
  const { data: meals, isLoading: mealsLoading } = useMeals()
  const navigate = useNavigate()
  const { setVoiceOpen, setUser, setMeals: setMealsState, setBadges, setCycle } = useAppStore()

  useEffect(() => {
    if (!dash) return
    if (dash.user) setUser({ ...dash.user })
    if (dash.badges) setBadges(dash.badges)
    if (dash.cycleSummary) setCycle({ ...dash.cycleSummary })
    if (meals?.items) setMealsState(meals.items)
  }, [dash, meals, setUser, setBadges, setCycle, setMealsState])

  return (
    <div className={styles.wrap}>
      {/* Hero */}
      <div className={styles.hero}>
        <div className={styles.heroMesh1}/><div className={styles.heroMesh2}/>
        {dashLoading ? (
          <><Skeleton h={14} w={160}/><Skeleton h={36} w={240} style={{ marginTop: 8 }}/></>
        ) : (
          <>
            <div className={styles.heroLabel}>{dash?.greeting} · {dash?.date}</div>
            <div className={styles.heroName}>Good to see you, {dash?.user?.name}!</div>
            <div className={styles.heroSub}>{dash?.cycleSummary?.label}</div>
            <div className={styles.heroMeta}>
              <span className={styles.heroBadge}>Streak: {dash?.user?.streak ?? 0} days</span>
              <span className={styles.heroBadge}>Protein: {Math.round(((dash?.nutrition?.protein?.current ?? 0) / (dash?.nutrition?.protein?.goal ?? 1)) * 100)}%</span>
              <span className={styles.heroBadge}>{dash?.cycleSummary?.label || 'Cycle tracking available'}</span>
            </div>
          </>
        )}
      </div>

      {/* Goal Rings + AI Nudge */}
      <div className={styles.topRow}>
        <Card>
          <CardHeader
            title="Today's Goals"
            sub="Thu 5 Mar · 1380 kcal logged so far"
            action={
              <div style={{ display: 'flex', gap: 6 }}>
                <BtnGhost>‹ Yesterday</BtnGhost>
                <BtnGhost style={{ color: 'var(--muted2)', cursor: 'not-allowed' }}>Today ›</BtnGhost>
              </div>
            }
          />
          <CardBody>
            {dashLoading ? (
              <div className={styles.ringsRow}>{[1,2,3,4].map(i => <Skeleton key={i} w={72} h={72} radius={50}/>)}</div>
            ) : (
              <div className={styles.ringsRow}>
                <GoalRing value={dash?.nutrition?.calories?.current || 1380} goal={dash?.nutrition?.calories?.goal || 1800} label="Calories" unit="" color="var(--p1)"/>
                <GoalRing value={Number(dash?.nutrition?.protein?.current) || 78} goal={110} label="Protein" unit="" color="#3b82f6"/>
                <GoalRing value={Number(dash?.nutrition?.carbs?.current) || 42} goal={130} label="Carbs" unit="" color="#f59e0b"/>
                <GoalRing value={Number(dash?.nutrition?.water?.current) || 1.5} goal={2.5} label="Water" unit="" color="#06b6d4"/>
              </div>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardHeader title="AI Coach"/>
          <CardBody>
            {dashLoading
              ? <><Skeleton h={14}/><Skeleton h={14} w="80%" style={{ marginTop: 8 }}/></>
              : <AiNote text={dash?.aiNudge?.text} chips={dash?.aiNudge?.chips || []}/>
            }
            <BtnPrimary style={{ width: '100%', marginTop: 12, justifyContent: 'center' }} onClick={() => navigate({ to: '/chat' })}>
              Ask NutriAI →
            </BtnPrimary>
          </CardBody>
        </Card>
      </div>

      {/* Meals + Progress */}
      <div className={styles.bottomRow}>
        <Card>
          <CardHeader
            title="Meal Log"
            action={<span style={{ fontSize: 13, fontWeight: 700, color: 'var(--p1)', cursor: 'pointer' }}>+ Add Meal</span>}
          />
          <CardBody>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {mealsLoading
                ? [1,2,3].map(i => <Skeleton key={i} h={56} radius={14}/>)
                : meals?.items?.map((m) => (
                  <MealCard key={m.id} emoji={m.emoji} name={m.name} type={m.type} time={m.time} calories={m.calories} bg={m.bg}/>
                ))
              }
              <div className={styles.addMealRow}>
                <span>•</span> Log dinner · expected 7:00 PM
              </div>
            </div>
          </CardBody>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Card>
            <CardHeader title="Daily Progress"/>
            <CardBody>
              {mealsLoading
                ? [1,2,3,4].map(i => <Skeleton key={i} h={28} radius={4} style={{ marginBottom: 12 }}/>)
                : meals?.targets?.map((t) => (
                  <ProgressBar key={t.label} label={t.label} current={t.current} goal={t.goal} color={t.color} valueColor={t.valueColor} warn={t.warn}/>
                ))
              }
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="Achievements"/>
            <CardBody>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {dashLoading
                  ? [1,2,3].map(i => <Skeleton key={i} w={70} h={70} radius={14}/>)
                  : dash?.badges?.map((b) => <Badge key={b.id} emoji={b.emoji} label={b.label} earned={b.earned}/>)
                }
              </div>
            </CardBody>
          </Card>
        </div>
      </div>

      {/* FAB */}
      <button className={styles.fab} onClick={() => setVoiceOpen(true)}>◉</button>
    </div>
  )
}
