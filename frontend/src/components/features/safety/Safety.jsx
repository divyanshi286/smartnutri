import { BtnPrimary, BtnSecondary } from '@ui'
import styles from './Safety.module.css'

export default function Safety() {
  return (
    <div className={styles.wrap}>
      <div className={styles.grid}>
        {/* Demo chat */}
        <div>
          <div className={styles.demoCard}>
            <div className={styles.demoHead}>
              <div className={styles.demoAvatar}>🤖</div>
              <div>
                <div className={styles.demoName}>NutriAI Coach</div>
                <div className={styles.demoStatus}>● Active · Safety Mode</div>
              </div>
              <div className={styles.demoBadge}>🛡 Safety Demo</div>
            </div>

            {/* User dangerous query */}
            <div className={styles.bubbleUser}>
              <div className={styles.userAv}>SK</div>
              <div className={styles.userBody}>
                If I eat only 500 calories a day how fast will I lose weight? 😬
              </div>
            </div>

            {/* Safety response */}
            <div className={styles.safetyCard}>
              <div className={styles.safetyHead}>
                <div className={styles.safetyAvatar}>🤖</div>
                <div>
                  <div style={{ fontWeight: 700 }}>NutriAI Coach</div>
                  <div className={styles.safetyBadge}>💛 Safety Response — Never shame, always care</div>
                </div>
              </div>
              <div className={styles.safetyBody}>
                Hey, I noticed that question — and I want you to know:{' '}
                <strong>I care about you, not just numbers.</strong>
                <br /><br />
                500 calories is far below what your body needs to function safely.
                Instead of answering that, here's what <em>actually</em> works: a 1500–1700
                calorie balanced plan will help you feel amazing <em>and</em> reach your goals,
                with zero crash or nutrient deficiency.
              </div>
              <div className={styles.safetyActions}>
                <BtnPrimary style={{ padding: '9px 16px', fontSize: 13 }}>
                  Show me the safe plan 💚
                </BtnPrimary>
                <BtnSecondary>Talk to someone 🤝</BtnSecondary>
              </div>
            </div>

            {/* SOS */}
            <div className={styles.sosCard}>
              <div className={styles.sosTitle}>🆘 Struggling with food or body image?</div>
              <div className={styles.sosBody}>
                📞 <strong>iCall:</strong> 9152987821<br />
                💬 <strong>AASRA:</strong> 9820466627 (24/7)<br />
                🌐 <strong>Vandrevala:</strong> 1860-2662-345
              </div>
              <div className={styles.sosCta}>You are not alone. Reaching out is brave. 💙</div>
            </div>
          </div>
        </div>

        {/* Info panels */}
        <div className={styles.infoCol}>
          <div className={styles.infoCard}>
            <div className={styles.infoTitle}>🚨 Trigger Phrase Detection</div>
            <div className={styles.infoBody}>
              Phrases that trigger safety intervention:
              <ul className={styles.triggerList}>
                <li>"only X calories" (below 800)</li>
                <li>"starve", "purge", "not eat"</li>
                <li>Extreme restriction queries</li>
                <li>Rapid weight-loss requests</li>
                <li>Negative body image language</li>
              </ul>
              <div className={styles.triggerNote}>
                <strong>Response always:</strong> Warm → Alternative → Resources<br />
                <strong>Never shame. Never judge.</strong>
              </div>
            </div>
          </div>

          <div className={styles.infoCard}>
            <div className={styles.infoTitle}>🔄 Safety Flow</div>
            <div className={styles.flowList}>
              <div className={styles.flowStep} style={{ background: 'var(--p3)', borderColor: 'var(--p1)' }}>
                💬 Teen sends query
              </div>
              <div className={styles.flowArrow}>↓</div>
              <div className={styles.flowStep} style={{ background: '#fef9c3', borderColor: '#f59e0b' }}>
                🔍 Safety Filter scans for triggers
              </div>
              <div className={styles.flowArrow}>↓</div>
              <div className={styles.flowStep} style={{ background: '#d1fae5', borderColor: '#6ee7b7' }}>
                ✅ Safe → Normal educational response
              </div>
              <div className={styles.flowStep} style={{ background: '#fee2e2', borderColor: '#fca5a5', marginTop: 6 }}>
                ⚠️ Unsafe → Warm intervention + resources
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
