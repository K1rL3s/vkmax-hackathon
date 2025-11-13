import {
  CellHeader,
  CellInput,
  CellList,
  Container,
  Flex,
  Panel,
  Typography,
} from '@maxhub/max-ui'
import { createFileRoute } from '@tanstack/react-router'
import { Header } from '@/components/header'
import { Avatar } from '@/components/avatar'
import { useMe } from '@/hooks/user'
import { TimezoneInput } from '@/components/timezone-input'

export const Route = createFileRoute('/profile')({
  component: ProfilePage,
})

function ProfilePage() {
  const { data, isPending } = useMe()

  return (
    <Flex className="h-screen" direction="column" gapY={24}>
      <Header />
      <Panel className="w-full h-full">
        <Container className="h-full w-full">
          <Flex
            className="w-full h-full"
            justify="space-between"
            direction="column"
          >
            <Flex className="w-full h-full" direction="column" gapY={34}>
              <Flex className="w-full" justify="center">
                <Avatar
                  size={88}
                  firstName={data?.firstName ?? ''}
                  lastName={data?.lastName ?? ''}
                />
                <Typography.Headline>
                  {data?.firstName} {data?.lastName}
                </Typography.Headline>
              </Flex>
              <CellList
                filled
                mode="island"
                header={<CellHeader>Личные данные</CellHeader>}
              >
                <CellInput before={'Имя'} value={data?.firstName ?? ''} />
                <CellInput before={'Фамилия'} value={data?.lastName ?? ''} />
                <CellInput before={'Телефон'} value={data?.phone ?? ''} />
              </CellList>
              <CellList header={<CellHeader>Настройки</CellHeader>}>
                <TimezoneInput mode="primary" />
              </CellList>
            </Flex>
          </Flex>
        </Container>
      </Panel>
    </Flex>
  )
}
