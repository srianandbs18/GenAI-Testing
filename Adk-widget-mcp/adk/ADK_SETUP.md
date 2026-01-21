# Google ADK Setup

## Using Official google-adk Library

This implementation uses **google-adk==1.22.1** with `LlmAgent` and `FunctionTool`.

## Installation

```bash
cd adk
pip install -r requirements.txt
```

## API Key Setup

Get key from: https://aistudio.google.com/app/apikey

**Set environment variable:**
```bash
# Mac/Linux
export GOOGLE_API_KEY="your-key"

# Windows PowerShell
$env:GOOGLE_API_KEY="your-key"
```

## Running

```bash
python main.py
```

Expected output:
```
🤖 Google ADK Agent initialized
   Model: gemini-2.0-flash-exp
   Tools: 3 registered
```

## Architecture

```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk import Runner

# Define tool functions
def get_schedule_meeting_widget() -> str:
    """Fetches schedule meeting widget from MCP"""
    ...

# Create FunctionTools
tools = [
    FunctionTool(get_schedule_meeting_widget),
    FunctionTool(get_timezone_selector_widget),
    FunctionTool(list_available_widgets)
]

# Create agent
agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    system_instruction="You are a meeting scheduler...",
    tools=tools,
    api_key=api_key
)

# Create runner
runner = Runner(agent=agent)

# Run
response = runner.run("User wants to schedule meeting")
```

## Features

- ✅ Uses official `google-adk` package
- ✅ `LlmAgent` with Gemini model
- ✅ `FunctionTool` for MCP integration
- ✅ `Runner` for execution
- ✅ Fallback mode without API key

## Verified

- Package: `google-adk==1.22.1` ✅
- Imports: `LlmAgent`, `FunctionTool`, `Runner` ✅
- Tools: 3 MCP tools registered ✅
- Works with/without API key ✅

**Ready to use!** 🎉
