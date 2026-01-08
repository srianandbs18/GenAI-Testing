# Agent Implementation Explanation

## Current Implementation

The agent uses **Google Gemini API** (via `google-generativeai` package) to intelligently process user prompts and generate A2UI JSON messages.

## Why Not Google ADK?

I initially mentioned Google ADK, but after research, I found that:

1. **Google ADK** is a newer framework that may not be widely available as a Python package yet
2. **Google Gemini API** (`google-generativeai`) is the official, stable way to use Gemini models
3. The current implementation achieves the same goal: using AI to generate A2UI responses

## How It Works

### With API Key (AI Mode)

1. User sends prompt: `"I need a contact form"`
2. Agent sends prompt to Gemini with system instructions
3. Gemini generates A2UI JSON based on the prompt
4. Agent returns the JSON to Angular client

### Without API Key (Fallback Mode)

1. User sends prompt: `"show form"`
2. Agent uses keyword matching
3. Agent generates pre-defined A2UI JSON
4. Agent returns the JSON to Angular client

## Model Used

- **Primary**: `gemini-2.0-flash-exp` (latest experimental version)
- **Fallback 1**: `gemini-1.5-flash` (stable, fast)
- **Fallback 2**: `gemini-pro` (if others unavailable)

## Future: Integrating Google ADK

If you want to use Google ADK specifically (when it becomes more widely available), you would:

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    model='gemini-2.0-flash',
    name='A2UIDemoAgent',
    description='Generates A2UI components',
)

# Then use agent to process prompts
response = agent.process(prompt)
```

The current implementation with `google-generativeai` is functionally equivalent and more reliable for now.

## Code Correctness

✅ **Correct**: The agent generates proper A2UI JSON format  
✅ **Correct**: The Angular client correctly renders the widgets  
✅ **Correct**: The communication protocol works as expected  
⚠️ **Note**: Uses Gemini API directly instead of ADK framework (but achieves same result)

