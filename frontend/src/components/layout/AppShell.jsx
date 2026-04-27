import { useAppStore } from '@store'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import VoiceModal from '@features/VoiceModal'
import Dashboard from '@features/dashboard/Dashboard'
import Chat from '@features/chat/Chat'
import Meals from '@features/meals/Meals'
import Progress from '@features/progress/Progress'
import Nutrition from '@features/nutrition/Nutrition'
import Cycle from '@features/cycle/Cycle'
import Education from '@features/education/Education'
import Safety from '@features/safety/Safety'
import Onboarding from '@features/onboarding/Onboarding'
import Parent from '@features/parent/Parent'
import Components from '@features/design/Components'
import StyleGuide from '@features/design/StyleGuide'
import Gestures from '@features/design/Gestures'
import PrivacyDoc from '@features/design/PrivacyDoc'
import styles from './AppShell.module.css'

const PAGE_MAP = {
  dashboard: Dashboard,
  chat:       Chat,
  meals:      Meals,
  progress:   Progress,
  nutrition:  Nutrition,
  cycle:      Cycle,
  education:  Education,
  safety:     Safety,
  onboarding: Onboarding,
  parent:     Parent,
  components: Components,
  styleguide: StyleGuide,
  gestures:   Gestures,
  privacydoc: PrivacyDoc,
}

export const PAGE_TITLES = {
  dashboard:  'Dashboard',
  chat:       'AI Coach',
  meals:      'Meal Log',
  progress:   'Progress',
  nutrition:  'Nutrition Detail',
  cycle:      'Cycle Tracker',
  education:  'Learn',
  safety:     'Safety Demo',
  onboarding: 'Onboarding (Step 3/5)',
  parent:     'Parent Dashboard',
  components: 'Component Library',
  styleguide: 'Style Guide',
  gestures:   'Gesture Controls',
  privacydoc: 'Safety & Privacy',
}

export default function AppShell({ children }) {
  const { activePage, sidebarOpen } = useAppStore()

  return (
    <div className={styles.shell}>
      <Sidebar />
      {sidebarOpen && <div className={styles.overlay} onClick={() => useAppStore.getState().setSidebarOpen(false)}/>}
      <div className={styles.main}>
        <Topbar title={PAGE_TITLES[activePage] || 'Dashboard'}/>
        <main className={styles.content}>
          {children}
        </main>
      </div>
      <VoiceModal />
    </div>
  )
}
