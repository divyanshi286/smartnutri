import { useState, useRef, useEffect } from 'react'
import { useAppStore } from '@store'
import { useSendChat, useChatSuggestions } from '@hooks/useQueries'
import { IconBtn, BtnPrimary } from '@ui'
import styles from './Chat.module.css'

export default function Chat() {
  const { user, messages, addMessage, setVoiceOpen } = useAppStore()
  const { data: suggestions = [] } = useChatSuggestions()
  const { mutateAsync, isPending } = useSendChat()
  const [input, setInput] = useState('')
  const historyRef = useRef(null)

  useEffect(() => {
    if (historyRef.current) historyRef.current.scrollTop = historyRef.current.scrollHeight
  }, [messages, isPending])

  async function send(text) {
    const msg = text || input.trim()
    if (!msg) return
    setInput('')
    addMessage({ role: 'user', content: msg })
    const reply = await mutateAsync(msg)
    addMessage(reply)
  }

  return (
    <div className={styles.layout}>
      {/* Suggestions sidebar */}
      <div className={styles.chatSidebar}>
        <div className={styles.sidebarHd}>
          <div style={{ fontWeight: 700, fontSize: 14 }}>Suggested Questions</div>
          <div style={{ fontSize: 12, color: 'var(--muted)', marginTop: 3 }}>Personalized for PCOS</div>
        </div>
        <div className={styles.suggList}>
          {(suggestions.length ? suggestions : [
            { label: '🥩 Best protein foods for PCOS?', msg: 'Best protein foods for PCOS?' },
            { label: '🚫 Foods I should avoid?', msg: 'Foods I should avoid?' },
            { label: '⚡ Pre-workout snack ideas?', msg: 'Pre-workout snack ideas?' },
          ]).map((s) => (
            <button key={s.msg} className={styles.suggBtn} onClick={() => send(s.msg)}>{s.label}</button>
          ))}
        </div>
        <div className={styles.safetyNote}>
          <div style={{ fontSize: 12, fontWeight: 700, color: '#92400e', marginBottom: 6 }}>🛡 Safety First</div>
          <div style={{ fontSize: 11.5, color: '#78350f', lineHeight: 1.65 }}>All responses are screened for your safety. Harmful content is replaced with helpful alternatives.</div>
        </div>
      </div>

      {/* Main chat area */}
      <div className={styles.chatMain}>
        {/* Header */}
        <div className={styles.chatHead}>
          <div className={styles.chatAvatar}>💡</div>
          <div>
            <div style={{ fontFamily: 'var(--ff-display)', fontWeight: 700, fontSize: 16 }}>Smart Suggestions</div>
            <div style={{ fontSize: 12, color: 'var(--p1)', fontWeight: 700 }}>
              ● Online · {user?.conditions?.length ? `Personalized for ${user.conditions.join(', ')}` : 'Personalized support'}
            </div>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
            <IconBtn onClick={() => setVoiceOpen(true)}>🎙</IconBtn>
            <IconBtn>📷</IconBtn>
          </div>
        </div>

        {/* Messages */}
        <div className={styles.history} ref={historyRef}>
          {messages.map((msg) => (
            <div key={msg.id} className={msg.role === 'user' ? styles.bubbleUser : styles.bubbleAi}>
              {msg.role === 'ai' && <div className={styles.aiBubbleAvatar}>💡</div>}
              <div>
                <div className={`${styles.bubbleBody} ${msg.role === 'user' ? styles.userBody : styles.aiBody}`}>
                  <span dangerouslySetInnerHTML={{ __html: msg.content }}/>
                </div>
                {msg.chips?.length > 0 && (
                  <div className={styles.chipRow}>
                    {msg.chips.map((c) => <button key={c} className={styles.suggBtn} onClick={() => send(c)}>{c}</button>)}
                  </div>
                )}
              </div>
              {msg.role === 'user' && <div className={styles.userAvatar}>P</div>}
            </div>
          ))}
          {isPending && (
            <div className={styles.bubbleAi}>
              <div className={styles.aiBubbleAvatar}>💡</div>
              <div className={`${styles.bubbleBody} ${styles.aiBody}`} style={{ color: 'var(--muted)' }}>
                Thinking…
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className={styles.inputArea}>
          <IconBtn>📷</IconBtn>
          <input
            className={styles.chatInput}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
            placeholder="Ask NutriAI anything… (try: 'Log dal rice for lunch')"
          />
          <IconBtn onClick={() => setVoiceOpen(true)}>🎙</IconBtn>
          <BtnPrimary style={{ padding: '10px 18px' }} onClick={() => send()}>Send ➤</BtnPrimary>
        </div>
      </div>
    </div>
  )
}
