#!/usr/bin/env python3
"""
Log Levels Example - ModernLogger

This example demonstrates how to use different log levels
and control which messages are displayed or recorded.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("📊 Log Levels Example")
    print("=" * 30)
    
    # Show all available log levels
    print("\n📋 Available log levels:")
    print(f"   DEBUG    = {Logger.DEBUG}")
    print(f"   INFO     = {Logger.INFO}")
    print(f"   WARNING  = {Logger.WARNING}")
    print(f"   ERROR    = {Logger.ERROR}")
    print(f"   CRITICAL = {Logger.CRITICAL}")
    
    # Create logger with INFO level (default)
    print(f"\n🔍 Logger with INFO level (shows INFO and above):")
    info_logger = ModernLogger()
    info_logger.debug("Debug message - won't show")
    info_logger.info("Info message - will show")
    info_logger.warning("Warning message - will show")
    info_logger.error("Error message - will show")
    info_logger.critical("Critical message - will show")
    
    # Create logger with WARNING level
    print(f"\n⚠️ Logger with WARNING level (shows WARNING and above):")
    warning_logger = ModernLogger()
    warning_logger.multi_logger.set_level(Logger.WARNING)
    warning_logger.debug("Debug message - won't show")
    warning_logger.info("Info message - won't show")
    warning_logger.warning("Warning message - will show")
    warning_logger.error("Error message - will show")
    warning_logger.critical("Critical message - will show")
    
    # Create logger with DEBUG level (shows everything)
    print(f"\n🐛 Logger with DEBUG level (shows everything):")
    debug_logger = ModernLogger()
    debug_logger.multi_logger.set_level(Logger.DEBUG)
    debug_logger.debug("Debug message - will show")
    debug_logger.info("Info message - will show")
    debug_logger.warning("Warning message - will show")
    debug_logger.error("Error message - will show")
    debug_logger.critical("Critical message - will show")
    
    # Create logger with ERROR level (only errors and critical)
    print(f"\n🚨 Logger with ERROR level (shows ERROR and CRITICAL only):")
    error_logger = ModernLogger()
    error_logger.multi_logger.set_level(Logger.ERROR)
    error_logger.debug("Debug message - won't show")
    error_logger.info("Info message - won't show")
    error_logger.warning("Warning message - won't show")
    error_logger.error("Error message - will show")
    error_logger.critical("Critical message - will show")
    
    # Exception logging
    print(f"\n💥 Exception logging:")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        error_logger.exception("Division by zero occurred")
    
    # Clean up
    info_logger.close()
    warning_logger.close()
    debug_logger.close()
    error_logger.close()
    
    print("\n✅ Log levels example completed!")

if __name__ == "__main__":
    main() 