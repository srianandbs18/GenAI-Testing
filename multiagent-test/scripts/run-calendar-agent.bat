@echo off
echo Starting Calendar Agent (A2A Service)...
cd /d "%~dp0\.."
python agent/calendar_agent.py
pause
