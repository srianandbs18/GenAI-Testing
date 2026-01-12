"""
Real MCP Server for Banking Widgets
Uses MCP protocol with stdio transport
Exposes widgets as MCP tools
"""
import asyncio
import json
import sys
from typing import Any, Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import widget definitions
from widgets import WIDGETS

# Create MCP server instance
server = Server("banking-widgets-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools (widgets) in MCP format
    """
    tools = []
    for widget_id, widget_info in WIDGETS.items():
        tools.append(
            Tool(
                name=widget_info["name"],
                description=widget_info["description"],
                inputSchema={
                    "type": "object",
                    "properties": {
                        "widget_type": {
                            "type": "string",
                            "description": f"The type of widget: {widget_info['widget_type']}"
                        }
                    },
                    "required": []
                }
            )
        )
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """
    Call a tool (widget) and return its A2UI data
    """
    if name not in WIDGETS:
        raise ValueError(f"Tool '{name}' not found. Available tools: {list(WIDGETS.keys())}")
    
    widget_info = WIDGETS[name]
    
    # Return widget data as JSON string in MCP TextContent format
    widget_data = {
        "widget_type": widget_info["widget_type"],
        "widget_data": widget_info["data"]
    }
    
    return [
        TextContent(
            type="text",
            text=json.dumps(widget_data, indent=2)
        )
    ]


async def main():
    """
    Run the MCP server using stdio transport
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
