// Components.jsx
import { Card, CardHeader, CardBody, BtnPrimary, BtnSecondary, BtnGhost, GoalRing, ProgressBar, Badge, Tag } from '@ui'
import styles from './Design.module.css'

export default function Components() {
  return (
    <div className={styles.wrap}>
      <Section title="Buttons — 3 variants × sizes" sub="All meet 44px min touch target. Primary uses theme gradient.">
        <div className={styles.compRow}>
          <Group label="Primary">
            <BtnPrimary style={{ padding:'7px 14px',fontSize:12 }}>Small</BtnPrimary>
            <BtnPrimary>Default</BtnPrimary>
            <BtnPrimary style={{ padding:'13px 24px',fontSize:15 }}>Large</BtnPrimary>
          </Group>
          <Group label="Secondary">
            <BtnSecondary style={{ padding:'7px 14px',fontSize:12 }}>Small</BtnSecondary>
            <BtnSecondary>Default</BtnSecondary>
            <BtnSecondary style={{ padding:'12px 22px',fontSize:15 }}>Large</BtnSecondary>
          </Group>
          <Group label="Ghost">
            <BtnGhost>Default</BtnGhost>
            <BtnGhost active>Active</BtnGhost>
          </Group>
          <Group label="FAB">
            <div style={{ width:50,height:50,borderRadius:'50%',background:'var(--grad)',color:'#fff',border:'none',fontSize:22,display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',boxShadow:'0 6px 20px color-mix(in srgb,var(--p1) 40%,transparent)',transition:'.2s var(--ease-spring)' }}>＋</div>
          </Group>
        </div>
      </Section>

      <Section title="Progress Indicators" sub="Rings, bars, and tags">
        <div className={styles.compRow} style={{ alignItems:'flex-start' }}>
          <Group label="Goal Rings">
            <div style={{ display:'flex',gap:14 }}>
              <GoalRing value={1350} goal={1800} label="Calories" unit="" color="var(--p1)"/>
              <GoalRing value="D14" goal={28} label="Cycle" unit="" color="#e879a0"/>
            </div>
          </Group>
          <Group label="Progress Bars" style={{ minWidth:260 }}>
            <ProgressBar label="Protein" current={78} goal={110} unit="g" color="var(--grad)" valueColor="#3b82f6"/>
            <ProgressBar label="Iron ⚠️" current={7} goal={18} unit="mg" color="linear-gradient(90deg,#f9a8d4,#be185d)" warn/>
          </Group>
          <Group label="Tags">
            <Tag variant="g">✅ EAT</Tag>
            <Tag variant="y">⚠️ MODERATE</Tag>
            <Tag variant="r">❌ AVOID</Tag>
            <Tag variant="b">🔵 INFO</Tag>
          </Group>
        </div>
      </Section>

      <Section title="Achievement Badges" sub="Earned vs locked states">
        <div style={{ display:'flex',gap:8,flexWrap:'wrap' }}>
          <Badge emoji="🔥" label="12 Day Streak" earned/>
          <Badge emoji="💪" label="Protein Pro" earned/>
          <Badge emoji="💧" label="Hydration Hero" earned/>
          <Badge emoji="🌙" label="Night Owl"/>
          <Badge emoji="🌱" label="Plant Power"/>
        </div>
      </Section>

      <Section title="Cards — Various types" sub="All card variants from the design system">
        <div className={styles.compRow}>
          <div style={{ background:'linear-gradient(135deg,#fce4ec,#fff)',border:'1.5px solid #f9a8d4',borderRadius:18,padding:16,width:180 }}>
            <div style={{ fontSize:20,marginBottom:8 }}>🌸</div>
            <div style={{ fontWeight:700,fontSize:13,color:'#7c3aed' }}>Period Tracking</div>
            <div style={{ fontSize:11,color:'#9d174d',marginTop:2 }}>Day 14 · Ovulation</div>
          </div>
          <div style={{ background:'linear-gradient(135deg,#dbeafe,#fff)',border:'1.5px solid #93c5fd',borderRadius:18,padding:16,width:180 }}>
            <div style={{ fontSize:20,marginBottom:8 }}>💪</div>
            <div style={{ fontWeight:700,fontSize:13,color:'#1d4ed8' }}>Muscle Progress</div>
            <div style={{ fontSize:11,color:'#1e40af',marginTop:2 }}>Protein: 78g / 110g</div>
            <div style={{ marginTop:8,height:5,background:'#bfdbfe',borderRadius:3 }}><div style={{ width:'71%',height:'100%',background:'#3b82f6',borderRadius:3 }}/></div>
          </div>
          <div style={{ background:'linear-gradient(135deg,#fffbeb,#fef9c3)',border:'2px solid #f59e0b',borderRadius:18,padding:16,width:200 }}>
            <div style={{ fontWeight:700,fontSize:13,marginBottom:8 }}>⚠️ Safety Callout</div>
            <div style={{ fontSize:12,color:'#78350f',lineHeight:1.65 }}>For AI safety interventions and nutritional warnings.</div>
            <BtnPrimary style={{ marginTop:10,padding:'7px 14px',fontSize:12 }}>Take Action</BtnPrimary>
          </div>
        </div>
      </Section>
    </div>
  )
}

function Section({ title, sub, children }) {
  return (
    <div className={styles.section}>
      <div className={styles.sectionTitle}>{title}</div>
      {sub && <div className={styles.sectionSub}>{sub}</div>}
      {children}
    </div>
  )
}
function Group({ label, children, style }) {
  return (
    <div className={styles.group} style={style}>
      <div className={styles.groupLabel}>{label}</div>
      {children}
    </div>
  )
}
