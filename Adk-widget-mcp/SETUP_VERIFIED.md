# ✅ READY TO RUN - Verified Setup

## What This Is

A **working demo** of an ADK agent with MCP widgets for meeting scheduling.

---

## Architecture

```
React UI (3000) ←→ WebSocket ←→ ADK + Gemini (8000) ←→ MCP Server (8001)
```

- **MCP Server**: Provides widget schemas (structure only)
- **ADK Agent**: Uses Gemini to fetch schemas, populates with data
- **React UI**: Renders widgets dynamically

---

## Verified Components

### ✅ MCP Server (`mcp-server/`)
- `main.py` - FastMCP server
- `schemas/` - Widget definitions
- **Works**: Returns widget schemas

### ✅ ADK Server (`adk/`)
- `main.py` - WebSocket server
- `src/adk_agent.py` - Gemini agent with function calling
- `src/session_manager.py` - In-memory sessions
- `src/mcp_client.py` - MCP communication
- `src/widget_populator.py` - Data population
- **Works**: With or without API key (fallback mode)

### ✅ React UI (`ui/`)
- `src/App.jsx` - Main app
- `src/components/` - Widget renderers
- `src/hooks/useWebSocket.js` - WebSocket connection
- **Works**: Dynamic rendering

---

## Installation (One-Time)

```bash
# MCP Server
cd mcp-server
pip install -r requirements.txt
cd ..

# ADK Server  
cd adk
pip install -r requirements.txt
cd ..

# UI
cd ui
npm install
cd ..
```

---

## Running (Every Time)

### Option 1: With API Key (Agent Mode)

**Set API key first:**
```bash
# Mac/Linux
export GOOGLE_API_KEY="your-key-from-aistudio"

# Windows PowerShell
$env:GOOGLE_API_KEY="your-key-from-aistudio"
```

**Then run 3 terminals:**
```bash
# Terminal 1
cd mcp-server && python main.py

# Terminal 2
cd adk && python main.py

# Terminal 3
cd ui && npm run dev
```

### Option 2: Without API Key (Fallback Mode)

Just run the 3 terminals without setting GOOGLE_API_KEY.
Everything still works, just without AI agent.

---

## Testing Checklist

### ✅ Basic Flow
1. Open http://localhost:3000
2. See schedule meeting widget
3. Click a date - it highlights
4. Click a time - button enables
5. Click "Schedule meeting" - success message

### ✅ Follow-up Action (Key Feature!)
1. Select date and time
2. Click "CHANGE TIME ZONE"
3. New widget appears with timezone list
4. Select "Pacific Time (PT)"
5. Click "Confirm"
6. **Returns to schedule widget**
7. **Your date/time selections are preserved!**
8. Time labels now show "PT" instead of "ET"

---

## What Actually Happens

### With API Key:
```
User Action → ADK Agent (Gemini) → Calls MCP Tool → Gets Schema → 
Populates with Data → Sends to UI
```

### Without API Key:
```
User Action → Direct Logic → Calls MCP → Gets Schema → 
Populates with Data → Sends to UI
```

**Both modes work perfectly!**

---

## File Structure

```
adk-widget-mcp/
├── mcp-server/          # Widget schemas
├── adk/                 # Agent + sessions
├── ui/                  # React frontend
├── README.md           # This file
├── QUICKSTART.md       # Detailed guide
├── TESTING.md          # Test scenarios
└── ARCHITECTURE.md     # Technical details
```

---

## Key Features Demonstrated

1. ✅ **MCP Widget Schemas** - Schemas from MCP server
2. ✅ **ADK Agent** - Gemini with function calling
3. ✅ **Session Management** - Context preserved
4. ✅ **Follow-up Actions** - Timezone change flow
5. ✅ **Dynamic UI** - Schema-driven rendering
6. ✅ **Fallback Mode** - Works without API key

---

## No Surprises

- **Tested**: All imports work
- **Simple**: Only 5 Python dependencies
- **Clean**: Removed confusing docs
- **Works**: With or without API key
- **Fast**: Minimal setup

---

## Get Started Now

```bash
# 1. Install (once)
./install.sh  # Or manually: pip/npm install in each folder

# 2. Run (always)
# Terminal 1: cd mcp-server && python main.py
# Terminal 2: cd adk && python main.py  
# Terminal 3: cd ui && npm run dev

# 3. Open: http://localhost:3000
```

**That's it. Simple, verified, ready.** ✅
