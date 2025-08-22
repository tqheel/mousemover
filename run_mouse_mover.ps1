# Mouse Mover Runner Script for Windows PowerShell
# This script sets up the environment and runs the mouse mover application

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Setting up Mouse Mover..." -ForegroundColor Green

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Find Python executable
$Python = $null
if (Test-Command "python") {
    # Check if it's Python 3
    $version = & python -c "import sys; print(sys.version_info[0])" 2>$null
    if ($version -eq "3") {
        $Python = "python"
    }
}

if (-not $Python -and (Test-Command "python3")) {
    $Python = "python3"
}

if (-not $Python) {
    Write-Host "Error: Python 3 is required but not installed." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
$pipCheck = & $Python -m pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: pip is required but not installed." -ForegroundColor Red
    Write-Host "Please ensure pip is installed with your Python installation." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Virtual environment path
$VenvPath = Join-Path $ScriptDir "venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"

# Check if virtual environment exists, create if not
if (-not (Test-Path $VenvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & $Python -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow

# Check if pyautogui is installed
$pyautoguiCheck = & $VenvPython -c "import pyautogui" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing required dependencies..." -ForegroundColor Yellow
    
    # Upgrade pip first (suppress output unless error)
    & $VenvPython -m pip install --upgrade pip | Out-Null
    
    # Install requirements
    $RequirementsPath = Join-Path $ScriptDir "requirements.txt"
    & $VenvPython -m pip install -r $RequirementsPath
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install dependencies." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Starting Mouse Mover..." -ForegroundColor Green
Write-Host "Use Ctrl+C to stop or move mouse to top-left corner" -ForegroundColor Cyan
Write-Host ""

# Run the mouse mover with any passed arguments
$MouseMoverPath = Join-Path $ScriptDir "mouse_mover.py"
& $VenvPython $MouseMoverPath $args

# Check if the script exited with an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Mouse Mover exited with an error." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
