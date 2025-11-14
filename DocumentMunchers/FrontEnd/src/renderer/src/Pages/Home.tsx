import React from 'react'
import SearchBox from '../Components/SearchBox'
import { Result } from './SearchResults';

export default function Home() {
  const handleSearch = (results: Result[], q: string) => {
    const encoded = encodeURIComponent(q || '')

    try{
      sessionStorage.setItem('latestSearchResults', JSON.stringify(
        { 
          query: q, 
          results: results
        }));
    } catch (error){
      console.warn('Could not store search results', error);
    }
    window.location.hash = `#/results?q=${encoded}`
  }

  return <SearchBox onSearch={handleSearch} autoFocus />
}
