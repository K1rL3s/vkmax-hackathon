import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/groups/$groupId/events/create')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/groups/$groupId/events/create"!</div>
}
