import React from 'react'
import '../css/components/ListResultCard.css'

type Props = {
  title: string
  summary: string
  relevance: number
  lastOpened: string
  onClick?: () => void
}

export default function ListResultCard({ title, summary, relevance, lastOpened, onClick }: Props) {
  return (
    <div className="result-card"
         onClick={onClick}
         style={{ cursor: onClick ? 'pointer' : 'default'}}
    >
      <div className="result-left">
        <div className="pdf-icon" aria-hidden>
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="14" height="18" rx="2" stroke="#000" strokeWidth="1.6" fill="none" />
            <path d="M17 7v-4l4 4" stroke="#000" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
            <text x="6" y="18" fontSize="8" fill="#000">PDF</text>
          </svg>
        </div>
      </div>

      <div className="result-body">
        <div className="result-top">
          <h3 className="result-title">{title.split('/')[title.split('/').length - 1]}</h3>
          <div className="relevance-pill">{relevance}% Relevant</div>
        </div>

        <div className="result-summary">
          <strong>AI Summary:</strong>
          <div className="summary-text">{summary}</div>
        </div>

        <div className="result-meta">Last opened: {lastOpened}</div>
      </div>
    </div>
  )
}
