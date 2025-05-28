#!/usr/bin/env python3
"""
Export Log Example - ModernLogger

This example demonstrates how to export log records
to standard .log format files.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("📄 Export Log Example")
    print("=" * 30)
    
    # Create logger and generate some sample logs
    logger = ModernLogger()
    
    print("\n📝 Generating sample logs...")
    logger.info("Application started")
    logger.debug("Loading configuration")
    logger.warning("Configuration file not found, using defaults")
    logger.info("Database connection established")
    logger.error("Failed to connect to external service")
    logger.critical("System running low on memory")
    logger.info("Application shutdown initiated")
    
    # Export all logs to standard log format
    print("\n💾 Exporting logs to standard format...")
    
    # Basic export
    success = logger.export_log("export_all.log", "log")
    print(f"   ✅ All logs exported: {'Success' if success else 'Failed'}")
    
    # Export with level filter (WARNING and above)
    success = logger.export_log("export_warnings.log", "log", level_filter=Logger.WARNING)
    print(f"   ⚠️  Warnings+ exported: {'Success' if success else 'Failed'}")
    
    # Export with limit (last 3 logs)
    success = logger.export_log("export_recent.log", "log", limit=3)
    print(f"   🕐 Last 3 logs exported: {'Success' if success else 'Failed'}")
    
    # Clean up
    logger.close()
    
    # Show exported file contents
    print("\n📖 Exported file contents:")
    
    files_to_show = [
        ("export_all.log", "All logs"),
        ("export_warnings.log", "Warnings and above"),
        ("export_recent.log", "Last 3 logs")
    ]
    
    for filename, description in files_to_show:
        print(f"\n   {description} ({filename}):")
        try:
            with open(filename, 'r') as f:
                for line in f:
                    print(f"      {line.strip()}")
        except FileNotFoundError:
            print(f"      File not found")
    
    print("\n✅ Export log example completed!")

if __name__ == "__main__":
    main() 