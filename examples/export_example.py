#!/usr/bin/env python3
"""
Modern Logger Export Example

This example demonstrates how to use the export functionality to save logs
in different formats: .log, .csv, .xml, and .json
"""

import os
import sys
import time
from datetime import datetime

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from modern_logger import ModernLogger, Logger
    print("✅ Successfully imported modern_logger package")
except ImportError as e:
    print(f"❌ Failed to import modern_logger: {e}")
    sys.exit(1)

def generate_sample_logs(logger):
    """Generate diverse sample log messages"""
    
    # Different types of log messages
    log_messages = [
        (Logger.DEBUG, "Debug: Starting application initialization"),
        (Logger.INFO, "Info: Application started successfully"),
        (Logger.INFO, "Info: Processing user request #12345"),
        (Logger.WARNING, "Warning: High memory usage detected (85%)"),
        (Logger.INFO, "Info: Database connection established"),
        (Logger.DEBUG, "Debug: Cache hit for key 'user_session_abc123'"),
        (Logger.ERROR, "Error: Failed to connect to external API service"),
        (Logger.WARNING, "Warning: Retry attempt 2/3 for API connection"),
        (Logger.INFO, "Info: Successfully connected to backup API endpoint"),
        (Logger.DEBUG, "Debug: Processing 150 records from queue"),
        (Logger.INFO, "Info: Batch processing completed successfully"),
        (Logger.WARNING, "Warning: Disk space running low (15% remaining)"),
        (Logger.CRITICAL, "Critical: System overload detected - 98% CPU usage"),
        (Logger.ERROR, "Error: Authentication failed for user 'john.doe'"),
        (Logger.INFO, "Info: User logout processed for session xyz789"),
        (Logger.DEBUG, "Debug: Garbage collection completed"),
        (Logger.INFO, "Info: Application shutdown initiated"),
        (Logger.CRITICAL, "Critical: Emergency shutdown required")
    ]
    
    print("📝 Generating sample log messages...")
    for level, message in log_messages:
        if level == Logger.DEBUG:
            logger.debug(message)
        elif level == Logger.INFO:
            logger.info(message)
        elif level == Logger.WARNING:
            logger.warning(message)
        elif level == Logger.ERROR:
            logger.error(message)
        elif level == Logger.CRITICAL:
            logger.critical(message)
        
        # Small delay for realistic timestamps
        time.sleep(0.1)

def demonstrate_exports(logger):
    """Demonstrate different export formats"""
    
    # Create exports directory
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n📤 Exporting logs in different formats...")
    
    # 1. Export all logs as standard log format
    log_file = f"{export_dir}/complete_logs_{timestamp}.log"
    success = logger.export_log(log_file, "log")
    print(f"   📄 Log format: {'✅ Success' if success else '❌ Failed'} - {log_file}")
    
    # 2. Export all logs as CSV
    csv_file = f"{export_dir}/complete_logs_{timestamp}.csv"
    success = logger.export_log(csv_file, "csv")
    print(f"   📊 CSV format: {'✅ Success' if success else '❌ Failed'} - {csv_file}")
    
    # 3. Export all logs as XML
    xml_file = f"{export_dir}/complete_logs_{timestamp}.xml"
    success = logger.export_log(xml_file, "xml")
    print(f"   🏷️  XML format: {'✅ Success' if success else '❌ Failed'} - {xml_file}")
    
    # 4. Export all logs as JSON
    json_file = f"{export_dir}/complete_logs_{timestamp}.json"
    success = logger.export_log(json_file, "json")
    print(f"   📋 JSON format: {'✅ Success' if success else '❌ Failed'} - {json_file}")
    
    print("\n🔍 Filtered exports...")
    
    # 5. Export only ERROR and CRITICAL logs as CSV
    error_csv = f"{export_dir}/errors_only_{timestamp}.csv"
    success = logger.export_log(error_csv, "csv", level_filter=Logger.ERROR)
    print(f"   🚨 Errors only (CSV): {'✅ Success' if success else '❌ Failed'} - {error_csv}")
    
    # 6. Export only WARNING and above as JSON
    warnings_json = f"{export_dir}/warnings_and_above_{timestamp}.json"
    success = logger.export_log(warnings_json, "json", level_filter=Logger.WARNING)
    print(f"   ⚠️  Warnings+ (JSON): {'✅ Success' if success else '❌ Failed'} - {warnings_json}")
    
    # 7. Export last 5 logs as XML
    recent_xml = f"{export_dir}/recent_5_logs_{timestamp}.xml"
    success = logger.export_log(recent_xml, "xml", limit=5)
    print(f"   🕐 Last 5 logs (XML): {'✅ Success' if success else '❌ Failed'} - {recent_xml}")
    
    # 8. Export last 3 ERROR+ logs as JSON
    recent_errors_json = f"{export_dir}/recent_3_errors_{timestamp}.json"
    success = logger.export_log(recent_errors_json, "json", level_filter=Logger.ERROR, limit=3)
    print(f"   🚨 Last 3 errors (JSON): {'✅ Success' if success else '❌ Failed'} - {recent_errors_json}")

def show_export_contents(logger):
    """Show sample content from exports"""
    
    print("\n📖 Sample export contents:")
    
    # Show log record count
    total_records = len(logger.get_records())
    error_records = len(logger.get_records(level_filter=Logger.ERROR))
    warning_records = len(logger.get_records(level_filter=Logger.WARNING))
    
    print(f"   📊 Total records stored: {total_records}")
    print(f"   🚨 ERROR+ records: {error_records}")
    print(f"   ⚠️  WARNING+ records: {warning_records}")
    
    # Show sample of recent records
    recent_records = logger.get_records(limit=3)
    print(f"\n   📝 Last 3 log records:")
    for i, record in enumerate(recent_records, 1):
        print(f"      {i}. [{record.level_name}] {record.message}")

def main():
    """Main function to run the export example"""
    
    print("🚀 Modern Logger Export Example")
    print("=" * 50)
    
    # Create logger with console output only (to see the logs)
    logger = ModernLogger(console=True, file=False, gui=False)
    
    # Set lower level to capture debug messages
    logger.multi_logger.set_level(Logger.DEBUG)
    
    # Generate sample logs
    generate_sample_logs(logger)
    
    # Show current records
    show_export_contents(logger)
    
    # Demonstrate exports
    demonstrate_exports(logger)
    
    print("\n✅ Export example completed!")
    print("\n💡 Tips:")
    print("   - Check the 'exports/' directory for generated files")
    print("   - Open CSV files in Excel or similar spreadsheet applications")
    print("   - View JSON/XML files in a text editor or browser")
    print("   - Use level_filter to export only specific log levels")
    print("   - Use limit parameter to export only recent logs")
    
    # Clean up
    logger.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Export example interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running export example: {e}")
        import traceback
        traceback.print_exc() 