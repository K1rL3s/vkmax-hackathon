import clsx from 'clsx'
import { X } from 'lucide-react'
import { Typography } from '@maxhub/max-ui'
import type { TagResponse } from '@/lib/api/gen.schemas'

type TagProps = {
  tag: TagResponse
  onClick?: () => void
}

export function Tag({ tag, onClick }: TagProps) {
  const tagColorStyles = {
    red: 'bg-red-500',
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500',
    cyan: 'bg-cyan-500',
    pink: 'bg-pink-500',
    orange: 'bg-orange-500',
  }
  return (
    <div
      className={clsx(
        'rounded-full text-(--text-contrast-static) flex items-center space-x-2 px-2 py-1 w-fit mr-2 my-1',
        tagColorStyles[tag.color as keyof typeof tagColorStyles],
      )}
    >
      <Typography.Body>{tag.name}</Typography.Body>
      {onClick && <X size={16} onClick={onClick} />}
    </div>
  )
}
