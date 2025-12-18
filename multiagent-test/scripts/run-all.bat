@echo off
echo ========================================
echo Multi-Agent System - Start All Services
echo ========================================
echo.
echo This will start both agents in separate windows.
echo.
echo Press any key to continue...
pause >nul

cd /d "%~dp0\.."

echo.
echo Starting Calendar Agent (Port 8001)...
start "Calendar Agent" cmd /k "python agent/calendar_agent.py"

timeout /t 3 /nobreak >nul

echo Starting Root Agent (Port 8000)...
start "Root Agent" cmd /k "python agent/root_agent.py"

echo.
echo ========================================
echo Both agents are starting in separate windows.
echo.
echo Calendar Agent: http://localhost:8001/
echo Root Agent: http://localhost:8000/
echo.
echo Press any key to exit this window...
pause >nul
