import { useAppStore } from '@store'
import AppShell from '@layout/AppShell'

export default function App() {
  const { theme, dark } = useAppStore()

  return <AppShell />
}
