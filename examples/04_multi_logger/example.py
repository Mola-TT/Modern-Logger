#!/usr/bin/env python3
"""
Multi-Logger Example - ModernLogger

This example demonstrates how to combine multiple loggers
to send messages to different destinations simultaneously.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger

def main():
    print("🔀 Multi-Logger Example")
    print("=" * 30)
    
    # Create individual loggers
    console_logger = ConsoleLogger(level=Logger.DEBUG)
    file_logger = FileLogger("multi_example.log", level=Logger.INFO)
    error_file_logger = FileLogger("errors.log", level=Logger.ERROR)
    
    # Create a multi-logger that combines all three
    multi_logger = MultiLogger(loggers=[console_logger, file_logger, error_file_logger])
    
    print("\n📝 Logging to multiple destinations:")
    print("   - Console (DEBUG and above)")
    print("   - multi_example.log (INFO and above)")
    print("   - errors.log (ERROR and above)")
    
    # Log messages at different levels
    multi_logger.debug("Debug message - only goes to console")
    multi_logger.info("Info message - goes to console and multi_example.log")
    multi_logger.warning("Warning message - goes to console and multi_example.log")
    multi_logger.error("Error message - goes to all three destinations")
    multi_logger.critical("Critical message - goes to all three destinations")
    
    # Add another logger dynamically
    print("\n➕ Adding another file logger...")
    warnings_logger = FileLogger("warnings.log", level=Logger.WARNING)
    multi_logger.add_logger(warnings_logger)
    
    multi_logger.warning("This warning goes to 4 destinations now!")
    multi_logger.error("This error goes to 4 destinations too!")
    
    # Clean up
    multi_logger.close()
    
    # Show what was written to files
    print("\n📄 File contents:")
    for filename in ["multi_example.log", "errors.log", "warnings.log"]:
        print(f"\n   {filename}:")
        try:
            with open(filename, 'r') as f:
                for line in f:
                    print(f"      {line.strip()}")
        except FileNotFoundError:
            print(f"      File not found")
    
    print("\n✅ Multi-logger example completed!")

if __name__ == "__main__":
    main() 