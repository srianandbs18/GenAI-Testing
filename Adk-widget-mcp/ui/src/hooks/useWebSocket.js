import { useState, useEffect, useRef } from 'react';

const WS_URL = 'ws://localhost:8000';

export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false);
  const [widget, setWidget] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [message, setMessage] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('✅ Connected to ADK server');
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('📨 Received:', data);

          if (data.type === 'widget_render') {
            setWidget(data.widget);
            setSessionId(data.session_id);
          } else if (data.type === 'meeting_scheduled') {
            setMessage({
              type: 'success',
              text: data.message
            });
            setTimeout(() => setMessage(null), 3000);
          } else if (data.type === 'closed') {
            setMessage({
              type: 'info',
              text: data.message
            });
          }
        } catch (error) {
          console.error('❌ Error parsing message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log('❌ Disconnected from ADK server');
        setIsConnected(false);
        
        // Reconnect after 3 seconds
        setTimeout(() => {
          console.log('🔄 Reconnecting...');
          connectWebSocket();
        }, 3000);
      };
    } catch (error) {
      console.error('❌ WebSocket connection error:', error);
    }
  };

  const sendMessage = (action, data = {}) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      const message = {
        action,
        session_id: sessionId,
        ...data
      };
      console.log('📤 Sending:', message);
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return {
    isConnected,
    widget,
    sessionId,
    message,
    sendMessage
  };
}
