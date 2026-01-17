# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-01-17

### Fixed
- **Improved cursor positioning**: Mouse now moves from current user position instead of jumping back to previous automated position
- Added detection of user mouse movement between automated moves
- Enhanced logging to show when user has moved the mouse
- Eliminated jarring cursor jumps when user moves mouse between automated intervals

### Technical Details
- Added `last_automated_pos` tracking to detect user movement
- Modified `move_mouse()` method to always calculate movement from current cursor position
- Added user movement status indicator in log output

## [2.1.0] - 2025-12-30

### Changed
- **Failsafe is now disabled by default** to prevent unintentional triggering
- Failsafe feature moved to optional command line argument `-f, --failsafe`
- Updated startup messages to show failsafe status
- Improved user experience by reducing accidental shutdowns

### Fixed
- Resolved issue where failsafe was triggered unintentionally during normal use
- Users can now choose whether to enable the top-left corner failsafe mechanism

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
