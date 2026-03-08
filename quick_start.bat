@echo off
echo ========================================
echo Smart Retail Demand Prediction System
echo Quick Start Script
echo ========================================
echo.

echo Step 1: Creating Sample Data...
echo.
python model\process_excel.py --create-sample
echo.

echo Step 2: Finding cleaned data file...
for /f %%i in ('dir /b /od data\cleaned_data_*.csv 2^>nul') do set LATEST_FILE=%%i

if not defined LATEST_FILE (
    echo ERROR: No cleaned data file found!
    echo Please run: python model\process_excel.py
    pause
    exit /b 1
)

echo Found: %LATEST_FILE%
echo.

echo Step 3: Training Model...
python model\train_model.py --source csv --file "data\%LATEST_FILE%"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open a terminal and run: python backend\app.py
echo 2. Open another terminal and run: streamlit run dashboard\app.py
echo.
echo Press any key to exit...
pause >nul
