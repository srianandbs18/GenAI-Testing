#!/usr/bin/env python3
"""
Simple test script to test the multi-agent system.

Usage:
    python test_agents.py
"""

import requests
import json
import time
import sys

def test_endpoint(url, message, description):
    """Test an agent endpoint with a message"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"Message: {message}")
    print(f"URL: {url}")
    print(f"{'='*60}\n")
    
    payload = {
        "threadId": f"test_session_{int(time.time())}",
        "runId": f"run_{int(time.time())}",
        "messages": [{
            "id": f"msg_{int(time.time())}",
            "role": "user",
            "content": message
        }],
        "state": {},
        "tools": [],
        "context": [],
        "forwardedProps": {}
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"[ERROR] HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
        
        print("📥 Response Events:")
        event_count = 0
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])  # Remove 'data: ' prefix
                        event_type = data.get('type', 'UNKNOWN')
                        print(f"  [{event_count}] {event_type}")
                        
                        if event_type == 'TEXT_MESSAGE_CONTENT':
                            delta = data.get('delta', '')
                            if delta:
                                print(f"      Content: {delta[:100]}...")
                        
                        if event_type == 'TOOL_CALL_START':
                            tool_name = data.get('name', 'unknown')
                            print(f"      [TOOL] Tool Called: {tool_name}")
                            if tool_name == 'CalendarAgent':
                                print(f"      [OK] Calendar Agent is being called!")
                            elif tool_name == 'TextResponder':
                                print(f"      [OK] Text Agent is being called!")
                        
                        if event_type == 'TOOL_CALL_ARGS':
                            tool_name = data.get('name', 'unknown')
                            args = data.get('arguments', {})
                            print(f"      📋 Tool Arguments: {json.dumps(args, indent=8)}")
                        
                        if event_type == 'STATE_SNAPSHOT':
                            state = data.get('state', {})
                            if 'current_booking' in state:
                                print(f"      [CALENDAR] Calendar booking detected!")
                                print(f"      Booking: {json.dumps(state['current_booking'], indent=8)}")
                        
                        if event_type == 'RUN_ERROR':
                            error = data.get('error', {})
                            error_message = error.get('message', 'Unknown error') if isinstance(error, dict) else str(error)
                            error_details = data.get('details', '')
                            print(f"      [ERROR] {error_message}")
                            if error_details:
                                print(f"      Details: {error_details}")
                            # Print full error data for debugging
                            print(f"      Full error data: {json.dumps(data, indent=6)}")
                        
                        event_count += 1
                    except json.JSONDecodeError:
                        pass
        
        print(f"\n[OK] Received {event_count} events")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection Error: Could not connect to {url}")
        print(f"   Make sure the service is running!")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("Multi-Agent System Test Suite")
    print("="*60)
    
    # Test cases
    tests = [
        # Root Agent Tests
        {
            "url": "http://localhost:8000/",
            "message": "What is Python?",
            "description": "Root Agent - General Query (should route to text_responder)"
        },
        {
            "url": "http://localhost:8000/",
            "message": "I want to book an appointment for tomorrow at 2pm",
            "description": "Root Agent - Calendar Booking (should route to calendar_booking via A2A)"
        },
        {
            "url": "http://localhost:8000/",
            "message": "Tell me a joke",
            "description": "Root Agent - General Query (should route to text_responder)"
        },
        
        # Calendar Agent Direct Tests
        {
            "url": "http://localhost:8001/",
            "message": "Book a meeting for next Monday at 10am titled 'Team Standup'",
            "description": "Calendar Agent - Direct Booking"
        },
    ]
    
    results = []
    
    for test in tests:
        result = test_endpoint(test["url"], test["message"], test["description"])
        results.append((test["description"], result))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for description, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {description}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("SUCCESS: All tests passed!")
        return 0
    else:
        print("WARNING: Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
