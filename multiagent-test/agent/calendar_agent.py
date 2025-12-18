"""
Calendar Agent - A2A Service with AG-UI support for calendar booking.

This agent handles calendar/booking requests and triggers calendar UI via AG-UI protocol.
Exposed as A2A service so it can be called by the root agent.
"""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()

import os
from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Google ADK imports
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, ToolContext

# AG-UI ADK integration
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint


# ============================================================================
# CALENDAR BOOKING TOOL
# ============================================================================

def book_calendar_appointment(
    tool_context: ToolContext,
    title: str,
    date: str,
    time: str,
    duration: int = 60
) -> Dict[str, str]:
    """
    Book an appointment and trigger calendar UI.
    
    This tool stores booking information in state, which triggers
    AG-UI STATE_SNAPSHOT events that the frontend can use to render calendar UI.
    
    Args:
        tool_context: Provides access to session state
        title: Appointment title/description
        date: Appointment date (YYYY-MM-DD format)
        time: Appointment time (HH:MM format)
        duration: Duration in minutes (default: 60)
    
    Returns:
        Dict with status and message
    """
    try:
        # Create booking object
        booking = {
            "title": title,
            "date": date,
            "time": time,
            "duration": duration,
            "status": "pending"
        }
        
        # Store in state - this triggers AG-UI STATE_SNAPSHOT event
        tool_context.state["current_booking"] = booking
        
        # Also maintain a list of bookings
        if "bookings" not in tool_context.state:
            tool_context.state["bookings"] = []
        tool_context.state["bookings"].append(booking)
        
        return {
            "status": "success",
            "message": f"Calendar opened for booking: {title} on {date} at {time}",
            "booking": booking
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error booking appointment: {str(e)}"
        }


# ============================================================================
# CALENDAR AGENT DEFINITION
# ============================================================================

calendar_agent = Agent(
    name="CalendarAgent",
    model="gemini-2.5-flash",
    tools=[book_calendar_appointment],
    instruction="""
    You are a calendar booking assistant. Help users book appointments and manage their calendar.
    
    Your capabilities:
    - Book appointments using the book_calendar_appointment tool
    - Understand date/time requests in natural language
    - Confirm booking details with users
    
    When a user wants to book an appointment:
    1. Extract the appointment details (title, date, time, duration)
    2. Call book_calendar_appointment with the details
    3. Confirm the booking with the user
    
    Be helpful and confirm all details before booking.
    """
)


# ============================================================================
# ADK AGENT WRAPPER - Bridge ADK agent with AG-UI protocol
# ============================================================================

# Wrap calendar agent with ADKAgent middleware for AG-UI protocol
adk_calendar_agent = ADKAgent(
    adk_agent=calendar_agent,
    app_name="calendar_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)


# ============================================================================
# FASTAPI APPLICATION - Web server setup
# ============================================================================

# Create FastAPI app
app = FastAPI(title="Calendar Agent - A2A Service with AG-UI")

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
        "service": "Calendar Agent",
        "port": int(os.getenv("CALENDAR_AGENT_PORT", 8001))
    }

# Agent card endpoint (for A2A discovery)
@app.get("/.well-known/agent-card.json")
async def agent_card():
    """Agent card for A2A discovery"""
    return {
        "name": "CalendarAgent",
        "description": "Calendar booking agent with AG-UI support",
        "version": "1.0.0",
        "capabilities": ["calendar_booking", "appointment_management"],
        "endpoints": {
            "ag_ui": "http://localhost:8001/",
            "a2a": "http://localhost:8001/a2a"  # A2A endpoint (if exposed)
        }
    }

# Add the AG-UI endpoint
add_adk_fastapi_endpoint(app, adk_calendar_agent, path="/")


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
    port = int(os.getenv("CALENDAR_AGENT_PORT", 8001))
    
    print(f"🚀 Starting Calendar Agent (A2A Service)")
    print(f"   Port: {port}")
    print(f"   AG-UI endpoint: http://localhost:{port}/")
    print(f"   Agent card: http://localhost:{port}/.well-known/agent-card.json")
    print(f"   Health check: http://localhost:{port}/health")
    print()
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port)
