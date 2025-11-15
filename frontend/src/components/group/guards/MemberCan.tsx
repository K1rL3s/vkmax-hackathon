import { useMemberHasRole } from '@/hooks/groups'

export function MemberCan({
  children,
  rolesIds,
  groupId,
  memberId,
}: {
  children: React.ReactNode
  groupId: string
  rolesIds: Array<number>
  memberId: number
}) {
  const hasPermission = useMemberHasRole(Number(groupId), rolesIds, memberId)
  return hasPermission ? <>{children}</> : null
}
