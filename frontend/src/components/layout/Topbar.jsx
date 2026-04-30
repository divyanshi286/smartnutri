import { useAppStore } from '@store'
import { useNavigate } from '@tanstack/react-router'
import { IconBtn, BtnPrimary } from '@ui'
import { Mic, Bell, Search } from 'lucide-react'
import styles from './Topbar.module.css'

export default function Topbar({ title }) {
  const { setVoiceOpen, setSidebarOpen } = useAppStore()
  const navigate = useNavigate()
  
  return (
    <header className={styles.topbar}>
      <button className={styles.menuBtn} onClick={() => setSidebarOpen(true)}>≡</button>
      <div className={styles.title}>{title}</div>
      <div className={styles.actions}>
        <IconBtn onClick={() => setVoiceOpen(true)} title="Voice Input"><Mic size={20} strokeWidth={1.5} /></IconBtn>
        <IconBtn title="Notifications"><Bell size={20} strokeWidth={1.5} /></IconBtn>
        <IconBtn title="Search"><Search size={20} strokeWidth={1.5} /></IconBtn>
        <BtnPrimary style={{ padding: '7px 16px', fontSize: 13 }} onClick={() => navigate({ to: '/meals' })}>+ Log Meal</BtnPrimary>
      </div>
    </header>
  )
}
