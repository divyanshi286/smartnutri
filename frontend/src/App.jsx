import { useEffect } from 'react'
import { useAppStore } from '@store'
import AppShell from '@layout/AppShell'

export default function App() {
  const { theme, dark } = useAppStore()

  useEffect(() => {
    const body = document.body
    body.className = [theme, dark ? 'dark' : ''].filter(Boolean).join(' ')
  }, [theme, dark])

  return <AppShell />
}
