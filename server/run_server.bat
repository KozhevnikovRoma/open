@echo off
echo Checking if the server is already running...
netstat -ano | findstr :8000 > nul
if %errorlevel% equ 0 (
    echo Server is already running on port 8000.
    pause
    exit
)
echo Starting the AI_Coordinator Server...
cd /d D:\AI_Coordinator_Project
set PYTHONPATH=%CD%
call venv\Scripts\activate
python -m uvicorn server.server:app --reload --log-level debug
pause
