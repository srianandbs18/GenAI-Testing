#!/usr/bin/env python3
"""
Simple Python script to test the Investment Agent's AG-UI protocol flow.
This script sends a request to the agent and displays the protocol events.
"""

import requests
import json
import sys
from typing import Dict, List, Any

def test_investment_agent(
    agent_url: str = "http://localhost:8000/",
    message: str = "I want to invest $50,000. What are my options?",
    session_id: str = None
):
    """
    Test the investment agent by sending a request and displaying events.
    
    Args:
        agent_url: URL of the investment agent endpoint
        message: Investment request message
        session_id: Optional session ID for conversation continuity
    """
    if session_id is None:
        session_id = f"investment_test_{int(__import__('time').time())}"
    
    print("=" * 80)
    print("💼 Investment Agent AG-UI Protocol Test")
    print("=" * 80)
    print(f"Agent URL: {agent_url}")
    print(f"Session ID: {session_id}")
    print(f"Message: {message}")
    print("=" * 80)
    print()
    
    # First, check health endpoint
    try:
        health_url = agent_url.rstrip('/') + '/health'
        print(f"🔍 Checking agent health at {health_url}...")
        health_response = requests.get(health_url, timeout=5)
        if health_response.ok:
            health_data = health_response.json()
            print(f"✅ Agent is healthy: {health_data.get('status', 'unknown')}")
        else:
            print(f"⚠️  Agent health check returned status {health_response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check agent health: {e}")
        print("   Continuing anyway...")
    print()
    
    # Construct AG-UI protocol request
    request_body = {
        "threadId": session_id,
        "runId": f"run_{int(__import__('time').time() * 1000)}",
        "state": {},  # Must be an object/dictionary
        "messages": [
            {
                "id": f"msg_{int(__import__('time').time() * 1000)}",
                "role": "user",
                "content": message
            }
        ],
        "tools": [],  # Array of tool definitions
        "context": [],  # Must be an array
        "forwardedProps": {}  # Required by add_adk_fastapi_endpoint
    }
    
    print("📤 Sending AG-UI protocol request...")
    print(f"Request body: {json.dumps(request_body, indent=2)}")
    print()
    
    try:
        # Send request with SSE support
        response = requests.post(
            agent_url,
            json=request_body,
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream"
            },
            stream=True,  # Important for SSE
            timeout=60
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        print()
        
        if not response.ok:
            error_text = response.text
            print(f"❌ Error Response:")
            print(error_text[:500])
            return
        
        # Parse SSE stream
        events = []
        content_type = response.headers.get('Content-Type', '')
        
        if 'text/event-stream' in content_type:
            print("📡 Parsing Server-Sent Events (SSE) stream...")
            print()
            
            buffer = ""
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                
                if line.startswith('data: '):
                    try:
                        event_data = json.loads(line[6:])  # Remove 'data: ' prefix
                        events.append(event_data)
                        print(f"📨 Event {len(events)}: {event_data.get('type', 'UNKNOWN')}")
                    except json.JSONDecodeError as e:
                        print(f"⚠️  Failed to parse event: {line[:100]}...")
                        print(f"   Error: {e}")
        else:
            # Try JSON response
            try:
                data = response.json()
                events = [data] if isinstance(data, dict) else data
                print("📨 Received JSON response (not SSE)")
            except:
                text = response.text
                print(f"📨 Received text response: {text[:200]}...")
                events = []
        
        print()
        print("=" * 80)
        print("📊 Protocol Events Analysis")
        print("=" * 80)
        print()
        
        # Analyze events
        event_types = {}
        investment_options = None
        state_snapshots = []
        tool_calls = []
        text_messages = []
        
        for event in events:
            event_type = event.get('type', 'UNKNOWN')
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Extract investment options from STATE_SNAPSHOT
            if event_type == 'STATE_SNAPSHOT' and event.get('state'):
                state = event.get('state', {})
                if 'investment_options' in state:
                    investment_options = state['investment_options']
                state_snapshots.append(state)
            
            # Extract tool calls
            if event_type in ['TOOL_CALL_START', 'TOOL_CALL_END', 'TOOL_CALL_RESULT']:
                tool_calls.append(event)
            
            # Extract text messages
            if event_type in ['TEXT_MESSAGE_CONTENT', 'TEXT_MESSAGE_END']:
                text_messages.append(event)
        
        # Display summary
        print(f"📈 Total Events: {len(events)}")
        print(f"📋 Event Types: {', '.join(event_types.keys())}")
        print()
        
        for event_type, count in event_types.items():
            print(f"   {event_type}: {count}")
        print()
        
        # Display investment options if found
        if investment_options:
            print("=" * 80)
            print("💼 Investment Options Found")
            print("=" * 80)
            print()
            for i, option in enumerate(investment_options, 1):
                print(f"{i}. {option.get('name', 'Unnamed')}")
                print(f"   Description: {option.get('description', 'N/A')}")
                print(f"   Risk Level: {option.get('riskLevel', 'N/A')}")
                print(f"   Minimum Amount: ${option.get('minimumAmount', 0):,}")
                print(f"   Status: {option.get('status', 'N/A')}")
                print()
        else:
            print("⚠️  No investment options found in STATE_SNAPSHOT events")
            print("   The agent may not have called generate_investment_options tool yet")
            print()
        
        # Display tool calls
        if tool_calls:
            print("=" * 80)
            print("🔧 Tool Calls")
            print("=" * 80)
            for tool_call in tool_calls:
                print(f"Type: {tool_call.get('type')}")
                if 'name' in tool_call:
                    print(f"Tool: {tool_call.get('name')}")
                if 'result' in tool_call:
                    print(f"Result: {json.dumps(tool_call.get('result'), indent=2)}")
                print()
        
        # Display text messages
        if text_messages:
            print("=" * 80)
            print("💬 Text Messages")
            print("=" * 80)
            message_content = []
            for msg in text_messages:
                content = msg.get('content') or msg.get('text') or msg.get('delta', '')
                if content:
                    message_content.append(content)
            if message_content:
                print(''.join(message_content))
            print()
        
        # Display all events in detail
        print("=" * 80)
        print("📋 All Events (Detailed)")
        print("=" * 80)
        for i, event in enumerate(events, 1):
            print(f"\nEvent {i}:")
            print(json.dumps(event, indent=2))
        
        print()
        print("=" * 80)
        print("✅ Test Complete")
        print("=" * 80)
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to agent server")
        print(f"   Make sure the agent is running at: {agent_url}")
        print("   Start it with: npm run dev:agent")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Agent did not respond in time")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Investment Agent AG-UI Protocol")
    parser.add_argument(
        "--url",
        default="http://localhost:8000/",
        help="Agent URL (default: http://localhost:8000/)"
    )
    parser.add_argument(
        "--message",
        default="I want to invest $50,000. What are my options?",
        help="Investment request message"
    )
    parser.add_argument(
        "--session",
        default=None,
        help="Session ID (optional, auto-generated if not provided)"
    )
    
    args = parser.parse_args()
    
    test_investment_agent(
        agent_url=args.url,
        message=args.message,
        session_id=args.session
    )

