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
        <div className="pdf-icon">📄</div>
        {typeof relevance === 'number' && (
          <div className="relevance-pill">{relevance}% Relevant</div>
        )}
      </div>

      <div className="grid-title">{title.split('/')[title.split('/').length - 1]}</div>

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
