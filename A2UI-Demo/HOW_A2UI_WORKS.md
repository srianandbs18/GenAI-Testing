# How A2UI Works - Detailed Explanation

## The Confusion: "Why create widgets in Angular if the agent provides them?"

This is a common question! Let me clarify the **A2UI architecture**:

## Key Concept: Declarative Protocol, Not Executable Code

**The AI agent does NOT send widgets. It sends JSON instructions that describe what to render.**

The Angular client has **pre-approved widget templates** that know how to interpret these instructions.

## The A2UI Flow

```
┌─────────────────┐
│   User Prompt   │
│  "show card"    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│      Angular Client (Frontend)      │
│  Sends HTTP POST to agent           │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   ADK Agent (Backend)                │
│                                      │
│   Analyzes prompt: "show card"      │
│   Generates A2UI JSON message:      │
│   {                                  │
│     "type": "card",                 │
│     "data": {                        │
│       "title": "Product Info",       │
│       "content": "...",              │
│       "actions": [...]               │
│     }                                │
│   }                                  │
└────────┬────────────────────────────┘
         │
         │ JSON Response (NOT executable code!)
         │
         ▼
┌─────────────────────────────────────┐
│   Angular Client Receives JSON      │
│                                      │
│   A2UIRenderer reads:               │
│   - message.type = "card"            │
│   - message.data = {...}             │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   Widget Template Selection         │
│                                      │
│   if (type === "card") {            │
│     render CardWidgetComponent      │
│     pass data to component          │
│   }                                  │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   CardWidgetComponent Renders       │
│   Using Angular Native Components   │
│                                      │
│   <div class="card">                 │
│     <h3>{{ data.title }}</h3>       │
│     <p>{{ data.content }}</p>       │
│     <button *ngFor="action">        │
│   </div>                             │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   User Sees Rendered Widget         │
│   (Styled with Angular CSS)         │
└─────────────────────────────────────┘
```

## Why This Architecture?

### 1. **Security** 🔒
- Agent can ONLY request pre-approved widget types
- Agent sends **data**, not code
- Client controls what can be rendered
- Prevents UI injection attacks

### 2. **Framework Agnostic** 🌐
- Same A2UI JSON can work with:
  - Angular (this demo)
  - React
  - Vue
  - Flutter
  - Native mobile apps
- Each framework has its own widget templates
- Agent doesn't need to know the framework

### 3. **LLM-Friendly** 🤖
- LLMs are great at generating structured JSON
- Easy to parse and validate
- Streaming updates possible

## Real Example from Our Code

### Step 1: Agent Generates JSON (agent.py)

```python
def generate_card_widget() -> Dict[str, Any]:
    return {
        "type": "card",  # ← Agent says "I want a card"
        "data": {        # ← Agent provides the data
            "title": "Product Information",
            "content": "Description...",
            "actions": [{"label": "Learn More"}]
        }
    }
```

**This is sent as JSON over HTTP:**
```json
{
  "text": "Here's a card widget:",
  "a2ui": {
    "type": "card",
    "data": {
      "title": "Product Information",
      "content": "Description...",
      "actions": [{"label": "Learn More"}]
    }
  }
}
```

### Step 2: Angular Receives and Parses (a2ui-renderer.component.ts)

```typescript
// Angular receives the JSON
message = {
  type: "card",
  data: { title: "Product Information", ... }
}

// Renderer checks the type
if (message.type === "card") {
  // Renders CardWidgetComponent
  // Passes message.data to it
}
```

### Step 3: Widget Component Renders (card-widget.component.ts)

```typescript
@Component({
  template: `
    <div class="card-widget">
      <h3>{{ data.title }}</h3>      <!-- Uses data from agent -->
      <p>{{ data.content }}</p>       <!-- Uses data from agent -->
      <button *ngFor="let action of data.actions">
        {{ action.label }}            <!-- Uses data from agent -->
      </button>
    </div>
  `
})
export class CardWidgetComponent {
  @Input() data: any;  // ← Receives data from agent
}
```

## The Widget Templates Are Like "Stencils"

Think of it this way:

- **Agent** = Artist who says "I want to draw a house"
- **A2UI JSON** = Instructions: `{type: "house", data: {doors: 2, windows: 4}}`
- **Widget Template** = Stencil/pre-made template for drawing houses
- **Angular** = The canvas that uses the stencil with the provided data

The agent doesn't draw the house itself. It provides instructions, and the client uses its pre-approved stencil to render it.

## What If Agent Requests Unknown Widget?

The client has a **whitelist** of allowed widget types:

```typescript
isValidType(type: string): boolean {
  return ['card', 'form', 'table'].includes(type);
}
```

If agent requests `"type": "malicious_widget"`, the client **rejects it** and shows an error. This is the security model!

## Summary

| Component | Responsibility |
|-----------|---------------|
| **AI Agent** | Generates A2UI JSON describing what to render |
| **Angular Client** | Has widget templates that know how to render |
| **A2UI Protocol** | The JSON format that connects them |
| **Widget Templates** | Pre-approved, secure rendering components |

**The agent provides the "what" (data + widget type).**  
**The client provides the "how" (rendering templates).**

This separation is what makes A2UI secure, framework-agnostic, and powerful!

