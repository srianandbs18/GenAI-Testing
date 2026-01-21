# ADK Widget MCP Demo - Quick Start Guide

## 🚀 Installation & Setup

### Step 0: Get Google API Key (Required for Agent)

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in and create an API key
3. Copy the key

**Set the API key:**

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

**Mac/Linux:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

> **Note:** Without an API key, the server runs in fallback mode (still works, just without AI agent).

### Step 1: Install MCP Server Dependencies
```bash
cd mcp-server
pip install -r requirements.txt
cd ..
```

### Step 2: Install ADK Dependencies
```bash
cd adk
pip install -r requirements.txt
cd ..
```

### Step 3: Install UI Dependencies
```bash
cd ui
npm install
cd ..
```

## ▶️ Running the Demo

You need **3 separate terminals** (or use the startup scripts):

### Option A: Using Startup Scripts (Windows)

**Terminal 1 - MCP Server:**
```bash
start-mcp.bat
```

**Terminal 2 - ADK Server:**
```bash
start-adk.bat
```

**Terminal 3 - React UI:**
```bash
start-ui.bat
```

### Option B: Using Startup Scripts (Mac/Linux)

Make scripts executable first:
```bash
chmod +x start-mcp.sh start-adk.sh start-ui.sh
```

**Terminal 1 - MCP Server:**
```bash
./start-mcp.sh
```

**Terminal 2 - ADK Server:**
```bash
./start-adk.sh
```

**Terminal 3 - React UI:**
```bash
./start-ui.sh
```

### Option C: Manual Commands

**Terminal 1 - MCP Server:**
```bash
cd mcp-server
python main.py
```

**Terminal 2 - ADK Server:**
```bash
cd adk
python main.py
```

**Terminal 3 - React UI:**
```bash
cd ui
npm run dev
```

## 🌐 Access the Demo

Once all three servers are running:

1. Open your browser
2. Go to: **http://localhost:3000**
3. You should see the "Schedule Meeting" widget!

## 🎯 Demo Features to Test

### 1. Initial Widget Load
- ✅ Widget appears with dates and times
- ✅ Current timezone shows "Eastern Time (ET)"
- ✅ "Schedule meeting" button is disabled

### 2. Date Selection
- ✅ Click any date (e.g., "TUE Sep 23")
- ✅ Selected date highlights
- ✅ Button still disabled (need time too)

### 3. Time Selection
- ✅ Click any time (e.g., "1:45 PM ET")
- ✅ Selected time highlights
- ✅ "Schedule meeting" button becomes enabled!

### 4. Change Timezone (Follow-up Action)
- ✅ Click "CHANGE TIME ZONE"
- ✅ New widget appears with timezone options
- ✅ Select "Pacific Time (PT)"
- ✅ Click "Confirm"
- ✅ Returns to schedule widget with PT times
- ✅ Your date/time selections are preserved!

### 5. Schedule Meeting
- ✅ With date & time selected, click "Schedule meeting"
- ✅ Success message appears at top
- ✅ Console shows meeting details

## 🏗️ Architecture Overview

```
┌─────────────┐     WebSocket      ┌─────────────┐      HTTP       ┌─────────────┐
│  React UI   │ ←─────────────────→ │     ADK     │ ←──────────────→ │ MCP Server  │
│  (Port 3000)│     Real-time      │  (Port 8000)│   Tool Calls    │ (Port 8001) │
└─────────────┘                     └─────────────┘                  └─────────────┘
     │                                     │                                │
     │                                     │                                │
  Renders UI                    Session Management              Widget Schemas
  from Schema                   + Data Population                (Contracts)
```

## 📦 What Each Component Does

### MCP Server (Port 8001)
- Provides widget **schemas** (structure/contracts)
- Tools: `get_schedule_meeting_widget()`, `get_timezone_selector_widget()`
- **Does NOT provide data** - only structure

### ADK Server (Port 8000)
- Maintains user **session** (timezone, selections)
- Calls MCP to get widget schemas
- **Populates schemas** with actual data (dates, times)
- Handles **follow-up actions** (timezone change)
- Sends populated widgets to UI via WebSocket

### React UI (Port 3000)
- **Renders widgets** based on schemas
- Sends user actions to ADK
- No business logic - pure renderer

## 🔍 Monitoring & Debugging

### Check ADK Server Logs
You'll see:
```
✅ Client connected from ('127.0.0.1', 54321)
📝 Created session: abc-123-def-456
📨 Received action: select_date
📅 Date selected: 2024-09-23
⏰ Time selected: 13:45
🌍 Timezone change requested (follow-up action)
```

### Check Browser Console
Press F12 and look for:
```
✅ Connected to ADK server
📨 Received: {type: "widget_render", ...}
📤 Sending: {action: "select_date", ...}
```

## ⚠️ Troubleshooting

### "Cannot connect to ADK server"
- Make sure ADK server is running on port 8000
- Check for port conflicts: `netstat -an | findstr 8000`

### "Module not found" errors
- Make sure you installed dependencies:
  - `pip install -r requirements.txt` in both mcp-server and adk
  - `npm install` in ui

### UI doesn't load
- Check if React dev server is running on port 3000
- Try clearing browser cache

### Import errors in Python
- Make sure you're running from the correct directory
- ADK modules use relative imports from `src/` folder

## 🎨 UI Customization

The UI is styled to match the image with:
- Dark theme (#2D2D2D background)
- Gradient header (#3a2f29 to #2d2d2d)
- Cream colored buttons (#d4c5b9)
- Rounded corners and smooth transitions

To modify styling, edit:
- `ui/src/components/ScheduleMeetingWidget.css`
- `ui/src/components/TimezoneSelectorWidget.css`

## 📚 Next Steps

After testing the demo:

1. **Add more widgets** - Create new schemas in MCP server
2. **Add more time slots** - Edit `WidgetPopulator` in ADK
3. **Connect real calendar** - Integrate Google Calendar API
4. **Add persistence** - Use Redis for session storage
5. **Deploy** - Dockerize all three components

## 🆘 Need Help?

Check the detailed architecture doc:
```bash
cat ARCHITECTURE.md
```

Or check the code:
- MCP Server: `mcp-server/main.py`
- ADK Agent: `adk/main.py`
- React UI: `ui/src/App.jsx`

---

**Enjoy the demo! 🎉**
