import React, { useState } from 'react'
import IconButton from './IconButton'
import '../css/components/GridButton.css'

// Button to open workspace management

type Workspace = {
  id?: string
  name: string
  desc?: string
  current?: boolean
}

export default function GridButton({ workspaces, onSelect }: { workspaces?: Workspace[]; onSelect?: (w: Workspace) => void }) {
  const [open, setOpen] = useState(false)
  const [menuOpen, setMenuOpen] = useState<string | null>(null)
  const [editWorkspace, setEditWorkspace] = useState<Workspace | null>(null)
  const [filePaths, setFilePaths] = useState<string[]>([])
  const [newFilePath, setNewFilePath] = useState('')

  // Query back end to get all existing workspaces
  const list = (workspaces && workspaces.length > 0) ? workspaces : [{ id: 'default', name: 'Default workspace', desc: '', current: true }]

  const handleEdit = (workspace: Workspace) => {
    setEditWorkspace({...workspace}) // Create a copy to avoid mutating original
    setMenuOpen(null)
    // Load file paths for the workspace from the back end
    setFilePaths([]) // Reset or load existing paths
  }

  // Button action for adding a new workspace
  const handleNewWorkspace = (workspace: Workspace) =>{
    setEditWorkspace({...workspace})
    setMenuOpen(null)
    setFilePaths([])
  }

  const addFilePath = () => {
    if (newFilePath.trim()) {
      setFilePaths([...filePaths, newFilePath.trim()])
      setNewFilePath('')
    }
  }

  const removeFilePath = (index: number) => {
    setFilePaths(filePaths.filter((_, i) => i !== index))
  }

  const saveFilePaths = () => {
    // Save file paths to back end
    console.log('Saving file paths for workspace:', editWorkspace?.name, filePaths)
    setEditWorkspace(null)
    setFilePaths([])
  }

  const updateWorkspaceName = (name: string) => {
    if (editWorkspace) {
      setEditWorkspace({...editWorkspace, name})
    }
  }

  return (
    <>
      <IconButton title="Workspace" onClick={() => setOpen(v => !v)}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
          <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
          <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
          <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
        </svg>
      </IconButton>

      {/* Workspace Selection Window */}
      {open && (
        <div className="modal-backdrop" onClick={() => setOpen(false)}>
          <div className="workspace-modal" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
            <div className="workspace-header">Workspace</div>

            <div className="workspace-list">
              {list.map((w, idx) => (
                <div key={w.id || idx} className={`workspace-item ${w.current ? 'current' : ''}`} onClick={() => { onSelect?.(w); setOpen(false) }}>
                  <div className="workspace-avatar">👤</div>
                  <div className="workspace-body">
                    <div className="workspace-title">{w.name} {w.current && <span className="current-badge">Current</span>}</div>
                    {w.desc && <div className="workspace-desc">{w.desc}</div>}
                  </div>
                  
                  {/* Workspace actions menu */}
                  <div 
                    className="workspace-actions" 
                    onClick={(e) => {
                      e.stopPropagation()
                      setMenuOpen(menuOpen === w.id ? null : w.id || idx.toString())
                    }}
                  >
                    ⋮
                    {menuOpen === (w.id || idx.toString()) && (
                      <div className="workspace-menu">
                        <div className="menu-item" onClick={() => handleEdit(w)}>Edit</div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="workspace-footer">
              {/* Button to add a new workspace */}
              {/*<button className="new-workspace" onClick={() => handleNewWorkspace(w)}> + New Workspace </button>*/}
              <button className='new-workspace'> + New Workspace </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit workspace window */}
      {editWorkspace && (
        <div className="modal-backdrop" onClick={() => setEditWorkspace(null)}>
          <div className="edit-modal" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                Workspace Name 
                <input
                  type="text"
                  value={editWorkspace.name}
                  onChange={(e) => updateWorkspaceName(e.target.value)}
                  className="workspace-name-input"
                />
              </h3>
              <button className="close-button" onClick={() => setEditWorkspace(null)}>×</button>
            </div>
            
            <div className="modal-content">
              <div className="file-paths-section">
                <h4>File Paths</h4>
                <div className="add-path">
                  <input
                    type="text"
                    placeholder="Enter file path..."
                    value={newFilePath}
                    onChange={(e) => setNewFilePath(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addFilePath()}
                  />
                  <button onClick={addFilePath}>Add</button>
                </div>
                
                <div className="file-paths-list">
                  {filePaths.map((path, index) => (
                    <div key={index} className="file-path-item">
                      <span className="path-text">{path}</span>
                      <button 
                        className="remove-path"
                        onClick={() => removeFilePath(index)}
                      >
                        ×
                      </button>
                    </div>
                  ))}
                  {filePaths.length === 0 && (
                    <div className="no-paths">No file paths added yet</div>
                  )}
                </div>
              </div>
            </div>
            
            <div className="modal-footer">
              <button className="cancel-button" onClick={() => setEditWorkspace(null)}>
                Cancel
              </button>
              <button className="save-button" onClick={saveFilePaths}>
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}