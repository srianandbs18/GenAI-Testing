# Banking Widgets MCP Server

Real MCP (Model Context Protocol) server that provides banking-related widgets as tools using the official MCP protocol.

## Architecture

This is a **real MCP server** using the official `mcp` Python package, not just an HTTP API. It communicates via stdio transport following the MCP specification.

## Available Tools (Widgets)

1. **account_summary** - Displays account balance, account number, and recent transactions
2. **deposit** - Form for making deposits
3. **withdrawal** - Form for making withdrawals
4. **general** - General purpose card widget for common questions

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running

The MCP server is designed to run via stdio (standard input/output) and is typically invoked by the agent, not directly.

However, for testing, you can run:

```bash
python mcp_server.py
```

The server will communicate via stdio, so you won't see typical HTTP output.

## MCP Protocol

This server implements the MCP protocol with:

- **Transport**: stdio (standard input/output)
- **Tools**: Exposes 4 banking widgets as MCP tools
- **Tool Calling**: Returns widget data in structured JSON format

## Integration with Agent

The agent connects to this MCP server using:

```python
McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='python',
            args=['mcp_server.py'],
        ),
    ),
)
```

## Tool Response Format

Each tool returns widget data in this format:

```json
{
  "widget_type": "account_summary|deposit|withdrawal|card",
  "widget_data": {
    // Widget-specific data structure
  }
}
```

## Files

- `mcp_server.py` - Main MCP server implementation
- `widgets.py` - Widget definitions
- `requirements.txt` - Dependencies (includes `mcp` package)
