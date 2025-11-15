import { Container, Flex, Panel } from '@maxhub/max-ui'
import { createFileRoute } from '@tanstack/react-router'
import { Smartphone } from 'lucide-react'
import { Card } from '@/components/card'

export const Route = createFileRoute('/max-error')({
  component: MaxErrorPage,
})

function MaxErrorPage() {
  return (
    <Panel centeredX centeredY className="h-screen! w-full">
      <Container className="w-full h-full flex items-center justify-center">
        <Card className="w-fit h-fit!">
          <Flex
            gapY={15}
            className="w-full"
            justify="center"
            direction="column"
          >
            <Smartphone size={100} />
          </Flex>
        </Card>
      </Container>
    </Panel>
  )
}
