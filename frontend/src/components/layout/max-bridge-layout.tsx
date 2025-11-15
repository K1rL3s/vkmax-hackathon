import { useNavigate } from '@tanstack/react-router'
import { FallbackLoader } from '../ui/fallback-loader'
import { useAuth } from '@/hooks/auth'

export function MaxBridgeLayout({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  const { isPending, isError } = useAuth()

  if (isError) {
    navigate({ to: '/max-error' })
  }

  return <FallbackLoader isLoading={isPending}>{children}</FallbackLoader>
}
