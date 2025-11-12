import { Flex, Spinner } from '@maxhub/max-ui'

import clsx from 'clsx'
import { Header } from '../header'
import { useGroup } from '@/hooks/groups'

export function GroupPageLayout({
  groupId,
  children,
  heading,
  className,
}: {
  groupId: number
  children: React.ReactNode
  heading?: React.ReactNode
  className?: string
}) {
  const { data, isPending } = useGroup(groupId)

  return (
    <div className={clsx('w-full h-screen', className)}>
      <Flex className="h-full" direction="column" gapY={24}>
        {isPending ? (
          <div className="p-4">
            <Spinner />
          </div>
        ) : (
          <Flex direction="column" className="h-full w-full">
            <Header title={data?.group.name}>{heading}</Header>
            <div className="w-full h-full px-(--spacing-size-xl)">
              {children}
            </div>
          </Flex>
        )}
      </Flex>
    </div>
  )
}
