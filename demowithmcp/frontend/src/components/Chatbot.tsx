import React, { useState, useEffect, useRef } from 'react'
import A2UIRenderer from './A2UIRenderer'
import './Chatbot.css'

interface Message {
  id: number
  type: 'user' | 'bot'
  text: string
  a2ui?: any
  timestamp: Date
}

const AGENT_URL = 'http://localhost:8001'

function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Welcome message
    setMessages([{
      id: 0,
      type: 'bot',
      text: 'Hello! I\'m your banking assistant. I can help you with:\n\n• View account summary\n• Make deposits\n• Process withdrawals\n\nWhat would you like to do?',
      timestamp: new Date()
    }])
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSend = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      text: inputText.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    const prompt = inputText.trim()
    setInputText('')
    setIsLoading(true)

    try {
      const response = await fetch(`${AGENT_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: prompt })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      const botMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: data.text || 'Here is the widget:',
        a2ui: data.a2ui,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error: any) {
      console.error('Error communicating with agent:', error)
      const errorMessage: Message = {
        id: Date.now() + 1,
        type: 'bot',
        text: `Sorry, I encountered an error. ${error.message || 'Please make sure the agent is running on http://localhost:8001'}`,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chatbot">
      <div className="chatbot-messages">
        {messages.map((message) => (
          <div key={message.id} className={`message message-${message.type}`}>
            <div className="message-content">
              {message.type === 'user' ? (
                <div className="message-text">{message.text}</div>
              ) : (
                <>
                  {message.text && (
                    <div className="message-text">{message.text}</div>
                  )}
                  {message.a2ui && (
                    <div className="a2ui-container">
                      <A2UIRenderer message={message.a2ui} />
                    </div>
                  )}
                </>
              )}
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message message-bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about your account, make a deposit, or withdrawal..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading || !inputText.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

export default Chatbot

