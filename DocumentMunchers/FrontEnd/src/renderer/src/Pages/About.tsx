import React from 'react'
import '../css/pages/About.css'

export default function About() {
  return (
    <div className="about-container">
      <h1 className="about-title">About our software</h1>

      <div className="about-body">
        <p>
          Hello! We're a small, non-profit team dedicated to building simple,
           secure software you can trust. Our program changes how you find
            files by using a smart AI to search. Instead of just matching 
            keywords, it understands what your files are actually about—think
             of it like searching based on meaning, not just words.
        </p>

        <p>
          Getting started is easy: you simply tell the software which folders
           to look in, and it will never look anywhere else.
            That's why you don't have to worry about security or privacy: because the entire program runs only on your computer, all the searching and all the AI's "thinking" stays right there with you.
        </p>

        <p>
          Nothing ever leaves your computer or gets sent to us or anyone else. Your information is 100% private and secure.
        </p>
      </div>
    </div>
  )
}
