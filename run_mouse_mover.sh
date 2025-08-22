#!/bin/bash

# Mouse Mover Runner Script
# This script sets up the environment and runs the mouse mover application

# Get the directory where this script is located, resolving symlinks
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, resolve it relative to the symlink's location
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

echo "Setting up Mouse Mover..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/venv"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Install requirements if pyautogui is not available
if ! python3 -c "import pyautogui" 2>/dev/null; then
    echo "Installing required dependencies..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
fi

# Make the Python script executable
chmod +x "$SCRIPT_DIR/mouse_mover.py"

echo "Starting Mouse Mover..."
echo "Use Ctrl+C to stop or move mouse to top-left corner"
echo ""

# Run the mouse mover with any passed arguments
python3 "$SCRIPT_DIR/mouse_mover.py" "$@"
