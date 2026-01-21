#!/usr/bin/env python3
"""
MCP Server for Widget Schemas
Provides widget contracts/structures for ADK to populate
"""
import json
import os
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Widget Schema Server")

# Get schemas directory
SCHEMAS_DIR = Path(__file__).parent / "schemas"


def load_schema(schema_name: str) -> dict:
    """Load a widget schema from JSON file"""
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_name}")
    
    with open(schema_path, 'r') as f:
        return json.load(f)


@mcp.tool()
def get_schedule_meeting_widget() -> dict:
    """
    Returns the complete schedule meeting widget schema.
    ADK will populate the date_selector options and time_slots options.
    
    Returns:
        dict: Widget schema with empty options arrays to be populated by ADK
    """
    schema = load_schema("schedule_meeting")
    return {
        "success": True,
        "widget": schema,
        "message": "Schedule meeting widget schema retrieved"
    }


@mcp.tool()
def get_timezone_selector_widget() -> dict:
    """
    Returns the timezone selector widget schema.
    ADK will populate the timezone_list options.
    
    Returns:
        dict: Widget schema for timezone selection
    """
    schema = load_schema("timezone_selector")
    return {
        "success": True,
        "widget": schema,
        "message": "Timezone selector widget schema retrieved"
    }


@mcp.tool()
def list_available_widgets() -> dict:
    """
    Lists all available widget schemas in the MCP server.
    
    Returns:
        dict: List of available widget types
    """
    widgets = []
    for schema_file in SCHEMAS_DIR.glob("*.json"):
        schema = load_schema(schema_file.stem)
        widgets.append({
            "name": schema_file.stem,
            "widget_type": schema.get("widget_type"),
            "version": schema.get("schema_version"),
            "title": schema.get("metadata", {}).get("title")
        })
    
    return {
        "success": True,
        "widgets": widgets,
        "count": len(widgets)
    }


if __name__ == "__main__":
    # Run MCP server
    print("🚀 Starting MCP Widget Schema Server...")
    print("📦 Available tools:")
    print("   - get_schedule_meeting_widget()")
    print("   - get_timezone_selector_widget()")
    print("   - list_available_widgets()")
    
    mcp.run(transport="stdio")
