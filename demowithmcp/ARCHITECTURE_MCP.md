# Real MCP Architecture

This document explains the **real MCP (Model Context Protocol)** implementation.

## Key Difference from Previous Version

### Previous (HTTP-based)
- MCP Server: FastAPI HTTP server
- Agent: HTTP calls to MCP server
- Not using official MCP protocol

### Current (Real MCP)
- MCP Server: Official MCP server using `mcp` Python package
- Agent: Registers MCP tools using `McpToolset`
- Communication: stdio transport (MCP protocol)
- Full MCP protocol compliance

## Architecture Flow

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│                  (Port 4201)                            │
│  - HTTP POST /chat                                       │
│  - Receives A2UI messages                                │
│  - Renders widgets dynamically                          │
└──────────────┬──────────────────────────────────────────┘
               │ HTTP POST
               ▼
┌─────────────────────────────────────────────────────────┐
│              Google ADK Agent                            │
│                  (Port 8001)                             │
│                                                           │
│  ┌─────────────────────────────────────────────────┐   │
│  │  McpToolset Registration                        │   │
│  │  - StdioConnectionParams                         │   │
│  │  - Spawns MCP server process                     │   │
│  │  - Registers tools:                              │   │
│  │    • account_summary                             │   │
│  │    • deposit                                     │   │
│  │    • withdrawal                                  │   │
│  │    • general                                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                           │
│  When user asks for widget:                              │
│  1. Analyzes query (AI)                                  │
│  2. Calls appropriate MCP tool                           │
│  3. Receives widget data                                 │
│  4. Converts to A2UI format                              │
│  5. Returns to frontend                                  │
└──────────────┬──────────────────────────────────────────┘
               │ MCP Protocol (stdio)
               │ Tool Call: account_summary
               ▼
┌─────────────────────────────────────────────────────────┐
│            Real MCP Server                               │
│         (Python mcp package)                            │
│  - Runs via stdio transport                             │
│  - Implements MCP protocol                               │
│  - Exposes tools:                                        │
│    • account_summary → returns widget data               │
│    • deposit → returns widget data                      │
│    • withdrawal → returns widget data                    │
│    • general → returns widget data                      │
└─────────────────────────────────────────────────────────┘
```

## MCP Server Implementation

### Using Official MCP Package

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("banking-widgets-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    # Return available tools
    pass

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Return widget data
    pass
```

### Transport: stdio

- MCP server communicates via standard input/output
- Agent spawns MCP server process
- Communication follows MCP JSON-RPC protocol

## Agent MCP Integration

### McpToolset Registration

```python
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StdioServerParameters
)

mcp_tools = [
    McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='python',
                args=['mcp_server.py'],
            ),
        ),
    )
]

agent = ADKAgent(
    model='gemini-2.0-flash-exp',
    tools=mcp_tools,  # MCP tools registered here
    ...
)
```

### How Agent Uses MCP Tools

1. **User Query**: "Show me my account balance"
2. **Agent Analysis**: Determines `account_summary` tool needed
3. **MCP Tool Call**: Agent calls `account_summary` tool via MCP protocol
4. **MCP Response**: Server returns widget data
5. **A2UI Conversion**: Agent converts to A2UI format
6. **Frontend Response**: Returns A2UI to React frontend

## Tool Response Format

MCP tools return data in this format:

```json
{
  "widget_type": "account_summary",
  "widget_data": {
    "title": "Account Summary",
    "accountNumber": "****1234",
    "balance": 12543.67,
    ...
  }
}
```

Agent converts this to A2UI format:

```json
{
  "type": "account_summary",
  "data": {
    "title": "Account Summary",
    "accountNumber": "****1234",
    "balance": 12543.67,
    ...
  }
}
```

## Benefits of Real MCP

1. **Standard Protocol**: Uses official MCP specification
2. **Tool Discovery**: Agent automatically discovers available tools
3. **Type Safety**: MCP provides structured tool definitions
4. **Extensibility**: Easy to add new tools/widgets
5. **Interoperability**: Works with any MCP-compatible client

## Troubleshooting

### MCP Server Not Starting

- Check Python path in `StdioServerParameters`
- Verify `mcp` package is installed
- Check MCP server script path

### Tools Not Available

- Verify MCP server is running
- Check tool names match exactly
- Review MCP server logs

### Agent Can't Call Tools

- Ensure `McpToolset` is properly configured
- Check stdio communication
- Verify Google ADK supports MCP tools

## Future Enhancements

- [ ] Add SSE transport support
- [ ] Implement MCP resources
- [ ] Add tool streaming
- [ ] Support multiple MCP servers
- [ ] Add tool filtering

