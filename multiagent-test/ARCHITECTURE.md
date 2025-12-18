# Multi-Agent System Architecture

## System Overview

This document provides a detailed architecture diagram and explanation of the multi-agent system.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Web Browser / Frontend)                     │
│                                                                 │
│  • Chat Interface                                               │
│  • Calendar Component (rendered when booking)                  │
│  • Text Responses                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ AG-UI Protocol (SSE/WebSocket)
                             │ HTTP Requests
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ROOT AGENT SERVICE                           │
│                    (FastAPI + ADKAgent)                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Root ADK Agent                               │  │
│  │  • Intent Detection                                       │  │
│  │  • Request Routing                                       │  │
│  │  • Tool Orchestration                                    │  │
│  └──────┬───────────────────────────────────────┬────────────┘  │
│         │                                       │               │
│         │ AgentTool                            │ AgentTool     │
│         │                                       │               │
│         ▼                                       ▼               │
│  ┌──────────────┐                    ┌──────────────────────┐ │
│  │ Text Agent   │                    │ Calendar Agent       │ │
│  │ (Tool 1)     │                    │ (Tool 2)             │ │
│  │              │                    │                      │ │
│  │ • LlmAgent   │                    │ • LlmAgent           │ │
│  │ • Direct     │                    │ • ADKAgent wrapper   │ │
│  │ • Text only  │                    │ • Calendar tool      │ │
│  │              │                    │ • AG-UI protocol     │ │
│  └──────────────┘                    └──────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ADKAgent Middleware                         │  │
│  │  • Protocol Translation (ADK ↔ AG-UI)                   │  │
│  │  • Session Management                                    │  │
│  │  • State Management                                      │  │
│  │  • Event Streaming                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │
                             ▼
                    ┌─────────────────┐
                    │  LLM Backend   │
                    │  (Gemini API)  │
                    └─────────────────┘
```

## Component Details

### 1. Root Agent Service

**Technology Stack**:
- FastAPI (Web framework)
- ADKAgent (AG-UI middleware)
- Google ADK (Agent framework)

**Responsibilities**:
1. Receive user requests via AG-UI protocol
2. Detect intent (calendar vs general)
3. Route to appropriate tool agent
4. Aggregate responses
5. Stream events back to frontend

**Key Files**:
- `agent/root_agent.py`: Main orchestrator

### 2. Text Agent (Tool Agent 1)

**Type**: Regular LlmAgent (no middleware)

**Purpose**: Handle general text queries

**Characteristics**:
- Fast and lightweight
- Direct text responses
- No special UI components
- Stateless (or minimal state)

**Key Files**:
- `agent/text_agent.py`: Text responder implementation

### 3. Calendar Agent (Tool Agent 2)

**Type**: LlmAgent + ADKAgent middleware

**Purpose**: Handle calendar/booking requests with interactive UI

**Characteristics**:
- Uses AG-UI protocol
- Triggers calendar UI components
- Maintains booking state
- Interactive date/time selection

**Key Files**:
- `agent/calendar_agent.py`: Calendar agent implementation
- `agent/tools.py`: Calendar booking tool

## Data Flow Examples

### Example 1: General Query Flow

```
1. User sends: "What is Python?"
   ↓
2. Frontend → Root Agent (AG-UI protocol)
   ↓
3. Root Agent detects: General query
   ↓
4. Root Agent calls: text_responder tool
   ↓
5. Text Agent processes with LLM
   ↓
6. Text Agent returns: "Python is a programming language..."
   ↓
7. Root Agent forwards response
   ↓
8. ADKAgent middleware converts to AG-UI events
   ↓
9. Frontend receives: TEXT_MESSAGE_START/CONTENT/END events
   ↓
10. User sees text response
```

### Example 2: Calendar Booking Flow

```
1. User sends: "I want to book an appointment"
   ↓
2. Frontend → Root Agent (AG-UI protocol)
   ↓
3. Root Agent detects: Calendar intent
   ↓
4. Root Agent calls: calendar_booking tool
   ↓
5. Calendar Agent processes with LLM
   ↓
6. Calendar Agent calls: book_calendar_appointment tool
   ↓
7. Tool updates state: current_booking = {...}
   ↓
8. ADKAgent middleware emits: STATE_SNAPSHOT event
   ↓
9. Frontend receives state update
   ↓
10. Frontend detects calendar state
   ↓
11. Frontend renders: Calendar UI component
   ↓
12. User interacts with calendar
   ↓
13. User selects date/time
   ↓
14. Frontend sends selection back
   ↓
15. Calendar Agent confirms booking
   ↓
16. State updated: booking confirmed
   ↓
17. Frontend shows confirmation
```

## State Management

### Root Agent State
```python
{
    "routing_history": [
        {"timestamp": "...", "tool": "text_responder", "query": "..."}
    ],
    "session_context": {
        "user_preferences": {...},
        "conversation_summary": "..."
    }
}
```

### Calendar Agent State
```python
{
    "current_booking": {
        "title": "Meeting with John",
        "date": "2024-01-15",
        "time": "14:00",
        "duration": 60,
        "status": "pending"
    },
    "bookings": [
        {
            "id": "booking_1",
            "title": "...",
            "date": "...",
            "time": "...",
            "status": "confirmed"
        }
    ],
    "calendar_state": {
        "view": "month",
        "selected_date": "2024-01-15"
    }
}
```

### Text Agent State
```python
{
    # Minimal state - mostly stateless
    "conversation_context": "..."
}
```

## Protocol Translation

### ADK → AG-UI Events

| ADK Event | AG-UI Event |
|-----------|-------------|
| Agent starts | `RUN_STARTED` |
| Text response | `TEXT_MESSAGE_START/CONTENT/END` |
| Tool call | `TOOL_CALL_START/END` |
| State update | `STATE_SNAPSHOT` |
| Agent finishes | `RUN_FINISHED` |
| Error | `RUN_ERROR` |

### AG-UI → ADK Conversion

| AG-UI Input | ADK Format |
|-------------|------------|
| `RunAgentInput` | ADK `InvocationContext` |
| Messages | ADK `Content` objects |
| Thread ID | ADK Session ID |

## Integration Points

### 1. AgentTool Integration
```python
from google.adk.tools import AgentTool

# Wrap agents as tools
text_tool = AgentTool(agent=text_agent, name="text_responder")
calendar_tool = AgentTool(agent=calendar_agent, name="calendar_booking")

# Root agent uses them
root_agent = Agent(
    tools=[text_tool, calendar_tool]
)
```

### 2. ADKAgent Middleware
```python
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Wrap root agent
adk_root_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="multiagent_app",
    use_in_memory_services=True
)

# Add to FastAPI
add_adk_fastapi_endpoint(app, adk_root_agent, path="/")
```

### 3. Calendar Tool Function
```python
def book_calendar_appointment(
    tool_context: ToolContext,
    title: str,
    date: str,
    time: str
) -> Dict[str, str]:
    # Update state
    tool_context.state["current_booking"] = {
        "title": title,
        "date": date,
        "time": time
    }
    return {"status": "success"}
```

## Deployment Architecture

### Development (Single Process)
```
All agents in one Python process
├── Root Agent
├── Text Agent (in-process)
└── Calendar Agent (in-process)
```

### Production (Microservices)
```
Service 1: Root Agent Service
├── Root Agent
└── AgentTool (HTTP calls)

Service 2: Text Agent Service
└── Text Agent (HTTP endpoint)

Service 3: Calendar Agent Service
└── Calendar Agent (HTTP endpoint)
```

## Security Considerations

1. **API Keys**: Store in `.env`, never commit
2. **CORS**: Configure for frontend origins
3. **Rate Limiting**: Implement for production
4. **Input Validation**: Validate all user inputs
5. **State Isolation**: Ensure agent state isolation

## Performance Considerations

1. **Caching**: Cache LLM responses where appropriate
2. **Async Operations**: Use async/await for I/O
3. **Connection Pooling**: Reuse LLM connections
4. **State Management**: Efficient state storage
5. **Event Streaming**: Efficient SSE/WebSocket handling

## Monitoring & Logging

1. **Request Logging**: Log all user requests
2. **Routing Decisions**: Log which tool was used
3. **Performance Metrics**: Track response times
4. **Error Tracking**: Log and handle errors
5. **State Changes**: Log state updates

## Future Enhancements

1. **More Tool Agents**: Add specialized agents
2. **Agent Chaining**: Chain multiple agents
3. **Parallel Execution**: Run agents in parallel
4. **Persistent Storage**: Database for state
5. **Advanced Routing**: ML-based intent detection
