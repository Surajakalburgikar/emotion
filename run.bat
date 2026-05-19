@echo off
title Emotion Detector AI Launcher
echo 🚀 Launching Emotion Detector AI Full-Stack App...
echo --------------------------------------------------

:: Check if Anaconda exists, and set python path accordingly
set "PYTHON_PATH=python"
if exist "C:\Users\suraj\anaconda3\python.exe" (
    set "PYTHON_PATH=C:\Users\suraj\anaconda3\python.exe"
    echo ✓ Detected Anaconda environment. Using: C:\Users\suraj\anaconda3\python.exe
) else (
    echo ! Anaconda not found at default path. Using system default 'python'.
)

:: Start Backend in a new CMD window
echo 📦 Starting FastAPI Backend server...
start "Emotion Backend" cmd /k "cd /d "%~dp0backend" && "%PYTHON_PATH%" -m uvicorn app.main:app --reload"

:: Start Frontend in a new CMD window
echo 🎨 Starting Streamlit Frontend server...
start "Emotion Frontend" cmd /k "cd /d "%~dp0frontend" && "%PYTHON_PATH%" -m streamlit run app.py"

echo --------------------------------------------------
echo ✅ Both servers are starting in separate windows!
echo 🔗 Frontend: http://localhost:8501
echo 🔗 Backend:  http://127.0.0.1:8000
echo --------------------------------------------------
pause
