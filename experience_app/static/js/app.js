/**
 * Experience API WebSocket Chat Handler
 * Based on the original adk-streaming-ws app pattern
 */

// WebSocket connection
let websocket = null;
let currentMessageId = null;

// Audio playback
let audioPlayerNode = null;
let audioPlayerContext = null;

// Get DOM elements - cache them but also use direct access in handlers
const messageForm = document.getElementById("messageForm");
const messageInput = document.getElementById("messageInput");
const messagesDiv = document.getElementById("messages");
const wsConnect = document.getElementById("wsConnect");
const wsModality = document.getElementById("wsModality");
const sessionInput = document.getElementById("sessionId");

// REST form elements
const textForm = document.getElementById("textForm");
const textInput = document.getElementById("textInput");
const textModality = document.getElementById("textModality");
const textResponse = document.getElementById("textResponse");
const audioForm = document.getElementById("audioForm");
const audioInput = document.getElementById("audioInput");
const audioModality = document.getElementById("audioModality");
const audioResponse = document.getElementById("audioResponse");

function ensureSession() {
  const sessionIdEl = document.getElementById("sessionId");
  const current = sessionIdEl ? sessionIdEl.value.trim() : "";
  if (current.length > 0) {
    return current;
  }
  const generated = `session-${Math.random().toString(36).substring(7)}`;
  if (sessionIdEl) {
    sessionIdEl.value = generated;
  }
  return generated;
}

function wsUrl(sessionId, modality) {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://${window.location.host}/experience/ws/${encodeURIComponent(
    sessionId
  )}?response_modality=${encodeURIComponent(modality)}`;
}

function addMessage(text, isUser = false) {
  const messagesDiv = document.getElementById("messages");
  if (!messagesDiv) return;
  
  const p = document.createElement("p");
  p.className = isUser ? "user" : "assistant";
  p.textContent = text;
  messagesDiv.appendChild(p);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
  return p;
}

function clearMessages() {
  const messagesDiv = document.getElementById("messages");
  if (messagesDiv) {
    messagesDiv.innerHTML = "";
  }
}

// WebSocket connection handler - matches original app pattern
function connectWebsocket() {
  const sessionId = ensureSession();
  const modalityEl = document.getElementById("wsModality");
  const modality = modalityEl ? modalityEl.value : "text";
  const url = wsUrl(sessionId, modality);
  
  console.log("Connecting to:", url);
  
  if (websocket) {
    websocket.close();
    websocket = null;
  }
  
  clearMessages();
  addMessage("Connecting...", false);
  
  const connectBtn = document.getElementById("wsConnect");
  if (connectBtn) {
    connectBtn.disabled = true;
  }
  
  websocket = new WebSocket(url);
  
  // Handle connection open - use direct element access like original
  websocket.onopen = function () {
    console.log("WebSocket connection opened.");
    const messagesDiv = document.getElementById("messages");
    if (messagesDiv) {
      messagesDiv.innerHTML = "";
      addMessage("Connected! You can start chatting.", false);
    }
    
    // Enable the Send button - direct access like original
    const sendButton = document.getElementById("sendButton");
    if (sendButton) {
      sendButton.disabled = false;
    }
    
    // Update connect button
    const connectBtn = document.getElementById("wsConnect");
    if (connectBtn) {
      connectBtn.textContent = "Disconnect";
      connectBtn.disabled = false;
    }
    
    addSubmitHandler();
  };
  
  // Handle incoming messages - matches original pattern
  websocket.onmessage = function (event) {
    try {
      const message = JSON.parse(event.data);
      console.log("[SERVER TO CLIENT]", message);
      
      // Handle system/connection messages
      if (message.metadata && message.metadata.type === "connection") {
        // Connection confirmed - UI already updated in onopen
        return;
      }
      
      // Handle text responses - stream them like original
      if (message.mime_type === "text/plain" && message.data) {
        const messagesDiv = document.getElementById("messages");
        if (!messagesDiv) return;
        
        let text = message.data;
        // Remove any prefixes if present
        if (text.startsWith("[experience] ")) {
          text = text.substring(13);
        }
        
        // Add a new message for a new turn (like original)
        if (currentMessageId == null) {
          currentMessageId = Math.random().toString(36).substring(7);
          const messageEl = document.createElement("p");
          messageEl.id = currentMessageId;
          messageEl.className = "assistant";
          messagesDiv.appendChild(messageEl);
        }
        
        // Add message text to the existing message element (like original)
        const messageEl = document.getElementById(currentMessageId);
        if (messageEl) {
          messageEl.textContent += text;
        }
        
        // Scroll down to the bottom
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }
      
      // Handle audio responses - play them
      if (message.mime_type === "audio/pcm" && message.data) {
        console.log("[AUDIO] Received audio data, base64 length:", message.data.length);
        if (audioPlayerNode) {
          try {
            // Decode Base64 to ArrayBuffer, then convert to Int16Array
            const arrayBuffer = base64ToArray(message.data);
            const int16Array = new Int16Array(arrayBuffer);
            audioPlayerNode.port.postMessage(int16Array);
            console.log("[AUDIO] Playing audio chunk, samples:", int16Array.length);
            addMessage(`[Playing audio: ${int16Array.length} samples]`, false);
          } catch (e) {
            console.error("[AUDIO] Error playing audio:", e);
            addMessage("[Audio playback error: " + e.message + "]", false);
          }
        } else {
          console.log("[AUDIO] Audio player not initialized, initializing...");
          addMessage("[Initializing audio player...]", false);
          initAudioPlayer().then(() => {
            if (audioPlayerNode && message.data) {
              const arrayBuffer = base64ToArray(message.data);
              const int16Array = new Int16Array(arrayBuffer);
              audioPlayerNode.port.postMessage(int16Array);
              console.log("[AUDIO] Playing audio after initialization");
            }
          });
        }
      }
    } catch (e) {
      console.error("Error parsing message:", e, event.data);
    }
  };
  
  // Handle connection close - matches original pattern
  websocket.onclose = function () {
    console.log("WebSocket connection closed.");
    const sendButton = document.getElementById("sendButton");
    if (sendButton) {
      sendButton.disabled = true;
    }
    
    const connectBtn = document.getElementById("wsConnect");
    if (connectBtn) {
      connectBtn.textContent = "Connect";
      connectBtn.disabled = false;
    }
    
    addMessage("Connection closed.", false);
    currentMessageId = null;
  };
  
  websocket.onerror = function (e) {
    console.log("WebSocket error: ", e);
    const connectBtn = document.getElementById("wsConnect");
    if (connectBtn) {
      connectBtn.disabled = false;
      connectBtn.textContent = "Connect";
    }
    addMessage("Connection error occurred.", false);
  };
}

// Add submit handler to the form - matches original pattern
function addSubmitHandler() {
  const messageForm = document.getElementById("messageForm");
  const messageInput = document.getElementById("messageInput");
  
  if (!messageForm || !messageInput) return;
  
  messageForm.onsubmit = function (e) {
    e.preventDefault();
    const message = messageInput.value;
    if (message && websocket && websocket.readyState === WebSocket.OPEN) {
      const p = document.createElement("p");
      p.className = "user";
      p.textContent = message;
      const messagesDiv = document.getElementById("messages");
      if (messagesDiv) {
        messagesDiv.appendChild(p);
      }
      messageInput.value = "";
      
      // Reset for new assistant response
      currentMessageId = null;
      
      sendMessage({
        mime_type: "text/plain",
        data: message,
      });
      console.log("[CLIENT TO SERVER] " + message);
    }
    return false;
  };
}

// Send a message to the server as a JSON string - matches original
function sendMessage(message) {
  if (websocket && websocket.readyState == WebSocket.OPEN) {
    const messageJson = JSON.stringify(message);
    websocket.send(messageJson);
  }
}

// Decode Base64 data to ArrayBuffer (for audio)
function base64ToArray(base64) {
  const binaryString = window.atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}

// Initialize audio player
async function initAudioPlayer() {
  try {
    console.log("[AUDIO] Initializing audio player...");
    // Dynamic import for audio player module
    const { startAudioPlayerWorklet } = await import('./audio-player.js');
    const [node, ctx] = await startAudioPlayerWorklet();
    audioPlayerNode = node;
    audioPlayerContext = ctx;
    console.log("[AUDIO] Audio player initialized successfully");
    return true;
  } catch (error) {
    console.error("[AUDIO] Failed to initialize audio player:", error);
    addMessage("[Audio player initialization failed]", false);
    return false;
  }
}

// Initialize audio player when page loads (user gesture required)
document.addEventListener('click', function initAudioOnClick() {
  if (!audioPlayerNode) {
    initAudioPlayer();
    // Remove listener after first click
    document.removeEventListener('click', initAudioOnClick);
  }
}, { once: true });

// Connect/disconnect button handler
if (wsConnect) {
  wsConnect.addEventListener("click", function (e) {
    e.preventDefault();
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.close();
      websocket = null;
    } else {
      connectWebsocket();
    }
  });
}

// REST form handlers
function render(target, payload) {
  if (target) {
    target.textContent = JSON.stringify(payload, null, 2);
  }
}

async function sendJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function toBase64(value) {
  const trimmed = value.trim();
  const base64Regex = /^[A-Za-z0-9+/=]+$/;
  if (trimmed.length > 0 && trimmed.length % 4 === 0 && base64Regex.test(trimmed)) {
    return trimmed;
  }
  return window.btoa(unescape(encodeURIComponent(value || "dummy audio")));
}

if (textForm && textInput && textModality && textResponse) {
  textForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const sessionId = ensureSession();
    try {
      const payload = await sendJson("/experience/v1/messages:text", {
        session_id: sessionId,
        text: textInput.value,
        response_modality: textModality.value,
      });
      render(textResponse, payload);
    } catch (error) {
      render(textResponse, { error: error.message });
    }
  });
}

if (audioForm && audioInput && audioModality && audioResponse) {
  audioForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const sessionId = ensureSession();
    try {
      const payload = await sendJson("/experience/v1/messages:audio", {
        session_id: sessionId,
        audio_base64: toBase64(audioInput.value),
        response_modality: audioModality.value,
      });
      render(audioResponse, payload);
    } catch (error) {
      render(audioResponse, { error: error.message });
    }
  });
}
