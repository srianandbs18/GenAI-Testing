"""Human in the Loop Investment Agent."""

from __future__ import annotations

from dotenv import load_dotenv
load_dotenv()
import os
import json
from typing import Dict, List, Any, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# ADK imports
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import FunctionTool, ToolContext
from google.adk.models import LlmResponse, LlmRequest
from google.genai import types
from google.adk.models.lite_llm import LiteLlm

DEFINE_INVESTMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "generate_investment_options",
        "description": "Generate a list of investment options (5-7 options) for a customer based on their requirements. Each option should include name, description, risk level, and minimum amount.",
        "parameters": {
            "type": "object",
            "properties": {
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the investment option (e.g., 'Real Estate Investment', 'Stock Portfolio')"
                            },
                            "description": {
                                "type": "string",
                                "description": "Brief description of the investment option"
                            },
                            "riskLevel": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Risk level of the investment"
                            },
                            "minimumAmount": {
                                "type": "number",
                                "description": "Minimum investment amount required"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["enabled"],
                                "description": "The status of the option, always 'enabled' initially"
                            }
                        },
                        "required": ["name", "description", "riskLevel", "minimumAmount", "status"]
                    },
                    "description": "An array of 5-7 investment option objects"
                }
            },
            "required": ["options"]
        }
    }
}

def generate_investment_options(
    tool_context: ToolContext,
    options: List[Dict[str, Any]]
) -> Dict[str, str]:
    """
    Generate investment options for the customer.
    
    Args:
        options: List of investment option dictionaries with name, description, riskLevel, minimumAmount, status
    
    Returns:
        Dict indicating success status and message
    """
    try:
        # Store options in state for UI synchronization
        tool_context.state["investment_options"] = options
        return {
            "status": "success", 
            "message": f"Generated {len(options)} investment options successfully",
            "options": options
        }
    except Exception as e:
        return {"status": "error", "message": f"Error generating options: {str(e)}"}

def on_before_agent(callback_context: CallbackContext):
    """
    Initialize investment options state if it doesn't exist.
    """
    if "investment_options" not in callback_context.state:
        callback_context.state["investment_options"] = []
    
    if not isinstance(callback_context.state.get("investment_options"), list):
        callback_context.state["investment_options"] = []

    return None

def before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Modify LLM request to include current state."""
    agent_name = callback_context.agent_name
    if agent_name == "InvestmentAgent":
        # Get current investment options from state
        options_json = "No options generated yet"
        if "investment_options" in callback_context.state and callback_context.state["investment_options"]:
            try:
                options_json = json.dumps(callback_context.state["investment_options"], indent=2)
            except Exception as e:
                options_json = f"Error serializing options: {str(e)}"
        
        prefix = f"""You are a helpful investment advisor assistant.
        Current investment options state: {options_json}
        When generating new investment options, use the generate_investment_options tool."""
        
        # Extract original instruction text
        original_instruction_text = ""
        if llm_request.config.system_instruction:
            if isinstance(llm_request.config.system_instruction, str):
                original_instruction_text = llm_request.config.system_instruction
            elif isinstance(llm_request.config.system_instruction, types.Content):
                if llm_request.config.system_instruction.parts:
                    original_instruction_text = llm_request.config.system_instruction.parts[0].text or ""
        
        modified_text = prefix + original_instruction_text
        
        # Use string format for LiteLlm/OpenRouter
        try:
            if hasattr(callback_context, 'agent') and hasattr(callback_context.agent, 'model'):
                is_litellm = isinstance(callback_context.agent.model, LiteLlm)
            else:
                is_litellm = True
        except:
            is_litellm = True
        
        if is_litellm:
            llm_request.config.system_instruction = modified_text
        else:
            llm_request.config.system_instruction = types.Content(
                role="system", 
                parts=[types.Part(text=modified_text)]
            )

    return None

def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Inspect model responses - let ADK handle natural flow."""
    return None

investment_agent = LlmAgent(
    name="InvestmentAgent",
    model=LiteLlm(
        model="openrouter/deepseek/deepseek-r1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1"
    ),
    instruction=f"""
    You are a human-in-the-loop investment advisor assistant that helps customers choose investment options with human oversight and approval.

    **Your Primary Role:**
    - Generate personalized investment options based on customer requirements
    - Facilitate human review and modification of generated options
    - Guide customers through investment selection process

    **When a customer requests investment advice:**
    1. ALWAYS call the `generate_investment_options` function to create 5-7 investment options
    2. Each option must include:
       - Name: Clear investment type name (e.g., "Real Estate Investment", "Stock Portfolio", "High-Yield Savings Account")
       - Description: Brief explanation of the investment
       - Risk Level: "low", "medium", or "high"
       - Minimum Amount: Minimum investment required
       - Status: Always "enabled" initially
    3. Consider the customer's stated budget, risk tolerance, and goals
    4. Provide diverse options across different risk levels and investment types

    **After generating options:**
    - Present the options clearly to the customer
    - Wait for customer to review and select/deselect options
    - If customer accepts the plan, provide next steps for selected investments
    - If customer rejects, ask what they would like to change. DO NOT regenerate options until they provide feedback.

    **When customer confirms selections:**
    - Acknowledge their selections
    - Provide guidance on next steps for each selected investment type
    - Offer to help with specific investment pages or detailed information

    **Investment Types to Consider:**
    - Real Estate Investment
    - Stock Portfolio
    - Savings Account
    - Fixed Deposits / CDs
    - Mutual Funds
    - Bonds
    - Cryptocurrency
    - Retirement Accounts (401k, IRA)
    - Commodities
    - ETFs

    **Key Guidelines:**
    - Always generate exactly 5-7 options
    - Make options diverse in risk and type
    - Consider customer's stated budget and preferences
    - Be clear and professional in your recommendations

    Tool reference: {json.dumps(DEFINE_INVESTMENT_TOOL, indent=2)}
    """,
    tools=[generate_investment_options],
    before_agent_callback=on_before_agent,
    before_model_callback=before_model_modifier,
    after_model_callback=simple_after_model_modifier
)

# Create ADK middleware agent instance
adk_investment_agent = ADKAgent(
    adk_agent=investment_agent,
    app_name="investment_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="ADK Middleware Investment Agent")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for testing connectivity."""
    return {
        "status": "healthy",
        "service": "ADK Investment Agent",
        "port": int(os.getenv("PORT", 8000))
    }

# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_investment_agent, path="/")

if __name__ == "__main__":
    import uvicorn

    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  Warning: OPENROUTER_API_KEY environment variable not set!")
        print("   Set it in your .env file: OPENROUTER_API_KEY=your-key-here")
        print("   Get a key from: https://openrouter.ai/")
        print()

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

