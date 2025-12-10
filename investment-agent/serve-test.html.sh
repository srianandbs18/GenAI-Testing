#!/bin/bash
echo "Starting HTTP server for test-agent-direct.html..."
echo ""
echo "Open your browser and go to: http://localhost:8080/test-agent-direct.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m http.server 8080

