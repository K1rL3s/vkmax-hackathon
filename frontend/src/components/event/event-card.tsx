import { Container, Flex, Typography } from '@maxhub/max-ui'
import { Link } from '@tanstack/react-router'
import { CalendarIcon, MessageCircleMoreIcon } from 'lucide-react'
import type { CalendarEvent } from './event-list'

export function EventCard({ event }: { event: CalendarEvent }) {
  const beforeIcon = {
    event: <CalendarIcon size={18} />,
    message: <MessageCircleMoreIcon size={18} />,
  }[event.type]

  return (
    <Link to="/events/$id" params={{ id: event.id.toString() }}>
      <Container className="w-full bg-(--background-accent-themed)/40 rounded-xl py-2">
        <Flex align="center" gapX={8}>
          {beforeIcon}
          <Flex direction="column" gapY={6}>
            <Typography.Title>{event.title}</Typography.Title>
          </Flex>
        </Flex>
      </Container>
    </Link>
  )
}
