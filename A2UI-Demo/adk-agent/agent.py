"""
A2UI Demo Agent using Google ADK (Agent Development Kit)

This agent generates A2UI protocol messages based on user prompts using Google's ADK framework
with Gemini models. ADK provides a higher-level abstraction for building AI agents.
"""
import os
import json
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import Google ADK
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

# Configure Google ADK Agent
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Create ADK Agent for A2UI generation
a2ui_agent = None
if GOOGLE_API_KEY:
    try:
        # Create agent with Gemini model
        a2ui_agent = Agent(
            model='gemini-2.0-flash-exp',  # Try latest first
            name='a2ui_demo_agent',
            description='An AI agent that generates A2UI (Agent-to-User Interface) protocol messages based on user prompts.',
            instruction="""You are an AI agent that generates A2UI (Agent-to-User Interface) protocol messages.

Based on user prompts, you should generate JSON responses in this format:
{
  "type": "card|form|table",
  "data": { ... widget-specific data ... }
}

Available widget types:
1. "card" - For displaying information cards with title, content, image, and actions
2. "form" - For interactive forms with various input fields (text, email, select, textarea, checkbox)
3. "table" - For data tables with sortable columns and row actions

Generate appropriate A2UI JSON based on the user's request. If the user asks for a card, form, or table, generate the corresponding widget type with relevant, realistic data.

Return ONLY valid JSON, no additional text or markdown formatting.""",
            tools=[],
        )
        print("✅ Google ADK Agent initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize ADK agent: {e}")
        print("   Falling back to rule-based responses")
        a2ui_agent = None
else:
    print("⚠️  Warning: GOOGLE_API_KEY not found. Agent will use rule-based responses.")
    a2ui_agent = None

app = FastAPI(title="A2UI Demo Agent")

# Enable CORS for Angular client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    text: str
    a2ui: Dict[str, Any] | None = None


def generate_card_widget() -> Dict[str, Any]:
    """Generate a card widget A2UI message"""
    return {
        "type": "card",
        "data": {
            "title": "Product Information",
            "content": "This is a sample card widget demonstrating A2UI protocol. Cards are perfect for displaying structured information with optional images and actions.",
            "image": {
                "url": "https://via.placeholder.com/400x200?text=A2UI+Card+Widget",
                "alt": "Card widget example"
            },
            "footer": "A2UI Protocol v0.8",
            "actions": [
                {
                    "label": "Learn More",
                    "primary": True,
                    "data": {"action": "learn_more"}
                },
                {
                    "label": "Dismiss",
                    "primary": False
                }
            ]
        }
    }


def generate_form_widget() -> Dict[str, Any]:
    """Generate a form widget A2UI message"""
    return {
        "type": "form",
        "data": {
            "title": "Contact Form",
            "description": "Please fill out the form below. All fields marked with * are required.",
            "fields": [
                {
                    "name": "name",
                    "label": "Full Name",
                    "type": "text",
                    "placeholder": "Enter your full name",
                    "required": True
                },
                {
                    "name": "email",
                    "label": "Email Address",
                    "type": "email",
                    "placeholder": "your.email@example.com",
                    "required": True
                },
                {
                    "name": "subject",
                    "label": "Subject",
                    "type": "select",
                    "options": [
                        {"value": "general", "label": "General Inquiry"},
                        {"value": "support", "label": "Support Request"},
                        {"value": "feedback", "label": "Feedback"}
                    ],
                    "required": True
                },
                {
                    "name": "message",
                    "label": "Message",
                    "type": "textarea",
                    "placeholder": "Enter your message here...",
                    "rows": 5,
                    "required": True
                },
                {
                    "name": "newsletter",
                    "label": "Subscribe to newsletter",
                    "type": "checkbox",
                    "required": False
                }
            ],
            "submitLabel": "Submit Form"
        }
    }


def generate_table_widget() -> Dict[str, Any]:
    """Generate a data table widget A2UI message"""
    return {
        "type": "table",
        "data": {
            "title": "User Data Table",
            "description": "A sortable data table showing user information with action buttons.",
            "columns": [
                {"key": "id", "label": "ID", "sortable": True},
                {"key": "name", "label": "Name", "sortable": True},
                {"key": "email", "label": "Email", "sortable": True},
                {"key": "role", "label": "Role", "sortable": True},
                {"key": "active", "label": "Active", "sortable": True}
            ],
            "rows": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "role": "Admin",
                    "active": True
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "email": "jane.smith@example.com",
                    "role": "User",
                    "active": True
                },
                {
                    "id": 3,
                    "name": "Bob Johnson",
                    "email": "bob.johnson@example.com",
                    "role": "Editor",
                    "active": False
                },
                {
                    "id": 4,
                    "name": "Alice Williams",
                    "email": "alice.williams@example.com",
                    "role": "User",
                    "active": True
                },
                {
                    "id": 5,
                    "name": "Charlie Brown",
                    "email": "charlie.brown@example.com",
                    "role": "Viewer",
                    "active": True
                }
            ],
            "actions": [
                {
                    "label": "Edit",
                    "type": "primary",
                    "icon": "✏️"
                },
                {
                    "label": "Delete",
                    "type": "danger",
                    "icon": "🗑️"
                }
            ]
        }
    }


def generate_all_widgets() -> Dict[str, Any]:
    """Generate a response with all widgets"""
    return {
        "type": "multiple",
        "data": {
            "widgets": [
                generate_card_widget(),
                generate_form_widget(),
                generate_table_widget()
            ]
        }
    }


async def parse_user_prompt_with_ai(prompt: str) -> Optional[Dict[str, Any]]:
    """
    Use Google ADK Agent to intelligently parse user prompt and generate A2UI response
    """
    if not a2ui_agent:
        return None
    
    try:
        # Use ADK agent to generate response
        # The agent's instruction already guides it to generate A2UI JSON
        response = await a2ui_agent.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Try to parse JSON (might be wrapped in markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        a2ui_message = json.loads(response_text)
        return a2ui_message
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from ADK agent: {e}")
        print(f"Response was: {response_text[:200] if 'response_text' in locals() else 'N/A'}...")
        return None
    except Exception as e:
        print(f"Error using ADK agent: {e}")
        return None


async def parse_user_prompt(prompt: str) -> Dict[str, Any]:
    """
    Parse user prompt and generate appropriate A2UI response
    First tries ADK agent, falls back to rule-based if unavailable
    """
    # Try ADK agent first if available
    if a2ui_agent:
        ai_response = await parse_user_prompt_with_ai(prompt)
        if ai_response:
            return ai_response
    
    # Fallback to rule-based parsing
    prompt_lower = prompt.lower().strip()
    
    # Check for card-related prompts
    if any(keyword in prompt_lower for keyword in ["card", "show card", "display card", "card widget"]):
        return generate_card_widget()
    
    # Check for form-related prompts
    if any(keyword in prompt_lower for keyword in ["form", "show form", "display form", "form widget", "contact form"]):
        return generate_form_widget()
    
    # Check for table-related prompts
    if any(keyword in prompt_lower for keyword in ["table", "show table", "display table", "data table", "datatable"]):
        return generate_table_widget()
    
    # Check for all widgets
    if any(keyword in prompt_lower for keyword in ["all", "show all", "display all", "everything"]):
        return generate_all_widgets()
    
    # Default: return card widget
    return generate_card_widget()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "A2UI Demo Agent",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "health": "/"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint that processes user prompts and returns A2UI messages
    """
    try:
        prompt = request.message.strip()
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Generate A2UI response based on prompt using ADK agent
        a2ui_message = await parse_user_prompt(prompt)
        
        # Generate appropriate text response
        if a2ui_message.get("type") == "multiple":
            text = "Here are all three widget types:"
        elif a2ui_message.get("type") == "card":
            text = "Here's a card widget:"
        elif a2ui_message.get("type") == "form":
            text = "Here's a form widget:"
        elif a2ui_message.get("type") == "table":
            text = "Here's a data table widget:"
        else:
            text = "Here's the widget you requested:"
        
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

