# Multi-Agent Test System - A2A Architecture

A demonstration of a multi-agent system using Google ADK's **A2A (Agent-to-Agent) protocol**, where a root agent orchestrates multiple specialized agents.

## 🎯 Overview

This system demonstrates:
- **Root Agent**: Routes user requests to specialized agents (Port 8000)
- **Text Agent**: Handles general queries (local agent via AgentTool)
- **Calendar Agent**: Handles booking/appointments via A2A protocol (Port 8001, AG-UI enabled)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Web UI)                    │
│              (AG-UI Protocol / HTTP)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Root ADK Agent (Port 8000)                  │
│  - FastAPI + ADKAgent middleware                        │
│  - Routes requests based on intent                      │
│  - Uses A2A to call calendar agent                       │
│                                                          │
│  Tools:                                                  │
│  ├─ text_responder (AgentTool - local)                  │
│  └─ calendar_booking (RemoteA2aAgent - A2A)            │
└──────┬───────────────────────────────────────┬──────────┘
       │                                       │
       │ AgentTool                            │ RemoteA2aAgent
       │ (Local)                              │ (A2A Protocol)
       │                                       │
       ▼                                       ▼
┌──────────────────────┐          ┌──────────────────────┐
│  Text Agent          │          │  Calendar Agent       │
│  (Local Agent)       │          │  (A2A Service)        │
│                      │          │  Port 8001            │
│  - Simple Agent      │          │                       │
│  - Direct tool       │          │  - Agent              │
│  - No middleware     │          │  - ADKAgent wrapper  │
│                      │          │  - Calendar tool      │
│                      │          │  - AG-UI protocol     │
└──────────────────────┘          └──────────────────────┘
```

## 📋 Prerequisites

- Python 3.9 or higher
- Google API Key (for Gemini)
- pip (Python package manager)

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies

```bash
cd multiagent-test
pip install -r requirements.txt
```

### Step 2: Configure Environment

Create a `.env` file in the `multiagent-test` directory:

```env
GOOGLE_API_KEY=your-google-api-key-here
ROOT_AGENT_PORT=8000
CALENDAR_AGENT_PORT=8001
```

**Get your Google API Key:** https://aistudio.google.com/app/apikey

### Step 3: Start Calendar Agent

**Open Terminal 1:**
```bash
python agent/calendar_agent.py
```

**Expected Output:**
```
🚀 Starting Calendar Agent (A2A Service)
   Port: 8001
   AG-UI endpoint: http://localhost:8001/
```

**✅ Keep this terminal running!**

### Step 4: Start Root Agent

**Open Terminal 2 (NEW TERMINAL):**
```bash
python agent/root_agent.py
```

**Expected Output:**
```
🚀 Starting Root Agent (Multi-Agent Orchestrator)
   Port: 8000
   📋 Available Tools:
   ✅ text_responder (local agent)
   ✅ calendar_booking (A2A agent)
```

**✅ Keep this terminal running!**

### Step 5: Test the System

**Option A: Python Test Script (Recommended)**
```bash
python test_agents.py
```

**Option B: HTML Test UI**
- Open `test-ui.html` in your browser
- Test both agents visually

**Option C: curl Commands**
See [RUN_AND_TEST.md](./RUN_AND_TEST.md) for detailed curl commands

---

## 📖 Detailed Run & Test Guide

For complete step-by-step instructions, see **[RUN_AND_TEST.md](./RUN_AND_TEST.md)**

This includes:
- ✅ Detailed setup steps
- ✅ Multiple testing methods
- ✅ Expected outputs
- ✅ Troubleshooting guide
- ✅ Test scenarios

---

## 🧪 Quick Test Examples

#### Option A: Using curl

**Test Root Agent (General Query):**
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "{\"threadId\":\"test123\",\"runId\":\"run1\",\"messages\":[{\"role\":\"user\",\"content\":\"What is Python?\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"
```

**Test Root Agent (Calendar Booking):**
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "{\"threadId\":\"test123\",\"runId\":\"run2\",\"messages\":[{\"role\":\"user\",\"content\":\"I want to book an appointment for tomorrow at 2pm\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"
```

**Test Calendar Agent Directly:**
```bash
curl -X POST http://localhost:8001/ \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d "{\"threadId\":\"test123\",\"runId\":\"run3\",\"messages\":[{\"role\":\"user\",\"content\":\"Book a meeting for next Monday at 10am\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"
```

#### Option B: Using Python Test Script

Create `test_agents.py`:

```python
import requests
import json

# Test Root Agent
def test_root_agent(message):
    url = "http://localhost:8000/"
    payload = {
        "threadId": "test_session",
        "runId": "run_1",
        "messages": [{"role": "user", "content": message}],
        "state": {},
        "tools": [],
        "context": [],
        "forwardedProps": {}
    }
    
    response = requests.post(
        url,
        json=payload,
        headers={"Accept": "text/event-stream"},
        stream=True
    )
    
    print(f"Response for: {message}")
    for line in response.iter_lines():
        if line:
            print(line.decode('utf-8'))
    print("\n" + "="*50 + "\n")

# Test cases
test_root_agent("What is Python?")
test_root_agent("I want to book an appointment for tomorrow at 2pm")
```

Run it:
```bash
python test_agents.py
```

## 🧪 Testing Scenarios

### Scenario 1: General Query (Text Agent)

**Input:** "What is Python?"

**Expected Flow:**
1. Root agent detects: general query
2. Routes to: text_responder tool (local agent)
3. Response: Text explanation about Python

### Scenario 2: Calendar Booking (Calendar Agent via A2A)

**Input:** "I want to book an appointment for tomorrow at 2pm"

**Expected Flow:**
1. Root agent detects: calendar intent
2. Routes to: calendar_booking tool (A2A agent)
3. Calendar agent processes via A2A protocol
4. Calendar agent calls: book_calendar_appointment tool
5. State updated: current_booking = {...}
6. AG-UI emits: STATE_SNAPSHOT event
7. Frontend can render calendar UI

## 📁 Project Structure

```
multiagent-test/
├── README.md                 # This file
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .env.example              # Example environment file
│
├── agent/
│   ├── __init__.py
│   ├── root_agent.py         # Main orchestrator (Port 8000)
│   ├── text_agent.py         # Text responder (local)
│   └── calendar_agent.py     # Calendar booking (A2A, Port 8001)
│
└── scripts/
    ├── run-root-agent.bat    # Windows: Run root agent
    ├── run-calendar-agent.bat # Windows: Run calendar agent
    ├── run-all.bat           # Windows: Run both (requires multiple terminals)
    ├── run-root-agent.sh     # Linux/Mac: Run root agent
    └── run-calendar-agent.sh # Linux/Mac: Run calendar agent
```

## 🔍 How It Works

### 1. Root Agent Routing

The root agent analyzes user input and routes to appropriate agent:

- **Calendar keywords** → `calendar_booking` tool (A2A)
  - Keywords: calendar, book, appointment, schedule, meeting, reserve, slot, time
  
- **General queries** → `text_responder` tool (local)
  - Everything else: questions, explanations, information

### 2. A2A Communication

When root agent calls calendar agent:
- Uses `RemoteA2aAgent` to connect via A2A protocol
- Automatically shares:
  - Session ID
  - Conversation history
  - State
- Calendar agent processes and returns response

### 3. AG-UI Protocol

Both agents use AG-UI protocol:
- Root agent: Wrapped with `ADKAgent` middleware
- Calendar agent: Wrapped with `ADKAgent` middleware
- Events streamed as SSE (Server-Sent Events)
- Frontend receives: TEXT_MESSAGE, STATE_SNAPSHOT, etc.

## 🎨 Frontend Integration

The system uses AG-UI protocol, compatible with:
- **CopilotKit** - React components
- **Custom AG-UI clients** - Any frontend that supports AG-UI
- **Direct HTTP** - For testing

### Example Frontend Connection

```typescript
// Connect to root agent
const eventSource = new EventSource("http://localhost:8000/");

eventSource.onmessage = (event) => {
    const aguiEvent = JSON.parse(event.data);
    
    // Handle different event types
    switch(aguiEvent.type) {
        case "TEXT_MESSAGE_CONTENT":
            // Display text
            break;
        case "STATE_SNAPSHOT":
            // Render calendar UI if current_booking exists
            if (aguiEvent.state.current_booking) {
                renderCalendar(aguiEvent.state.current_booking);
            }
            break;
    }
};
```

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not set"

**Solution:** 
1. Create `.env` file in `multiagent-test/` directory
2. Add: `GOOGLE_API_KEY=your-key-here`
3. Restart the agent

### Issue: "Calendar agent not available"

**Solution:**
1. Make sure calendar agent is running on port 8001
2. Check: `curl http://localhost:8001/health`
3. Verify agent card: `curl http://localhost:8001/.well-known/agent-card.json`

### Issue: "Port already in use"

**Solution:**
1. Change ports in `.env` file:
   ```
   ROOT_AGENT_PORT=8002
   CALENDAR_AGENT_PORT=8003
   ```
2. Update agent card URL in `root_agent.py` if needed

### Issue: "A2A connection fails"

**Solution:**
1. Verify calendar agent is running
2. Check agent card endpoint is accessible
3. Ensure both agents are on same network/localhost
4. Check firewall settings

### Issue: "Import errors"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify installation
pip list | grep -E "google-adk|ag-ui-adk|fastapi"
```

## 📊 Health Checks

### Root Agent
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Root Agent",
  "port": 8000,
  "tools": {
    "text_responder": "available",
    "calendar_booking": "available"
  }
}
```

### Calendar Agent
```bash
curl http://localhost:8001/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Calendar Agent",
  "port": 8001
}
```

### Agent Card (A2A Discovery)
```bash
curl http://localhost:8001/.well-known/agent-card.json
```

## 🎓 Key Concepts

### A2A (Agent-to-Agent) Protocol
- Native ADK protocol for agent communication
- Automatic context sharing
- Agent discovery via Agent Cards
- Standardized communication

### AgentTool
- Wraps an agent so it can be used as a tool
- Used for local agents (text_responder)

### RemoteA2aAgent
- Connects to remote agents via A2A protocol
- Used for calendar agent communication
- Automatically handles context sharing

### ADKAgent Middleware
- Bridges ADK agents with AG-UI protocol
- Converts ADK events to AG-UI events
- Enables frontend integration

## 📝 Example Conversations

### Example 1: General Query
```
User: "What is machine learning?"
Root Agent: [Routes to text_responder]
Text Agent: "Machine learning is a subset of artificial intelligence..."
```

### Example 2: Calendar Booking
```
User: "I need to schedule a meeting for next Monday at 10am"
Root Agent: [Routes to calendar_booking via A2A]
Calendar Agent: [Processes via A2A, calls book_calendar_appointment]
Calendar Agent: "I've opened the calendar for booking. Meeting scheduled for Monday at 10am."
[STATE_SNAPSHOT event emitted with booking details]
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google API key for Gemini | Required |
| `ROOT_AGENT_PORT` | Root agent port | 8000 |
| `CALENDAR_AGENT_PORT` | Calendar agent port | 8001 |

### Customization

**Change routing logic:**
Edit `agent/root_agent.py` → `root_agent.instruction`

**Modify calendar tool:**
Edit `agent/calendar_agent.py` → `book_calendar_appointment` function

**Add new agents:**
1. Create agent file in `agent/`
2. Add to root agent tools
3. Update routing logic

## 📚 Documentation

- [A2A_ARCHITECTURE.md](./A2A_ARCHITECTURE.md) - A2A architecture details
- [A2A_SETUP.md](./A2A_SETUP.md) - Detailed A2A setup guide
- [PLAN_A2A.md](./PLAN_A2A.md) - Implementation plan

## 🚦 Status

- ✅ Root agent implemented
- ✅ Text agent implemented
- ✅ Calendar agent implemented
- ✅ A2A integration
- ✅ AG-UI protocol support
- ✅ Health checks
- ✅ Agent cards

## 🤝 Contributing

This is a demonstration project. Feel free to:
- Add more agents
- Improve routing logic
- Enhance calendar UI
- Add more tools

## 📄 License

[To be determined]

## 🙏 Acknowledgments

- Google ADK for agent framework and A2A protocol
- AG-UI protocol for standardized communication
- FastAPI for web framework

---

**Happy Building! 🚀**

For questions or issues, check the troubleshooting section or review the documentation files.
