import React from 'react'
import '../css/components/IconButton.css'

export default function IconButton({ children, title, onClick }: { children: React.ReactNode; title?: string; onClick?: () => void }) {
  return (
    <button className="icon-btn" title={title} aria-label={title} onClick={onClick}>
      {children}
    </button>
  )
}
