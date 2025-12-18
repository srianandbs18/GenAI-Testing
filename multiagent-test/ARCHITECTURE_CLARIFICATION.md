# Architecture Clarification: AG-UI for Calendar Agent Only

## Your Questions

1. **Does this setup use WebSocket?**
2. **Can we use AG-UI for calendar agent alone, not for root agent?**

## Answer 1: Transport Mechanism (SSE vs WebSocket)

### Current Implementation: **SSE (Server-Sent Events)**

The `add_adk_fastapi_endpoint` from `ag_ui_adk` uses **SSE (Server-Sent Events)**, not WebSocket by default.

**Evidence:**
- Test files show: `'Accept': 'text/event-stream'` (SSE header)
- FastAPI endpoint returns SSE stream
- One-way communication: Server → Client

**SSE Characteristics:**
- ✅ Simpler than WebSocket
- ✅ Automatic reconnection
- ✅ Works over HTTP
- ❌ One-way only (server pushes to client)
- ❌ No bidirectional communication

**If you need WebSocket:**
- AG-UI protocol supports WebSocket
- Would need custom implementation
- More complex but enables bidirectional communication

## Answer 2: AG-UI for Calendar Agent Only

### The Challenge

You want:
- **Root Agent**: Regular ADK (no AG-UI middleware)
- **Calendar Agent**: AG-UI middleware (for calendar UI)

**Problem:** If root agent doesn't use AG-UI, how does it:
1. Expose web interface?
2. Forward AG-UI events from calendar agent?

### Solution Options

#### Option A: Hybrid Architecture (Recommended)

```
┌─────────────────────────────────────────────────┐
│           Frontend (Web UI)                      │
│     (AG-UI Protocol via SSE/WebSocket)           │
└──────────────────┬──────────────────────────────┘
                    │
                    │ AG-UI Protocol
                    ▼
┌─────────────────────────────────────────────────┐
│         Root Agent Service                      │
│  ┌──────────────────────────────────────────┐  │
│  │  Root ADK Agent                          │  │
│  │  (No AG-UI middleware)                   │  │
│  │  - Direct ADK web interface              │  │
│  │  - Routes to tool agents                 │  │
│  └──────┬───────────────────────┬──────────┘  │
│         │                       │              │
│         │ AgentTool            │ AgentTool    │
│         │                       │              │
│         ▼                       ▼              │
│  ┌──────────────┐    ┌────────────────────┐  │
│  │ Text Agent   │    │ Calendar Agent     │  │
│  │ (Direct ADK) │    │ (AG-UI Middleware) │  │
│  └──────────────┘    └──────────┬─────────┘  │
│                                  │             │
│                                  │ AG-UI       │
│                                  │ Events      │
│                                  ▼             │
│                          ┌──────────────┐     │
│                          │ ADKAgent     │     │
│                          │ Middleware   │     │
│                          └──────────────┘     │
└─────────────────────────────────────────────────┘
```

**Implementation:**
1. Root agent uses **direct ADK web interface** (not AG-UI)
2. Calendar agent wrapped with **ADKAgent middleware** (AG-UI)
3. Calendar agent runs as **separate service** on different port
4. Root agent calls calendar agent via **HTTP** and forwards AG-UI events

#### Option B: Root Agent with AG-UI, Calendar Agent Embedded

```
┌─────────────────────────────────────────────────┐
│         Root Agent Service                      │
│  ┌──────────────────────────────────────────┐  │
│  │  Root ADK Agent                          │  │
│  │  (AG-UI Middleware)                      │  │
│  │  - Exposes AG-UI endpoint                │  │
│  │  - Routes to tool agents                 │  │
│  └──────┬───────────────────────┬──────────┘  │
│         │                       │              │
│         │ AgentTool            │ AgentTool    │
│         │                       │              │
│         ▼                       ▼              │
│  ┌──────────────┐    ┌────────────────────┐  │
│  │ Text Agent   │    │ Calendar Agent     │  │
│  │ (Direct ADK) │    │ (AG-UI Middleware) │  │
│  └──────────────┘    └────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Problem:** Root agent uses AG-UI, which you don't want.

#### Option C: Separate Services (Best for Your Requirement)

```
┌─────────────────────────────────────────────────┐
│           Frontend (Web UI)                      │
└──────┬──────────────────────────────┬────────────┘
       │                              │
       │ Direct ADK                   │ AG-UI Protocol
       │                              │
       ▼                              ▼
┌──────────────────┐        ┌──────────────────────┐
│  Root Agent      │        │  Calendar Agent     │
│  Service         │        │  Service            │
│                  │        │                     │
│  - Direct ADK    │        │  - AG-UI Middleware │
│  - Web interface │        │  - Calendar UI      │
│  - Routes        │        │  - Port 8001       │
│  - Port 8000     │        │                     │
└──────────────────┘        └──────────────────────┘
```

**Implementation:**
- Root agent: Direct ADK web interface (port 8000)
- Calendar agent: Separate service with AG-UI (port 8001)
- Root agent calls calendar agent via HTTP
- Frontend connects to both services

## Recommended Architecture for Your Use Case

### Architecture: Separate Services with Protocol Bridge

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend                              │
│  - Connects to Root Agent (Direct ADK)                  │
│  - Connects to Calendar Agent (AG-UI) when needed        │
└──────┬──────────────────────────────┬────────────────────┘
       │                              │
       │ Direct ADK HTTP              │ AG-UI SSE/WebSocket
       │                              │
       ▼                              ▼
┌──────────────────┐        ┌──────────────────────┐
│  Root Agent      │        │  Calendar Agent       │
│  (Port 8000)     │        │  (Port 8001)         │
│                  │        │                      │
│  - Direct ADK    │        │  - ADKAgent wrapper  │
│  - FastAPI       │        │  - AG-UI protocol    │
│  - Routes        │        │  - Calendar tool     │
│                  │        │  - State management  │
│  Tools:          │        │                      │
│  - text_agent    │        │                      │
│  - calendar_http │        │                      │
└──────────────────┘        └──────────────────────┘
```

### Implementation Details

#### 1. Root Agent (No AG-UI)

```python
from fastapi import FastAPI
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, ToolContext
import httpx

# Direct ADK agent (no AG-UI middleware)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    tools=[text_responder_tool, call_calendar_agent_tool],
    instruction="Route requests appropriately"
)

# Direct ADK web interface (not AG-UI)
@app.post("/adk/chat")
async def direct_adk_chat(request: ChatRequest):
    """Direct ADK endpoint (no AG-UI)"""
    response = await root_agent.run(request.messages)
    return {"response": response.text}
```

#### 2. Calendar Agent (With AG-UI)

```python
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Calendar agent with AG-UI middleware
calendar_agent = Agent(
    name="CalendarAgent",
    model="gemini-2.5-flash",
    tools=[book_calendar_appointment],
    instruction="Help users book appointments"
)

# Wrap with AG-UI middleware
adk_calendar_agent = ADKAgent(
    adk_agent=calendar_agent,
    app_name="calendar_app",
    use_in_memory_services=True
)

# Separate FastAPI app for calendar agent
calendar_app = FastAPI(title="Calendar Agent")

# Add AG-UI endpoint
add_adk_fastapi_endpoint(calendar_app, adk_calendar_agent, path="/")
```

#### 3. Root Agent Calls Calendar Agent

```python
async def call_calendar_agent(
    tool_context: ToolContext,
    user_message: str
) -> Dict[str, str]:
    """Call calendar agent via HTTP and forward AG-UI events"""
    
    # Call calendar agent service
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/",  # Calendar agent endpoint
            json={
                "messages": [{"role": "user", "content": user_message}],
                "threadId": tool_context.session_id
            },
            headers={"Accept": "text/event-stream"}
        )
        
        # Forward AG-UI events to frontend
        # (This requires custom implementation)
        return {"status": "success", "message": "Calendar agent called"}
```

## Challenges & Solutions

### Challenge 1: Forwarding AG-UI Events

**Problem:** Root agent (Direct ADK) needs to forward AG-UI events from calendar agent.

**Solution Options:**
1. **Proxy Pattern**: Root agent proxies AG-UI events
2. **Frontend Direct Connection**: Frontend connects to calendar agent directly
3. **Event Bridge**: Custom middleware to bridge protocols

### Challenge 2: State Synchronization

**Problem:** Root agent and calendar agent have separate state.

**Solution:** 
- Use shared session IDs
- Pass state via tool context
- Use external state store (Redis, database)

### Challenge 3: WebSocket Support

**Problem:** Current implementation uses SSE, you might need WebSocket.

**Solution:**
- AG-UI protocol supports WebSocket
- Need custom WebSocket handler
- More complex but enables bidirectional communication

## Recommended Approach

For your use case, I recommend:

1. **Root Agent**: Direct ADK web interface (no AG-UI)
   - Simple HTTP endpoints
   - Fast and lightweight
   - Easy to route requests

2. **Calendar Agent**: Separate service with AG-UI
   - Runs on different port (8001)
   - Full AG-UI protocol support
   - Calendar UI components work

3. **Frontend**: Connects to both
   - Root agent for general queries
   - Calendar agent for booking (direct connection)

4. **Transport**: Start with SSE, add WebSocket if needed

## Next Steps

1. Decide on architecture (Option C recommended)
2. Implement root agent with direct ADK
3. Implement calendar agent with AG-UI
4. Create frontend that connects to both
5. Add WebSocket support if needed

Would you like me to implement this architecture?
