# MCP Integration & Tool Registration - Explained

## Your Questions Answered

### 1. Where MCP Tools Are Registered

**Location:** `adk/src/adk_agent.py` in the `_create_tools()` method (lines 184-217)

```python
def _create_tools(self):
    """Create FunctionTool instances for MCP tools"""
    
    # Define tool functions that call MCP
    def get_schedule_meeting_widget() -> str:
        """Fetches the schedule meeting widget schema from MCP server."""
        result = self.mcp_client.call_tool("get_schedule_meeting_widget", {})
        return json.dumps(result)
    
    # ... more tool functions ...
    
    # Wrap with FunctionTool and return
    return [
        FunctionTool(get_schedule_meeting_widget),
        FunctionTool(get_timezone_selector_widget),
        FunctionTool(list_available_widgets)
    ]
```

**Then registered in `_initialize_agent()`:**
```python
def _initialize_agent(self):
    tools = self._create_tools()  # Get the FunctionTool instances
    
    self.agent = LlmAgent(
        model=self.model,
        system_instruction=SYSTEM_INSTRUCTION,
        tools=tools,  # ← MCP tools registered here!
        api_key=self.api_key
    )
```

### 2. How MCP Communication Works

**Current Implementation:** Direct function calls (in-process)

```
┌─────────────────────────────────────────┐
│           ADK Agent Process             │
│                                         │
│  ┌─────────────┐      ┌──────────────┐│
│  │  ADK Agent  │──────→│ MCP Client   ││
│  │  (Gemini)   │      │              ││
│  └─────────────┘      └──────┬───────┘│
│                              │        │
│                              ↓        │
│                       ┌──────────────┐│
│                       │  MCP Server  ││
│                       │  Functions   ││
│                       │  (imported)  ││
│                       └──────────────┘│
└─────────────────────────────────────────┘
```

**Code:** `adk/src/mcp_client.py`
```python
# Import MCP server functions directly
from main import get_schedule_meeting_widget, ...

# Call them directly
def call_tool(self, tool_name: str, ...):
    if tool_name == "get_schedule_meeting_widget":
        return get_schedule_meeting_widget()  # ← Direct call!
```

**Why this approach for demo:**
- ✅ Simple - no HTTP server needed
- ✅ Fast - no network overhead
- ✅ Easy to debug
- ✅ Works immediately

---

## Alternative: HTTP-Based MCP (For Production)

If you want MCP as a separate HTTP server, here's how:

### Option A: HTTP with FastAPI

**MCP Server** (`mcp-server/main.py`):
```python
from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("Widget Schema Server")

@app.post("/mcp/call")
async def call_mcp_tool(request: dict):
    tool_name = request["tool"]
    # ... call MCP tool ...
    return result

# Run: uvicorn main:app --port 8001
```

**MCP Client** (`adk/src/mcp_client.py`):
```python
import aiohttp

class MCPClient:
    async def call_tool(self, tool_name: str, ...):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8001/mcp/call",
                json={"tool": tool_name, "args": arguments}
            ) as resp:
                return await resp.json()
```

**Flow:**
```
ADK Agent → HTTP POST → MCP Server (port 8001) → Response
```

### Option B: MCP Protocol (stdio/SSE)

**Official MCP Protocol:**
```python
# Using mcp package
from mcp import Client, StdioServerParameters

client = Client()
server_params = StdioServerParameters(
    command="python",
    args=["mcp-server/main.py"]
)

async with stdio_client(server_params) as (read, write):
    async with Client(read, write) as session:
        result = await session.call_tool("get_schedule_meeting_widget", {})
```

---

## Current Setup Summary

### ✅ What's Implemented

| Component | Method | Status |
|-----------|--------|--------|
| **Tool Registration** | `FunctionTool` wrapping MCP calls | ✅ Working |
| **MCP Communication** | Direct function import | ✅ Working |
| **ADK Integration** | `LlmAgent` with tools | ✅ Working |

### 📍 Tool Registration Flow

```
1. ADK Agent starts
   ↓
2. _create_tools() creates Python functions
   Each function calls self.mcp_client.call_tool(...)
   ↓
3. Each function wrapped with FunctionTool
   FunctionTool(get_schedule_meeting_widget)
   ↓
4. Tools array passed to LlmAgent constructor
   LlmAgent(..., tools=[tool1, tool2, tool3])
   ↓
5. Gemini model now knows about these tools
   Agent can call them via function calling
```

### 🔧 Tool Execution Flow

```
User Action: "connect"
   ↓
ADK Agent: "I need the schedule widget"
   ↓
Gemini decides: Call get_schedule_meeting_widget()
   ↓
FunctionTool executes the wrapped function
   ↓
Function calls: self.mcp_client.call_tool("get_schedule_meeting_widget", {})
   ↓
MCP Client: Directly imports and calls MCP server function
   ↓
MCP Server function returns widget schema
   ↓
Schema returned to ADK Agent
   ↓
Widget Populator fills schema with data
   ↓
Populated widget sent to UI
```

---

## Verification

**Check tool registration:**
```python
# In adk/src/adk_agent.py line 219-237
def _initialize_agent(self):
    tools = self._create_tools()  # ← Creates 3 FunctionTools
    
    self.agent = LlmAgent(
        model=self.model,
        system_instruction=SYSTEM_INSTRUCTION,
        tools=tools,  # ← Registers with agent
        api_key=self.api_key
    )
```

**Check MCP calls:**
```python
# In adk/src/adk_agent.py line 188-194
def get_schedule_meeting_widget() -> str:
    result = self.mcp_client.call_tool("get_schedule_meeting_widget", {})
    return json.dumps(result)

# FunctionTool wraps this
FunctionTool(get_schedule_meeting_widget)  # line 214
```

**Check MCP client:**
```python
# In adk/src/mcp_client.py line 27-30
def call_tool(self, tool_name: str, ...):
    if tool_name == "get_schedule_meeting_widget":
        return get_schedule_meeting_widget()  # Direct call!
```

---

## Summary

### Your Questions:

1. **"Where we registered mcp as a tool?"**
   - **Answer:** In `_create_tools()` method, MCP calls are wrapped in Python functions, then wrapped with `FunctionTool`, then registered with `LlmAgent` via the `tools` parameter.

2. **"Does MCP run as HTTP and agent calls via HTTP?"**
   - **Answer:** No, currently MCP functions are imported directly (same process). This is simpler for demo. Can be changed to HTTP if needed.

### Current Architecture:
- ✅ MCP functions: Direct import (in-process)
- ✅ Tool registration: via `FunctionTool` + `LlmAgent` constructor
- ✅ Works immediately without additional setup

### If You Want HTTP:
- Would need to run MCP server separately
- Add HTTP client in `mcp_client.py`
- More complex but production-ready

**The current setup works perfectly for your demo!** 🎉
