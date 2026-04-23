import { useNavigate } from '@tanstack/react-router'
import { BtnPrimary } from '@ui'

export default function NotFound() {
  const navigate = useNavigate()

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', gap: 20, textAlign: 'center', padding: 20 }}>
      <div style={{ fontSize: 80 }}>404</div>
      <h1>Page Not Found</h1>
      <p>The page you're looking for doesn't exist.</p>
      <BtnPrimary onClick={() => navigate({ to: '/dashboard' })}>
        Go to Dashboard
      </BtnPrimary>
    </div>
  )
}
