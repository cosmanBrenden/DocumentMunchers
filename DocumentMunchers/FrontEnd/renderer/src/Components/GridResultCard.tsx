import React from 'react'
import '../css/components/GridResultCard.css'

type Props = {
  title: string
  summary?: string
  keywords?: string[]
  relevance?: number
  lastOpened?: string
  onClick?: () => void
}

export default function GridResultCard({ title, summary, keywords, relevance, lastOpened, onClick }: Props) {
  return (
    <div className="grid-result-card"
          onClick={onClick}
          style={{ cursor: onClick ? 'pointer' : 'default'}}
    >
      <div className="grid-top">
        <div className="pdf-icon" aria-hidden>
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="14" height="18" rx="2" stroke="#000" strokeWidth="1.6" fill="none" />
            <text x="5" y="15" fontSize="6" fill="#000">PDF</text>
          </svg>
        </div>
        {typeof relevance === 'number' && (
          <div className="relevance-pill">{relevance}% Relevant</div>
        )}
      </div>

      <div className="grid-title">{title.split(/[\\/]/).pop()}</div>

      {keywords && keywords.length > 0 ? (
        <div className="grid-keywords">
          <div className="kw-label">Keywords by AI:</div>
          <ul>
            {keywords.map((k, i) => (
              <li key={i}>{k}</li>
            ))}
          </ul>
        </div>
      ) : (
        summary && <div className="grid-summary">{summary}</div>
      )}

      {lastOpened && <div className="grid-last">Last opened: {lastOpened}</div>}
    </div>
  )
}
