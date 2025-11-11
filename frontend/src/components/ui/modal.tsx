import ReactDOM from 'react-dom'
import { Container } from '@maxhub/max-ui'
import clsx from 'clsx'
import * as MaxUiProvider from '@/integrations/max-ui/root-provider'

type ModalProps = {
  isOpen: boolean
  onClose: () => void
  children: React.ReactNode
  className?: string
}

export function Modal({ isOpen, onClose, children, className }: ModalProps) {
  if (!isOpen) return null
  const modalRoot = document.getElementById('modal') as Element
  return ReactDOM.createPortal(
    <MaxUiProvider.Provider>
      <div
        className="fixed inset-0 z-50 flex items-center justify-center bg-(--background-overlay-secondary)"
        onClick={onClose}
      >
        <Container
          onClick={(e) => e.stopPropagation()}
          className={clsx(
            'bg-(--background-surface-floating) rounded-3xl py-4 max-h-[75vh] max-w-[70vw]',
            className,
          )}
        >
          {children}
        </Container>
      </div>
    </MaxUiProvider.Provider>,
    modalRoot,
  )
}
