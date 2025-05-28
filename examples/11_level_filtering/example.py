#!/usr/bin/env python3
"""
Level Filtering Example - ModernLogger

This example demonstrates how to filter log exports
by log level to get only the logs you need.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("🔍 Level Filtering Example")
    print("=" * 30)
    
    # Create logger and generate diverse logs
    logger = ModernLogger()
    
    print("\n📝 Generating logs at all levels...")
    logger.debug("Debug: Variable x = 42")
    logger.debug("Debug: Function entered")
    logger.info("Info: User logged in")
    logger.info("Info: Processing request")
    logger.warning("Warning: High memory usage")
    logger.warning("Warning: Slow response time")
    logger.error("Error: Database timeout")
    logger.error("Error: File not found")
    logger.critical("Critical: System overload")
    logger.critical("Critical: Emergency shutdown")
    
    print(f"\n📊 Total logs generated: {len(logger.get_records())}")
    
    # Show filtering examples
    print("\n🔍 Filtering examples:")
    
    # Filter by different levels
    filters = [
        (Logger.DEBUG, "DEBUG+", "all logs"),
        (Logger.INFO, "INFO+", "info and above"),
        (Logger.WARNING, "WARNING+", "warnings and above"),
        (Logger.ERROR, "ERROR+", "errors and critical only"),
        (Logger.CRITICAL, "CRITICAL", "critical only")
    ]
    
    for level, name, description in filters:
        filtered = logger.get_records(level_filter=level)
        print(f"   {name:12} ({description:25}): {len(filtered):2} records")
    
    # Export with different filters
    print("\n💾 Exporting with level filters...")
    
    # Export all levels
    logger.export_log("all_levels.log", "log")
    print("   ✅ All levels exported to all_levels.log")
    
    # Export warnings and above
    logger.export_log("warnings_plus.log", "log", level_filter=Logger.WARNING)
    print("   ⚠️  Warnings+ exported to warnings_plus.log")
    
    # Export errors only
    logger.export_log("errors_only.log", "log", level_filter=Logger.ERROR)
    print("   🚨 Errors+ exported to errors_only.log")
    
    # Export to different formats with filtering
    logger.export_log("errors.csv", "csv", level_filter=Logger.ERROR)
    logger.export_log("warnings.json", "json", level_filter=Logger.WARNING)
    
    print("   📊 Errors exported to CSV format")
    print("   📋 Warnings+ exported to JSON format")
    
    # Clean up
    logger.close()
    
    # Show filtered file contents
    print("\n📖 Filtered export contents:")
    
    print("\n   Warnings and above (warnings_plus.log):")
    try:
        with open("warnings_plus.log", 'r') as f:
            for line in f:
                print(f"      {line.strip()}")
    except FileNotFoundError:
        print("      File not found")
    
    print("\n   Errors and critical (errors_only.log):")
    try:
        with open("errors_only.log", 'r') as f:
            for line in f:
                print(f"      {line.strip()}")
    except FileNotFoundError:
        print("      File not found")
    
    print("\n✅ Level filtering example completed!")

if __name__ == "__main__":
    main() 