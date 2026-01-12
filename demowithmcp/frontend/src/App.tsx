import React from 'react'
import Chatbot from './components/Chatbot'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🏦 Banking Demo with MCP</h1>
        <p>Dynamic UI powered by Google ADK Agent + MCP Server</p>
      </header>
      <main className="app-main">
        <Chatbot />
      </main>
    </div>
  )
}

export default App

