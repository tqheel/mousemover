#!/usr/bin/env python3
"""
Mouse Mover Application
Keeps sessions alive by periodically moving the mouse cursor slightly.
"""

import time
import random
import sys
import signal
from datetime import datetime

try:
    import pyautogui
    from screeninfo import get_monitors
except ImportError as e:
    missing_module = str(e).split("'")[1] if "'" in str(e) else "required modules"
    print(f"Error: {missing_module} is required. Install with: pip install pyautogui screeninfo")
    sys.exit(1)

class MouseMover:
    def __init__(self, interval=60, movement_range=5):
        """
        Initialize the mouse mover.
        
        Args:
            interval (int): Time in seconds between mouse movements (default: 60)
            movement_range (int): Maximum pixels to move in any direction (default: 5)
        """
        self.interval = interval
        self.movement_range = movement_range
        self.running = True
        self.move_count = 0
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to stop
        pyautogui.PAUSE = 0.1
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\nReceived signal {signum}. Shutting down gracefully...")
        self.running = False
    
    def get_current_monitor_bounds(self, x, y):
        """Get the bounds of the monitor containing the given coordinates."""
        try:
            monitors = get_monitors()
            for monitor in monitors:
                if (monitor.x <= x < monitor.x + monitor.width and 
                    monitor.y <= y < monitor.y + monitor.height):
                    return {
                        'left': monitor.x,
                        'top': monitor.y,
                        'right': monitor.x + monitor.width - 1,
                        'bottom': monitor.y + monitor.height - 1
                    }
            
            # Fallback to primary monitor if not found
            primary = monitors[0] if monitors else None
            if primary:
                return {
                    'left': primary.x,
                    'top': primary.y,
                    'right': primary.x + primary.width - 1,
                    'bottom': primary.y + primary.height - 1
                }
        except Exception as e:
            print(f"Warning: Could not detect monitors ({e}), using full screen bounds")
        
        # Ultimate fallback to pyautogui screen size
        screen_width, screen_height = pyautogui.size()
        return {
            'left': 0,
            'top': 0,
            'right': screen_width - 1,
            'bottom': screen_height - 1
        }
    
    def move_mouse(self):
        """Move the mouse cursor slightly in a random direction within the current monitor."""
        try:
            # Get current mouse position
            current_x, current_y = pyautogui.position()
            
            # Get bounds of the monitor containing the current mouse position
            bounds = self.get_current_monitor_bounds(current_x, current_y)
            
            # Generate random movement within the specified range
            dx = random.randint(-self.movement_range, self.movement_range)
            dy = random.randint(-self.movement_range, self.movement_range)
            
            # Calculate new position
            new_x = current_x + dx
            new_y = current_y + dy
            
            # Ensure the new position is within the current monitor bounds
            new_x = max(bounds['left'], min(new_x, bounds['right']))
            new_y = max(bounds['top'], min(new_y, bounds['bottom']))
            
            # Move the mouse
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            
            self.move_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Mouse moved to ({new_x}, {new_y}) on monitor [{bounds['left']},{bounds['top']} to {bounds['right']},{bounds['bottom']}] - Move #{self.move_count}")
            
        except pyautogui.FailSafeException:
            print("FailSafe triggered! Mouse moved to top-left corner. Exiting...")
            self.running = False
        except Exception as e:
            print(f"Error moving mouse: {e}")
    
    def start(self):
        """Start the mouse mover loop."""
        print(f"Mouse Mover started!")
        print(f"Interval: {self.interval} seconds")
        print(f"Movement range: ±{self.movement_range} pixels")
        print("Press Ctrl+C to stop or move mouse to top-left corner")
        print("-" * 50)
        
        try:
            while self.running:
                self.move_mouse()
                
                # Sleep in small intervals to allow for responsive shutdown
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received. Stopping...")
        finally:
            print(f"\nMouse Mover stopped. Total moves: {self.move_count}")

def main():
    """Main function with command line argument parsing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Keep sessions alive by moving the mouse periodically")
    parser.add_argument("-i", "--interval", type=int, default=60,
                       help="Time in seconds between mouse movements (default: 60)")
    parser.add_argument("-r", "--range", type=int, default=5,
                       help="Maximum pixels to move in any direction (default: 5)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.interval < 1:
        print("Error: Interval must be at least 1 second")
        sys.exit(1)
    
    if args.range < 1:
        print("Error: Movement range must be at least 1 pixel")
        sys.exit(1)
    
    # Create and start the mouse mover
    mover = MouseMover(interval=args.interval, movement_range=args.range)
    mover.start()

if __name__ == "__main__":
    main()
