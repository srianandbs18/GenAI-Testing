# Investment Options Human-in-the-Loop Agent

A human-in-the-loop agent that presents investment options to customers and dynamically updates the UI based on their selections.

## Features

- **Investment Options Generation**: Agent generates personalized investment recommendations
- **Human-in-the-Loop**: Users can select/deselect options before confirming
- **Dynamic UI**: Interface changes based on selected investment types
- **Investment Pages**: Dedicated pages for each investment type (Real Estate, Stocks, Savings, etc.)

## Project Structure

```
investment-agent/
├── agent/
│   ├── agent.py          # Human-in-the-loop investment agent
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables (OPENROUTER_API_KEY)
├── src/
│   ├── app/
│   │   ├── page.tsx      # Main investment UI with human-in-the-loop
│   │   ├── layout.tsx    # CopilotKit wrapper
│   │   ├── api/
│   │   │   └── copilotkit/
│   │   │       └── route.ts  # CopilotKit API route
│   │   └── globals.css
├── scripts/
│   ├── run-agent.js      # Cross-platform agent runner
│   └── setup-agent.js    # Agent setup script
├── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.12+
- OpenRouter API Key

### Installation

#### Install UI Only (if running agent separately)

```bash
npm install
# Or explicitly:
npm run install:ui
```

#### Install Agent Only (if running UI separately)

```bash
npm run install:agent
```

#### Install Both (Full Setup)

```bash
# Install UI dependencies
npm install

# Install Python agent dependencies
npm run install:agent
```

#### Environment Setup

Create `.env` file in `agent/` directory:
```
OPENROUTER_API_KEY=your-key-here
PORT=8000
```

**See [INSTALL.md](./INSTALL.md) for detailed installation instructions.**

### Running

#### Run UI Only

```bash
npm run dev:ui
```

Opens at: `http://localhost:3000`

**Note:** Make sure agent is running separately on `http://localhost:8000`

#### Run Agent Only

```bash
npm run dev:agent
```

Runs on: `http://localhost:8000`

**Note:** Make sure UI is running separately if you want to use the CopilotKit frontend

#### Run Both Together

```bash
npm run dev
```

Starts both UI and agent in the same terminal.

## Usage

### Using the CopilotKit UI

1. Open the app at `http://localhost:3000`
2. Ask the agent: "I want to invest $50,000"
3. Agent will generate investment options
4. Select/deselect options
5. Click "Confirm" to proceed
6. UI will dynamically show relevant investment pages based on selections

### Testing the Agent Directly (Without UI)

You can test the investment agent's AG-UI protocol events directly without the CopilotKit UI:

#### Option 1: HTML Test Page

1. **Start the agent server:**
   ```bash
   npm run dev:agent
   ```

2. **Serve the HTML test page:**
   - **Windows:** Run `serve-test.html.bat`
   - **Mac/Linux:** Run `./serve-test.html.sh`
   - **Or manually:** `python -m http.server 8080`

3. **Open in browser:**
   - Navigate to `http://localhost:8080/test-agent-direct.html`
   - Enter your investment request
   - Click "Send Request"
   - View protocol events and investment options

#### Option 2: Python Test Script

```bash
# Basic test
python test-agent-simple.py

# Custom message
python test-agent-simple.py --message "I want to invest $25,000 in low-risk options"

# Custom agent URL
python test-agent-simple.py --url "http://localhost:8000/" --message "Show me investment options"
```

The test tools will:
- ✅ Check agent health
- ✅ Send AG-UI protocol requests
- ✅ Parse Server-Sent Events (SSE) stream
- ✅ Extract and display investment options
- ✅ Show all protocol events
- ✅ Analyze tool calls and state snapshots

## Investment Options

The agent can generate options for:
- Real Estate Investment
- Stock Portfolio
- Savings Account
- Fixed Deposits
- Mutual Funds
- Bonds
- Cryptocurrency
- And more...


