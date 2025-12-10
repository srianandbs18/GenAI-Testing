# Installation Guide - Separated UI and Agent

This project has **two separate layers** that can be installed and run independently:

1. **UI Layer** - Next.js frontend with CopilotKit
2. **Agent Layer** - Python FastAPI backend with ADK

## Installation Options

### Option 1: Install UI Only (Recommended if running agent separately)

```bash
# Install only UI dependencies
npm run install:ui
# Or simply:
npm install
```

This installs:
- Next.js and React dependencies
- CopilotKit packages
- TypeScript and build tools

**No Python dependencies are installed.**

### Option 2: Install Agent Only

```bash
# Install only Python agent dependencies
npm run install:agent
```

This:
- Creates Python virtual environment (`agent/venv/` or `agent/.venv/`)
- Installs Python packages from `agent/requirements.txt`

**No Node.js dependencies are installed.**

### Option 3: Install Both (Full Setup)

```bash
# Install UI dependencies
npm install

# Install agent dependencies
npm run install:agent
```

## Running Separately

### Run UI Only

```bash
npm run dev:ui
```

Then open: `http://localhost:3000`

**Note:** Make sure your agent server is running separately on `http://localhost:8000`

### Run Agent Only

```bash
npm run dev:agent
```

Agent will run on: `http://localhost:8000`

**Note:** Make sure UI is running separately on `http://localhost:3000` if you want to use the CopilotKit frontend.

### Run Both Together

```bash
npm run dev
```

This starts both UI and agent in the same terminal.

## Prerequisites

### For UI Only:
- Node.js 18+
- npm or pnpm

### For Agent Only:
- Python 3.12+
- pip

### For Both:
- Node.js 18+
- Python 3.12+
- OpenRouter API Key (for agent)

## Environment Setup

### Agent Environment Variables

Create `agent/.env` file:

```
OPENROUTER_API_KEY=your-key-here
PORT=8000
```

### UI Configuration

The UI connects to the agent via:
- `src/app/api/copilotkit/route.ts` - Points to `http://localhost:8000/`
- `src/app/layout.tsx` - Uses agent name `"investment_agent"`

## Verification

### Verify UI Installation

```bash
npm run dev:ui
# Should start Next.js dev server on port 3000
```

### Verify Agent Installation

```bash
npm run dev:agent
# Should start FastAPI server on port 8000
# Check: http://localhost:8000/health
```

## Troubleshooting

### UI Dependencies Issues

```bash
# Clean and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Agent Dependencies Issues

```bash
# Reinstall agent dependencies
npm run install:agent
```

### Port Conflicts

- **Port 3000 in use:** Change in `package.json` script: `"dev:ui": "next dev --turbopack -p 3001"`
- **Port 8000 in use:** Change in `agent/.env`: `PORT=8001` and update `route.ts` accordingly

