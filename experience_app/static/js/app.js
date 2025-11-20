/**
 * Experience Voice Chat App
 * Handles microphone recording, WebSocket streaming, and UI state management.
 */

import { AudioRecorder } from './audio-recorder.js';

// State
const state = {
  isRecording: false,
  isProcessing: false,
  isSpeaking: false,
  sessionId: ensureSession(),
  websocket: null,
  audioPlayerNode: null,
  recorder: new AudioRecorder(),
};

// UI Elements
const ui = {
  chatHistory: document.getElementById('chatHistory'),
  statusIndicator: document.getElementById('statusIndicator'),
  micButton: document.getElementById('micButton'),
  textForm: document.getElementById('textForm'),
  textInput: document.getElementById('textInput'),
  sessionIdDisplay: document.getElementById('sessionIdDisplay'),
};

// Initialize
function init() {
  if (ui.sessionIdDisplay) ui.sessionIdDisplay.textContent = state.sessionId;

  // Setup WebSocket
  connectWebsocket();

  // Setup Audio Player (on first click)
  document.addEventListener('click', initAudioContext, { once: true });

  // Mic Button Handler
  ui.micButton.addEventListener('click', toggleRecording);

  // Text Form Handler
  ui.textForm.addEventListener('submit', handleTextSubmit);
}

function ensureSession() {
  let sid = localStorage.getItem('experience_session_id');
  if (!sid) {
    sid = `sess-${Math.random().toString(36).substring(7)}`;
    localStorage.setItem('experience_session_id', sid);
  }
  return sid;
}

async function initAudioContext() {
  if (state.audioPlayerNode) return;
  try {
    const { startAudioPlayerWorklet } = await import('./audio-player.js');
    const [node, ctx] = await startAudioPlayerWorklet();
    state.audioPlayerNode = node;
    console.log("Audio player initialized");
  } catch (e) {
    console.error("Failed to init audio player", e);
  }
}

// WebSocket Logic
function connectWebsocket() {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const url = `${protocol}://${window.location.host}/experience/ws/${state.sessionId}?response_modality=audio`;

  state.websocket = new WebSocket(url);

  state.websocket.onopen = () => {
    console.log("Connected to WebSocket");
    updateStatus("Idle");
  };

  state.websocket.onmessage = async (event) => {
    const msg = JSON.parse(event.data);

    if (msg.mime_type === "text/plain") {
      // Append to chat history
      if (msg.data && !msg.data.startsWith("[experience]")) {
        appendMessage("bot", msg.data);
        updateStatus("Idle"); // Clear processing status
      }
    } else if (msg.mime_type === "audio/pcm") {
      // Play audio
      playAudio(msg.data);
    }
  };

  state.websocket.onclose = () => {
    console.log("WebSocket closed, reconnecting in 2s...");
    setTimeout(connectWebsocket, 2000);
  };
}

// Recording Logic
async function toggleRecording() {
  if (state.isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
}

async function startRecording() {
  if (state.isSpeaking) {
    // Ideally stop speaking
  }

  const started = await state.recorder.start();
  if (started) {
    state.isRecording = true;
    ui.micButton.classList.add('active');
    updateStatus("Listening...");
  }
}

async function stopRecording() {
  if (!state.isRecording) return;

  state.isRecording = false;
  ui.micButton.classList.remove('active');
  updateStatus("Thinking...");

  const pcmData = state.recorder.stop();

  // Send to backend
  if (state.websocket && state.websocket.readyState === WebSocket.OPEN) {
    const base64Audio = AudioRecorder.toBase64(pcmData);
    state.websocket.send(JSON.stringify({
      mime_type: "audio/pcm",
      data: base64Audio,
      response_modality: "audio"
    }));
  } else {
    console.error("WebSocket not connected");
    updateStatus("Error: Not Connected");
  }
}

// Text Handling
function handleTextSubmit(e) {
  e.preventDefault();
  const text = ui.textInput.value.trim();
  if (!text) return;

  if (state.websocket && state.websocket.readyState === WebSocket.OPEN) {
    // Send text
    state.websocket.send(JSON.stringify({
      mime_type: "text/plain",
      data: text,
      response_modality: "audio"
    }));

    appendMessage("user", text);
    ui.textInput.value = "";
    updateStatus("Thinking...");
  } else {
    console.error("WebSocket not connected");
  }
}

function appendMessage(sender, text) {
  const div = document.createElement('div');
  div.className = `message ${sender}`;
  div.textContent = text;
  ui.chatHistory.appendChild(div);
  ui.chatHistory.scrollTop = ui.chatHistory.scrollHeight;
}

function updateStatus(text) {
  if (text === "Idle") {
    ui.statusIndicator.classList.remove('visible');
  } else {
    ui.statusIndicator.textContent = text;
    ui.statusIndicator.classList.add('visible');
  }
}

// Audio Playback
function playAudio(base64Data) {
  if (!state.audioPlayerNode) return;

  state.isSpeaking = true;

  const binaryString = window.atob(base64Data);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  const int16Data = new Int16Array(bytes.buffer);

  state.audioPlayerNode.port.postMessage(int16Data);

  const durationSec = int16Data.length / 24000;
  setTimeout(() => {
    state.isSpeaking = false;
  }, durationSec * 1000 + 500);
}

// Start
init();
