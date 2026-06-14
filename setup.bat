@echo off
cd /d "%~dp0"
echo ===============================================
echo   Yap for Windows - Installing dependencies
echo ===============================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Download at: https://www.python.org/downloads/
    echo Make sure to tick "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo.
echo Installing packages...
echo.

pip install sounddevice numpy keyboard pyperclip groq Pillow pystray pywin32 customtkinter

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed.
    echo Try: right-click this file, Run as administrator
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   Done! Run run.bat to start Yap.
echo ===============================================
echo.
pause
