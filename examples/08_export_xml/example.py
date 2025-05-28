#!/usr/bin/env python3
"""
Export XML Example - ModernLogger

This example demonstrates how to export log records
to XML format for structured data processing.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("🏷️ Export XML Example")
    print("=" * 30)
    
    # Create logger and generate sample logs
    logger = ModernLogger()
    
    print("\n📝 Generating sample logs...")
    logger.info("System initialization started")
    logger.warning("Memory usage at 75%")
    logger.error("Service connection failed")
    logger.critical("Emergency shutdown required")
    
    # Export to XML format
    print("\n💾 Exporting to XML format...")
    success = logger.export_log("logs_export.xml", "xml")
    print(f"   ✅ XML export: {'Success' if success else 'Failed'}")
    
    # Clean up
    logger.close()
    
    # Show XML contents
    print("\n📖 XML file contents:")
    try:
        with open("logs_export.xml", 'r') as f:
            content = f.read()
            # Pretty print the XML (simple formatting)
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    print(f"   {line}")
    except FileNotFoundError:
        print("   File not found")
    
    print("\n💡 Tip: XML format is perfect for system integration!")
    print("✅ XML export example completed!")

if __name__ == "__main__":
    main() 