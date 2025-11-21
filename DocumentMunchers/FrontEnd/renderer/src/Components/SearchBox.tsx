import React, { useState } from 'react'
import { Result } from '../Pages/SearchResults';

type Props = {
  placeholder?: string
  autoFocus?: boolean
  onSearch?:(results: Result[], q: string) => void;
  initialValue?: string
}

export default function SearchBox({ placeholder, autoFocus, onSearch, initialValue }: Props) {
  const [q, setQ] = useState(initialValue || '')
  // update local state when initialValue changes
  React.useEffect(() => {
    if (typeof initialValue === 'string') setQ(initialValue)
  }, [initialValue])

  const submit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    const val = q.trim()
    if (onSearch) {
    try {
        const baseUrl = 'http://localhost:5000/api/data';
        const searchData = {
          "type":"search_query",
          "content":{
          "action":"search",
          "query":val.trim()
          }
        };

        const response = await fetch(baseUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchData)
        });

        if(!response.ok){
            throw new Error('SearchBox threw HTTP error, status: ${response.status}');
        }

        const results: Result[] = await response.json();
        console.log('Response Data: ', results, '\n')
        // onSearch(results, val);
        
        // Save into sessionStorage so the results page can pick them up
        try {
            sessionStorage.setItem('latestSearchResults',JSON.stringify(results));
            console.log('JSON Results: ', JSON.stringify(results), '\n');
        } catch (err) {
          // sessionStorage may be unavailable in some contexts; ignore silently
          console.warn('Could not save search results to sessionStorage', err)
        }

        onSearch(results, val);
        
      } catch (err) {
        console.error('Search failed', err)
      } finally {
        // navigate to results page (include query in hash)
        const encoded = encodeURIComponent(val)
        window.location.hash = `#/results?q=${encoded}`
      }
    }
  }

  


  return (
    <div className="search-row">
      <form className="search-box" onSubmit={submit} role="search">
        <input
          className="search-input"
          placeholder={placeholder || 'Type keyword or context of the file that you are looking for!'}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          aria-label="Search"
          autoFocus={autoFocus}
        />

        <button className="search-action" aria-label="Search" type="submit" onClick={(e) => submit(e)}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 6l6 6-6 6" stroke="#2E7D32" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      </form>
    </div>
  )
}
