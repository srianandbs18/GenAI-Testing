# Investment Options Human-in-the-Loop Agent - Implementation Proposal

## Overview
Create a human-in-the-loop agent that presents investment options to customers and dynamically updates the UI based on their selections. This will be a separate project from `adk-ag-ui-demo`.

## Architecture

### Backend Agent (`investment-agent/agent/agent.py`)
- **Model**: OpenRouter (DeepSeek R1) via LiteLlm (same as agent.py)
- **Tool**: `generate_investment_options` - generates a list of investment options
- **Pattern**: Human-in-the-loop where:
  1. Agent generates investment options
  2. User selects/deselects options
  3. User confirms or rejects
  4. Based on selection, agent provides next steps or redirects to specific investment pages

### Frontend UI (`investment-agent/src/app/page.tsx`)
- **Framework**: Next.js with CopilotKit
- **Components**:
  - Investment options list (selectable checkboxes)
  - Dynamic content area that changes based on selection
  - Confirmation/Rejection buttons
  - Investment-specific pages/sections (e.g., Real Estate, Stocks, Savings, etc.)

## Investment Options Structure

Each investment option will have:
- `name`: Investment type (e.g., "Real Estate", "Stock Portfolio", "Savings Account")
- `description`: Brief description
- `status`: "enabled" | "disabled" | "executing"
- `riskLevel`: "low" | "medium" | "high"
- `minimumAmount`: Minimum investment required

## Flow

1. **User Request**: "I want to invest $50,000"
2. **Agent Response**: Generates 5-7 investment options using `generate_investment_options` tool
3. **UI Display**: Shows options as selectable cards with details
4. **User Selection**: User enables/disables options
5. **User Confirmation**: User clicks "Confirm" or "Reject"
6. **Agent Processing**: 
   - If confirmed: Provides next steps for selected investments
   - If rejected: Asks what to change
7. **Dynamic UI Update**: Based on selections, show relevant investment pages

## Implementation Plan

### Phase 1: Backend Agent
1. Create `investment-agent/agent/agent.py` with:
   - OpenRouter configuration (like agent.py)
   - `generate_investment_options` tool
   - Human-in-the-loop instruction
   - FastAPI setup with CORS and health endpoint

### Phase 2: Frontend UI
1. Create Next.js app structure
2. Implement investment options display component
3. Add dynamic routing/content based on selections
4. Integrate CopilotKit with useHumanInTheLoop

### Phase 3: Investment Pages
1. Create pages for each investment type:
   - Real Estate investment page
   - Stock Portfolio page
   - Savings Account page
   - etc.
2. Dynamic navigation based on user selections

## File Structure

```
investment-agent/
├── agent/
│   ├── agent.py          # Human-in-the-loop investment agent
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
├── src/
│   ├── app/
│   │   ├── page.tsx      # Main investment UI
│   │   ├── layout.tsx    # CopilotKit wrapper
│   │   ├── api/
│   │   │   └── copilotkit/
│   │   │       └── route.ts  # CopilotKit API route
│   │   ├── investments/      # Dynamic investment pages
│   │   │   ├── real-estate/
│   │   │   ├── stocks/
│   │   │   ├── savings/
│   │   │   └── ...
│   │   └── globals.css
│   └── components/
│       ├── InvestmentOptions.tsx
│       ├── InvestmentCard.tsx
│       └── DynamicContent.tsx
├── package.json
├── README.md
└── PROPOSAL.md
```

## Key Features

1. **Investment Options Tool**: Generates personalized investment recommendations
2. **Interactive Selection**: Users can enable/disable options before confirming
3. **Dynamic Content**: UI changes based on selected investment types
4. **Investment Pages**: Dedicated pages for each investment type
5. **State Management**: Sync between agent state and UI state

## Technical Details

- **Backend**: FastAPI + ADK + OpenRouter
- **Frontend**: Next.js 15 + CopilotKit + React 19
- **State Sync**: AG-UI protocol events (STATE_SNAPSHOT)
- **Human-in-the-Loop**: useHumanInTheLoop hook from CopilotKit

## Implementation Status

✅ **Completed:**
1. ✅ Created project structure
2. ✅ Implemented backend agent with `generate_investment_options` tool
3. ✅ Implemented frontend UI with human-in-the-loop components
4. ✅ Set up CopilotKit integration
5. ✅ Added OpenRouter configuration (same as agent.py)

🔄 **Future Enhancements:**
- Add dynamic investment pages based on selections
- Add investment-specific detail pages (Real Estate, Stocks, etc.)
- Add state persistence
- Add investment tracking dashboard

## Next Steps

1. Test end-to-end flow
2. Add `.env` file with `OPENROUTER_API_KEY`
3. Run `npm install` and `npm run dev`
4. Test with sample queries like "I want to invest $50,000"

