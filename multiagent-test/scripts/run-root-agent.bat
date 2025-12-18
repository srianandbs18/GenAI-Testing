@echo off
echo Starting Root Agent...
cd /d "%~dp0\.."
python agent/root_agent.py
pause
