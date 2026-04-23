import styles from './ui.module.css'

/* ─────────────── CARD ─────────────── */
export function Card({ children, className = '', style }) {
  return <div className={`${styles.card} ${className}`} style={style}>{children}</div>
}
export function CardHeader({ title, sub, action }) {
  return (
    <div className={styles.cardHd}>
      <div>
        <div className={styles.cardTitle}>{title}</div>
        {sub && <div className={styles.cardSub}>{sub}</div>}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}
export function CardBody({ children, className = '' }) {
  return <div className={`${styles.cardBody} ${className}`}>{children}</div>
}

/* ─────────────── BUTTONS ─────────────── */
export function BtnPrimary({ children, onClick, style, className = '' }) {
  return <button className={`${styles.btnP} ${className}`} style={style} onClick={onClick}>{children}</button>
}
export function BtnSecondary({ children, onClick, style, className = '' }) {
  return <button className={`${styles.btnS} ${className}`} style={style} onClick={onClick}>{children}</button>
}
export function BtnGhost({ children, onClick, style, active }) {
  return <button className={`${styles.btnGhost} ${active ? styles.btnGhostActive : ''}`} style={style} onClick={onClick}>{children}</button>
}
export function IconBtn({ children, onClick, title }) {
  return <button className={styles.iconBtn} onClick={onClick} title={title}>{children}</button>
}

/* ─────────────── GOAL RING ─────────────── */
export function GoalRing({ value, goal, label, unit, color = 'var(--p1)', size = 72, stroke = 6 }) {
  const r = (size / 2) - stroke
  const circ = 2 * Math.PI * r
  const pct = Math.min(value / goal, 1)
  const offset = circ * (1 - pct)
  return (
    <div className={styles.ringTile}>
      <div className={styles.ringWrap} style={{ width: size, height: size }}>
        <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ transform: 'rotate(-90deg)' }}>
          <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="var(--border)" strokeWidth={stroke}/>
          <circle
            cx={size/2} cy={size/2} r={r} fill="none"
            stroke={color} strokeWidth={stroke} strokeLinecap="round"
            strokeDasharray={circ} strokeDashoffset={offset}
            style={{ transition: 'stroke-dashoffset 0.8s var(--ease-smooth)' }}
          />
        </svg>
        <div className={styles.ringCenter}>
          <span className={styles.ringVal} style={{ color }}>{value}{unit}</span>
        </div>
      </div>
      <span className={styles.ringName}>{label}</span>
      <span className={styles.ringPct}>{goal}{unit} goal · {Math.round(pct*100)}%</span>
    </div>
  )
}

/* ─────────────── PROGRESS BAR ─────────────── */
export function ProgressBar({ label, current, goal, unit = '', color = 'var(--grad)', valueColor, warn }) {
  const pct = Math.min((current / goal) * 100, 100)
  return (
    <div className={styles.progItem}>
      <div className={styles.progRow}>
        <span className={styles.progLabel}>{label}</span>
        <span className={styles.progValue} style={{ color: valueColor || (warn ? '#e879a0' : 'var(--muted)') }}>
          {current} / {goal}{unit}{warn ? ' ⚠️' : ''}
        </span>
      </div>
      <div className={styles.progTrack}>
        <div className={styles.progFill} style={{ width: `${pct}%`, background: color }}/>
      </div>
    </div>
  )
}

/* ─────────────── BADGE ─────────────── */
export function Badge({ emoji, label, earned }) {
  return (
    <div className={`${styles.badge} ${earned ? styles.badgeEarned : ''}`}>
      <span className={styles.badgeIco}>{emoji}</span>
      <span className={styles.badgeLbl}>{label}</span>
    </div>
  )
}

/* ─────────────── STAT CARD ─────────────── */
export function StatCard({ ico, bg, label, value, color }) {
  return (
    <div className={styles.statCard}>
      <div className={styles.statIco} style={{ background: bg }}>{ico}</div>
      <div>
        <div className={styles.statLabel}>{label}</div>
        <div className={styles.statVal} style={{ color }}>{value}</div>
      </div>
    </div>
  )
}

/* ─────────────── CHIP ─────────────── */
export function Chip({ label, type = 'default', onClick }) {
  const cls = { go: styles.chipGo, no: styles.chipNo, ok: styles.chipOk }[type] || ''
  return <span className={`${styles.chip} ${cls}`} onClick={onClick} style={onClick ? { cursor: 'pointer' } : {}}>{label}</span>
}

/* ─────────────── AI NOTE ─────────────── */
export function AiNote({ text, chips = [] }) {
  return (
    <div className={styles.aiNote}>
      <div className={styles.aiPip}>🤖</div>
      <div className={styles.aiText} dangerouslySetInnerHTML={{ __html: text }}/>
      {chips.length > 0 && (
        <div className={styles.chipSet}>
          {chips.map((c, i) => <Chip key={i} label={c.label} type={c.type}/>)}
        </div>
      )}
    </div>
  )
}

/* ─────────────── MEAL CARD ─────────────── */
export function MealCard({ emoji, name, type, time, calories, bg, onEdit, onDelete }) {
  return (
    <div className={styles.mealCard}>
      <div className={styles.mealIco} style={{ background: bg || 'var(--p3)' }}>{emoji}</div>
      <div className={styles.mealInfo}>
        <div className={styles.mealName}>{name}</div>
        <div className={styles.mealTime}>{type} · {time}</div>
      </div>
      <div className={styles.mealCal}>{calories}</div>
      <div className={styles.mealActions}>
        <button className={styles.mealAct} onClick={onEdit}>✏️</button>
        <button className={styles.mealAct} onClick={onDelete}>🗑</button>
      </div>
    </div>
  )
}

/* ─────────────── SKELETON ─────────────── */
export function Skeleton({ w = '100%', h = 20, radius = 8 }) {
  return (
    <div style={{
      width: w, height: h, borderRadius: radius,
      background: 'linear-gradient(90deg, var(--border) 25%, var(--border-md) 50%, var(--border) 75%)',
      backgroundSize: '200% 100%',
      animation: 'shimmer 1.5s infinite',
    }}/>
  )
}

/* ─────────────── TAG ─────────────── */
export function Tag({ children, variant = 'b' }) {
  const cls = { g: styles.tagG, r: styles.tagR, y: styles.tagY, b: styles.tagB }[variant] || styles.tagB
  return <span className={`${styles.tag} ${cls}`}>{children}</span>
}
