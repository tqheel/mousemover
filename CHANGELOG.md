# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-29

### Added
- **Multi-screen awareness**: Mouse movements are now constrained to the monitor where the cursor is currently located
- New dependency: `screeninfo==0.8.1` for multi-monitor detection
- Enhanced logging that shows which monitor bounds are being used for movements
- Robust fallback system for monitor detection failures

### Changed
- Mouse movement logic now detects current monitor and constrains movements within its bounds
- Updated error handling to gracefully handle monitor detection issues
- Improved user experience by preventing cross-monitor cursor jumps

### Technical Details
- Added `get_current_monitor_bounds()` method to detect active monitor
- Modified `move_mouse()` method to use monitor-specific boundaries
- Updated import statements to include `screeninfo.get_monitors`
- Enhanced error messages for missing dependencies

## [1.0.0] - Initial Release

### Added
- Basic mouse movement functionality with configurable interval and range
- Cross-platform support (macOS, Windows, Linux)
- Automated setup scripts for all platforms
- Virtual environment isolation
- Graceful shutdown with Ctrl+C
- Failsafe mechanism (move to top-left corner to stop)
- Command line argument parsing
- Signal handling for clean shutdown
- Comprehensive documentation and troubleshooting guides
