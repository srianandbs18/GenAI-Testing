# A2UI Demo Agent

FastAPI-based agent that generates A2UI protocol messages based on user prompts using **Google ADK (Agent Development Kit)**.

## Features

- **Google ADK**: Uses Google's Agent Development Kit framework for building AI agents
- **AI-Powered**: Uses Gemini 2.0 Flash model through ADK to intelligently parse user prompts
- **Fallback Mode**: Works without API key using rule-based responses for demo purposes
- **A2UI Protocol**: Generates proper A2UI JSON messages for widget rendering

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get Google API Key (for ADK):
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy the key

4. Copy environment file:
```bash
cp .env.example .env
```

5. Update `.env` with your Google API key:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

   Note: `GEMINI_API_KEY` also works as a fallback.

## Running

```bash
python agent.py
```

The agent will start on `http://localhost:8001`

**Note**: The agent works in two modes:
- **AI Mode** (with API key): Uses Google ADK with Gemini to intelligently understand prompts and generate A2UI responses
- **Fallback Mode** (without API key): Uses rule-based keyword matching (still functional for demo)

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Process user prompts and return A2UI messages

## Example Request

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "show card"}'
```

## Model Used

- **Framework**: Google ADK (Agent Development Kit)
- **Model**: `gemini-2.0-flash-exp` (latest experimental via ADK)
- **No API Key**: Rule-based keyword matching fallback

## About Google ADK

Google ADK is a framework for building AI agents. It provides:
- Agent orchestration and management
- Tool integration capabilities
- Model abstraction (works with Gemini models)
- Higher-level agent development patterns

This implementation uses ADK to create an agent specifically designed for generating A2UI protocol messages.

