@echo off
title AI Resume Screening System
cd /d "%~dp0"

echo ========================================
echo    AI Resume Screening System
echo ========================================
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo       ERROR: Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)
echo       Python found.

echo [2/4] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo       Virtual environment activated.
) else (
    echo       No virtual environment found. Using system Python.
)

echo [3/4] Checking dependencies...
python -c "import streamlit, pandas, pdfplumber, sklearn, plotly, reportlab" >nul 2>&1
if errorlevel 1 (
    echo       Installing missing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo       ERROR: Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo       All dependencies OK.
)

echo [4/4] Starting application...
echo.
echo ========================================
echo    Opening at http://localhost:8501
echo ========================================
echo.
streamlit run app.py
pause
