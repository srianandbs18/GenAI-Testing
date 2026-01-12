# React Frontend for Banking Demo with MCP

React-based frontend using Vite for the Banking Demo with MCP application.

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# or
npm start
```

The app will start on `http://localhost:4201`

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Structure

```
src/
  ├── App.tsx                 # Main app component
  ├── components/
  │   ├── Chatbot.tsx        # Chat interface
  │   ├── A2UIRenderer.tsx   # Widget renderer
  │   └── widgets/
  │       ├── CardWidget.tsx
  │       ├── AccountSummaryWidget.tsx
  │       ├── DepositWidget.tsx
  │       └── WithdrawalWidget.tsx
  └── main.tsx               # Entry point
```

## Features

- React 18 with TypeScript
- Vite for fast development
- Dynamic widget rendering
- Chat interface with message history
- Banking-specific widgets

