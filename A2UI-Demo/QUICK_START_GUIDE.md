# Quick Start Guide - Running and Testing the A2UI Demo

## Prerequisites Check

Before starting, ensure you have:

- ✅ **Node.js 18+** installed (`node --version`)
- ✅ **Python 3.10+** installed (`python --version`)
- ✅ **npm** installed (`npm --version`)
- ✅ **pip** installed (`pip --version`)

## Step-by-Step Setup

### Step 1: Setup Angular Client (Terminal 1)

```bash
# Navigate to Angular client directory
cd angular-client

# Install dependencies (first time only)
npm install

# If Angular CLI is not installed globally, install it:
npm install -g @angular/cli
```

### Step 2: Setup ADK Agent (Terminal 2)

Open a **new terminal window** and run:

```bash
# Navigate to agent directory
cd adk-agent

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (CMD):
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt
```

### Step 3: Configure API Key (Optional but Recommended)

```bash
# In the adk-agent directory, copy the example env file
# On Windows:
copy .env.example .env
# On macOS/Linux:
cp .env.example .env

# Edit .env file and add your Google API key:
# GOOGLE_API_KEY=your_actual_api_key_here
```

**Get API Key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in `.env` file

**Note:** The demo works without API key (uses rule-based responses), but AI mode is much better!

### Step 4: Start the ADK Agent

In **Terminal 2** (where you activated venv):

```bash
# Make sure you're in adk-agent directory and venv is activated
python agent.py
```

You should see:
```
✅ Google ADK Agent initialized successfully
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

**Keep this terminal open!** The agent must be running.

### Step 5: Start the Angular Client

In **Terminal 1** (angular-client directory):

```bash
# Make sure you're in angular-client directory
npm start
# or
ng serve
```

You should see:
```
✔ Browser application bundle generation complete.
** Angular Live Development Server is listening on localhost:4200 **
```

The browser should automatically open to `http://localhost:4200`

**Keep this terminal open too!**

## Testing the Demo

### Test 1: Basic Widget Commands

In the chatbot interface, try these commands:

1. **Card Widget:**
   ```
   show card
   ```
   or
   ```
   display card
   ```

2. **Form Widget:**
   ```
   show form
   ```
   or
   ```
   display form
   ```

3. **Table Widget:**
   ```
   show table
   ```
   or
   ```
   display table
   ```

4. **All Widgets:**
   ```
   show all
   ```

### Test 2: Natural Language (With API Key)

If you have the API key configured, try natural language:

```
I need a contact form for customer support
```

```
Can you show me a data table with user information?
```

```
Display a product card with an image
```

### Test 3: Interact with Widgets

1. **Card Widget:**
   - Click action buttons
   - See the card with image, title, content

2. **Form Widget:**
   - Fill out the form fields
   - Try submitting (will show alert with data)
   - Test validation (leave required fields empty)

3. **Table Widget:**
   - Click column headers to sort
   - Click action buttons (Edit, Delete)
   - See row data displayed

## Expected Behavior

### With API Key (AI Mode)
- ✅ Agent intelligently understands prompts
- ✅ Generates appropriate A2UI JSON
- ✅ Can handle natural language requests
- ✅ More dynamic and contextual responses

### Without API Key (Fallback Mode)
- ✅ Still works with keyword matching
- ✅ Responds to: "show card", "show form", "show table"
- ✅ Generates pre-defined widget templates
- ⚠️ Limited to exact keyword matches

## Troubleshooting

### Issue: "Cannot connect to agent"

**Solution:**
1. Check agent is running on `http://localhost:8001`
2. Open browser and visit: `http://localhost:8001`
3. Should see: `{"status":"running",...}`
4. Check CORS settings in `agent.py`

### Issue: "Module not found: google.adk"

**Solution:**
```bash
cd adk-agent
# Make sure venv is activated
pip install google-adk
```

### Issue: Angular won't start

**Solution:**
```bash
cd angular-client
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Port 8001 already in use"

**Solution:**
- Another process is using port 8001
- Kill the process or change port in `agent.py`:
  ```python
  port = int(os.getenv("PORT", 8002))  # Change to 8002
  ```

### Issue: Widgets not rendering

**Check:**
1. Browser console for errors (F12)
2. Network tab - is `/chat` request successful?
3. Agent terminal - any error messages?
4. A2UI JSON format - check response in Network tab

## Verification Checklist

Before testing, verify:

- [ ] Angular client running on `http://localhost:4200`
- [ ] ADK agent running on `http://localhost:8001`
- [ ] Browser opened to Angular app
- [ ] No errors in browser console (F12)
- [ ] No errors in agent terminal
- [ ] API key configured (optional but recommended)

## Quick Test Commands

Copy-paste these into the chatbot:

```
show card
```

```
show form
```

```
show table
```

```
show all
```

## What You Should See

1. **Chatbot Interface:**
   - Welcome message with instructions
   - Input field at bottom
   - Send button

2. **When you send a command:**
   - Your message appears on the right (blue)
   - Bot response appears on the left (gray)
   - Widget appears in a dashed border box
   - Widget is fully interactive

3. **Widget Features:**
   - **Card**: Image, title, content, buttons
   - **Form**: Input fields, validation, submit
   - **Table**: Sortable columns, action buttons, data rows

## Next Steps After Testing

1. ✅ Try different prompts
2. ✅ Test widget interactions
3. ✅ Check browser console for A2UI messages
4. ✅ Review agent terminal for AI responses
5. ✅ Customize widgets (see README.md for instructions)

## Stopping the Demo

1. **Stop Angular:** Press `Ctrl+C` in Terminal 1
2. **Stop Agent:** Press `Ctrl+C` in Terminal 2
3. **Deactivate venv:** Type `deactivate` in Terminal 2

## Need Help?

- Check `README.md` for detailed documentation
- Review `HOW_A2UI_WORKS.md` for architecture explanation
- Check browser console (F12) for errors
- Check agent terminal for error messages

Happy testing! 🚀

