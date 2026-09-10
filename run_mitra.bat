@echo off
title Entrepreneur Mitra (SIH26092) Launcher
color 0B

echo ======================================================================
echo           SIH26092: Entrepreneur Mitra (उद्यमी मित्र)
echo      Ministry of Social Justice and Empowerment (MoSJE)
echo ======================================================================
echo.
echo [1/2] Navigating to project directory...
cd /d C:\Users\diksh\Entrepreneur-Mitra

echo [2/2] Launching browser and starting FastAPI server...
timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000/

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
if errorlevel 1 (
    echo.
    echo [ERROR] Could not start server. Please ensure Python is installed and added to PATH.
    pause
)
