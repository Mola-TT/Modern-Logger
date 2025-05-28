#!/usr/bin/env python3
"""
Memory Management Example - ModernLogger

This example demonstrates how ModernLogger manages memory
when handling large volumes of log records.
"""

import sys
import os
import time

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ModernLogger, Logger

def main():
    print("💾 Memory Management Example")
    print("=" * 30)
    
    # Create logger with default memory management
    print("\n📝 Creating logger with default memory limit...")
    logger = ModernLogger()
    
    # Show current memory usage
    print(f"Initial records in memory: {len(logger.get_records())}")
    print(f"Memory management: Automatic (default limit: 10,000 records)")
    
    # Generate many log records to demonstrate memory management
    print("\n🔄 Generating 50 log records to demonstrate memory handling...")
    for i in range(50):
        if i % 10 == 0:
            logger.error(f"Error #{i}: Something went wrong")
        elif i % 5 == 0:
            logger.warning(f"Warning #{i}: Resource usage high")
        else:
            logger.info(f"Info #{i}: Processing item {i}")
        
        # Show progress every 20 records
        if (i + 1) % 20 == 0:
            print(f"   Generated {i + 1} records, memory contains: {len(logger.get_records())}")
    
    # Check final memory state
    final_count = len(logger.get_records())
    print(f"\n📊 Memory state:")
    print(f"   Records generated: 50")
    print(f"   Records in memory: {final_count}")
    
    # Show most recent records
    print(f"\n🔍 Most recent records in memory:")
    recent_records = logger.get_records(limit=5)
    for i, record in enumerate(recent_records):
        print(f"   {i+1}. [{record.level_name}] {record.message}")
    
    # Demonstrate memory efficiency with different record counts
    print(f"\n📈 Testing memory efficiency:")
    
    # Test with different volumes
    test_volumes = [10, 25, 50]
    for volume in test_volumes:
        test_logger = ModernLogger()
        
        # Generate test records
        for i in range(volume):
            test_logger.info(f"Test record #{i} for volume {volume}")
        
        memory_count = len(test_logger.get_records())
        print(f"   Volume {volume:2d}: {memory_count:2d} records stored in memory")
        test_logger.close()
    
    # Test export functionality
    print(f"\n💾 Testing export with current records...")
    success = logger.export_log("memory_test.log", "log")
    print(f"   Export success: {success}")
    
    # Export to different formats
    logger.export_log("memory_test.csv", "csv")
    logger.export_log("memory_test.json", "json")
    print(f"   Exported to multiple formats (log, csv, json)")
    
    # Show that records are still available for export
    print(f"\n📖 Sample of exported content:")
    try:
        with open("memory_test.log", 'r') as f:
            lines = f.readlines()
            print(f"   Total lines in export: {len(lines)}")
            print(f"   Last few entries:")
            for line in lines[-3:]:
                print(f"      {line.strip()}")
    except FileNotFoundError:
        print("   Export file not found")
    
    # Memory management benefits
    print(f"\n💡 Memory Management Benefits:")
    print(f"   ✅ Prevents memory leaks in long-running applications")
    print(f"   ✅ Maintains recent logs for debugging and export")
    print(f"   ✅ Automatic cleanup of old records")
    print(f"   ✅ Configurable limits for different use cases")
    
    # Clean up
    logger.close()
    
    print(f"\n✅ Memory management example completed!")

if __name__ == "__main__":
    main() 