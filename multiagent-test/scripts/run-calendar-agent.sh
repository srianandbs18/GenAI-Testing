#!/bin/bash
# Start Calendar Agent (A2A Service)

echo "Starting Calendar Agent (A2A Service)..."
cd "$(dirname "$0")/.."
python agent/calendar_agent.py
