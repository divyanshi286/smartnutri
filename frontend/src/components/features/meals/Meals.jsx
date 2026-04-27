import { useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { useMeals, useSearchFoods, useFoodCategories } from '@hooks/useQueries'
import { Card, CardHeader, CardBody, MealCard, ProgressBar, BtnPrimary, BtnSecondary, Skeleton } from '@ui'
import { logMeal } from '@api'
import styles from './Meals.module.css'

export default function Meals() {
  const queryClient = useQueryClient()
  const today = new Date().toISOString().split('T')[0]
  const { data, isLoading } = useMeals(today)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMealType, setSelectedMealType] = useState('breakfast')
  const [showFoodSearch, setShowFoodSearch] = useState(false)
  const { data: searchResults = [] } = useSearchFoods(searchQuery)
  const { data: categories = [] } = useFoodCategories()
  const [isLoggingMeal, setIsLoggingMeal] = useState(false)

  const handleAddFood = async (food) => {
    if (isLoggingMeal) return
    
    try {
      setIsLoggingMeal(true)
      await logMeal(selectedMealType, food)
      
      // Refresh meals data
      queryClient.invalidateQueries({ queryKey: ['meals', today] })
      
      // Close modal and reset
      setShowFoodSearch(false)
      setSearchQuery('')
      
      // Show success (could add toast notification here)
      console.log('Meal logged successfully!')
    } catch (err) {
      console.error('Failed to log meal:', err)
      alert('Failed to log meal. Please try again.')
    } finally {
      setIsLoggingMeal(false)
    }
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.grid}>
        <div>
          <Card style={{ marginBottom: 16 }}>
            <CardHeader
              title="🍽 Meal Timeline"
              sub={isLoading ? '...' : `${data?.date} · ${data?.totalCalories} kcal so far`}
              action={<BtnPrimary style={{ padding: '8px 16px', fontSize: 13 }} onClick={() => setShowFoodSearch(true)}>＋ Add Meal</BtnPrimary>}
            />
            <CardBody>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {isLoading
                  ? [1,2,3].map(i => <Skeleton key={i} h={56} radius={14}/>)
                  : data?.items?.map((m) => (
                    <MealCard key={m.id} emoji={m.emoji} name={m.name} type={m.type} time={m.time} calories={m.calories} bg={m.bg}/>
                  ))
                }
                <div className={styles.addPlaceholder}>🌙 Log dinner · expected 7:00 PM</div>
              </div>
            </CardBody>
          </Card>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <Card>
            <CardHeader title="📊 Daily Targets"/>
            <CardBody>
              {isLoading
                ? [1,2,3,4].map(i => <Skeleton key={i} h={28} radius={4} style={{ marginBottom: 12 }}/>)
                : data?.targets?.map((t) => (
                  <ProgressBar key={t.label} label={t.label} current={t.current} goal={t.goal} color={t.color} valueColor={t.valueColor} warn={t.warn}/>
                ))
              }
            </CardBody>
          </Card>

          <Card>
            <CardHeader title="📱 Input Methods"/>
            <CardBody>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                <BtnSecondary style={{ justifyContent: 'center', opacity: 0.5, cursor: 'not-allowed' }} disabled>📷 Camera Scan</BtnSecondary>
                <BtnSecondary style={{ justifyContent: 'center', opacity: 0.5, cursor: 'not-allowed' }} disabled>🎙 Voice Log</BtnSecondary>
                <BtnSecondary style={{ justifyContent: 'center' }} onClick={() => setShowFoodSearch(true)}>🔍 Search Food</BtnSecondary>
                <BtnSecondary style={{ justifyContent: 'center', opacity: 0.5, cursor: 'not-allowed' }} disabled>🏷 Barcode</BtnSecondary>
              </div>
            </CardBody>
          </Card>
        </div>
      </div>

      {/* Food Search Modal */}
      {showFoodSearch && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'flex-end',
          zIndex: 1000
        }} onClick={() => setShowFoodSearch(false)}>
          <div style={{
            width: '100%',
            maxHeight: '80vh',
            background: 'var(--bg)',
            borderRadius: '24px 24px 0 0',
            padding: 20,
            display: 'flex',
            flexDirection: 'column'
          }} onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <h3 style={{ margin: 0 }}>🔍 Search Foods</h3>
              <button onClick={() => setShowFoodSearch(false)} style={{ background: 'none', border: 'none', fontSize: 24, cursor: 'pointer' }}>✕</button>
            </div>

            {/* Meal Type Selection */}
            <div style={{ display: 'flex', gap: 8, marginBottom: 16, borderBottom: '1px solid var(--border)', paddingBottom: 12, overflowX: 'auto' }}>
              {['breakfast', 'lunch', 'dinner', 'snack'].map((type) => (
                <button
                  key={type}
                  onClick={() => setSelectedMealType(type)}
                  style={{
                    padding: '8px 14px',
                    borderRadius: 8,
                    border: selectedMealType === type ? '2px solid var(--primary)' : '1px solid var(--border)',
                    background: selectedMealType === type ? 'var(--primary)15' : 'transparent',
                    color: 'var(--text)',
                    cursor: 'pointer',
                    fontSize: 13,
                    fontWeight: 600,
                    textTransform: 'capitalize',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {type}
                </button>
              ))}
            </div>

            {/* Search Input */}
            <input
              type="text"
              placeholder="Search foods... (e.g., chicken, rice, dal)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: 8,
                border: '1px solid var(--border)',
                marginBottom: 16,
                fontSize: 14,
                fontFamily: 'inherit',
                boxSizing: 'border-box'
              }}
              autoFocus
            />

            {/* Categories */}
            {!searchQuery && categories && categories.length > 0 && (
              <div style={{ marginBottom: 16 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--muted)', marginBottom: 8 }}>CATEGORIES</div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: 8 }}>
                  {categories.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSearchQuery(cat.label)}
                      style={{
                        padding: '8px 12px',
                        borderRadius: 8,
                        border: '1px solid var(--border)',
                        background: 'var(--bg-secondary)',
                        cursor: 'pointer',
                        fontSize: 12,
                        fontWeight: 600,
                      }}
                    >
                      {cat.emoji} {cat.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Search Results */}
            <div style={{ flex: 1, overflowY: 'auto', minHeight: 0 }}>
              {searchQuery && searchResults.length === 0 && (
                <div style={{ textAlign: 'center', color: 'var(--muted)', padding: '20px 0' }}>
                  No foods found. Try a different search.
                </div>
              )}

              {searchResults.map((food) => (
                <div
                  key={food.id}
                  style={{
                    padding: '12px',
                    borderRadius: 8,
                    border: '1px solid var(--border)',
                    marginBottom: 8,
                    cursor: isLoggingMeal ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    opacity: isLoggingMeal ? 0.6 : 1,
                    transition: 'opacity 0.2s'
                  }}
                  onClick={() => !isLoggingMeal && handleAddFood(food)}
                >
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14 }}>{food.name}</div>
                    <div style={{ fontSize: 12, color: 'var(--muted)' }}>
                      {food.calories} cal • P: {food.protein?.toFixed(1)}g • C: {food.carbs?.toFixed(1)}g • F: {food.fats?.toFixed(1)}g
                    </div>
                  </div>
                  <button
                    disabled={isLoggingMeal}
                    style={{
                      padding: '6px 12px',
                      borderRadius: 6,
                      border: 'none',
                      background: isLoggingMeal ? 'var(--muted)' : 'var(--primary)',
                      color: 'white',
                      cursor: isLoggingMeal ? 'not-allowed' : 'pointer',
                      fontSize: 12,
                      fontWeight: 700,
                      whiteSpace: 'nowrap',
                      marginLeft: 8,
                      opacity: isLoggingMeal ? 0.6 : 1,
                      transition: 'all 0.2s'
                    }}
                    onClick={(e) => {
                      e.stopPropagation()
                      if (!isLoggingMeal) handleAddFood(food)
                    }}
                  >
                    {isLoggingMeal ? '⏳ Adding...' : '＋ Add'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
