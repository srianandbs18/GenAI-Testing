"""
ADK Agent using google-adk library
Proper Google ADK implementation with LlmAgent and FunctionTool
"""
import os
import sys
from typing import Dict, Any, Optional
import json

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from google.adk.agents import LlmAgent
    from google.adk.tools import FunctionTool
    from google.adk import Runner
    ADK_AVAILABLE = True
except ImportError:
    print("⚠️  Google ADK not installed. Run: pip install google-adk")
    ADK_AVAILABLE = False
    LlmAgent = None
    FunctionTool = None
    Runner = None

from mcp_client import get_mcp_client
from widget_populator import get_widget_populator


# System instruction for the agent
SYSTEM_INSTRUCTION = """You are an intelligent meeting scheduling assistant powered by Google ADK.

YOUR ROLE:
- Help users schedule meetings by providing appropriate widgets
- Understand user intent from their messages and actions
- Call MCP tools to fetch widget schemas
- Maintain conversation context across multiple turns
- Handle follow-up actions intelligently

AVAILABLE MCP TOOLS:
1. get_schedule_meeting_widget() - Returns the schedule meeting widget schema
2. get_timezone_selector_widget() - Returns the timezone selector widget schema
3. list_available_widgets() - Lists all available widget types

YOUR WORKFLOW:

1. INITIAL CONNECTION (action: "connect"):
   - User has just connected to the meeting scheduler
   - Call get_schedule_meeting_widget() to fetch the main scheduling interface
   - The widget will be populated with next 5 business days and available time slots
   - Current timezone from session context will be displayed

2. DATE SELECTION (action: "select_date"):
   - User has selected a date from the available options
   - The selected date is stored in session context
   - Call get_schedule_meeting_widget() to refresh and show the selection highlighted
   - Keep the "Schedule meeting" button disabled until BOTH date and time are selected

3. TIME SELECTION (action: "select_time"):
   - User has selected a time slot
   - The selected time is stored in session context
   - Call get_schedule_meeting_widget() to refresh the widget
   - NOW enable the "Schedule meeting" button since both date AND time are selected

4. TIMEZONE CHANGE (action: "change_timezone") - **FOLLOW-UP ACTION**:
   - User clicked "CHANGE TIME ZONE" link - this is a FOLLOW-UP action
   - This is CRITICAL: User wants to switch to timezone selector temporarily
   - Call get_timezone_selector_widget() to show timezone options
   - IMPORTANT: The user's current date and time selections MUST be preserved in session!
   - Mark current timezone as selected in the widget
   - After timezone selection, user will return to schedule meeting widget

5. TIMEZONE CONFIRMATION (action: "confirm_timezone"):
   - User selected a new timezone and clicked "Confirm"
   - Session context is updated with new timezone (e.g., from ET to PT)
   - Call get_schedule_meeting_widget() to return to scheduling interface
   - CRITICAL: RESTORE the user's previous date and time selections from session!
   - Update time slot labels to show new timezone (e.g., "1:45 PM PT" instead of "1:45 PM ET")
   - Keep both date and time still selected
   - Keep "Schedule meeting" button enabled if both were selected before

6. TIMEZONE CANCELLATION (action: "cancel_timezone"):
   - User clicked "Cancel" on timezone selector
   - No changes to session context - timezone stays the same
   - Call get_schedule_meeting_widget() to return to scheduling interface
   - Keep all previous selections intact

7. MEETING SUBMISSION (action: "submit_schedule"):
   - User clicked "Schedule meeting" button
   - Both date and time must be selected (validated)
   - Extract meeting details from session context
   - Confirm the meeting is scheduled with full details

SESSION CONTEXT STRUCTURE:
The session context contains critical information you must preserve:
{
  "timezone": "Eastern Time (ET)",           // Current timezone full name
  "timezone_abbr": "ET",                     // Timezone abbreviation
  "selected_date": "TUE Sep 23",            // User's selected date (display)
  "selected_date_value": "2024-09-23",      // Date value for processing
  "selected_time": "1:45 PM ET",            // User's selected time (display)
  "selected_time_value": "13:45",           // Time value for processing
  "current_action": null or "selecting_timezone"  // Current flow state
}

CRITICAL RULES - MUST FOLLOW:

1. ALWAYS preserve session context during widget transitions
   - When switching from schedule widget to timezone selector, keep date/time
   - When returning from timezone selector, restore date/time selections

2. When user changes timezone:
   - Their date and time selections MUST be preserved
   - Only the timezone label changes (e.g., "1:45 PM ET" → "1:45 PM PT")
   - The actual time value stays the same
   - Both selections remain highlighted in the widget

3. Enable "Schedule meeting" button ONLY when:
   - Both date AND time are selected
   - Never enable with just one selection

4. For follow-up actions:
   - Update session context's current_action field appropriately
   - Remember the flow state (scheduling vs selecting_timezone)

5. Tool calling:
   - ALWAYS call the appropriate MCP tool to get widget schemas
   - NEVER create widget structures from scratch
   - Use MCP tools to get the empty schema, then it will be populated with data

6. Time zone handling:
   - Time slot labels MUST reflect the current timezone
   - When timezone changes, update all time labels accordingly
   - Preserve the underlying time value (only display changes)

RESPONSE EXPECTATIONS:
- Call the appropriate tool based on user action
- The widget schema will be populated with actual data by the system
- Focus on calling the right tool at the right time
- Preserve context across all interactions

CONVERSATION EXAMPLES:

Example 1 - Initial Connection:
User: "User connected and wants to schedule a meeting"
You: [Call get_schedule_meeting_widget()]
Result: Schedule widget appears with dates and times

Example 2 - Follow-up Action (IMPORTANT):
User: "User wants to change timezone (FOLLOW-UP ACTION). Current selections: TUE Sep 23, 1:45 PM"
You: [Call get_timezone_selector_widget()]
Result: Timezone picker appears, but date/time selections are preserved in session
After confirmation: [Call get_schedule_meeting_widget()]
Result: Back to schedule widget with PT times, previous selections restored

Example 3 - Context Preservation:
User: "User confirmed new timezone: PT. Previous selections were: TUE Sep 23, 1:45 PM ET"
You: [Call get_schedule_meeting_widget()]
Result: Schedule widget shows with:
  - Same date selected: TUE Sep 23 (still highlighted)
  - Same time selected: 1:45 PM PT (still highlighted, label updated)
  - Schedule button still enabled

Be intelligent, context-aware, and always preserve user selections. Your goal is to make scheduling meetings effortless."""


class ADKAgent:
    """Google ADK Agent using LlmAgent with FunctionTool"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
        self.model = model
        self.mcp_client = get_mcp_client()
        self.widget_populator = get_widget_populator()
        self.agent = None
        self.runner = None
        
        if ADK_AVAILABLE and self.api_key:
            self._initialize_agent()
        else:
            if not self.api_key:
                print("⚠️  No API key found. Using fallback mode.")
            print("   Set: export GOOGLE_API_KEY='your-key'")
    
    def _create_tools(self):
        """Create FunctionTool instances for MCP tools"""
        
        # Tool 1: Get schedule meeting widget
        def get_schedule_meeting_widget() -> str:
            """
            Fetches the schedule meeting widget schema from MCP server.
            Returns widget structure with empty options that need to be populated.
            """
            result = self.mcp_client.call_tool("get_schedule_meeting_widget", {})
            return json.dumps(result)
        
        # Tool 2: Get timezone selector widget
        def get_timezone_selector_widget() -> str:
            """
            Fetches the timezone selector widget schema from MCP server.
            Returns widget structure for timezone selection.
            """
            result = self.mcp_client.call_tool("get_timezone_selector_widget", {})
            return json.dumps(result)
        
        # Tool 3: List available widgets
        def list_available_widgets() -> str:
            """
            Lists all available widget types from the MCP server.
            """
            result = self.mcp_client.call_tool("list_available_widgets", {})
            return json.dumps(result)
        
        return [
            FunctionTool(get_schedule_meeting_widget),
            FunctionTool(get_timezone_selector_widget),
            FunctionTool(list_available_widgets)
        ]
    
    def _initialize_agent(self):
        """Initialize the Google ADK LlmAgent"""
        try:
            # Create tools
            tools = self._create_tools()
            
            # Create LlmAgent
            self.agent = LlmAgent(
                model=self.model,
                system_instruction=SYSTEM_INSTRUCTION,
                tools=tools,
                api_key=self.api_key
            )
            
            # Create Runner
            self.runner = Runner(agent=self.agent)
            
            print("🤖 Google ADK Agent initialized")
            print(f"   Model: {self.model}")
            print(f"   Tools: {len(tools)} registered")
            
        except Exception as e:
            print(f"❌ Failed to initialize ADK agent: {e}")
            import traceback
            traceback.print_exc()
            self.agent = None
            self.runner = None
    
    async def process_user_action(
        self,
        action: str,
        session_context: Dict[str, Any],
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process user action using the ADK agent
        
        Args:
            action: User action type
            session_context: Current session state
            data: Additional action data
            
        Returns:
            Response dictionary with widget or message
        """
        
        if not self.agent or not self.runner:
            return await self._fallback_processing(action, session_context, data)
        
        try:
            # Build prompt for the agent
            user_message = self._build_action_message(action, session_context, data)
            
            print(f"🧠 Agent processing: {action}")
            
            # Run the agent with the message
            response = self.runner.run(user_message)
            
            # The agent will call tools and we need to extract the result
            # Check if tools were called
            tool_name = self._determine_tool_for_action(action)
            
            if tool_name:
                print(f"🔧 Expected tool: {tool_name}")
                
                # Call MCP directly for now (agent should have called it via tools)
                mcp_result = self.mcp_client.call_tool(tool_name, {})
                
                if mcp_result.get("success"):
                    return await self._process_mcp_result(mcp_result, session_context)
            
            return await self._fallback_processing(action, session_context, data)
            
        except Exception as e:
            print(f"❌ Agent error: {e}")
            import traceback
            traceback.print_exc()
            return await self._fallback_processing(action, session_context, data)
    
    def _determine_tool_for_action(self, action: str) -> Optional[str]:
        """Determine which MCP tool to call based on action"""
        tool_map = {
            "connect": "get_schedule_meeting_widget",
            "select_date": "get_schedule_meeting_widget",
            "select_time": "get_schedule_meeting_widget",
            "change_timezone": "get_timezone_selector_widget",
            "confirm_timezone": "get_schedule_meeting_widget",
            "cancel_timezone": "get_schedule_meeting_widget",
        }
        return tool_map.get(action)
    
    def _build_action_message(
        self,
        action: str,
        session_context: Dict[str, Any],
        data: Optional[Dict[str, Any]]
    ) -> str:
        """Build message for the agent"""
        
        context_str = json.dumps(session_context, indent=2)
        
        messages = {
            "connect": f"User connected and wants to schedule a meeting.\nSession: {context_str}\n\nPlease fetch the schedule meeting widget.",
            "select_date": f"User selected date: {data.get('label') if data else 'unknown'}.\nSession: {context_str}\n\nRefresh the schedule widget.",
            "select_time": f"User selected time: {data.get('label') if data else 'unknown'}.\nSession: {context_str}\n\nRefresh the schedule widget.",
            "change_timezone": f"User wants to change timezone (FOLLOW-UP ACTION).\nSession: {context_str}\n\nShow timezone selector. PRESERVE date/time selections!",
            "confirm_timezone": f"User confirmed new timezone: {data.get('timezone') if data else 'unknown'}.\nSession: {context_str}\n\nShow schedule widget. RESTORE previous selections!",
            "cancel_timezone": f"User cancelled timezone change.\nSession: {context_str}\n\nShow schedule widget.",
        }
        
        return messages.get(action, f"Action: {action}\nSession: {context_str}")
    
    async def _process_mcp_result(
        self,
        mcp_result: Dict[str, Any],
        session_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process MCP tool result and populate widget"""
        
        if not mcp_result.get("success"):
            return {"type": "error", "message": "Failed to fetch widget from MCP"}
        
        widget_schema = mcp_result.get("widget")
        if not widget_schema:
            return {"type": "error", "message": "No widget in MCP response"}
        
        widget_type = widget_schema.get("widget_type")
        
        # Populate widget with session data
        if widget_type == "schedule_meeting":
            populated = self.widget_populator.populate_schedule_meeting_widget(
                widget_schema, session_context
            )
        elif widget_type == "timezone_selector":
            populated = self.widget_populator.populate_timezone_selector_widget(
                widget_schema, session_context
            )
        else:
            populated = widget_schema
        
        return {
            "type": "widget_render",
            "widget": populated
        }
    
    async def _fallback_processing(
        self,
        action: str,
        session_context: Dict[str, Any],
        data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Fallback processing without ADK agent"""
        
        print(f"⚠️  Fallback mode for: {action}")
        
        if action in ["connect", "select_date", "select_time", "confirm_timezone", "cancel_timezone"]:
            result = self.mcp_client.call_tool("get_schedule_meeting_widget", {})
            if result.get("success"):
                widget = self.widget_populator.populate_schedule_meeting_widget(
                    result["widget"], session_context
                )
                return {"type": "widget_render", "widget": widget}
        
        elif action == "change_timezone":
            result = self.mcp_client.call_tool("get_timezone_selector_widget", {})
            if result.get("success"):
                widget = self.widget_populator.populate_timezone_selector_widget(
                    result["widget"], session_context
                )
                return {"type": "widget_render", "widget": widget}
        
        elif action == "submit_schedule":
            return {
                "type": "meeting_scheduled",
                "meeting": {
                    "date": session_context.get("selected_date"),
                    "time": session_context.get("selected_time"),
                    "timezone": session_context.get("timezone")
                },
                "message": f"Meeting scheduled for {session_context.get('selected_date')} at {session_context.get('selected_time')}"
            }
        
        return {"type": "error", "message": f"Unknown action: {action}"}


def get_adk_agent(api_key: Optional[str] = None, model: str = "gemini-2.0-flash-exp") -> ADKAgent:
    """Create and return ADK agent instance"""
    return ADKAgent(api_key=api_key, model=model)
