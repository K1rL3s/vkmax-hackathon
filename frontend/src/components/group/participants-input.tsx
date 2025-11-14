import { Flex } from '@maxhub/max-ui'
import clsx from 'clsx'
import { useState } from 'react'
import { User } from 'lucide-react'
import { Avatar } from '../avatar'
import { ParticipantSelectModal } from './participant-select-modal'
import type { GroupUserItem } from '@/lib/api/gen.schemas'

type ParticipantsInput = {
  value: Array<number>
  options: Array<GroupUserItem>
  onChange: (participantId: number) => void
  header?: React.ReactNode
  before?: React.ReactNode
  disabled?: boolean
  mode?: 'primary' | 'secondary'
}

export function ParticipantsInput({
  value,
  onChange,
  options,
  header,
  before,
  mode = 'primary',
  disabled = false,
}: ParticipantsInput) {
  const [isSelecting, setIsSelecting] = useState(false)

  const modeStyles = {
    primary: 'bg-(--background-surface-card) text-(--text-secondary)',
    secondary:
      'bg-(--background-accent-neutral-fade-secondary) text-(--text-secondary)',
  }

  return (
    <>
      <Flex direction="column" gapY={12} className="w-full">
        {header}
        <button
          type="button"
          onClick={() => !disabled && setIsSelecting(true)}
          className={clsx(
            'min-h-[52px] py-2 w-full rounded-(--size-border-radius-semantic-border-radius-card) cursor-pointer text-start px-3',
            modeStyles[mode],
          )}
        >
          <Flex align="center" gapX={12}>
            {before}
            {value.length === 0 ? (
              <>
                <Flex align="center" gapX={12}>
                  <div className="rounded-full border border-dashed p-2">
                    <User />
                  </div>
                  Никто не назначен
                </Flex>
              </>
            ) : (
              <>
                {options
                  .filter((option) => value.includes(option.userId))
                  .slice(0, 3)
                  .map((option, index) => (
                    <div key={option.userId}>
                      <Avatar
                        className={clsx({ '-ml-5': index !== 0 }, `z-${index}`)}
                        size={28}
                        firstName={option.firstName?.toString()}
                        lastName={option.lastName?.toString()}
                      />
                    </div>
                  ))}
                {value.length > 3 && (
                  <Avatar
                    className="border -ml-5! z-5"
                    size={28}
                    firstName={`+`}
                    lastName={`${value.length - 3}`}
                  />
                )}
              </>
            )}
          </Flex>
        </button>
      </Flex>
      <ParticipantSelectModal
        isOpen={isSelecting}
        onClose={() => setIsSelecting(false)}
        options={options}
        onSelect={onChange}
        value={value}
      />
    </>
  )
}
