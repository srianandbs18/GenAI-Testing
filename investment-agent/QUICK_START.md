# Quick Start Guide - Running the Investment Agent UI

## Step-by-Step Instructions

### 1. Navigate to the Investment Agent Directory

```bash
cd investment-agent
```

### 2. Install UI Dependencies Only

Since you're running the agent separately, you only need UI dependencies:

```bash
# Install only UI dependencies (Next.js, CopilotKit, etc.)
npm install
```

**Note:** If you also need to set up the agent, run `npm run install:agent` separately.

### 3. Verify Environment Variables

Make sure you have a `.env` file in the `agent/` directory:

```bash
# Create .env file if it doesn't exist
cd agent
echo OPENROUTER_API_KEY=your-key-here > .env
echo PORT=8000 >> .env
cd ..
```

**Important:** Replace `your-key-here` with your actual OpenRouter API key!

### 4. Start the UI

Since you're running the agent separately, just start the UI:

```bash
npm run dev:ui
```

This starts:
- **Next.js UI** on `http://localhost:3000`

**Make sure your agent server is already running on `http://localhost:8000`**

---

**Alternative: Start Both Together**

If you want to run both from this project:

```bash
npm run dev
```

This starts both UI and agent in the same terminal.

### 5. Open the UI in Browser

Once both servers are running, open:

```
http://localhost:3000
```

### 6. Test the Investment Agent

1. **You'll see a chat interface** with a sidebar
2. **Try these sample queries:**
   - "I want to invest $50,000. What are my options?"
   - "Show me low-risk investment options for $25,000"
   - "I need a diversified investment portfolio for $100,000"

3. **The agent will:**
   - Generate 5-7 investment options
   - Display them in an interactive card format
   - Allow you to select/deselect options
   - Show risk levels and minimum amounts

4. **You can:**
   - Click checkboxes to enable/disable options
   - Click "Confirm" to accept the selected options
   - Click "Reject" to ask for different options

### 7. What to Expect

- **Investment Options Cards**: Each option shows:
  - Name (e.g., "Real Estate Investment")
  - Description
  - Risk Level badge (Low/Medium/High)
  - Minimum investment amount
  - Checkbox to enable/disable

- **Protocol Events**: The agent communicates via AG-UI protocol:
  - `STATE_SNAPSHOT` events contain investment options
  - `TOOL_CALL_START/END` events show when `generate_investment_options` is called
  - `TEXT_MESSAGE_CONTENT` events show agent responses

## Troubleshooting

### Agent Not Starting

**Check:**
- Python virtual environment exists: `agent/venv/` or `agent/.venv/`
- `.env` file exists with `OPENROUTER_API_KEY`
- Port 8000 is not already in use

**Fix:**
```bash
npm run install:agent  # Reinstall Python dependencies
```

### UI Not Starting

**Check:**
- Node.js dependencies installed: `node_modules/` exists
- Port 3000 is not already in use

**Fix:**
```bash
npm install  # Reinstall Node.js dependencies
```

### Connection Errors

**If you see "Failed to fetch" or connection errors:**

1. **Verify agent is running:**
   ```bash
   curl http://localhost:8000/health
   # Or open in browser: http://localhost:8000/health
   ```

2. **Check CORS configuration** in `agent/agent.py`:
   - Should include `http://localhost:3000` in `allow_origins`

3. **Verify agent name matches:**
   - In `src/app/api/copilotkit/route.ts`: `"investment_agent"`
   - In `src/app/layout.tsx`: `agent="investment_agent"`

### No Investment Options Showing

**Check:**
- Agent is calling `generate_investment_options` tool
- Check browser console for errors
- Check agent terminal for errors

**Debug:**
- Use the HTML test page: `test-agent-direct.html`
- Use Python script: `python test-agent-simple.py`

## Development Tips

- **Hot Reload**: Both UI and agent support hot reload
- **Logs**: Check both terminal windows for detailed logs
- **Browser Console**: Open DevTools (F12) to see protocol events
- **Network Tab**: Check `/api/copilotkit` requests in browser DevTools

## Next Steps

After testing the basic flow:
1. Test different investment amounts
2. Test different risk preferences
3. Try rejecting options and asking for changes
4. Verify state synchronization between agent and UI

