#!/usr/bin/env python3
"""
File Logging Example - ModernLogger

This example demonstrates how to log messages to a file
with optional rotation and backup management.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger

def main():
    print("📁 File Logging Example")
    print("=" * 30)
    
    # Create a logger that writes to file
    log_file = "example.log"
    logger = ModernLogger(console=True, file=log_file)
    
    # Log some messages
    logger.info("This message goes to both console and file")
    logger.warning("File logging is working!")
    logger.error("Error messages are saved to file")
    
    # File-only logger
    file_only_logger = ModernLogger(console=False, file="file_only.log")
    file_only_logger.info("This message only goes to file_only.log")
    file_only_logger.critical("Critical error logged to file")
    
    print(f"\n📄 Log files created:")
    print(f"   - {log_file}")
    print(f"   - file_only.log")
    
    # Clean up
    logger.close()
    file_only_logger.close()
    
    # Show file contents
    print(f"\n📖 Contents of {log_file}:")
    try:
        with open(log_file, 'r') as f:
            for line in f:
                print(f"   {line.strip()}")
    except FileNotFoundError:
        print("   File not found")
    
    print("\n✅ File logging example completed!")

if __name__ == "__main__":
    main() 