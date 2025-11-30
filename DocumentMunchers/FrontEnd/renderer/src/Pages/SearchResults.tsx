import React, { useState, useEffect } from 'react'
import '../css/pages/SearchResults.css'
import SearchBox from '../Components/SearchBox'
import ListResultCard from '../Components/ListResultCard'
import GridResultCard from '../Components/GridResultCard'
import IconButton from '../Components/IconButton'
import { mockResults } from '../data/mockResults'

export type Result = {
  id: string
  title: string
  summary: string
  relevance: number
  lastOpened: string
  keywords?: string[]
}


export default function SearchResults({ query, results: externalResults, onResultsUpdate}: { query?: string, results?: Result[],
    onResultsUpdate?: (results: Result[]) => void})

  {
  // Results state: if `externalResults` prop is provided, use it.
  // Otherwise we'll fetch from an API (placeholder below) and fall back to mocks.
  console.log('SearchResults function called')
  console.log('External Results: ', externalResults)
  const [resultsState, setResultsState] = useState<Result[] | null>(
    externalResults !== undefined ? externalResults : null
  )
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // If parent passed results, use them and skip fetching
    if (externalResults !== undefined) {
      setResultsState(externalResults)
      return
    }

    // If the search bar previously stored results in sessionStorage, use them.
    // This is how SearchBox passes fetched results to this page without a global store.
    try {
      const raw = sessionStorage.getItem('latestSearchResults')
      if (raw) {
        const parsed = JSON.parse(raw)
        
        const currentQuery = query || ''
        const storedQuery = parsed.query || ''

        if(storedQuery == currentQuery){
          console.log("Parsed Results: ", parsed.results)
          setResultsState(parsed.results || [])
          sessionStorage.removeItem('latestSearchResults')
          return
        }
      }
      } catch (err) {
        // sessionStorage unavailable or JSON parse error - ignore and continue to fetch
        console.warn('Could not read cached search results', err)
    }

    // If there are not search results the program will display the mock search results
    setResultsState(null)
  }, [externalResults, query])


   // Handle new results that the SearchBox has received from the API
    const handleSearchResults = (newResults: Result[], searchQuery: string) => {
      setResultsState(newResults);
      // Notify the parent component about the update to the search results
      if (onResultsUpdate) {
        onResultsUpdate(newResults);
      }
      
      // Store the latest search results in sessionStorage so that they can be accessed later
      try {
        sessionStorage.setItem('latestSearchResults', JSON.stringify({
          query: searchQuery,
          results: newResults
        }));
      } catch (err) {
        console.warn('Could not store search results', err);
      }
    }

  // Show the fetched/external results unless the resultsState is null, in which case show mockResults
  /* 
   const results = externalResults && externalResults.length > 0
   ? externalResults : resultsState === null ? mockResults(query || '') 
   : resultsState || []
  */
  
   // Get the final results to display

  // /*
  const getDisplayResults = () => {
    console.log("External Results: ", externalResults)
    // if (externalResults !== undefined && externalResults.length > 0) {

    console.log("Results State: ", resultsState)
    if (externalResults !== undefined) {
      return externalResults
    }
    return resultsState || [];
    /*
    if (resultsState !== null){
      return resultsState || []
    }
    else{
      return mockResults(query || '')
    }
      */
  }
 // */
  const results = getDisplayResults();

  const [view, setView] = useState<'list' | 'grid'>('list');

 const hasSearchBeenAttempted = resultsState !== null || 
  (externalResults !== undefined)

  const hasNoResults = hasSearchBeenAttempted && (results.length === 0 || results[0].id == null);
  console.log("Has no results?", hasNoResults);
  console.log("Results: ", results);
  console.log("Results[0]: ", results[0]);

    return (
    <div className="results-root">
    <SearchBox initialValue={query || ''}
      onSearch={handleSearchResults}
    />
      
      {hasNoResults ? (
        // Error page when no results
        <div className="error-page">
          <h2>No search results found</h2>
          <p>Your search for "{query || ''}" did not return any results.</p>
          <p>Please try different keywords or check your spelling.</p>
        </div>
      ) : (
        // Display results when available
        <>
          <div className="results-header">
            <div className="results-query">Search results{query ? ` for "${query}"` : ''}</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              <div className="results-count">{results.length} results</div>
              <IconButton title={view === 'list' ? 'Switch to grid view' : 'Switch to list view'} onClick={() => setView((v) => (v === 'list' ? 'grid' : 'list'))}>
                {view === 'list' ? (
                  // grid icon
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
                    <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
                    <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
                    <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="#2E7D32" strokeWidth="1.6" />
                  </svg>
                ) : (
                  // list icon
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="4" y="5" width="16" height="2" rx="1" fill="#2E7D32" />
                    <rect x="4" y="11" width="16" height="2" rx="1" fill="#2E7D32" />
                    <rect x="4" y="17" width="16" height="2" rx="1" fill="#2E7D32" />
                  </svg>
                )}
              </IconButton>
            </div>
          </div>

          {view === 'list' ? (
            <div className="results-list">
              {results.map((r) => (
                <ListResultCard key={r.id} title={r.title} summary={r.summary} relevance={r.relevance} lastOpened={r.lastOpened} onClick={() => handleResultClick(r)} />
              ))}
            </div>
          ) : (
            <div className="results-grid">
              {results.map((r) => (
                <GridResultCard key={r.id} title={r.title} summary={r.summary} relevance={r.relevance} lastOpened={r.lastOpened} keywords={r.keywords} onClick={() => handleResultClick(r)} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

// Handle clicks on list results or grid results 
const handleResultClick = async (result: Result) => {
  console.log('Clicked result:', result);
  // Send click data to Flask backend
  await sendClickToBackend(result);
}

// Let the back end know that the user is trying to open a file
// Query format: {"type":"os_query", "content":{"action":"open", "filepath": "/path/to/file"}}
const sendClickToBackend = async (result: Result) => {
  try {
    const response = await fetch('http://localhost:5000/api/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "type":"os_query",
        "content":{
            "action":"open", 
            "filepath":result.title
          }
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
  } catch (error) {
    console.error('Error sending click to backend:', error);
  }
};