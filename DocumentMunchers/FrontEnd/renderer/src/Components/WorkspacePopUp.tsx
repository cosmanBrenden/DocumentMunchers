import React from 'react'

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
  onSave: () => void
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
  if (!workspace) return null

  const handleBackdropClick = () => {
    if (allowClose) {
      onClose();
    }
  };

  const handleCloseClick = () => {
    if (allowClose) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="edit-modal" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h3>
            Workspace Name
            <input
              type="text"
              value={workspace.name}
              onChange={(e) => onUpdateName(e.target.value)}
              className="workspace-name-input"
              placeholder="Workspace Name"
            />
          </h3>
          {allowClose && <button className="close-button" onClick={handleCloseClick}>×</button>}
        </div>
        <div className="modal-content">
          <h4>
            Description
            <input
              type="text"
              value={workspace.desc}
              onChange={(e) => onUpdateDescription(e.target.value)}
              className="workspace-description-input"
            />
          </h4>
          <div className="file-paths-section">
            <h4>Workspace Files</h4>
            <div className="file-paths-list">
              {filePaths.map((path, index) => (
                <div key={index} className="file-path-item">
                  <span className="path-text">{path}</span>
                  <button 
                    className="remove-path"
                    onClick={() => onRemoveFilePath(index)}
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
              <button onClick={onAddFilePath}>Add Files...</button>
            </div>
          </div>
        </div>
        
        <div className="modal-footer">
          {allowClose && (
            <button className="cancel-button" onClick={handleCloseClick}>
              Cancel
            </button>
          )}
          <button className="save-button" onClick={onSave}>
            Save Changes
          </button>
        </div>
      </div>
    </div>
  )
}
