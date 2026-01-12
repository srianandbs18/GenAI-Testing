# Quick Start Guide

Get the demo running in 5 minutes!

## Step 1: Get API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy it

## Step 2: Setup MCP Server

```bash
cd demowithmcp/mcp-server
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python mcp_server.py
```

✅ MCP Server running on http://localhost:8002

## Step 3: Setup Agent

```bash
# In a NEW terminal
cd demowithmcp/agent
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "MCP_SERVER_URL=http://localhost:8002" >> .env

# Edit .env and paste your API key
python agent.py
```

✅ Agent running on http://localhost:8001

## Step 4: Setup Frontend

```bash
# In a NEW terminal
cd demowithmcp/frontend
npm install
npm run dev
# or
npm start
```

✅ Frontend running on http://localhost:4201

## Step 5: Test!

1. Open http://localhost:4201
2. Try: "Show me my account summary"
3. Try: "I want to make a deposit"
4. Try: "Help me withdraw money"

## Troubleshooting

**Agent can't connect to MCP?**
- Make sure MCP server is running first
- Check port 8002 is not in use

**Widgets not showing?**
- Check browser console (F12)
- Verify agent is running on port 8001

**AI not working?**
- Check .env file has correct API key
- Agent will use rule-based fallback if AI fails

## What's Next?

- Read the full README.md for architecture details
- Add more widgets to MCP server
- Customize the UI components
- Extend agent intelligence

