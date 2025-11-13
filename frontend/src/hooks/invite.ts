import { useMutation } from '@tanstack/react-query'
import { createInviteRouteGroupsGroupIdInvitePost } from '@/lib/api/groups/groups'

export function useInvite() {
  return useMutation({
    mutationKey: ['invite'],
    mutationFn: ({ groupId }: { groupId: number }) =>
      createInviteRouteGroupsGroupIdInvitePost(groupId),
    onSuccess: (data) => {
      navigator.clipboard.writeText(
        `https://max.ru/t123_hakaton_bot?start=${data.inviteKey}`,
      )
    },
  })
}
