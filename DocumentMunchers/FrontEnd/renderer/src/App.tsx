import React, { useEffect, useState } from 'react'
import Header from './Components/Header'
import SearchHistory from './Pages/SearchHistory'
import FileHistory from './Pages/FileHistory'
import Statistics from './Pages/Statistics'
import About from './Pages/About'
import Home from './Pages/Home'
import SearchResults from './Pages/SearchResults'
import LoadingScreen from './Components/LoadingScreen'


//import WorkspacePopUp from './Components/WorkspacePopUp'

export default function App() {
  const [route, setRoute] = useState(window.location.hash || '#/')
  const [shouldCheckWorkspaces, setShouldCheckWorkspaces] = useState(true)
  const [isBackendReady, setIsBackendReady] = useState(false)
  const [loadingMessage, setLoadingMessage] = useState('Starting up...')
  const [workspacesChecked, setWorkspacesChecked] = useState(false)
  const [showWorkspacePopup, setShowWorkspacePopup] = useState(false)

  useEffect(() => {
    const onHash = () => setRoute(window.location.hash || '#/')
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  // Listen for the openWorkspacePopup event
  useEffect(() => {
    const handleOpenWorkspacePopup = () => {
      setShowWorkspacePopup(true)
    }

    window.addEventListener('openWorkspacePopup', handleOpenWorkspacePopup)
    
    return () => {
      window.removeEventListener('openWorkspacePopup', handleOpenWorkspacePopup)
    }
  }, [])

  // Check if back end is ready
  useEffect(() => {
    const checkBackendReady = async () => {
      const attemptConnection = async () => {
        try {
          setLoadingMessage('Loading...')
          const response = await fetch('http://localhost:5000/api/health', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          });

          if (response.ok) {
            setIsBackendReady(true)
            setLoadingMessage('Loading complete!')
            return true
          }
        } catch (error) {
          // If back end isn't up yet, wait three seconds
          setLoadingMessage("Waiting on database...")
          setTimeout(attemptConnection, 5000)
        }
        return false
      }

      await attemptConnection()
    }

    checkBackendReady()
  }, [])

  // Check if workspaces exist on initial load (only after back end is ready)
  useEffect(() => {
    if (!isBackendReady || workspacesChecked) return

    const checkWorkspaces = async () => {
      try {
        setLoadingMessage('Checking workspaces...')
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
          setWorkspacesChecked(true)
          
          if (Array.isArray(result) && result.length === 0) {
            // No workspaces exist, directly show the popup
            setLoadingMessage('No workspaces found. Opening setup...')
            console.warn("No workspaces set up")
            
            // Small delay to show the message
            setTimeout(() => {
              setShowWorkspacePopup(true)
            }, 5000)
          } else {
            setLoadingMessage('Loading complete!')
            setTimeout(() => {}, 5000)
          }
        }
      } catch (error) {
        console.error('Error checking workspaces:', error);
        setWorkspacesChecked(true)
      }
    };

    checkWorkspaces();
  }, [isBackendReady, workspacesChecked])

  const handleCloseWorkspacePopup = () => {
    setShowWorkspacePopup(false)
  }

  // Don't render the main app until backend is ready AND workspaces check is complete
  if (!isBackendReady || !workspacesChecked) {
    return <LoadingScreen message={loadingMessage} />
  }

  return (
    <div className="app-root">
      <Header />
      
      {/* Render WorkspacePopup if showWorkspacePopup is true 
      {showWorkspacePopup && ( 
        <WorkspacePopUp onClose={handleCloseWorkspacePopup} />
      )}
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