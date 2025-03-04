"""
Basic usage example for Modern Logger.

This example demonstrates how to use the different logger types.
"""

import sys
import os
import time
import traceback
import random

# Add the parent directory to the path so we can import the package
try:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
    print(f"Added {parent_dir} to Python path")
except Exception as e:
    print(f"Warning: Could not add parent directory to path: {e}")

try:
    # Import directly from the modern_logger package
    from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger, ModernLogger
    print("Successfully imported modern_logger package")
except ImportError as e:
    print(f"Error importing modern_logger: {e}")
    print("\nPossible solutions:")
    print("1. Make sure you're running this script from the examples directory")
    print("2. Install the package with: pip install -e ..")
    print("3. Check if the modern_logger directory exists in the parent directory")
    sys.exit(1)


def demonstrate_file_logger():
    """Demonstrate the FileLogger"""
    print("\n=== File Logger Example ===")
    
    # Create log directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "example.log")
    
    try:
        # Create a file logger with rotation
        file_logger = FileLogger(
            name="ExampleFileLogger",
            level=Logger.DEBUG,
            filename=log_file,
            max_size=1024*10,  # 10KB
            backup_count=3
        )
        
        # Log some messages
        file_logger.debug("This is a debug message")
        file_logger.info("This is an info message")
        file_logger.warning("This is a warning message")
        file_logger.error("This is an error message")
        file_logger.critical("This is a critical message")
        
        # Log an exception
        try:
            1/0
        except Exception:
            file_logger.exception("An error occurred")
        
        # Close the logger
        file_logger.close()
        
        print(f"Log file created at: {os.path.abspath(log_file)}")
    except Exception as e:
        print(f"Error in file logger demonstration: {e}")
        traceback.print_exc()


def demonstrate_console_logger():
    """Demonstrate the ConsoleLogger"""
    print("\n=== Console Logger Example ===")
    
    try:
        # Create a console logger with colors
        console_logger = ConsoleLogger(
            name="ExampleConsoleLogger",
            level=Logger.DEBUG,
            use_colors=True
        )
        
        # Log some messages
        console_logger.debug("This is a debug message")
        console_logger.info("This is an info message")
        console_logger.warning("This is a warning message")
        console_logger.error("This is an error message")
        console_logger.critical("This is a critical message")
        
        # Log an exception
        try:
            1/0
        except Exception:
            console_logger.exception("An error occurred")
    except Exception as e:
        print(f"Error in console logger demonstration: {e}")
        traceback.print_exc()


def demonstrate_multi_logger():
    """Demonstrate the MultiLogger"""
    print("\n=== Multi Logger Example ===")
    
    # Create log directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "multi.log")
    
    try:
        # Create individual loggers
        file_logger = FileLogger(
            name="MultiFileLogger",
            level=Logger.INFO,
            filename=log_file
        )
        
        console_logger = ConsoleLogger(
            name="MultiConsoleLogger",
            level=Logger.DEBUG,
            use_colors=True
        )
        
        # Create a multi-logger
        multi_logger = MultiLogger(
            name="ExampleMultiLogger",
            level=Logger.DEBUG,
            loggers=[file_logger, console_logger]
        )
        
        # Log some messages
        multi_logger.debug("This is a debug message")
        multi_logger.info("This is an info message")
        multi_logger.warning("This is a warning message")
        multi_logger.error("This is an error message")
        multi_logger.critical("This is a critical message")
        
        # Log an exception
        try:
            1/0
        except Exception:
            multi_logger.exception("An error occurred")
        
        # Close the logger
        multi_logger.close()
        
        print(f"Multi-logger log file created at: {os.path.abspath(log_file)}")
    except Exception as e:
        print(f"Error in multi-logger demonstration: {e}")
        traceback.print_exc()


def main():
    # Create a logger with console and file output
    logger = ModernLogger(
        console=True,  # Enable console output (default)
        file="logs/basic_example.log"  # Enable file output with custom path
    )
    
    # Log some messages
    logger.info("Starting basic example...")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Simulate some work with progress messages
    for i in range(5):
        time.sleep(0.5)
        logger.info(f"Processing item {i+1}/5...")
        
        # Randomly throw an error
        if random.random() < 0.2:
            try:
                raise ValueError(f"Random error on item {i+1}")
            except Exception:
                logger.exception("An error occurred!")
    
    logger.info("Basic example completed!")


if __name__ == "__main__":
    print("Starting Modern Logger basic usage example...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        demonstrate_file_logger()
        demonstrate_console_logger()
        demonstrate_multi_logger()
        
        main()
        
        print("\nAll examples completed. Check the log files for output.")
    except Exception as e:
        print(f"Error running examples: {e}")
        traceback.print_exc() 