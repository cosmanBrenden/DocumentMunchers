import React from 'react'
import '../css/components/LoadingScreen.css'

// Loading screen for when the program is starting up and the front end is waiting on the back end
const LoadingScreen = ({ message = 'Starting up...' }) => {
  return (
    <div className="loading-screen">
      <div className="loading-content">
        <div className="loading-icon">
          <img src={"/logo-no-text.png"} alt="" />
        </div>
        <p className="loading-message">{message}</p>
        <div className="loading-progress-container">
          <div className="loading-progress-bar"></div>
        </div>
      </div>
    </div>
  )
}

export default LoadingScreen