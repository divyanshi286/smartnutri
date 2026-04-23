import { useEffect } from 'react'
import { useAppStore } from '@store'
import { useVoiceExamples } from '@hooks/useQueries'
import { BtnSecondary } from '@ui'
import styles from './VoiceModal.module.css'

export default function VoiceModal() {
  const { voiceOpen, setVoiceOpen } = useAppStore()
  const { data: examples = [] } = useVoiceExamples()

  useEffect(() => {
    if (voiceOpen) {
      const t = setTimeout(() => setVoiceOpen(false), 4000)
      return () => clearTimeout(t)
    }
  }, [voiceOpen, setVoiceOpen])

  if (!voiceOpen) return null

  return (
    <div className={styles.overlay} onClick={() => setVoiceOpen(false)}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.orb}>🎙</div>
        <div className={styles.title}>Listening…</div>
        <div className={styles.sub}>Speak your command or question</div>
        <div className={styles.examples}>
          {(examples.length ? examples : [
            'Log dal rice for lunch',
            'How much protein do I have today?',
            'Add 2 glasses of water',
            'What foods help with PCOS?',
            'Show my weekly progress',
          ]).map((item, index) => (
            <div key={`${item}-${index}`}>🎙 {`"${item}"`}</div>
          ))}
        </div>
        <BtnSecondary style={{ width: '100%', marginTop: 16, justifyContent: 'center' }} onClick={() => setVoiceOpen(false)}>
          ✕ Cancel
        </BtnSecondary>
      </div>
    </div>
  )
}
