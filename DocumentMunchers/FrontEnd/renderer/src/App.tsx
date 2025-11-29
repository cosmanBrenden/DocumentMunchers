import React, { useEffect, useState } from 'react'
import Header from './Components/Header'

import SearchHistory from './Pages/SearchHistory'
import FileHistory from './Pages/FileHistory'
import Statistics from './Pages/Statistics'
import About from './Pages/About'
import Home from './Pages/Home'
import SearchResults from './Pages/SearchResults'

export default function App() {
  const [route, setRoute] = useState(window.location.hash || '#/')
  const [shouldCheckWorkspaces, setShouldCheckWorkspaces] = useState(true)

  useEffect(() => {
    const onHash = () => setRoute(window.location.hash || '#/')
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  // Check if workspaces exist on initial load
  useEffect(() => {
    if (!shouldCheckWorkspaces) return

    const checkWorkspaces = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "type": "workspace_query",
            "content": {
              "action": "list_workspaces"
            }
          }),
        });

        if (response.ok) {
          const result = await response.json();
          if (Array.isArray(result) && result.length === 0) {
            // No workspaces exist, trigger the workspace popup by dispatching a custom event
            window.dispatchEvent(new CustomEvent('openWorkspacePopup'));
          }
        }
      } catch (error) {
        console.error('Error checking workspaces:', error);
      } finally {
        setShouldCheckWorkspaces(false);
      }
    };

    checkWorkspaces();
  }, [shouldCheckWorkspaces])

  return (
    <div className="app-root">
      <Header />
      {/* Optional: pass workspaces here. If omitted, GridButton will show a default workspace.
          Example:
          workspaces={[{id:'w1', name:'Research', desc:'Reinforcement Learning papers', current:false}]}
      */}

      <main className="main-area">
        {/* Simple router based on hash */}
        {route === '#/search-history' && <SearchHistory />}
        {route === '#/file-history' && <FileHistory />}
        {route === '#/statistics' && <Statistics />}
        {route === '#/about' && <About />}

        {/* Results route */}
        {route.startsWith('#/results') && (() => {
          // parse query param from hash like '#/results?q=term'
          const qIndex = route.indexOf('?')
          const qs = qIndex >= 0 ? route.substring(qIndex) : ''
          const params = new URLSearchParams(qs.replace(/^\?/, ''))
          const q = params.get('q') || ''
          return <SearchResults query={decodeURIComponent(q)} />
        })()}

        {/* Default content (home) */}
        {route === '#' || route === '' || route === '#/' ? <Home /> : null}
      </main>
    </div>
  )
}
