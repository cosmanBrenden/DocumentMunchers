import React, { useState } from 'react'

import '../css/components/WorkspacePopUp.css'

type Workspace = {
  id?: string
  name: string
  desc?: string
  current?: boolean
}

type WorkspaceEditModalProps = {
  workspace: Workspace | null
  filePaths: string[]
  onClose: () => void
  onSave: () => Promise<void>
  onUpdateName: (name: string) => void
  onUpdateDescription: (desc: string) => void
  onRemoveFilePath: (index: number) => void
  onAddFilePath: () => void 
  allowClose?: boolean
}



export default function WorkspaceEditModal({
  workspace,
  filePaths,
  onClose,
  onSave,
  onUpdateName,
  onUpdateDescription,
  onRemoveFilePath,
  onAddFilePath,
  allowClose = true
}: WorkspaceEditModalProps) {
  const[isSaving, setIsSaving] = useState(false)
  const [isSelecting, setIsSelecting] = useState(false)
  if (!workspace) return null

  const handleBackdropClick = () => {
    if (allowClose && !isSaving) {
      onClose();
    }
  };

  const handleCloseClick = () => {
    if (allowClose && !isSaving) {
      onClose();
    }
  };

  const handleSaveClick = async () => {
    if (isSaving) return;
    
    setIsSaving(true);
    try {
      await onSave();
    } catch (error) {
      console.error('Error saving workspace:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleRemoveFilePath = (index: number) => {
    if (!isSaving) {
      onRemoveFilePath(index);
    }
  };

  ///*
  const handleAddFilePath = () => {
    if (!isSaving) {
      onAddFilePath();
    }
  };

  const handleUpdateName = (name: string) => {
    if (!isSaving) {
      onUpdateName(name);
    }
  };

  const handleUpdateDescription = (desc: string) => {
    if (!isSaving) {
      onUpdateDescription(desc);
    }
  };


 return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="edit-panel" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
        {/* Loading Overlay */}
        {isSaving && (
          <div className="saving-overlay">
            <div className="saving-spinner">
              <img src={"/logo-no-text.png"} alt="" />
            </div>
            <div className="saving-text">Preprocessing workspace files...</div>
          </div>
        )}
        
        <div className="edit-workspace-header">
          {allowClose && (
            <button 
              className="close-button" 
              onClick={handleCloseClick}
              disabled={isSaving}
            >
              ×
            </button>
          )}
        </div>
        <div className="edit-workspace-title">
          Workspace Editor
        </div>
        <div className="edit-name">
            Name
            <input
              type="text"
              value={workspace.name}
              onChange={(e) => handleUpdateName(e.target.value)}
              className="workspace-name-input"
              placeholder="enter a workspace name..."
              disabled={isSaving}
            />
        </div>
        <div className="edit-description">
            Description
            <input
              type="text"
              value={workspace.desc}
              onChange={(e) => handleUpdateDescription(e.target.value)}
              className="workspace-description-input"
              placeholder="enter a workspace description..."
              disabled={isSaving}
            />
        </div>
        <div className="modal-content">
          <div className="file-paths-section">
            <div className="files-text">
              Workspace Files
            </div>
            <div className="file-paths-list">
              {filePaths.map((path, index) => (
                <div key={index} className="file-path-item">
                  <span className="path-text">{path}</span>
                  <button 
                    className="remove-path"
                    onClick={() => handleRemoveFilePath(index)}
                    disabled={isSaving}
                  >
                    ×
                  </button>
                </div>
              ))}
              {filePaths.length === 0 && (
                <div className="no-paths">No files added yet</div>
              )}
            </div>

            <div className="add-path">
              <button 
                onClick={handleAddFilePath} 
                disabled={isSaving}
              >
                Add Files...
              </button>
            </div>
          </div>
        </div>
        
        <div className="modal-footer">
          {allowClose && (
            <button 
              className="cancel-button" 
              onClick={handleCloseClick}
              disabled={isSaving}
            >
              Cancel
            </button>
          )}
          <button 
            className="save-button" 
            onClick={handleSaveClick}
            disabled={isSaving}
          >
            {isSaving ? (
              <>
                <span className="save-spinner"></span>
              </>
            ) : (
              'Save Changes'
            )}
          </button>
        </div>
      </div>
    </div>
  )
}