import React, { useState } from 'react'
import MenuButton from './MenuButton'
import FilterButton from './FilterButton'
import GridButton from './GridButton'
import Logo from './Logo'
import SideMenu from './SideMenu'
import '../css/components/Header.css'

type Workspace = { id?: string; name: string; desc?: string; current?: boolean }

type HeaderProps = {
  workspaces?: Workspace[]
}

export default function Header({ workspaces }: HeaderProps) {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <>
      <SideMenu open={menuOpen} onClose={() => setMenuOpen(false)} />
      <header className="topbar">
        <div className="top-left">
          <MenuButton onClick={() => setMenuOpen(true)} />
          <div className="logo-area">
            <Logo />
          </div>
        </div>

        <div className="top-right">
          <FilterButton />
          <GridButton workspaces={workspaces} />
        </div>
      </header>
    </>
  )
}
