@echo off
setlocal enabledelayedexpansion

echo.
echo 🚀 IoT Predictive Maintenance Dashboard - Setup
echo ==================================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
echo Project directory: %SCRIPT_DIR%

REM Change to project directory
cd /d "%SCRIPT_DIR%"

REM Create virtual environment
echo.
echo 1️⃣ Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 2️⃣ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 3️⃣ Upgrading pip...
python -m pip install --upgrade pip setuptools wheel

REM Install requirements
echo 4️⃣ Installing dependencies from requirements.txt...
if exist requirements.txt (
    pip install -r requirements.txt
    echo ✓ Dependencies installed
) else (
    echo ⚠️ requirements.txt not found!
    pause
    exit /b 1
)

REM Run setup.py
echo 5️⃣ Initializing project structure...
python setup.py

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Activate environment: venv\Scripts\activate
echo 2. Run app: streamlit run app.py
echo.
pause
