import React from 'react'

export default function Logo({ onClick }: { onClick?: () => void }) {
  // default navigation behavior: go to home hash
  const navigateHome = () => {
    try {
      window.location.hash = '#/'
    } catch (e) {
      // noop in environments where location isn't available
    }
  }

  const handleActivate = () => {
    if (onClick) return onClick()
    navigateHome()
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleActivate()
    }
  }

  return (
    <div
      className="logo"
      onClick={handleActivate}
      style={{ cursor: 'pointer' }}
      role="link"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      aria-label="Go to home"
    >
      <img src="/logo-transparent.png" alt="Document Munchers" className="brand-img" />
    </div>
  )
}
