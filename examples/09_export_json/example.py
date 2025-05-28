#!/usr/bin/env python3
"""
Export JSON Example - ModernLogger

This example demonstrates how to export log records
to JSON format for API integration and data processing.
"""

import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("📋 Export JSON Example")
    print("=" * 30)
    
    # Create logger and generate sample logs
    logger = ModernLogger()
    
    print("\n📝 Generating sample logs...")
    logger.info("API request started")
    logger.warning("Rate limit approaching")
    logger.error("Authentication failed")
    logger.critical("Database connection lost")
    
    # Export to JSON format
    print("\n💾 Exporting to JSON format...")
    success = logger.export_log("logs_export.json", "json")
    print(f"   ✅ JSON export: {'Success' if success else 'Failed'}")
    
    # Clean up
    logger.close()
    
    # Show JSON contents (pretty formatted)
    print("\n📖 JSON file contents:")
    try:
        with open("logs_export.json", 'r') as f:
            data = json.load(f)
            # Pretty print the JSON
            print(json.dumps(data, indent=2)[:500] + "...")
    except FileNotFoundError:
        print("   File not found")
    except json.JSONDecodeError:
        print("   Invalid JSON format")
    
    print("\n💡 Tip: JSON format is perfect for APIs and data processing!")
    print("✅ JSON export example completed!")

if __name__ == "__main__":
    main() 