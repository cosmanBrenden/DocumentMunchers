import React, { useState, useEffect } from 'react' 
import IconButton from './IconButton'
import WorkspaceEditModal from './WorkspacePopUp'
import '../css/components/GridButton.css'

// Grid Button opens workspace selection and management

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
  const [backendWorkspaces, setBackendWorkspaces] = useState<Workspace[]>([]) 
  const [currentWorkspaceId, setCurrentWorkspaceId] = useState<string | null>(null);
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);
  const [isSavingWorkspace, setIsSavingWorkspace] = useState(false);

  // Fetch workspaces on initial load to check if popup should be shown
  useEffect(() => {
    fetchWorkspaces().then(() => setInitialLoadComplete(true));
  }, [])

  // Listen for custom event to open workspace popup
  useEffect(() => {
    const handleOpenPopup = () => {
      handleNewWorkspace();
    };
    window.addEventListener('openWorkspacePopup', handleOpenPopup);
    return () => window.removeEventListener('openWorkspacePopup', handleOpenPopup);
  }, [])

  // Fetch workspaces when the workspaces window is opened
  useEffect(() => {
    if (open) {
      fetchWorkspaces()
    }
  }, [open])

  const fetchWorkspaces = async () => {
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
        console.log("Workspaces: ", result);
        if (Array.isArray(result)){
          const mappedWorkspaces = result.map((workspace: any) => ({
            id: workspace.id,
            name: workspace.name,
            desc: workspace.description,
            current: workspace.current || workspace.is_current || false
          }));
          setBackendWorkspaces(mappedWorkspaces);

          const currentWorkspace = mappedWorkspaces.find(w => w.current);
          if(currentWorkspace && currentWorkspace.id){
            setCurrentWorkspaceId(currentWorkspace.id);
          }
        }
      } 
    } catch (error) {
      console.error('Error fetching workspaces:', error);
    }
  };

  // Use workspaces from back end if available, otherwise use default
  const list = backendWorkspaces.length > 0 ? backendWorkspaces : 
               (workspaces && workspaces.length > 0) ? workspaces : 
               [{ id: 'default', name: 'Default workspace', desc: '', current: true }]


  // Edit an existing workspace
  const handleEdit = async (workspace: Workspace) => {
    setEditWorkspace({...workspace})
    setMenuOpen(null)
    try {
      // Fetch the workspace details including file paths from the backend
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": "workspace_query",
          "content": {
            "action": "open_workspace",
            "id": workspace.id
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Workspace details: ", result);
        
        // Extract file paths from the workspace data
        if (result.filepaths && Array.isArray(result.filepaths)) {
          const paths = result.filepaths.map((tuple: [string, boolean]) => tuple[0]);
          setFilePaths(paths);
        }
      }
    } catch (error) {
      console.error('Error fetching workspace details:', error);
      setFilePaths([]);
    }
  };

  // Create a new workspace
  const handleNewWorkspace = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": "workspace_query",
          "content": {
            "action": "gen_id",
            "name": "new_ws"
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        setEditWorkspace({ 
          id: result.id,
          name: "", 
          desc: ""
        });
        setFilePaths([]);
      }
    } catch (error) {
      console.error('Error generating ID:', error);
    }
  };

  // Remove a filepath from the list of a workspace's filepaths
  const removeFilePath = (index: number) => {
    setFilePaths(filePaths.filter((_, i) => i !== index))
  }

  // Update a workspace's name
  const updateWorkspaceName = (name: string) => {
    if (editWorkspace) {
      setEditWorkspace({...editWorkspace, name})
    }
  }

  // Update a workspace's description 
  const updateWorkspaceDescription =(desc: string) => {
    if(editWorkspace){
      setEditWorkspace({...editWorkspace, desc})
    }
  }

  // Save a new/edited workspace
  const saveWorkspace = async (): Promise<void> => {
    if (!editWorkspace) return;

    // True if the files should be preprocessed, false otherwise (all true for now)
    const filePathTuples = filePaths.map(path => [path, true]);
    // Set loading state
    setIsSavingWorkspace(true); 

    try {
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": "workspace_query",
          "content": {
            "action": "add_workspace",
            "data": {
              "description": editWorkspace.desc,
              "filepaths": filePathTuples,
              "id": editWorkspace["id"],
              "name": editWorkspace["name"]
            }
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Workspace saved: ", result);
        setEditWorkspace(null);
        setFilePaths([]);
        // Wait for workspaces to refresh
        await fetchWorkspaces(); 
      } else {
        throw new Error('Failed to save workspace');
      }
    } catch (error) {
      console.error('Error saving workspace:', error);
      throw error; 
    } finally {
      // Clear loading state
      setIsSavingWorkspace(false); 
    }
  };

  // Add new file paths to the workspace that is being edited 
  const addFilePath = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
          "type": "os_query", 
          "content":{
            "action": "ask_directory"
          }
          }),
        });

        if (response.ok) {
          const result = await response.json();
          console.log("Files: ", result);
          if (Array.isArray(result)) {
            setFilePaths([...filePaths, ...result]);
          }
        } 
      } catch (error) {
        console.error('Error adding directory:', error);
    }
  };

  // Select a workspace to be the current active workspace
  const handleWorkspaceSelect = async (workspace: Workspace) => {
    try {
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": "workspace_query",
          "content": {
            "action": "select_workspace",
            "id": workspace.id
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Workspace activated: ", result);

        if(workspace.id){
          setCurrentWorkspaceId(workspace.id);
        }

        onSelect?.(workspace);
        setOpen(false);
        fetchWorkspaces();
      }
    } catch (error) {
      console.error('Error activating workspace:', error);
    }
  };

  // Delete a workspace 
  const removeWorkspace = async (workspace: Workspace) => {
    if (!workspace.id) {
      console.error('Cannot remove workspace without ID');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          "type": "workspace_query",
          "content": {
            "action": "remove_workspace",
            "id": workspace.id
          }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        console.log("Workspace removed: ", result);
        
        // Close menu & update workspaces list
        setMenuOpen(null);
        fetchWorkspaces();
      }
    } catch (error) {
      console.error('Error removing workspace:', error);
    }
  };

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
            <div className="workspace-header">Workspaces</div>

            <div className="workspace-list">
              {list.map((w, idx) => (
                <div key={w.id || idx} className={`workspace-item ${w.current ? 'current' : ''}`} onClick={() => handleWorkspaceSelect(w)}>
                  <div className="workspace-avatar">👤</div>
                  <div className="workspace-body">
                    <div className="workspace-title">{w.name} {w.id == currentWorkspaceId && <span className="current-badge">Current</span>}</div>
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
                        <div className="menu-item" onClick={() => removeWorkspace(w)}>Remove</div>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="workspace-footer">
              {/* Button to add a new workspace */}
              <button className='new-workspace' onClick={handleNewWorkspace}> + New Workspace </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit workspace window */}
      <WorkspaceEditModal
        workspace={editWorkspace}
        filePaths={filePaths}
        onClose={() => {
          if (!isSavingWorkspace) {
            setEditWorkspace(null);
          }
        }}
        onSave={saveWorkspace}
        onUpdateName={updateWorkspaceName}
        onUpdateDescription={updateWorkspaceDescription}
        onRemoveFilePath={removeFilePath}
        onAddFilePath={addFilePath}
        allowClose={backendWorkspaces.length > 0}
      />
    </>
  )
}