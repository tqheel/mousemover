# Mouse Mover

A simple Python application that automatically moves your mouse cursor to prevent screen timeout and keep your system active.

## Features

- Configurable movement interval (default: 60 seconds)
- Configurable movement range (default: ±5 pixels)
- **Multi-screen awareness** - keeps mouse movements within the current monitor
- Graceful shutdown with Ctrl+C
- Optional failsafe: move mouse to top-left corner to stop (disabled by default)
- Minimal CPU usage
- Cross-platform compatibility (macOS, Windows, Linux)
- Automated setup scripts for all platforms
- Virtual environment isolation

## Prerequisites

- Python 3.6 or higher
- pip (usually included with Python)

### Platform-Specific Requirements

- **Windows**: [Download Python](https://www.python.org/downloads/) - ensure "Add Python to PATH" is checked during installation
- **macOS**: Python 3 usually comes pre-installed, or install via Homebrew: `brew install python3`
- **Linux**: Install via package manager: `sudo apt install python3 python3-pip` (Ubuntu/Debian) or `sudo yum install python3 python3-pip` (RHEL/CentOS)

## Quick Start

### macOS / Linux

1. Clone or download this repository
2. Open Terminal in the mouse-mover directory
3. Run the setup script:
   ```bash
   ./run_mouse_mover.sh
   ```

### Windows

1. Clone or download this repository
2. Double-click `setup_windows.bat` for automated setup, OR
3. Open Command Prompt/PowerShell in the mouse-mover directory and run:
   - **Command Prompt**: `run_mouse_mover.bat`
   - **PowerShell**: `.\run_mouse_mover.ps1`

## Installation for Global Access

### macOS / Linux - Creating a Symlink

To run Mouse Mover from anywhere on your system, create a symlink:

```bash
# Create ~/.local/bin if it doesn't exist
mkdir -p ~/.local/bin

# Create symlink (choose your preferred name)
ln -sf /full/path/to/mouse-mover/run_mouse_mover.sh ~/.local/bin/msmvr

# Ensure ~/.local/bin is in your PATH (add to ~/.bashrc or ~/.zshrc if needed)
export PATH="$HOME/.local/bin:$PATH"
```

Now you can run `msmvr` from any directory.

**Alternative locations for the symlink:**
- `/usr/local/bin/msmvr` (requires sudo, system-wide)
- `~/bin/msmvr` (if ~/bin is in your PATH)

### Windows - Adding to PATH

**Option 1: Automated Setup (Recommended)**
1. Run `setup_windows.bat` as Administrator
2. Choose "y" when prompted to add to PATH
3. Restart Command Prompt
4. Run `msmvr` from anywhere

**Option 2: Manual PATH Configuration**
1. Run `setup_windows.bat` (creates `msmvr.bat`)
2. Add the mouse-mover directory to your PATH:
   - Open System Properties → Environment Variables
   - Edit the PATH variable
   - Add the full path to your mouse-mover directory
3. Restart Command Prompt
4. Run `msmvr` from anywhere

## Usage

Once installed, you can run Mouse Mover using:

- **Global command** (if set up): `msmvr`
- **From project directory**:
  - macOS/Linux: `./run_mouse_mover.sh`
  - Windows: `run_mouse_mover.bat` or `.\run_mouse_mover.ps1`
- **Direct Python execution** (with manual venv activation):
  ```bash
  # Default settings
  python mouse_mover.py
  
  # Custom interval (30 seconds)
  python mouse_mover.py --interval 30
  
  # Custom movement range (±10 pixels)
  python mouse_mover.py --range 10
  
  # Enable failsafe feature
  python mouse_mover.py --failsafe
  
  # Both custom settings with failsafe
  python mouse_mover.py --interval 45 --range 3 --failsafe
  ```

### Command Line Options

- `-i, --interval`: Time in seconds between mouse movements (default: 60)
- `-r, --range`: Maximum pixels to move in any direction (default: 5)
- `-f, --failsafe`: Enable failsafe (move mouse to top-left corner to stop)
- `-h, --help`: Show help message

### Stopping the Application

- Press `Ctrl+C` in the terminal, OR
- Move your mouse to the top-left corner of the screen (only if failsafe is enabled with `-f`)

## Project Structure

```
mouse-mover/
├── mouse_mover.py           # Main Python application
├── requirements.txt         # Python dependencies
├── run_mouse_mover.sh      # macOS/Linux runner script
├── run_mouse_mover.bat     # Windows Command Prompt runner
├── run_mouse_mover.ps1     # Windows PowerShell runner
├── setup_windows.bat       # Windows setup/installer
├── README.md              # Project documentation
├── CHANGELOG.md           # Version history and changes
├── .gitignore             # Git ignore rules
└── venv/                  # Virtual environment (auto-created)
```

## How It Works

The runner scripts automatically:
1. Check for Python 3 installation
2. Create a virtual environment if it doesn't exist
3. Install required dependencies (pyautogui, screeninfo)
4. Run the mouse mover application

The application detects all connected monitors and constrains mouse movements to the monitor where the cursor is currently located. This prevents the mouse from jumping to other screens and interrupting your workflow.

All scripts use absolute paths, so they work correctly even when called via symlinks or from different directories.

## Troubleshooting

### All Platforms

**Virtual Environment Issues**
- Delete the `venv` folder and run the script again
- Ensure you have write permissions in the directory

**Mouse Doesn't Move**
- Check if security software is blocking pyautogui
- Try running with elevated permissions (sudo/Administrator)
- Ensure no other mouse automation software is running

**Multi-Monitor Issues**
- Mouse movements are constrained to the current monitor automatically
- If monitor detection fails, check that `screeninfo` is properly installed
- Fallback behavior uses primary monitor or full screen bounds

### Windows-Specific

**"Python is not recognized"**
- Ensure Python is installed with "Add to PATH" option
- Restart Command Prompt after Python installation
- Try `python` instead of `python3`

**PowerShell Execution Policy Error**
```powershell
# Run as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Or bypass for single execution:
```powershell
powershell -ExecutionPolicy Bypass -File run_mouse_mover.ps1
```

### macOS-Specific

**"Permission denied" Error**
```bash
chmod +x run_mouse_mover.sh
```

**Accessibility Permissions**
- Go to System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal (or your terminal app) to the allowed list

### Linux-Specific

**Missing Python tkinter (required by pyautogui)**
```bash
# Ubuntu/Debian:
sudo apt-get install python3-tk

# RHEL/CentOS/Fedora:
sudo yum install python3-tkinter
```

**X11 Display Issues (for headless/SSH sessions)**
- Mouse automation requires a display server
- Won't work over SSH without X11 forwarding

## Safety Features

- **Optional failsafe**: Moving the mouse to the top-left corner stops the application (disabled by default, enable with `-f`)
- **Boundary checking**: Mouse movements are constrained within screen boundaries
- **Graceful shutdown**: Handles interrupt signals properly
- **Error handling**: Continues running even if individual mouse movements fail

## Use Cases

- Preventing screen savers during presentations
- Keeping remote desktop sessions active
- Maintaining VPN connections that timeout on inactivity
- Preventing automatic logout from web applications
- Keeping development environments active during long builds

## Uninstallation

1. Remove virtual environment: `rm -rf venv` (or `rmdir /s venv` on Windows)
2. Remove symlink/PATH entry (if created):
   - macOS/Linux: `rm ~/.local/bin/msmvr`
   - Windows: Remove from PATH via Environment Variables
3. Delete the mouse-mover directory

## Dependencies

- `pyautogui==0.9.54` - Mouse and keyboard automation
- `screeninfo==0.8.1` - Multi-monitor detection and bounds

## Security Note

This tool moves your mouse cursor automatically. Only use it on trusted systems and be aware that it will keep your system active, potentially preventing automatic locks or sleep modes.

## License

This project is provided as-is for personal use.

## Contributing

Feel free to submit issues or pull requests for improvements
