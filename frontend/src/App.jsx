import { useEffect } from 'react'
import { useAppStore } from '@store'
import AppShell from '@layout/AppShell'

export default function App() {
  const { theme, dark } = useAppStore()

  useEffect(() => {
  const token = localStorage.getItem("token")

  if (!token) return

  authApi.getMe()
  }, [])

  return <AppShell />
}
