@echo off
cd /d "%~dp0"
echo Starting Yap...
python app.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Make sure you ran setup.bat first.
    echo If "Access denied" - right-click and Run as administrator
    pause
)
