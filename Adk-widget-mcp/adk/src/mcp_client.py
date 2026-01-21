"""
MCP Client for ADK
Communicates with MCP server - uses direct imports for demo
"""
import sys
import os
from typing import Dict, Any

# Add mcp-server to path so we can import it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../mcp-server'))

try:
    # Import MCP server functions directly
    from main import get_schedule_meeting_widget, get_timezone_selector_widget, list_available_widgets
    MCP_AVAILABLE = True
except ImportError:
    print("⚠️  MCP server not accessible")
    MCP_AVAILABLE = False


class MCPClient:
    """Client to communicate with MCP server"""
    
    def __init__(self):
        self.mcp_available = MCP_AVAILABLE
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call an MCP tool and return the result
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments (optional)
        
        Returns:
            Tool execution result
        """
        if arguments is None:
            arguments = {}
        
        # Call MCP tools directly (they're in same process)
        if self.mcp_available:
            try:
                if tool_name == "get_schedule_meeting_widget":
                    return get_schedule_meeting_widget()
                elif tool_name == "get_timezone_selector_widget":
                    return get_timezone_selector_widget()
                elif tool_name == "list_available_widgets":
                    return list_available_widgets()
                else:
                    print(f"⚠️  Unknown MCP tool: {tool_name}")
            except Exception as e:
                print(f"❌ MCP tool error: {e}")
        
        # Fallback - return mock data
        print(f"⚠️  Using mock data for {tool_name}")
        return self._get_mock_response(tool_name)
    
    def _get_mock_response(self, tool_name: str) -> Dict[str, Any]:
        """Return mock widget schema for demo purposes"""
        if tool_name == "get_schedule_meeting_widget":
            return {
                "success": True,
                "widget": {
                    "widget_type": "schedule_meeting",
                    "schema_version": "1.0",
                    "metadata": {
                        "title": "Schedule Meeting",
                        "description": "Select date and time for meeting"
                    },
                    "properties": {
                        "timezone": {
                            "type": "timezone_display",
                            "label": "CURRENT TIME ZONE",
                            "value": "",
                            "editable": True,
                            "action": "change_timezone"
                        },
                        "date_selector": {
                            "type": "button_group",
                            "label": "SELECT A DATE",
                            "style": "horizontal",
                            "multi_select": False,
                            "options": []
                        },
                        "time_slots": {
                            "type": "button_list",
                            "label": "SELECT A TIME",
                            "style": "vertical",
                            "multi_select": False,
                            "options": []
                        },
                        "actions": {
                            "type": "action_buttons",
                            "buttons": [
                                {
                                    "id": "schedule",
                                    "label": "Schedule meeting",
                                    "style": "primary",
                                    "enabled": False,
                                    "action": "submit_schedule"
                                },
                                {
                                    "id": "close",
                                    "label": "Close",
                                    "style": "secondary",
                                    "enabled": True,
                                    "action": "close_widget"
                                }
                            ]
                        }
                    },
                    "styling": {
                        "theme": "dark",
                        "background_color": "#2D2D2D",
                        "text_color": "#FFFFFF"
                    }
                },
                "message": "Schedule meeting widget schema retrieved (mock)"
            }
        
        elif tool_name == "get_timezone_selector_widget":
            return {
                "success": True,
                "widget": {
                    "widget_type": "timezone_selector",
                    "schema_version": "1.0",
                    "metadata": {
                        "title": "Change Time Zone",
                        "description": "Select your preferred timezone"
                    },
                    "properties": {
                        "timezone_list": {
                            "type": "radio_list",
                            "label": "SELECT TIME ZONE",
                            "options": []
                        },
                        "actions": {
                            "type": "action_buttons",
                            "buttons": [
                                {
                                    "id": "confirm",
                                    "label": "Confirm",
                                    "style": "primary",
                                    "enabled": True,
                                    "action": "confirm_timezone"
                                },
                                {
                                    "id": "cancel",
                                    "label": "Cancel",
                                    "style": "secondary",
                                    "enabled": True,
                                    "action": "cancel_timezone"
                                }
                            ]
                        }
                    },
                    "styling": {
                        "theme": "dark",
                        "background_color": "#2D2D2D",
                        "text_color": "#FFFFFF"
                    }
                },
                "message": "Timezone selector widget schema retrieved (mock)"
            }
        
        return {"success": False, "error": "Unknown tool"}


def get_mcp_client() -> MCPClient:
    """Get MCP client instance"""
    return MCPClient()
