import { useQuery } from '@tanstack/react-query'
import { checkInitDataAuthGet } from '@/lib/api/auth/auth'

export function useAuth() {
  return useQuery({
    queryKey: ['auth'],
    queryFn: () => checkInitDataAuthGet,
  })
}
