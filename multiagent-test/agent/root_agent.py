"""
Root Agent - Multi-Agent Orchestrator using A2A protocol.

This agent routes user requests to appropriate specialized agents:
- Text Agent: Local agent via AgentTool (for general queries)
- Calendar Agent: Remote agent via A2A protocol (for booking/appointments)
"""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Google ADK imports
from google.adk.agents import Agent
from google.adk.tools import AgentTool

# AG-UI ADK integration
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Import text agent (local)
from agent.text_agent import text_agent

# Try to import RemoteA2aAgent (may not be available in all ADK versions)
try:
    from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
    A2A_AVAILABLE = True
except ImportError:
    # Fallback: Use AgentTool with HTTP if RemoteA2aAgent not available
    A2A_AVAILABLE = False
    print("⚠️  RemoteA2aAgent not available. Using fallback approach.")


# ============================================================================
# CREATE TOOLS
# ============================================================================

# Tool 1: Text Responder (Local Agent via AgentTool)
# Note: AgentTool doesn't take 'name' parameter - tool name comes from agent.name
text_tool = AgentTool(agent=text_agent)

# Tool 2: Calendar Agent (Remote A2A Agent)
if A2A_AVAILABLE:
    try:
        calendar_a2a_agent = RemoteA2aAgent(
            name="CalendarAgent",
            description="Calendar booking agent with AG-UI support",
            agent_card="http://localhost:8001/.well-known/agent-card.json"
        )
        # AgentTool doesn't take 'name' parameter - tool name comes from agent.name
        calendar_tool = AgentTool(agent=calendar_a2a_agent)
        print("✅ A2A Calendar Agent configured")
    except Exception as e:
        print(f"⚠️  Failed to create A2A agent: {e}")
        print("   Calendar agent will not be available")
        calendar_tool = None
else:
    # Fallback: Create a simple tool that returns a message
    def call_calendar_fallback(tool_context, user_message: str):
        """Calendar booking (fallback - A2A not available). 
        Calendar agent is not available. Please connect directly to http://localhost:8001/"""
        return {
            "status": "info",
            "message": "Calendar agent is not available. Please connect directly to http://localhost:8001/"
        }
    
    from google.adk.tools import FunctionTool
    # FunctionTool only accepts 'func' parameter - name comes from function name, description from docstring
    calendar_tool = FunctionTool(func=call_calendar_fallback)


# ============================================================================
# ROOT AGENT DEFINITION
# ============================================================================

# Collect available tools
tools = [text_tool]
if calendar_tool:
    tools.append(calendar_tool)

root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    tools=tools,
    instruction="""
    You are a routing assistant that helps users by delegating to specialized agents.
    
    Your job is to analyze user requests and route them to the appropriate agent:
    
    1. **Calendar/Booking Requests:**
       - Keywords: calendar, book, appointment, schedule, meeting, reserve, slot, time
       - Action: Use the CalendarAgent tool (A2A agent)
       - Example: "I want to book an appointment", "Schedule a meeting", "Book a slot"
    
    2. **General Queries:**
       - Everything else: questions, explanations, information requests
       - Action: Use the TextResponder tool (local agent)
       - Example: "What is Python?", "Explain quantum computing", "Tell me a joke"
    
    **Routing Rules:**
    - Always analyze the user's intent first
    - If the request involves calendar/booking/scheduling → use CalendarAgent
    - For all other requests → use TextResponder
    - Explain which tool you're using and why
    
    Be helpful and clear in your responses.
    """
)


# ============================================================================
# ADK AGENT WRAPPER - Bridge ADK agent with AG-UI protocol
# ============================================================================

# Wrap root agent with ADKAgent middleware for AG-UI protocol
adk_root_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="root_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)


# ============================================================================
# FASTAPI APPLICATION - Web server setup
# ============================================================================

# Create FastAPI app
app = FastAPI(title="Root Agent - A2A Multi-Agent System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Root Agent",
        "port": int(os.getenv("ROOT_AGENT_PORT", 8000)),
        "tools": {
            "TextResponder": "available",
            "CalendarAgent": "available" if calendar_tool else "unavailable"
        }
    }

# Add the AG-UI endpoint
add_adk_fastapi_endpoint(app, adk_root_agent, path="/")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Check for required environment variable
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("   Set it in your .env file: GOOGLE_API_KEY=your-key-here")
        print("   Get a key from: https://aistudio.google.com/app/apikey")
        print()
    
    # Get port from environment or use default
    port = int(os.getenv("ROOT_AGENT_PORT", 8000))
    
    print(f"🚀 Starting Root Agent (Multi-Agent Orchestrator)")
    print(f"   Port: {port}")
    print(f"   AG-UI endpoint: http://localhost:{port}/")
    print(f"   Health check: http://localhost:{port}/health")
    print()
    print(f"📋 Available Tools:")
    print(f"   ✅ TextResponder (local agent)")
    if calendar_tool:
        print(f"   ✅ CalendarAgent (A2A agent)")
    else:
        print(f"   ⚠️  CalendarAgent (unavailable - A2A not configured)")
    print()
    print(f"💡 Make sure Calendar Agent is running on port 8001 for full functionality")
    print()
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port)
