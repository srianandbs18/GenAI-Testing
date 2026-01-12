# Banking Demo with MCP

A demo application showcasing dynamic UI generation using Google ADK Agent with MCP (Model Context Protocol) server. The agent intelligently selects banking widgets (Account Summary, Deposit, Withdrawal) based on user queries, and the UI dynamically updates to display the appropriate widget.

## Architecture

```
┌─────────────────┐
│  Angular Client │  (Port 4201)
│  (Frontend)     │
└────────┬────────┘
         │ HTTP POST /chat
         ▼
┌─────────────────┐
│  ADK Agent      │  (Port 8001)
│  (Google ADK)   │
└────────┬────────┘
         │ HTTP GET/POST
         ▼
┌─────────────────┐
│  MCP Server     │  (Port 8002)
│  (Widgets)      │
└─────────────────┘
```

## Components

1. **MCP Server** (`mcp-server/`) - **Real MCP server** using official MCP protocol
   - Uses `mcp` Python package
   - Communicates via stdio transport
   - Exposes 4 banking widgets as MCP tools:
     - Account Summary widget
     - Deposit widget
     - Withdrawal widget
     - General widget

2. **ADK Agent** (`agent/`) - Google ADK agent that:
   - **Registers MCP tools** using `McpToolset` with `StdioConnectionParams`
   - Connects to MCP server via stdio
   - Analyzes user queries using AI
   - **Calls MCP tools** to get widget data
   - Converts MCP tool responses to A2UI format
   - Returns A2UI to frontend

3. **React Frontend** (`frontend/`) - Reacts to agent responses
   - Chat interface
   - Dynamic widget rendering
   - Banking-specific widgets

## Prerequisites

- Python 3.11+
- Node.js 18+
- Angular CLI (`npm install -g @angular/cli`)
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Setup Instructions

### 1. Setup MCP Server

```bash
cd mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes mcp package)
pip install -r requirements.txt
```

**Note:** The MCP server uses the official `mcp` Python package and communicates via stdio. It's typically invoked by the agent, not run directly.

### 2. Setup ADK Agent

```bash
cd agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (includes google-adk, mcp)
pip install -r requirements.txt

# Create .env file
# Copy env.example and add your API key:
# GOOGLE_API_KEY=your_api_key_here
# MCP_SERVER_PATH=/path/to/mcp-server/mcp_server.py (optional, auto-detected)
```

**Note:** 
- The agent uses **only Google ADK** (no fallbacks)
- Registers MCP tools using `McpToolset` and connects to the MCP server via stdio
- The agent will automatically spawn the MCP server process
- Requires `GOOGLE_API_KEY` or `GEMINI_API_KEY` to be set

**Note:** The agent will work with either:
- `google.adk` (if available)
- `google-generativeai` (fallback, included in requirements)
- Rule-based fallback (if no API key)

### 3. Setup React Frontend

```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

You need to run **two services** (MCP server is spawned by the agent):

### Terminal 1: ADK Agent

```bash
cd demowithmcp/agent
source venv/bin/activate  # On Windows: venv\Scripts\activate
python agent.py
```

Agent will:
- Start on `http://localhost:8001`
- Automatically spawn MCP server process via stdio
- Register MCP tools using `McpToolset`

### Terminal 2: React Frontend

```bash
cd demowithmcp/frontend
npm install  # First time only
npm run dev
# or
npm start
```

Frontend will start on `http://localhost:4201`

## Usage

1. Open `http://localhost:4201` in your browser
2. Try these queries:
   - "Show me my account summary"
   - "I want to make a deposit"
   - "Help me withdraw money"
   - "What can you do?"
   - "Show my balance"

The agent will:
1. Analyze your query
2. Connect to MCP server
3. Select appropriate widget
4. Return A2UI format
5. Frontend renders the widget dynamically

## Available Widgets

### 1. Account Summary
- Displays account balance
- Shows account number and type
- Lists recent transactions
- Trigger: "account", "balance", "summary", "transactions"

### 2. Deposit
- Form for making deposits
- Amount, source, memo fields
- Trigger: "deposit", "add money", "transfer in"

### 3. Withdrawal
- Form for making withdrawals
- Amount, destination, memo fields
- Trigger: "withdraw", "withdrawal", "take out"

### 4. General
- General purpose card widget
- Help and navigation
- Trigger: "help", "what can you do", general questions

## How It Works

### 1. User Query
User types: "Show me my account balance"

### 2. Agent Processing
- Agent receives query via HTTP POST
- Google ADK agent analyzes intent
- Determines widget needed: `account_summary`

### 3. MCP Tool Call
- Agent **calls MCP tool** `account_summary` via stdio
- MCP server (spawned by agent) processes tool call
- MCP server returns widget data in structured format:
  ```json
  {
    "widget_type": "account_summary",
    "widget_data": {...}
  }
  ```

### 4. A2UI Conversion
- Agent converts MCP tool response to A2UI format
- Returns A2UI message to frontend:
  ```json
  {
    "type": "account_summary",
    "data": {...}
  }
  ```

### 5. Dynamic Rendering
- Frontend receives A2UI message
- A2UI renderer detects widget type
- Renders appropriate React component dynamically

## API Endpoints

### ADK Agent (Port 8001)

- `GET /` - Health check (shows MCP status)
- `POST /chat` - Process user query and return A2UI response

**Note:** MCP server communication happens via stdio, not HTTP endpoints.

## Challenges & Solutions

### Challenge 1: Google ADK Installation
**Issue:** Google ADK package must be installed.

**Solution:** 
- Install `google-adk` from requirements.txt: `pip install -r requirements.txt`
- Ensure `GOOGLE_API_KEY` is set in environment or `.env` file

### Challenge 2: MCP Protocol Implementation
**Issue:** Full MCP protocol can be complex.

**Solution:**
- Simplified MCP server using FastAPI
- HTTP-based tool calling (not full MCP transport)
- Easy to extend with more widgets

### Challenge 3: Dynamic Widget Selection
**Issue:** Agent needs to intelligently select widgets.

**Solution:**
- AI-powered intent recognition
- Keyword-based fallback
- Clear widget descriptions in MCP server

### Challenge 4: A2UI Format Consistency
**Issue:** Ensuring consistent A2UI format across widgets.

**Solution:**
- Standardized widget data structure
- Type-based rendering in frontend
- Clear widget type definitions

## Extending the Demo

### Adding New Widgets

1. **Add to MCP Server** (`mcp-server/mcp_server.py`):
```python
WIDGETS["new_widget"] = {
    "name": "new_widget",
    "description": "Description of new widget",
    "widget_type": "new_widget",
    "data": {...}
}
```

2. **Update Agent** (`agent/agent.py`):
   - Add keywords in `determine_widget_from_prompt()`
   - Update AI instructions

3. **Create Frontend Component**:
   - Create widget component in `frontend/src/app/components/widgets/`
   - Add to `a2ui-renderer.component.ts`

### Improving Agent Intelligence

- Add more context to AI prompts
- Implement conversation history
- Add widget-specific validation
- Implement multi-step workflows

## Troubleshooting

### Agent can't connect to MCP server
- Check MCP server is running on port 8002
- Verify `MCP_SERVER_URL` in agent `.env`
- Check firewall/network settings

### Widgets not rendering
- Check browser console for errors
- Verify A2UI message format
- Ensure widget component is registered in renderer

### AI not working
- Verify `GOOGLE_API_KEY` is set in `.env` file
- Check API key is valid
- Ensure `google-adk` package is installed: `pip install google-adk`
- Check that Google ADK can import: `python -c "from google.adk.agents import Agent"`

## Future Enhancements

- [ ] Full MCP protocol implementation
- [ ] WebSocket support for real-time updates
- [ ] Widget state persistence
- [ ] Multi-step workflows
- [ ] Widget validation and error handling
- [ ] Authentication and user sessions
- [ ] More banking widgets (transfers, bill pay, etc.)

## License

This is a demo application for educational purposes.

## Contributing

Feel free to extend this demo with more widgets, better AI integration, or improved UI/UX!

