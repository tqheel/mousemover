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
except ImportError:
    print("Error: pyautogui is required. Install it with: pip install pyautogui")
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
    
    def move_mouse(self):
        """Move the mouse cursor slightly in a random direction."""
        try:
            # Get current mouse position
            current_x, current_y = pyautogui.position()
            
            # Generate random movement within the specified range
            dx = random.randint(-self.movement_range, self.movement_range)
            dy = random.randint(-self.movement_range, self.movement_range)
            
            # Calculate new position
            new_x = current_x + dx
            new_y = current_y + dy
            
            # Ensure the new position is within screen bounds
            screen_width, screen_height = pyautogui.size()
            new_x = max(0, min(new_x, screen_width - 1))
            new_y = max(0, min(new_y, screen_height - 1))
            
            # Move the mouse
            pyautogui.moveTo(new_x, new_y, duration=0.1)
            
            self.move_count += 1
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Mouse moved to ({new_x}, {new_y}) - Move #{self.move_count}")
            
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
