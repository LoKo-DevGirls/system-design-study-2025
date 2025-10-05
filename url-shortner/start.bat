@echo off
echo 🚀 Starting URL Shortener - NeetCodeIO Style
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo.
echo 🎯 Starting the application...
echo 📱 Open your browser to: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
python run.py

pause
