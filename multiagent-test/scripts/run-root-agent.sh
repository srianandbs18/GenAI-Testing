#!/bin/bash
# Start Root Agent

echo "Starting Root Agent..."
cd "$(dirname "$0")/.."
python agent/root_agent.py
