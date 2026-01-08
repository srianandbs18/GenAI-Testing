# A2UI Demo - Angular + Google ADK Agent

A complete demonstration of the A2UI (Agent-to-User Interface) protocol, featuring an Angular client that renders three different widget templates based on user prompts, powered by a Google ADK agent.

## Overview

This demo showcases how AI agents can generate rich, interactive user interfaces using the A2UI protocol. The application consists of:

- **Angular Client**: A modern web application that renders A2UI widgets
- **ADK Agent**: A FastAPI-based agent using **Google ADK (Agent Development Kit)** that processes user prompts and generates A2UI protocol messages
- **Three Widget Templates**: Card, Form, and Data Table widgets

> **💡 Understanding A2UI Architecture**: The AI agent doesn't send executable widgets. Instead, it sends **declarative JSON messages** that describe what to render. The Angular client has **pre-approved widget templates** that interpret these messages and render them securely. See [HOW_A2UI_WORKS.md](./HOW_A2UI_WORKS.md) for a detailed explanation.

## Architecture

```
User Input → Angular Client → ADK Agent → A2UI JSON → Angular Renderer → Widget Display
```

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Angular CLI** (will be installed globally)
- **Google Gemini API Key** (optional but recommended - get from https://makersuite.google.com/app/apikey)

## Project Structure

```
A2UI-Demo/
├── angular-client/          # Angular frontend application
│   ├── src/
│   │   └── app/
│   │       ├── components/
│   │       │   ├── chatbot/         # Chatbot UI component
│   │       │   ├── a2ui-renderer/   # A2UI message renderer
│   │       │   └── widgets/         # Widget templates
│   │       │       ├── card-widget/
│   │       │       ├── form-widget/
│   │       │       └── data-table-widget/
│   │       └── app.component.ts
│   └── package.json
├── adk-agent/              # FastAPI agent server
│   ├── agent.py           # Main agent implementation
│   ├── requirements.txt   # Python dependencies
│   └── .env.example
└── README.md
```

## Setup Instructions

### 1. Setup Angular Client

```bash
# Navigate to Angular client directory
cd angular-client

# Install dependencies
npm install

# Install Angular CLI globally if not already installed
npm install -g @angular/cli
```

### 2. Setup ADK Agent

```bash
# Navigate to agent directory
cd adk-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your Google API key:
# GOOGLE_API_KEY=your_api_key_here
# 
# Get API key from: https://makersuite.google.com/app/apikey
# Note: The agent works without API key but will use rule-based responses instead of AI
```

## Running the Demo

> **📖 For detailed step-by-step instructions, see [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md)**

### Quick Start

**Terminal 1 - Angular Client:**
```bash
cd angular-client
npm install  # First time only
npm start
```

**Terminal 2 - ADK Agent:**
```bash
cd adk-agent
python -m venv venv
# Activate venv:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt  # First time only
python agent.py
```

### Step 1: Start the ADK Agent

Open a terminal and run:

```bash
cd adk-agent
# Activate virtual environment if not already active
source venv/bin/activate  # or venv\Scripts\activate on Windows
python agent.py
```

The agent will start on `http://localhost:8001`. You should see:
```
✅ Google ADK Agent initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Optional:** Add `GOOGLE_API_KEY` to `.env` file for AI-powered responses (get key from https://makersuite.google.com/app/apikey)

### Step 2: Start the Angular Client

Open a **new terminal** and run:

```bash
cd angular-client
npm start
# or
ng serve
```

The Angular app will start on `http://localhost:4200` and should automatically open in your browser.

### Step 3: Test the Demo

1. The chatbot interface will load with a welcome message
2. Try these commands:
   - `show card` or `display card` - Renders a card widget
   - `show form` or `display form` - Renders a form widget
   - `show table` or `display table` - Renders a data table widget
   - `show all` - Displays all three widgets

3. **With API Key:** Try natural language:
   - `I need a contact form for customer support`
   - `Show me a data table with user information`
   - `Display a product card`

4. Interact with the widgets:
   - **Card Widget**: Click action buttons
   - **Form Widget**: Fill out and submit the form
   - **Data Table Widget**: Click column headers to sort, use action buttons

## How It Works

### A2UI Protocol Flow

1. **User sends prompt** → Angular client captures user input
2. **HTTP POST request** → Client sends prompt to ADK agent at `/chat`
3. **Agent processes prompt** → Agent analyzes intent and generates A2UI JSON
4. **A2UI message returned** → Agent sends structured A2UI protocol message
5. **Renderer parses message** → Angular A2UIRenderer component identifies widget type
6. **Widget rendered** → Appropriate widget component displays the UI

### A2UI Message Format

The agent generates messages in this format:

```json
{
  "type": "card|form|table",
  "data": {
    // Widget-specific data structure
  }
}
```

## Widget Templates

### 1. Card Widget

Displays information in a card format with:
- Title and content
- Optional image
- Footer text
- Action buttons

**Example A2UI Message:**
```json
{
  "type": "card",
  "data": {
    "title": "Product Information",
    "content": "Description text",
    "image": {"url": "...", "alt": "..."},
    "actions": [{"label": "Action", "primary": true}]
  }
}
```

### 2. Form Widget

Interactive form with various input types:
- Text, email, password inputs
- Textarea
- Select dropdowns
- Checkboxes
- Form validation

**Example A2UI Message:**
```json
{
  "type": "form",
  "data": {
    "title": "Contact Form",
    "fields": [
      {"name": "email", "type": "email", "required": true}
    ]
  }
}
```

### 3. Data Table Widget

Sortable data table with:
- Multiple columns
- Sortable columns
- Action buttons per row
- Row data display

**Example A2UI Message:**
```json
{
  "type": "table",
  "data": {
    "columns": [{"key": "name", "label": "Name"}],
    "rows": [{"name": "John"}],
    "actions": [{"label": "Edit", "type": "primary"}]
  }
}
```

## Adding More Widgets

### Step 1: Create Widget Component

1. Create a new component in `angular-client/src/app/components/widgets/`:
   ```bash
   cd angular-client
   ng generate component components/widgets/my-widget
   ```

2. Implement the widget component following the pattern of existing widgets:
   - Accept `@Input() data: any` for widget data
   - Create template with widget-specific UI
   - Add styling in component CSS

### Step 2: Register Widget in A2UI Renderer

Edit `angular-client/src/app/components/a2ui-renderer/a2ui-renderer.component.ts`:

```typescript
import { MyWidgetComponent } from '../widgets/my-widget/my-widget.component';

// Add to imports array
imports: [..., MyWidgetComponent]

// Add to template
<app-my-widget *ngIf="message?.type === 'mywidget'" [data]="message.data"></app-my-widget>

// Update isValidType method
isValidType(type: string): boolean {
  return ['card', 'form', 'table', 'mywidget'].includes(type);
}
```

### Step 3: Add Widget Generation in Agent

Edit `adk-agent/agent.py`:

1. Create a function to generate your widget:
   ```python
   def generate_my_widget() -> Dict[str, Any]:
       return {
           "type": "mywidget",
           "data": {
               # Your widget data structure
           }
       }
   ```

2. Update `parse_user_prompt()` function:
   ```python
   def parse_user_prompt(prompt: str) -> Dict[str, Any]:
       prompt_lower = prompt.lower().strip()
       
       if "mywidget" in prompt_lower:
           return generate_my_widget()
       
       # ... existing code
   ```

### Step 4: Test

1. Restart the ADK agent
2. Restart the Angular client
3. Test with a prompt like: `show mywidget`

## Troubleshooting

### Agent not responding

- **Check agent is running**: Verify `http://localhost:8001` is accessible
- **Check CORS**: Ensure CORS is enabled in `agent.py` for `http://localhost:4200`
- **Check console**: Look for errors in browser console and agent terminal

### Widgets not rendering

- **Check A2UI message format**: Verify the agent returns correct JSON structure
- **Check component registration**: Ensure widget is registered in A2UIRenderer
- **Check browser console**: Look for Angular errors

### CORS errors

- Ensure `CORSMiddleware` is configured in `agent.py`
- Verify Angular client is running on `http://localhost:4200`
- Check agent allows origin `http://localhost:4200`

## Development

### Angular Client Development

```bash
cd angular-client
ng serve --open
```

### Agent Development

```bash
cd adk-agent
# Activate venv
python agent.py
# Or use uvicorn directly
uvicorn agent:app --reload --port 8001
```

## API Reference

### POST /chat

Send a user prompt to the agent.

**Request:**
```json
{
  "message": "show card"
}
```

**Response:**
```json
{
  "text": "Here's a card widget:",
  "a2ui": {
    "type": "card",
    "data": { ... }
  }
}
```

## Resources

- [A2UI Official Website](https://a2ui.org/)
- [A2UI Protocol Documentation](https://a2ui.org/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Angular Documentation](https://angular.io/docs)

## License

This demo is provided as-is for educational and demonstration purposes.

## Next Steps

- Add more widget types (charts, maps, etc.)
- Implement streaming A2UI updates
- Add authentication and user management
- Deploy to production environment
- Consider Google ADK framework if it becomes available for advanced agent orchestration

> **Note**: This demo uses **Google ADK (Agent Development Kit)** - a framework for building AI agents. ADK provides higher-level abstractions for agent development and uses Gemini models under the hood.

