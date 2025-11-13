import { useQuery } from '@tanstack/react-query'
import { getUserByIdRouteUsersMeGet } from '@/lib/api/users/users'

export function useMe() {
  return useQuery({
    queryKey: ['me'],
    queryFn: () => getUserByIdRouteUsersMeGet(),
  })
}
