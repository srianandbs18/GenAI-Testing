# Testing Guide - ADK Widget MCP Demo

## 🧪 Test Scenarios

### Test 1: Initial Connection & Widget Load

**Steps:**
1. Start all three servers (MCP, ADK, UI)
2. Open browser to http://localhost:3000
3. Wait for connection

**Expected Results:**
- ✅ "Connected to ADK" indicator shows green
- ✅ "Schedule Meeting" title appears
- ✅ Timezone shows "EASTERN TIME (ET)" with "CHANGE TIME ZONE" link
- ✅ 5 date buttons appear (next business days)
- ✅ 3 time slots appear (11:30 AM, 1:45 PM, 3:00 PM)
- ✅ "Schedule meeting" button is disabled (grayed out)
- ✅ "Close" button is enabled

**What This Tests:**
- WebSocket connection (UI ↔ ADK)
- MCP tool call: `get_schedule_meeting_widget()`
- Widget schema fetching
- Widget population with dates/times
- Session creation in ADK

---

### Test 2: Date Selection (Session Update)

**Steps:**
1. Click on "TUE Sep 23" button

**Expected Results:**
- ✅ Button background changes (highlighted/selected state)
- ✅ Border becomes brighter
- ✅ "Schedule meeting" button remains disabled (need time too)
- ✅ ADK console shows: `📅 Date selected: 2024-09-23`

**What This Tests:**
- User action sent via WebSocket
- Session context update in ADK
- Widget re-render with updated state
- State preservation (date selection remembered)

---

### Test 3: Time Selection (Enable Submit Button)

**Steps:**
1. Ensure date is already selected (from Test 2)
2. Click on "1:45 PM ET" button

**Expected Results:**
- ✅ Time button gets highlighted/selected
- ✅ "Schedule meeting" button becomes **enabled** (cream colored, clickable)
- ✅ ADK console shows: `⏰ Time selected: 13:45`
- ✅ Date selection is still visible/highlighted

**What This Tests:**
- Multi-step form validation
- Session context accumulation (both date AND time)
- Conditional button enabling
- State persistence across actions

---

### Test 4: Change Timezone (Follow-up Action)

**Steps:**
1. Click "CHANGE TIME ZONE" link at top

**Expected Results:**
- ✅ **New widget appears** - "Change Time Zone"
- ✅ Shows "SELECT TIME ZONE" label
- ✅ 4 timezone options appear as radio buttons:
  - Eastern Time (ET) ← selected by default
  - Central Time (CT)
  - Mountain Time (MT)
  - Pacific Time (PT)
- ✅ "Confirm" and "Cancel" buttons at bottom
- ✅ ADK console shows: `🌍 Timezone change requested (follow-up action)`

**What This Tests:**
- Follow-up action handling
- Widget switching (schedule → timezone selector)
- MCP tool call: `get_timezone_selector_widget()`
- Session context preservation during widget switch

---

### Test 5: Select New Timezone & Return

**Steps:**
1. In timezone selector, click "Pacific Time (PT)"
2. Click "Confirm" button

**Expected Results:**
- ✅ Radio button dot moves to Pacific Time
- ✅ Returns to Schedule Meeting widget
- ✅ Timezone now shows "PACIFIC TIME (PT)"
- ✅ Time slots update to show "PT" suffix:
  - "11:30 AM PT"
  - "1:45 PM PT"
  - "3:00 PM PT"
- ✅ **Date and time selections are preserved!**
- ✅ "Schedule meeting" button still enabled (if both were selected)
- ✅ ADK console shows: `🌍 Timezone changed to: Pacific Time (PT)`

**What This Tests:**
- **SESSION PERSISTENCE** - Critical demo feature!
- Timezone change affects widget data
- Context is maintained across widget transitions
- Widget re-population with new timezone
- Follow-up action completion

---

### Test 6: Cancel Timezone Change

**Steps:**
1. Click "CHANGE TIME ZONE" again
2. Select a different timezone (don't click Confirm)
3. Click "Cancel"

**Expected Results:**
- ✅ Returns to Schedule Meeting widget
- ✅ **Timezone is unchanged** (still shows PT from Test 5)
- ✅ All selections preserved
- ✅ No changes to session context

**What This Tests:**
- Action cancellation
- Session rollback (no unwanted changes)
- State consistency

---

### Test 7: Submit Meeting Schedule

**Steps:**
1. Ensure date and time are both selected
2. Click "Schedule meeting" button

**Expected Results:**
- ✅ Green success banner appears at top
- ✅ Message shows: "Meeting scheduled for [date] at [time]"
- ✅ Banner auto-disappears after 3 seconds
- ✅ ADK console shows:
  ```
  ✅ Meeting scheduled: {
    'date': 'TUE Sep 23',
    'time': '1:45 PM PT',
    'timezone': 'Pacific Time (PT)'
  }
  ```

**What This Tests:**
- Form submission
- Session data retrieval
- Success feedback to user
- Complete workflow end-to-end

---

### Test 8: Close Widget

**Steps:**
1. Click "Close" button

**Expected Results:**
- ✅ Message appears (implementation dependent)
- ✅ WebSocket remains connected
- ✅ Session persists in ADK

**What This Tests:**
- Close action handling
- Connection stability

---

### Test 9: Multiple Selections (State Changes)

**Steps:**
1. Select "FRI Sep 19" + "11:30 AM PT"
2. Note the button is enabled
3. Change date to "MON Sep 22"
4. Change time to "3:00 PM PT"

**Expected Results:**
- ✅ After each selection, old selection is deselected
- ✅ Only one date can be selected at a time
- ✅ Only one time can be selected at a time
- ✅ Button stays enabled throughout (since both always selected)
- ✅ Final selections are "MON Sep 22" + "3:00 PM PT"

**What This Tests:**
- Single-select behavior
- State updates without race conditions
- UI consistency

---

### Test 10: Reconnection After Disconnect

**Steps:**
1. Stop the ADK server (Ctrl+C in terminal)
2. Watch the UI - connection indicator turns red
3. Restart ADK server
4. Wait 3-5 seconds

**Expected Results:**
- ✅ Connection indicator shows "Disconnected" (red)
- ✅ Widget remains visible (last known state)
- ✅ After reconnect: indicator turns green
- ✅ New session created
- ✅ Widget reloads with fresh data
- ✅ **Previous selections lost** (new session)

**What This Tests:**
- WebSocket reconnection logic
- Error handling
- Session lifecycle
- Graceful degradation

---

## 🔍 Browser Console Tests

### Check WebSocket Messages

Open browser console (F12) → Console tab

**On connection:**
```javascript
✅ Connected to ADK server
📨 Received: {
  type: "widget_render",
  session_id: "abc-123...",
  widget: { widget_type: "schedule_meeting", ... }
}
```

**On date selection:**
```javascript
📤 Sending: {
  action: "select_date",
  session_id: "abc-123...",
  date: "2024-09-23",
  label: "TUE Sep 23"
}
```

**On timezone change:**
```javascript
📤 Sending: { action: "change_timezone", session_id: "abc-123..." }
📨 Received: {
  type: "widget_render",
  widget: { widget_type: "timezone_selector", ... }
}
```

---

## 🖥️ ADK Server Console Tests

Watch the ADK terminal for logs:

```
🚀 ADK WebSocket Server starting on ws://localhost:8000
✅ Client connected from ('127.0.0.1', 54321)
📝 Created session: a1b2c3d4-...
📨 Received action: select_date
📅 Date selected: 2024-09-23
📨 Received action: select_time
⏰ Time selected: 13:45
📨 Received action: change_timezone
🌍 Timezone change requested (follow-up action)
📨 Received action: confirm_timezone
🌍 Timezone changed to: Pacific Time (PT)
📨 Received action: submit_schedule
✅ Meeting scheduled: {'date': 'TUE Sep 23', 'time': '1:45 PM PT', ...}
```

---

## 🎯 Key Demo Features Validation

### ✅ Widget Schema from MCP
- MCP provides structure (empty options arrays)
- ADK populates with actual data
- **Verify**: Check `mcp-server/schemas/*.json` files

### ✅ Session Management
- Session created on connection
- Context updated on each action
- Preserved across widget switches
- **Verify**: Watch ADK console for session ID consistency

### ✅ Follow-up Actions
- "Change timezone" triggers new widget
- Returns to original widget after confirmation
- Context preserved throughout
- **Verify**: Date/time selections survive timezone change

### ✅ Dynamic UI Rendering
- UI renders any widget from schema
- No hardcoded business logic in React
- Schema drives the presentation
- **Verify**: Inspect WebSocket messages in browser console

---

## 🐛 Common Issues & Fixes

### Issue: "Schedule meeting" button never enables
**Check:**
- Both date AND time selected?
- Selections highlighted in UI?
- ADK console shows both selections?

### Issue: Timezone change doesn't work
**Check:**
- ADK server running?
- Console shows "change_timezone" action?
- MCP server accessible?

### Issue: Widget doesn't appear
**Check:**
- WebSocket connected? (green indicator)
- ADK console shows session creation?
- Browser console has errors?

### Issue: Selections not preserved after timezone change
**Check:**
- Session ID same before and after?
- ADK updating session context correctly?
- Widget populator using session context?

---

## 📊 Success Criteria

All these should work perfectly:

1. ✅ Initial widget loads with dates/times
2. ✅ Can select date and time
3. ✅ Button enables when both selected
4. ✅ Can change timezone (follow-up action)
5. ✅ Selections preserved after timezone change
6. ✅ Time labels update with new timezone
7. ✅ Can submit meeting schedule
8. ✅ Success message appears
9. ✅ Session persists across multiple actions
10. ✅ Auto-reconnect on disconnect

---

**If all 10 tests pass, the demo is working perfectly! 🎉**
