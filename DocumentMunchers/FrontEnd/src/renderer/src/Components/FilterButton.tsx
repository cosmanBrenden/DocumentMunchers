import React, { useState } from 'react'
import IconButton from './IconButton'
import '../css/components/FilterButton.css'

export default function FilterButton() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <IconButton title="Filter" onClick={() => setOpen(v => !v)}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M3 5h18M6 12h12M10 19h4" stroke="#2E7D32" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </IconButton>

      {open && (
        <div className="modal-backdrop" onClick={() => setOpen(false)}>
          <div className="modal" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
            <button className="modal-close" aria-label="Close" onClick={() => setOpen(false)}>×</button>
            <h2 className="modal-title">Advanced Searching Settings</h2>

            <section className="modal-section">
              <label className="section-label">Date</label>
              <div className="date-row">
                <input className="date-input" type="date" />
                <div className="date-sep">~</div>
                <input className="date-input" type="date" />
              </div>
            </section>

            <section className="modal-section">
              <label className="section-label">File Types</label>
              <div className="filetypes-grid">
                <label className="ft"><input type="checkbox" defaultChecked /> .pdf</label>
                <label className="ft"><input type="checkbox" /> .docs</label>
                <label className="ft"><input type="checkbox" /> .xlsx</label>
                <label className="ft"><input type="checkbox" defaultChecked /> .csv</label>
                <label className="ft"><input type="checkbox" /> .pptx</label>
                <label className="ft"><input type="checkbox" /> .jpg / .jpeg / .png</label>
              </div>
            </section>

            <div style={{display:'flex',justifyContent:'center',marginTop:20}}>
              <button className="apply-btn" onClick={() => setOpen(false)}>Apply</button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
