import React, { useEffect, useRef } from 'react'
import Logo from './Logo'
import '../css/components/SideMenu.css'

export default function SideMenu({ open, onClose }: { open: boolean; onClose?: () => void }) {
  const rootRef = useRef<HTMLDivElement | null>(null)
  const panelRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (!open) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose?.()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, onClose])

  // Close when clicking outside the panel (robust) — any click not inside the panel
  function handleClick(e: React.MouseEvent) {
    if (!onClose) return
    const target = e.target as Node
    if (panelRef.current && !panelRef.current.contains(target)) {
      onClose()
    }
  }

  // helper to close when a nav link is clicked
  function handleNavClick() {
    onClose?.()
  }

  return (
    <div
      ref={rootRef}
      className={`side-menu ${open ? 'open' : ''}`}
      role="dialog"
      aria-hidden={!open}
      onClick={handleClick}
    >
      <div className="side-menu-backdrop" aria-hidden="true" />
      <aside ref={panelRef} className="side-menu-panel" aria-modal={open}>
        <div style={{ padding: 16 }}>
          <div className="side-header">
            <Logo
              onClick={() => {
                // close side menu and navigate home
                handleNavClick()
                try {
                  window.location.hash = '#/'
                } catch (e) {
                  /* noop */
                }
              }}
            />
          </div>
          <ul className="side-menu-list">
            <li>
              <a href="#/search-history" className="side-link" onClick={handleNavClick}>
                Search History
              </a>
            </li>
            <li>
              <a href="#/file-history" className="side-link" onClick={handleNavClick}>
                File History
              </a>
            </li>
            <li>
              <a href="#/statistics" className="side-link" onClick={handleNavClick}>
                Statistics for Nerds
              </a>
            </li>
            <li>
              <a href="#/about" className="side-link" onClick={handleNavClick}>
                About this software
              </a>
            </li>
          </ul>
        </div>
      </aside>
    </div>
  )
}
