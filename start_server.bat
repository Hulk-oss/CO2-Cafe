@echo off
cd /d "%~dp0"
:loop
echo Starting CO2 Cafe Backend Server...
call venv\Scripts\activate.bat
python app.py
echo Server crashed or exited. Restarting in 5 seconds...
timeout /t 5
goto loop
