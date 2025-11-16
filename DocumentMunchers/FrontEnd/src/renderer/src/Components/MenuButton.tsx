import React from 'react'
import IconButton from './IconButton'

export default function MenuButton({ onClick }: { onClick?: () => void }) {
  return (
    <IconButton title="Menu" onClick={onClick}>
      <svg width="20" height="14" viewBox="0 0 20 14" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="20" height="2" rx="1" fill="#2E7D32" />
        <rect y="6" width="20" height="2" rx="1" fill="#2E7D32" />
        <rect y="12" width="20" height="2" rx="1" fill="#2E7D32" />
      </svg>
    </IconButton>
  )
}
