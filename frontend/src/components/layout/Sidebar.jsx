import { useAppStore } from '@store'
import { useNavigate } from '@tanstack/react-router'
import authApi from '@api/auth'
import { Flame, Moon } from 'lucide-react'
import styles from './Sidebar.module.css'

const NAV = [
  { section: 'Main' },
  { id: 'dashboard',  ico: '■', label: 'Dashboard'    },
  { id: 'chat',       ico: '◆', label: 'Smart Suggestions' },
  { id: 'meals',      ico: '●', label: 'Meal Log'      },
  { id: 'progress',   ico: '▲', label: 'Progress'      },
  { id: 'nutrition',  ico: '○', label: 'Nutrition'     },
  { section: 'Wellness' },
  { id: 'cycle',      ico: '●', label: 'Cycle Tracker' },
  { id: 'education',  ico: '▪', label: 'Learn'         },
  { id: 'safety',     ico: '■', label: 'Safety'        },
  { section: 'Account' },
  { id: 'onboarding', ico: '◇', label: 'Onboarding'    },
  { id: 'parent',     ico: '◈', label: 'Parent View'   },
  { section: 'Settings' },
  { id: 'components', ico: '◉', label: 'Components'    },
  { id: 'styleguide', ico: '▬', label: 'Style Guide'   },
  { id: 'gestures',   ico: '▮', label: 'Gestures'      },
  { id: 'privacydoc', ico: '▲', label: 'Privacy'       },
]

const THEMES = [
  { cls: 'th-adult',  label: 'Default', title: 'Default – Professional'         },
  { cls: 'th-boy',    label: 'Slate', title: 'Slate – Minimal'      },
  { cls: 'th-girl-h', label: 'Cycle', title: 'Cycle – Hormonal'   },
  { cls: 'th-girl-a', label: 'Mood', title: 'Mood – Warm'     },
]

export default function Sidebar() {
  const navigate = useNavigate()
  const { activePage, setActivePage, sidebarOpen, setSidebarOpen, theme, setTheme, dark, toggleDark, user, clearAuth } = useAppStore()

  async function handleLogout() {
    try {
      await authApi.logout()
    } catch (err) {
      console.error('Logout error:', err)
    }
    clearAuth()
    navigate({ to: '/auth/login' })
  }

  function handleNav(id) {
    setActivePage(id)
    if (window.innerWidth < 900) setSidebarOpen(false)
    // Navigate to the correct route
    navigate({ to: `/${id}` })
  }

  return (
    <aside className={`${styles.sidebar} ${sidebarOpen ? styles.open : ''}`}>
      {/* Brand */}
      <div className={styles.brand}>
        <div className={styles.brandMark}>N</div>
        <div>
          <div className={styles.brandName}>SmartNutri</div>
          <div className={styles.brandTag}>v3 · Web App</div>
        </div>
      </div>

      {/* User */}
      <div className={styles.userRow}>
        <div className={styles.avatar}>{user?.initials || 'U'}</div>
        <div>
          <div className={styles.userName}>{user?.name || 'Guest User'}</div>
          <div className={styles.userSub}>
            {user?.segment ? `${user.segment} plan` : 'Personalized health plan'} •
            {user?.conditions?.length ? ` ${user.conditions.join(', ')}` : ' No condition set'}
          </div>
          <div className={styles.userBadge}><Flame size={16} style={{ display: 'inline', marginRight: 4 }} /> {user?.streak ?? 0}-day streak</div>
        </div>
      </div>
      
      {/* Logout Button */}
      <button className={styles.logoutBtn} onClick={handleLogout}>
        Logout
      </button>

      {/* Nav */}
      <nav className={styles.nav}>
        {NAV.map((item, i) =>
          item.section ? (
            <div key={i} className={styles.navSection}>{item.section}</div>
          ) : (
            <button
              key={item.id}
              className={`${styles.navItem} ${activePage === item.id ? styles.navOn : ''}`}
              onClick={() => handleNav(item.id)}
            >
              <span className={styles.navIco}>{item.ico}</span>
              {item.label}
            </button>
          )
        )}
      </nav>

      {/* Footer */}
      <div className={styles.footer}>
        <div className={styles.themeSwitcher}>
          {THEMES.map((t) => (
            <button
              key={t.cls}
              className={`${styles.thBtn} ${theme === t.cls ? styles.thBtnActive : ''}`}
              onClick={() => setTheme(t.cls)}
              title={t.title}
            >
              {t.label}
            </button>
          ))}
        </div>
        <div className={styles.darkToggle} onClick={toggleDark}>
          <span><Moon size={16} style={{ display: 'inline', marginRight: 6 }} />Dark Mode</span>
          <div className={styles.togglePill}/>
        </div>
      </div>
    </aside>
  )
}
