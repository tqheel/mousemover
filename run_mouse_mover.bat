@echo off
REM Mouse Mover Runner Script for Windows
REM This script sets up the environment and runs the mouse mover application

echo Setting up Mouse Mover...

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Check if Python 3 is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error: Python 3 is required but not installed.
        echo Please install Python from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

REM Check Python version is 3.x
%PYTHON% -c "import sys; exit(0 if sys.version_info[0] >= 3 else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 is required. Current version is Python 2.
    pause
    exit /b 1
)

REM Check if pip is available
%PYTHON% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: pip is required but not installed.
    echo Please ensure pip is installed with your Python installation.
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "%SCRIPT_DIR%\venv" (
    echo Creating virtual environment...
    %PYTHON% -m venv "%SCRIPT_DIR%\venv"
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment and run commands
echo Activating virtual environment...

REM Check if pyautogui is installed in venv
"%SCRIPT_DIR%\venv\Scripts\python.exe" -c "import pyautogui" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    "%SCRIPT_DIR%\venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>&1
    "%SCRIPT_DIR%\venv\Scripts\python.exe" -m pip install -r "%SCRIPT_DIR%\requirements.txt"
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Starting Mouse Mover...
echo Use Ctrl+C to stop or move mouse to top-left corner
echo.

REM Run the mouse mover with any passed arguments
"%SCRIPT_DIR%\venv\Scripts\python.exe" "%SCRIPT_DIR%\mouse_mover.py" %*

REM Pause if the script exits (in case of error)
if %errorlevel% neq 0 (
    echo.
    echo Mouse Mover exited with an error.
    pause
)
