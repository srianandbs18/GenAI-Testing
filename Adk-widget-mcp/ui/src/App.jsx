import React from 'react';
import { useWebSocket } from './hooks/useWebSocket';
import { WidgetRenderer } from './components/WidgetRenderer';
import './index.css';
import './App.css';

function App() {
  const { isConnected, widget, message, sendMessage } = useWebSocket();

  const handleAction = (action, data = {}) => {
    sendMessage(action, data);
  };

  return (
    <div className="app">
      <div className="connection-indicator">
        <div className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></div>
        <span>{isConnected ? 'Connected to ADK' : 'Disconnected'}</span>
      </div>

      {message && (
        <div className={`message-banner ${message.type}`}>
          {message.text}
        </div>
      )}

      <WidgetRenderer widget={widget} onAction={handleAction} />
    </div>
  );
}

export default App;
