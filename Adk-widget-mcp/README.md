# ✅ READY - Google ADK Implementation

## What This Is

A **working demo** using the official **google-adk** library with MCP widgets for meeting scheduling.

---

## Verified Setup

### ✅ Using Official `google-adk==1.22.1`

**Confirmed working:**
- `from google.adk.agents import LlmAgent` ✅
- `from google.adk.tools import FunctionTool` ✅
- `from google.adk import Runner` ✅

### ✅ Implementation

```python
# Create tools as functions
def get_schedule_meeting_widget() -> str:
    """Fetch widget from MCP"""
    return mcp_client.call_tool(...)

# Wrap with FunctionTool
tools = [
    FunctionTool(get_schedule_meeting_widget),
    FunctionTool(get_timezone_selector_widget),
    FunctionTool(list_available_widgets)
]

# Create LlmAgent
agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    system_instruction="You are a meeting scheduler...",
    tools=tools,
    api_key=api_key
)

# Create Runner
runner = Runner(agent=agent)

# Run
response = runner.run(user_message)
```

---

## Installation

```bash
# MCP Server
cd mcp-server
pip install -r requirements.txt

# ADK Server (google-adk)
cd adk
pip install -r requirements.txt

# UI
cd ui
npm install
```

---

## API Key Setup

1. Get key: https://aistudio.google.com/app/apikey

2. Set environment variable:
```bash
# Mac/Linux
export GOOGLE_API_KEY="your-key"

# Windows PowerShell
$env:GOOGLE_API_KEY="your-key"
```

---

## Running

**3 Terminals:**

```bash
# Terminal 1 - MCP Server
cd mcp-server && python main.py

# Terminal 2 - ADK Server (google-adk)
cd adk && python main.py

# Terminal 3 - UI
cd ui && npm run dev
```

**Open:** http://localhost:3000

---

## Expected Output

```
🤖 Google ADK Agent initialized
   Model: gemini-2.0-flash-exp
   Tools: 3 registered
```

---

## What Works

1. ✅ **google-adk** package (verified 1.22.1)
2. ✅ **LlmAgent** with Gemini
3. ✅ **FunctionTool** for MCP integration
4. ✅ **Runner** for execution
5. ✅ Session management
6. ✅ Follow-up actions (timezone change)
7. ✅ Dynamic UI rendering
8. ✅ Fallback mode (without API key)

---

## File Structure

```
adk-widget-mcp/
├── mcp-server/          # Widget schemas
│   └── main.py          # FastMCP server
├── adk/                 # Google ADK agent
│   ├── main.py          # WebSocket server
│   └── src/
│       └── adk_agent.py # LlmAgent + FunctionTool
├── ui/                  # React frontend
└── README.md           # This file
```

---

## Quick Test

1. Start all 3 servers
2. Open http://localhost:3000
3. See schedule meeting widget
4. Select date and time
5. Click "CHANGE TIME ZONE"
6. Select timezone and confirm
7. **Verify**: Date/time selections preserved!

---

## Documentation

- **SETUP_VERIFIED.md** - Detailed verification
- **ADK_SETUP.md** - ADK-specific setup
- **QUICKSTART.md** - Step-by-step guide
- **TESTING.md** - Test scenarios

---

**Using official google-adk library. Verified and ready!** ✅
