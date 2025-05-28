"""
Command-line example for Modern Logger.

This example demonstrates how to use the loggers in a CLI application.
"""

import sys
import os
import time
import argparse
import random
import traceback
from modern_logger import ModernLogger

# Add the parent directory to the path so we can import the package
try:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
    print(f"Added {parent_dir} to Python path")
except Exception as e:
    print(f"Warning: Could not add parent directory to path: {e}")

try:
    # Import directly from the modern_logger package
    from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger
    print("Successfully imported modern_logger package")
except ImportError as e:
    print(f"Error importing modern_logger: {e}")
    print("\nPossible solutions:")
    print("1. Make sure you're running this script from the examples directory")
    print("2. Install the package with: pip install -e ..")
    print("3. Check if the modern_logger directory exists in the parent directory")
    sys.exit(1)

try:
    from colorama import Fore, Back, Style
    print("Successfully imported colorama")
except ImportError as e:
    print(f"Error importing colorama: {e}")
    print("\nPlease install colorama with: pip install colorama")
    sys.exit(1)


def simulate_application(logger, num_messages=20, delay=0.2):
    """Simulate an application that generates log messages"""
    
    logger.info("Application starting")
    
    # Log some debug messages
    for i in range(num_messages // 4):
        time.sleep(delay * random.uniform(0.5, 1.5))
        logger.debug(f"Debug message {i+1}: Processing data chunk {i}")
    
    # Log some info messages
    for i in range(num_messages // 4):
        time.sleep(delay * random.uniform(0.5, 1.5))
        logger.info(f"Info message {i+1}: Data chunk {i} processed successfully")
    
    # Simulate a warning condition
    time.sleep(delay * 2)
    logger.warning("Warning: System resources running low")
    
    # Continue with more info messages
    for i in range(num_messages // 4):
        time.sleep(delay * random.uniform(0.5, 1.5))
        logger.info(f"Info message {i+1+num_messages//4}: Processing continued")
    
    # Simulate an error condition
    time.sleep(delay * 2)
    logger.error("Error: Failed to connect to external service")
    
    # Try to recover
    time.sleep(delay * 3)
    logger.info("Attempting to reconnect to external service")
    
    # Simulate a critical error
    time.sleep(delay * 2)
    logger.critical("Critical: System shutdown required")
    
    # Log an exception
    try:
        # Simulate a division by zero error
        result = 100 / 0
    except Exception as e:
        logger.exception(f"Exception occurred during calculation: {e}")
    
    # Final messages
    for i in range(num_messages // 4):
        time.sleep(delay * random.uniform(0.5, 1.5))
        logger.info(f"Info message {i+1+num_messages//2}: Shutting down subsystem {i}")
    
    logger.info("Application shutdown complete")


def main():
    """Main function"""
    
    print("Starting Modern Logger CLI Example...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(description="Modern Logger CLI Example")
        parser.add_argument("--log-file", default="cli_example.log", help="Log file name (default: cli_example.log)")
        parser.add_argument("--log-dir", default="logs", help="Log file directory (default: logs)")
        parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
                            help="Minimum log level")
        parser.add_argument("--messages", type=int, default=20, help="Number of messages to generate")
        parser.add_argument("--delay", type=float, default=0.2, help="Delay between messages (seconds)")
        parser.add_argument("--no-color", action="store_true", help="Disable colored output")
        parser.add_argument("--max-size", type=int, default=1024*1024, help="Maximum log file size in bytes")
        parser.add_argument("--backup-count", type=int, default=3, help="Number of backup files to keep")
        
        args = parser.parse_args()
        
        # Construct full log file path
        log_file_path = os.path.join(args.log_dir, args.log_file)
        
        # Create log directory if it doesn't exist
        if args.log_dir and not os.path.exists(args.log_dir):
            os.makedirs(args.log_dir)
            print(f"Created log directory: {args.log_dir}")
        
        # Convert log level string to constant
        log_level = getattr(Logger, args.log_level)
        
        # Create logger with console output and optional file output
        logger = ModernLogger(
            console=True,  # Enable console output
            file=log_file_path  # Enable file output with constructed path
        )
        
        # Print startup message
        print(f"Modern Logger CLI Example")
        print(f"Log Level: {args.log_level}")
        print(f"Log File: {os.path.abspath(log_file_path)}")
        print(f"Generating {args.messages} messages with {args.delay}s delay...")
        print()
        
        # Run the simulation
        try:
            simulate_application(logger, args.messages, args.delay)
        except KeyboardInterrupt:
            logger.warning("Application interrupted by user")
        finally:
            # Close the logger
            logger.close()
            
        print()
        print(f"Log file created at: {os.path.abspath(log_file_path)}")
        
    except Exception as e:
        print(f"Error in CLI example: {e}")
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 