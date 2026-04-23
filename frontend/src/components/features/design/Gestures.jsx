// Gestures.jsx
import { useState } from 'react'
import styles from './Design.module.css'

const GESTURES = [
  { ico:'👈 👉', title:'Swipe Left / Right — Day Navigation', desc:'Swipe the day header horizontally to navigate between days. Arrow buttons serve as keyboard/accessibility fallback.', demo:'📅 Navigated to Friday · 6 Mar 2026!' },
  { ico:'⬇️', title:'Pull Down — Refresh Data', desc:'Pull from the top of any feed screen to trigger a data refresh. Spinning arrow confirms the action.', demo:'♻️ Refreshed! All nutrition data is up to date.' },
  { ico:'📱 👈', title:'Swipe Meal Card — Edit / Delete', desc:'Swipe any meal card leftward to reveal Edit and Delete actions beneath. Tap elsewhere or wait 3 seconds to dismiss.', demo:'✏️ Edit · 🗑 Delete — actions revealed!' },
  { ico:'☝️ ⏳', title:'Long Press — Quick Actions', desc:'Long-press (500ms) on any ring, food card, or meal entry to reveal contextual quick-action menu. Haptic feedback on supported devices.', demo:'📋 Copy · ✏️ Edit goal · 🗑 Remove — revealed!' },
  { ico:'🤌', title:'Pinch to Zoom — Charts', desc:'Pinch in/out on the progress bar chart to switch between daily, weekly, and monthly zoom levels.', demo:'🔍 Zoomed to: Last 30 days · Monthly view' },
  { ico:'🎙', title:'Voice Command — Always Accessible', desc:'Mic button pinned top-right on all screens. One tap to activate — available anywhere without navigation.', demo:'🎙 "Log dal rice for lunch"\n🎙 "How much protein today?"\n🎙 "Add a glass of water"\n🎙 "What foods help PCOS?"' },
]

export default function Gestures() {
  const [open, setOpen] = useState(null)
  return (
    <div className={styles.wrap}>
      <div className={styles.gestureGrid}>
        {GESTURES.map((g, i) => (
          <div key={i} className={styles.gCard} onClick={() => setOpen(open === i ? null : i)}>
            <span className={styles.gIcon} style={{ animation:`float 3s ease infinite ${i*0.4}s` }}>{g.ico}</span>
            <div className={styles.gTitle}>{g.title}</div>
            <div className={styles.gDesc}>{g.desc}</div>
            {open === i && (
              <div className={styles.gDemo}>{g.demo}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
