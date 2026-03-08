@echo off
echo ========================================
echo Smart Retail Demand Prediction System
echo Quick Start Setup
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Create virtual environment if it doesn't exist
if exist venv\ (
    echo [OK] Virtual environment found
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo.

REM Check if .env exists
if exist .env (
    echo [OK] .env file found
) else (
    echo Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please edit .env file with your MySQL credentials
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Configure MySQL credentials in .env file
echo 2. Run database schema in MySQL
echo 3. Train the model: python model\train_model.py
echo 4. Start backend: python backend\app.py
echo 5. Start dashboard: streamlit run dashboard\app.py
echo.
echo For detailed instructions, see README.md
echo.
pause
