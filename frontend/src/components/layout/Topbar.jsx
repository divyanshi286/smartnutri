import { useAppStore } from '@store'
import { IconBtn, BtnPrimary } from '@ui'
import styles from './Topbar.module.css'

export default function Topbar({ title }) {
  const { setVoiceOpen, setSidebarOpen } = useAppStore()
  return (
    <header className={styles.topbar}>
      <button className={styles.menuBtn} onClick={() => setSidebarOpen(true)}>☰</button>
      <div className={styles.title}>{title}</div>
      <div className={styles.actions}>
        <IconBtn onClick={() => setVoiceOpen(true)} title="Voice Input">🎙</IconBtn>
        <IconBtn title="Notifications">🔔</IconBtn>
        <IconBtn title="Search">🔍</IconBtn>
        <BtnPrimary style={{ padding: '7px 16px', fontSize: 13 }}>＋ Log Meal</BtnPrimary>
      </div>
    </header>
  )
}
