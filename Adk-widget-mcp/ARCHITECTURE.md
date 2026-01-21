# ADK-Widget-MCP Meeting Scheduler - Architecture & Implementation Plan

## 🎯 Project Overview
A demo application showcasing Google ADK (Agent Development Kit) integrated with MCP (Model Context Protocol) server for dynamic widget-based UI rendering. The app demonstrates an intelligent meeting scheduling interface with session management and follow-up action handling.

---

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        REACT UI (Port 3000)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components:                                              │  │
│  │  - WidgetRenderer (dynamic schema-based rendering)       │  │
│  │  - DateSelector (FRI, MON, TUE, WED, TUR buttons)       │  │
│  │  - TimeSlotPicker (11:30 AM, 1:45 PM, 3:00 PM)          │  │
│  │  - TimezoneDisplay (shows current timezone)              │  │
│  │  - ActionButtons (Schedule meeting, Close)               │  │
│  └──────────────────────────────────────────────────────────┘  │
│           ↕ WebSocket Connection (ws://localhost:8000/ws)      │
└─────────────────────────────────────────────────────────────────┘
                                    ↕
                    WebSocket Messages (JSON)
                    {
                      "type": "widget_render",
                      "widget": {...schema...},
                      "session_id": "xyz"
                    }
                                    ↕
┌─────────────────────────────────────────────────────────────────┐
│              ADK AGENT LAYER (Python - Port 8000)                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Core Components:                                         │  │
│  │  1. WebSocket Server (handles UI connections)            │  │
│  │  2. Session Manager (tracks conversation & context)      │  │
│  │  3. Agent Core (LLM-powered decision making)             │  │
│  │  4. MCP Client (communicates with MCP server)            │  │
│  │  5. Widget Populator (fills schema with actual data)     │  │
│  │  6. Follow-up Handler (manages multi-turn interactions)  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Session Storage:                                               │
│  {                                                               │
│    "session_id": "abc123",                                      │
│    "timezone": "Eastern Time (ET)",                             │
│    "selected_date": "Sep 23",                                   │
│    "selected_time": "1:45 PM ET",                               │
│    "conversation_history": [...],                               │
│    "current_action": "schedule_meeting"                         │
│  }                                                               │
│           ↕ MCP Protocol (FastMCP - Port 8001)                 │
└─────────────────────────────────────────────────────────────────┘
                                    ↕
                         FastMCP Tool Calls
                                    ↕
┌─────────────────────────────────────────────────────────────────┐
│              MCP SERVER (FastMCP - Port 8001)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Widget Schema Tools:                                     │  │
│  │                                                            │  │
│  │  🔧 get_schedule_meeting_widget()                        │  │
│  │     Returns: Full meeting scheduler widget schema        │  │
│  │                                                            │  │
│  │  🔧 get_date_selector_widget()                           │  │
│  │     Returns: Date picker component schema                │  │
│  │                                                            │  │
│  │  🔧 get_time_picker_widget()                             │  │
│  │     Returns: Time slot selector schema                   │  │
│  │                                                            │  │
│  │  🔧 get_timezone_widget()                                │  │
│  │     Returns: Timezone selector schema                    │  │
│  │                                                            │  │
│  │  📋 Widget Schema Structure:                             │  │
│  │  {                                                         │  │
│  │    "widget_type": "schedule_meeting",                    │  │
│  │    "schema_version": "1.0",                              │  │
│  │    "properties": {                                        │  │
│  │      "title": "Schedule Meeting",                        │  │
│  │      "timezone": {                                        │  │
│  │        "type": "timezone_selector",                      │  │
│  │        "current": "Eastern Time (ET)",                   │  │
│  │        "editable": true                                   │  │
│  │      },                                                    │  │
│  │      "date_selector": {                                   │  │
│  │        "type": "date_buttons",                           │  │
│  │        "options": []  // Will be populated by ADK        │  │
│  │      },                                                    │  │
│  │      "time_slots": {                                      │  │
│  │        "type": "time_picker",                            │  │
│  │        "options": []  // Will be populated by ADK        │  │
│  │      },                                                    │  │
│  │      "actions": [...]                                     │  │
│  │    }                                                       │  │
│  │  }                                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow - User Journey

### **Scenario 1: Initial Meeting Scheduling**

```
1. User opens app
   ↓
2. UI connects to ADK via WebSocket
   ↓
3. ADK creates session, calls MCP: get_schedule_meeting_widget()
   ↓
4. MCP returns widget schema
   ↓
5. ADK populates schema with data:
   - Dates: Next 5 business days
   - Times: Available slots (11:30 AM, 1:45 PM, 3:00 PM ET)
   - Timezone: Eastern Time (ET)
   ↓
6. ADK sends populated widget to UI
   ↓
7. UI renders Schedule Meeting interface
```

### **Scenario 2: Follow-up Action - Change Timezone**

```
1. User clicks "CHANGE TIME ZONE"
   ↓
2. UI sends: {"action": "change_timezone", "session_id": "xyz"}
   ↓
3. ADK retrieves session context
   ↓
4. ADK calls MCP: get_timezone_widget()
   ↓
5. MCP returns timezone selector schema
   ↓
6. ADK populates with available timezones
   ↓
7. ADK updates session: current_action = "select_timezone"
   ↓
8. UI renders timezone picker
   ↓
9. User selects "Pacific Time (PT)"
   ↓
10. ADK updates session, recalculates times
    ↓
11. ADK calls MCP: get_schedule_meeting_widget()
    ↓
12. Returns to Step 5 of Scenario 1 with updated timezone
```

### **Scenario 3: Follow-up Action - Edit Schedule**

```
1. User selects date (e.g., "TUE Sep 23")
   ↓
2. UI sends: {"action": "select_date", "date": "Sep 23", "session_id": "xyz"}
   ↓
3. ADK updates session context with selected date
   ↓
4. User selects time (e.g., "1:45 PM ET")
   ↓
5. UI sends: {"action": "select_time", "time": "1:45 PM", "session_id": "xyz"}
   ↓
6. ADK updates session with selected time
   ↓
7. User clicks "Schedule meeting" button
   ↓
8. ADK processes meeting creation
   ↓
9. ADK sends confirmation widget back to UI
```

---

## 🧩 Component Details

### **1. React UI (Frontend)**

**Directory Structure:**
```
ui/
├── src/
│   ├── components/
│   │   ├── WidgetRenderer.jsx         # Main renderer
│   │   ├── ScheduleMeetingWidget.jsx  # Meeting scheduler
│   │   ├── DateSelector.jsx           # Date buttons
│   │   ├── TimePicker.jsx             # Time slots
│   │   ├── TimezoneSelector.jsx       # Timezone picker
│   │   └── ActionButtons.jsx          # Bottom buttons
│   ├── hooks/
│   │   └── useWebSocket.js            # WebSocket connection
│   ├── utils/
│   │   └── schemaRenderer.js          # Schema interpretation
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

**Key Features:**
- Schema-driven rendering (interprets JSON schema from ADK)
- WebSocket communication with auto-reconnect
- Dark theme UI matching the image
- Responsive design
- State management for selections

---

### **2. ADK Agent Layer (Python)**

**Directory Structure:**
```
adk/
├── src/
│   ├── agent.py                  # Main ADK agent logic
│   ├── websocket_server.py       # WebSocket server
│   ├── session_manager.py        # Session storage & retrieval
│   ├── mcp_client.py             # MCP protocol client
│   ├── widget_populator.py       # Data population logic
│   ├── follow_up_handler.py      # Multi-turn conversation
│   └── config.py                 # Configuration
├── prompts/
│   └── agent_instructions.txt    # System prompts for agent
├── requirements.txt
└── main.py
```

**Key Responsibilities:**

**a) Session Manager:**
```python
class SessionManager:
    def create_session(self) -> str
    def get_session(self, session_id: str) -> dict
    def update_session(self, session_id: str, data: dict)
    def get_conversation_history(self, session_id: str) -> list
    def add_to_history(self, session_id: str, message: dict)
```

**b) MCP Client:**
```python
class MCPClient:
    def call_tool(self, tool_name: str, params: dict) -> dict
    def get_widget_schema(self, widget_type: str) -> dict
    def list_available_widgets(self) -> list
```

**c) Widget Populator:**
```python
class WidgetPopulator:
    def populate_schedule_meeting_widget(self, schema: dict, context: dict) -> dict
    def get_available_dates(self, start_date: date, count: int) -> list
    def get_available_time_slots(self, date: date, timezone: str) -> list
    def convert_timezone(self, time: str, from_tz: str, to_tz: str) -> str
```

**d) Follow-up Handler:**
```python
class FollowUpHandler:
    def handle_action(self, action: str, session_id: str, params: dict) -> dict
    def determine_next_widget(self, action: str, context: dict) -> str
```

**ADK Agent Instructions (Prompt):**
```
You are a meeting scheduling assistant. Your job is to:

1. UNDERSTAND user intent from their messages
2. CALL the appropriate MCP tool to get widget schemas
3. POPULATE widgets with relevant data based on user context
4. MAINTAIN session state across conversations
5. HANDLE follow-up actions intelligently

When user says "schedule a meeting":
- Call get_schedule_meeting_widget() from MCP
- Populate with next 5 business days
- Show available time slots
- Use session timezone

When user says "change timezone" or clicks CHANGE TIME ZONE:
- Call get_timezone_widget() from MCP
- Show timezone options
- Remember previous selections in session

When user selects date/time:
- Update session context
- Provide visual feedback
- Enable schedule button when both selected

ALWAYS maintain session continuity and remember user preferences.
```

---

### **3. MCP Server (FastMCP)**

**Directory Structure:**
```
mcp-server/
├── src/
│   ├── server.py                # Main FastMCP server
│   ├── schemas/
│   │   ├── schedule_meeting.json
│   │   ├── date_selector.json
│   │   ├── time_picker.json
│   │   └── timezone_selector.json
│   └── tools.py                 # MCP tool definitions
├── requirements.txt
└── main.py
```

**Widget Schema Tools:**

**Tool 1: get_schedule_meeting_widget()**
```json
{
  "name": "get_schedule_meeting_widget",
  "description": "Returns the complete schedule meeting widget schema",
  "input_schema": {
    "type": "object",
    "properties": {},
    "required": []
  },
  "output_schema": {
    "widget_type": "schedule_meeting",
    "schema_version": "1.0",
    "properties": {
      "title": "string",
      "timezone": "object",
      "date_selector": "object",
      "time_slots": "object",
      "actions": "array"
    }
  }
}
```

**Tool 2: get_date_selector_widget()**
```json
{
  "name": "get_date_selector_widget",
  "description": "Returns date selector component schema",
  "input_schema": {
    "type": "object",
    "properties": {
      "count": {
        "type": "number",
        "description": "Number of dates to show"
      }
    }
  }
}
```

**Tool 3: get_time_picker_widget()**
```json
{
  "name": "get_time_picker_widget",
  "description": "Returns time slot picker schema",
  "input_schema": {
    "type": "object",
    "properties": {
      "slots_count": {
        "type": "number",
        "description": "Number of time slots"
      }
    }
  }
}
```

---

## 🔐 Session Management

**Session Structure:**
```python
{
    "session_id": "uuid-v4",
    "created_at": "2026-01-21T10:00:00Z",
    "last_activity": "2026-01-21T10:05:00Z",
    "context": {
        "timezone": "Eastern Time (ET)",
        "timezone_offset": "-05:00",
        "selected_date": None,
        "selected_time": None,
        "available_dates": ["Sep 19", "Sep 22", "Sep 23", "Sep 24", "Sep 24"],
        "available_times": ["11:30 AM ET", "1:45 PM ET", "3:00 PM ET"],
        "current_widget": "schedule_meeting",
        "current_action": None
    },
    "conversation_history": [
        {
            "timestamp": "2026-01-21T10:00:00Z",
            "type": "user_action",
            "action": "open_scheduler",
            "data": {}
        },
        {
            "timestamp": "2026-01-21T10:00:01Z",
            "type": "agent_response",
            "widget": "schedule_meeting",
            "data": {...}
        }
    ]
}
```

**Session Lifecycle:**
1. Created when UI connects via WebSocket
2. Maintained in memory (Redis for production)
3. Updated on every user interaction
4. Expires after 30 minutes of inactivity
5. Cleaned up when user disconnects

---

## 📡 Communication Protocol

### **WebSocket Messages (UI ↔ ADK)**

**Message Types:**

**1. Connection Initialization**
```json
// UI → ADK
{
  "type": "connect",
  "data": {}
}

// ADK → UI
{
  "type": "connected",
  "session_id": "abc-123",
  "widget": {...schema...}
}
```

**2. User Action**
```json
// UI → ADK
{
  "type": "user_action",
  "session_id": "abc-123",
  "action": "select_date",
  "data": {
    "date": "Sep 23"
  }
}
```

**3. Widget Render**
```json
// ADK → UI
{
  "type": "widget_render",
  "session_id": "abc-123",
  "widget": {
    "widget_type": "schedule_meeting",
    "properties": {...}
  }
}
```

**4. Follow-up Action**
```json
// UI → ADK
{
  "type": "follow_up_action",
  "session_id": "abc-123",
  "action": "change_timezone",
  "data": {}
}
```

### **MCP Protocol (ADK ↔ MCP Server)**

Using FastMCP standard protocol:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_schedule_meeting_widget",
    "arguments": {}
  }
}
```

---

## 🎨 Widget Schemas (Examples)

### **Schedule Meeting Widget - Complete Schema**

```json
{
  "widget_type": "schedule_meeting",
  "schema_version": "1.0",
  "metadata": {
    "title": "Schedule Meeting",
    "description": "Select date and time for meeting"
  },
  "properties": {
    "timezone": {
      "type": "timezone_display",
      "label": "CURRENT TIME ZONE",
      "value": "EASTERN TIME (ET)",
      "editable": true,
      "action": "change_timezone"
    },
    "date_selector": {
      "type": "button_group",
      "label": "SELECT A DATE",
      "style": "horizontal",
      "multi_select": false,
      "options": [
        {
          "label": "FRI",
          "sublabel": "Sep 19",
          "value": "2024-09-19",
          "selected": false
        },
        {
          "label": "MON",
          "sublabel": "Sep 22",
          "value": "2024-09-22",
          "selected": false
        },
        {
          "label": "TUE",
          "sublabel": "Sep 23",
          "value": "2024-09-23",
          "selected": false
        },
        {
          "label": "WED",
          "sublabel": "Sep 24",
          "value": "2024-09-24",
          "selected": false
        },
        {
          "label": "TUR",
          "sublabel": "Sep 24",
          "value": "2024-09-24",
          "selected": false
        }
      ]
    },
    "time_slots": {
      "type": "button_list",
      "label": "SELECT A TIME",
      "style": "vertical",
      "multi_select": false,
      "options": [
        {
          "label": "11:30 AM ET",
          "value": "11:30",
          "selected": false
        },
        {
          "label": "1:45 PM ET",
          "value": "13:45",
          "selected": false
        },
        {
          "label": "3:00 PM ET",
          "value": "15:00",
          "selected": false
        }
      ]
    },
    "actions": {
      "type": "action_buttons",
      "buttons": [
        {
          "id": "schedule",
          "label": "Schedule meeting",
          "style": "primary",
          "enabled": false,
          "action": "submit_schedule"
        },
        {
          "id": "close",
          "label": "Close",
          "style": "secondary",
          "enabled": true,
          "action": "close_widget"
        }
      ]
    }
  },
  "validation": {
    "required_fields": ["date_selector", "time_slots"],
    "enable_submit": {
      "condition": "date_selector.selected && time_slots.selected"
    }
  },
  "styling": {
    "theme": "dark",
    "primary_color": "#E5E5E5",
    "background_color": "#1E1E1E",
    "border_radius": "8px"
  }
}
```

---

## 🚀 Implementation Phases

### **Phase 1: Foundation Setup** (Day 1)
- [x] Project structure creation
- [ ] Setup React UI with Vite
- [ ] Setup Python ADK server
- [ ] Setup FastMCP server
- [ ] Basic WebSocket connection (UI ↔ ADK)
- [ ] Basic MCP connection (ADK ↔ MCP)

### **Phase 2: MCP Server & Schemas** (Day 2)
- [ ] Define all widget schemas (JSON files)
- [ ] Implement MCP tools:
  - `get_schedule_meeting_widget()`
  - `get_date_selector_widget()`
  - `get_time_picker_widget()`
- [ ] Test MCP tools individually
- [ ] Document schema contracts

### **Phase 3: ADK Agent Core** (Day 3)
- [ ] Implement Session Manager
- [ ] Implement MCP Client
- [ ] Implement Widget Populator
- [ ] Implement Follow-up Handler
- [ ] Agent decision logic
- [ ] WebSocket message handlers

### **Phase 4: UI Implementation** (Day 4)
- [ ] WidgetRenderer component
- [ ] ScheduleMeetingWidget component
- [ ] DateSelector component
- [ ] TimePicker component
- [ ] TimezoneSelector component
- [ ] WebSocket hooks
- [ ] State management

### **Phase 5: Integration & Testing** (Day 5)
- [ ] End-to-end flow testing
- [ ] Session continuity testing
- [ ] Follow-up action testing
- [ ] Timezone change flow
- [ ] Edit schedule flow
- [ ] Error handling
- [ ] Edge cases

### **Phase 6: Polish & Documentation** (Day 6)
- [ ] UI styling to match image
- [ ] Loading states
- [ ] Error messages
- [ ] README documentation
- [ ] API documentation
- [ ] Deployment guide

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite | UI framework |
| | TailwindCSS | Styling (dark theme) |
| | WebSocket API | Real-time communication |
| **ADK Layer** | Python 3.11+ | Agent runtime |
| | websockets | WebSocket server |
| | aiohttp | HTTP client |
| | google-generativeai | LLM integration (optional) |
| **MCP Server** | FastMCP | MCP protocol server |
| | Python 3.11+ | Runtime |
| **Session Store** | In-memory dict | Development |
| | Redis | Production (future) |

---

## 📦 Dependencies

### **UI (package.json)**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.2.0"
  }
}
```

### **ADK (requirements.txt)**
```
websockets==12.0
aiohttp==3.9.1
fastmcp==0.3.0
python-dateutil==2.8.2
pytz==2024.1
pydantic==2.5.0
```

### **MCP Server (requirements.txt)**
```
fastmcp==0.3.0
pydantic==2.5.0
```

---

## 🔧 Configuration

### **Ports**
- React UI: `http://localhost:3000`
- ADK WebSocket: `ws://localhost:8000/ws`
- ADK HTTP: `http://localhost:8000`
- MCP Server: `http://localhost:8001` (or stdio)

### **Environment Variables**
```bash
# .env
ADK_PORT=8000
MCP_SERVER_URL=http://localhost:8001
MCP_PROTOCOL=http  # or stdio
SESSION_TIMEOUT=1800  # 30 minutes
LOG_LEVEL=INFO
```

---

## 🧪 Testing Strategy

### **Unit Tests**
- MCP tool output validation
- Widget schema validation
- Session manager operations
- Widget populator logic

### **Integration Tests**
- ADK ↔ MCP communication
- UI ↔ ADK WebSocket flow
- End-to-end widget rendering

### **User Flow Tests**
1. Open app → see schedule meeting widget
2. Click date → date gets selected
3. Click time → time gets selected, button enabled
4. Click "CHANGE TIME ZONE" → timezone picker shows
5. Select timezone → widget updates with new times
6. Click "Schedule meeting" → confirmation shown

---

## 🎯 Success Criteria

✅ **Functional Requirements:**
1. UI renders dynamically based on MCP schemas
2. ADK maintains session across interactions
3. Follow-up actions work (timezone change, edit schedule)
4. Widget data populates correctly from ADK
5. WebSocket communication is stable

✅ **Non-Functional Requirements:**
1. Response time < 500ms for widget rendering
2. Zero data loss during session
3. Clean error handling and recovery
4. Code is well-documented
5. Architecture is extensible for more widgets

---

## 🔮 Future Enhancements

1. **More Widgets:**
   - Calendar view widget
   - Attendee selector widget
   - Meeting duration picker

2. **Advanced Features:**
   - Multi-step flows
   - Conditional widget rendering
   - Real calendar integration (Google Calendar, Outlook)
   - Meeting conflict detection

3. **Production Readiness:**
   - Redis for session storage
   - Authentication & authorization
   - Rate limiting
   - Monitoring & logging
   - Docker containers
   - CI/CD pipeline

---

## 📝 Notes

- **MCP Server is SCHEMA-ONLY**: It provides widget contracts/structures, not data
- **ADK is the BRAIN**: It decides what widget to show and populates it with data
- **UI is RENDERER**: It just interprets and renders schemas, no business logic
- **Session is KING**: All context must be maintained in ADK session
- **Follow-up Actions**: ADK must understand conversation flow and context

---

## 🚦 Ready to Implement?

Once you approve this architecture, we'll implement in this order:

1. ✅ Create project structure
2. ✅ Setup MCP server with widget schemas
3. ✅ Setup ADK with session management
4. ✅ Setup React UI with WebSocket
5. ✅ Connect all three layers
6. ✅ Test end-to-end flows
7. ✅ Polish UI to match image

**Estimated Time:** 5-6 days for complete implementation with testing.

---

**Please review and approve this architecture. Any changes or concerns?**
