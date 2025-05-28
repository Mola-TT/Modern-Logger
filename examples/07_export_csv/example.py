#!/usr/bin/env python3
"""
Export CSV Example - ModernLogger

This example demonstrates how to export log records
to CSV format for spreadsheet analysis.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("📊 Export CSV Example")
    print("=" * 30)
    
    # Create logger and generate sample logs
    logger = ModernLogger()
    
    print("\n📝 Generating sample logs...")
    logger.info("User login: admin")
    logger.warning("Failed login attempt: user123")
    logger.error("Database connection timeout")
    logger.critical("System overload detected")
    logger.info("User logout: admin")
    
    # Export to CSV format
    print("\n💾 Exporting to CSV format...")
    success = logger.export_log("logs_export.csv", "csv")
    print(f"   ✅ CSV export: {'Success' if success else 'Failed'}")
    
    # Export errors only to CSV
    success = logger.export_log("errors_only.csv", "csv", level_filter=Logger.ERROR)
    print(f"   🚨 Errors CSV: {'Success' if success else 'Failed'}")
    
    # Clean up
    logger.close()
    
    # Show CSV contents
    print("\n📖 CSV file contents:")
    try:
        with open("logs_export.csv", 'r') as f:
            for i, line in enumerate(f):
                print(f"   {i+1}: {line.strip()}")
    except FileNotFoundError:
        print("   File not found")
    
    print("\n💡 Tip: Open the CSV file in Excel or any spreadsheet application!")
    print("✅ CSV export example completed!")

if __name__ == "__main__":
    main() 