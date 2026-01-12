"""
Google ADK Agent with Real MCP Server Integration
Uses McpToolset to register MCP tools and communicate via stdio
Only uses Google ADK - no fallbacks
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import Google ADK and MCP tools
from google.adk.agents import Agent as ADKAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters

load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY must be set in environment variables or .env file")

MCP_SERVER_PATH = os.getenv("MCP_SERVER_PATH", None)

# Get absolute path to MCP server script
if not MCP_SERVER_PATH:
    # Default: assume mcp_server.py is in ../mcp-server/
    current_dir = Path(__file__).parent
    mcp_server_dir = current_dir.parent / "mcp-server"
    mcp_server_script = mcp_server_dir / "mcp_server.py"
    MCP_SERVER_PATH = str(mcp_server_script.absolute())

print(f"📁 MCP Server Path: {MCP_SERVER_PATH}")

# Initialize MCP tools
try:
    mcp_tools = [
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python',
                    args=[
                        MCP_SERVER_PATH,
                    ],
                ),
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['account_summary', 'deposit', 'withdrawal', 'general']
        )
    ]
    print("✅ MCP Toolset configured successfully")
except Exception as e:
    raise RuntimeError(f"Failed to configure MCP Toolset: {e}") from e

# Initialize Google ADK Agent
try:
    agent = ADKAgent(
        model='gemini-2.0-flash-exp',
        name='banking_agent',
        description='A banking assistant that uses MCP server widgets to help users',
        instruction="""You are a banking assistant that helps users with their banking needs.

You have access to the following widgets via MCP server tools:
1. account_summary - Shows account balance and recent transactions
2. deposit - Form for making deposits
3. withdrawal - Form for making withdrawals
4. general - General purpose widget for common questions

When a user asks about:
- Account balance, account summary, transactions → call account_summary tool
- Making a deposit, adding money, depositing → call deposit tool
- Making a withdrawal, taking money out, withdrawing → call withdrawal tool
- General questions, help, what can you do → call general tool

The MCP tools will return widget data. You should extract the widget data and return it in A2UI format.

A2UI format should be:
{
  "type": "account_summary|deposit|withdrawal|card",
  "data": { ... widget_data from MCP tool response ... }
}

Always call the appropriate MCP tool based on user intent.""",
        tools=mcp_tools
    )
    print("✅ Google ADK Agent initialized successfully with MCP tools")
except Exception as e:
    raise RuntimeError(f"Failed to initialize Google ADK Agent: {e}") from e

app = FastAPI(title="Banking Agent with MCP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:4201"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    text: str
    a2ui: Dict[str, Any] | None = None


async def process_with_ai(prompt: str) -> Optional[Dict[str, Any]]:
    """Process prompt using Google ADK agent with MCP tools"""
    try:
        # Use ADK agent with MCP tools
        # The agent will automatically call the appropriate MCP tool
        response = await agent.generate_content(prompt)
        
        # Parse response - ADK agent should return structured data
        response_text = response.text.strip()
        
        # Try to extract JSON from response
        try:
            # Look for JSON in the response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                # Try to parse the whole response as JSON
                json_str = response_text
            
            # Parse JSON
            result = json.loads(json_str)
            
            # If it's already in A2UI format, return it
            if "type" in result and "data" in result:
                return result
            
            # Otherwise, try to extract widget data from MCP tool response
            # MCP tools return data in format: {"widget_type": "...", "widget_data": {...}}
            if "widget_type" in result and "widget_data" in result:
                return {
                    "type": result["widget_type"],
                    "data": result["widget_data"]
                }
                
        except json.JSONDecodeError:
            # If response is not JSON, the agent might have called the tool but returned text
            # In this case, we need to handle it differently
            # For now, return None to trigger error handling
            print(f"⚠️  Could not parse JSON from agent response: {response_text[:200]}")
            return None
        
    except Exception as e:
        print(f"Error processing with AI: {e}")
        import traceback
        traceback.print_exc()
        return None


async def process_prompt(prompt: str) -> Dict[str, Any]:
    """Process user prompt and return A2UI response"""
    # Use Google ADK agent
    ai_response = await process_with_ai(prompt)
    
    if not ai_response:
        # If agent didn't return valid A2UI, return error widget
        return {
            "type": "card",
            "data": {
                "title": "Error",
                "content": "Unable to process request. Please try again or rephrase your question.",
                "actions": []
            }
        }
    
    return ai_response


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Banking Agent with MCP",
        "version": "1.0.0",
        "mcp_server_path": MCP_SERVER_PATH,
        "agent_type": "Google ADK with MCP",
        "mcp_enabled": True
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        prompt = request.message.strip()
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Process prompt and get widget
        a2ui_message = await process_prompt(prompt)
        
        # Generate appropriate text response
        widget_type = a2ui_message.get("type", "card")
        if widget_type == "account_summary":
            text = "Here's your account summary:"
        elif widget_type == "deposit":
            text = "I'll help you make a deposit:"
        elif widget_type == "withdrawal":
            text = "I'll help you make a withdrawal:"
        else:
            text = "How can I help you today?"
        
        return ChatResponse(
            text=text,
            a2ui=a2ui_message
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
