#!/usr/bin/env python3
"""
Basic Logging Example - ModernLogger

This example demonstrates the simplest way to use ModernLogger
for basic console logging.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger

def main():
    # Create a basic logger (console output by default)
    logger = ModernLogger()
    
    print("🚀 Basic Logging Example")
    print("=" * 30)
    
    # Log different types of messages
    logger.info("Application started successfully")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    print("\n✅ Basic logging example completed!")
    
    # Clean up
    logger.close()

if __name__ == "__main__":
    main() 