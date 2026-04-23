// StyleGuide.jsx
import styles from './Design.module.css'

const THEMES_DATA = [
  { title: '🌿 Adult — Miso Sage',          titleColor:'#3d7a5c', swatches:[{bg:'#3d7a5c',label:'#3D7A5C\nPrimary'},{bg:'#2c5a42',label:'#2C5A42\nDark'},{bg:'#c8e6d4',color:'#1a3328',label:'#C8E6D4\nLight'},{bg:'#f2f9f5',color:'#2c5a42',label:'#F2F9F5\nBG'}], tone:'Professional, calm, data-forward' },
  { title: '💪 Teen Boys — Neon Slate',       titleColor:'#0284c7', swatches:[{bg:'#0ea5e9',label:'#0EA5E9'},{bg:'#6366f1',label:'#6366F1\nAccent'},{bg:'#bae6fd',color:'#0c2d4a',label:'#BAE6FD\nLight'},{bg:'#f0f9ff',color:'#0284c7',label:'#F0F9FF\nBG'}], tone:'Energetic, bold, athletic' },
  { title: '🌸 Teen Girls Hormonal — Petal Aurora', titleColor:'#c2185b', swatches:[{bg:'#e879a0',label:'#E879A0'},{bg:'#9b59b6',label:'#9B59B6\nAccent'},{bg:'#fce4ec',color:'#4a0e2b',label:'#FCE4EC\nLight'},{bg:'#fff5f8',color:'#c2185b',label:'#FFF5F8\nBG'}], tone:'Warm, empowering, educational' },
  { title: '⚡ Teen Girls Athletic — Ember Reef', titleColor:'#dc6804', swatches:[{bg:'#f97316',label:'#F97316'},{bg:'#e63946',label:'#E63946\nAccent'},{bg:'#fde8d0',color:'#431a07',label:'#FDE8D0\nLight'},{bg:'#fff8f2',color:'#dc6804',label:'#FFF8F2\nBG'}], tone:'Dynamic, strong, vibrant' },
]

export default function StyleGuide() {
  return (
    <div className={styles.wrap}>
      <div className={styles.sgGrid}>
        {THEMES_DATA.map((t) => (
          <div key={t.title} className={styles.sgCard}>
            <div className={styles.sgTitle} style={{ color: t.titleColor }}>{t.title}</div>
            <div className={styles.swatchRow}>
              {t.swatches.map((s) => (
                <div key={s.bg} className={styles.swatch} style={{ background: s.bg, color: s.color || '#fff' }}>{s.label}</div>
              ))}
            </div>
            <div style={{ fontFamily:'var(--ff-display)',fontWeight:700,fontSize:20,marginBottom:4 }}>Fraunces Display</div>
            <div style={{ fontSize:13,color:'var(--muted)' }}>Tone: {t.tone}</div>
          </div>
        ))}
        <div className={styles.sgCard} style={{ background:'#141920',borderColor:'#2d3748',gridColumn:'1/-1' }}>
          <div className={styles.sgTitle} style={{ color:'#edf2ef' }}>🌙 Dark Mode — All Themes</div>
          <div className={styles.swatchRow}>
            {[{bg:'#0d1117',l:'Canvas'},{bg:'#141920',l:'Surface'},{bg:'#1c2330',l:'Card'},{bg:'#2d3748',l:'Border'},{bg:'#edf2ef',color:'#141920',l:'Text'},{bg:'#6e7681',l:'Muted'}].map(s => (
              <div key={s.bg} className={styles.swatch} style={{ background:s.bg, color:s.color||'#fff' }}>{s.bg}<br/><span style={{ opacity:.7 }}>{s.l}</span></div>
            ))}
          </div>
          <div style={{ fontSize:12,color:'#6e7681',marginTop:8 }}>All 4 themes support dark mode. WCAG AA throughout, safety warnings at AAA (7:1).</div>
        </div>
      </div>

      <div className={styles.section} style={{ marginTop:24 }}>
        <div className={styles.sectionTitle}>Typography Scale</div>
        <div style={{ display:'flex',flexDirection:'column',gap:16 }}>
          <div style={{ fontFamily:'var(--ff-display)',fontWeight:900,fontSize:40,lineHeight:1,background:'var(--grad)',WebkitBackgroundClip:'text',WebkitTextFillColor:'transparent',backgroundClip:'text' }}>Display · Fraunces Black · 40px</div>
          <div style={{ fontFamily:'var(--ff-display)',fontWeight:700,fontSize:26 }}>H1 · Fraunces Bold · 26px · Screen titles</div>
          <div style={{ fontFamily:'var(--ff-display)',fontWeight:500,fontSize:20 }}>H2 · Fraunces Medium · 20px · Section headings</div>
          <div style={{ fontSize:15,color:'var(--muted)',lineHeight:1.75 }}>Body · Geist Regular · 15px · Line-height 1.75 — All descriptive text, AI responses, educational content.</div>
          <div style={{ fontSize:11,fontWeight:700,textTransform:'uppercase',letterSpacing:'1.1px',color:'var(--muted)' }}>LABEL · GEIST BOLD · 11PX · UPPERCASE · METRIC NAMES</div>
          <div style={{ fontFamily:'var(--ff-hand)',fontSize:20,color:'var(--p1)',fontWeight:600 }}>Handwriting · Caveat · 20px · Tips, callouts, annotations</div>
        </div>
      </div>
    </div>
  )
}
