# Export Log Example

This example demonstrates how to export stored log records to standard .log format files with various filtering options.

## What it shows

- Exporting all log records to a .log file
- Filtering exports by log level (WARNING and above)
- Limiting exports to recent records (last N logs)
- Standard log format with proper alignment and timestamps

## How to run

```bash
cd examples/06_export_log
python example.py
```

## Expected output

```
📄 Export Log Example
==============================

📝 Generating sample logs...
[2025-05-28 15:12:30] [INFO]     Application started
[2025-05-28 15:12:30] [WARNING]  Configuration file not found, using defaults
[2025-05-28 15:12:30] [INFO]     Database connection established
[2025-05-28 15:12:30] [ERROR]    Failed to connect to external service
[2025-05-28 15:12:30] [CRITICAL] System running low on memory
[2025-05-28 15:12:30] [INFO]     Application shutdown initiated

💾 Exporting logs to standard format...
   ✅ All logs exported: Success
   ⚠️  Warnings+ exported: Success
   🕐 Last 3 logs exported: Success

📖 Exported file contents:

   All logs (export_all.log):
      [2025-05-28 15:12:30] [INFO]     Application started
      [2025-05-28 15:12:30] [WARNING]  Configuration file not found, using defaults
      [2025-05-28 15:12:30] [INFO]     Database connection established
      [2025-05-28 15:12:30] [ERROR]    Failed to connect to external service
      [2025-05-28 15:12:30] [CRITICAL] System running low on memory
      [2025-05-28 15:12:30] [INFO]     Application shutdown initiated

   Warnings and above (export_warnings.log):
      [2025-05-28 15:12:30] [WARNING]  Configuration file not found, using defaults
      [2025-05-28 15:12:30] [ERROR]    Failed to connect to external service
      [2025-05-28 15:12:30] [CRITICAL] System running low on memory

   Last 3 logs (export_recent.log):
      [2025-05-28 15:12:30] [ERROR]    Failed to connect to external service
      [2025-05-28 15:12:30] [CRITICAL] System running low on memory
      [2025-05-28 15:12:30] [INFO]     Application shutdown initiated

✅ Export log example completed!
```

## Files created

After running this example, you'll find these log files:
- `export_all.log` - All log records in standard format
- `export_warnings.log` - Only WARNING, ERROR, and CRITICAL records
- `export_recent.log` - Only the last 3 log records

## Key features demonstrated

- **Standard Format**: Clean, aligned log format suitable for viewing and processing
- **Level Filtering**: Export only logs at or above a specific level
- **Record Limiting**: Export only the most recent N log records
- **Readable Output**: Properly formatted timestamps and aligned log levels

## Log format details

The exported .log format includes:
- **Timestamp**: `[YYYY-MM-DD HH:MM:SS]` format
- **Log Level**: `[LEVEL]` with consistent padding for alignment
- **Message**: The actual log message
- **Alignment**: All messages align perfectly for easy reading

## Export options

```python
# Export all logs
logger.export_log("all.log", "log")

# Export WARNING level and above
logger.export_log("warnings.log", "log", level_filter=Logger.WARNING)

# Export last 10 logs
logger.export_log("recent.log", "log", limit=10)

# Export last 5 errors
logger.export_log("recent_errors.log", "log", level_filter=Logger.ERROR, limit=5)
```

## Use cases

This format is perfect for:
- **Log Analysis**: Easy to read and process with text tools
- **Debugging**: Human-readable format for troubleshooting
- **Archiving**: Standard format for long-term storage
- **Sharing**: Easy to share with team members or support

## Next steps

- Try [CSV Export](../07_export_csv/) for spreadsheet analysis
- Explore [JSON Export](../09_export_json/) for API integration
- Learn about [Level Filtering](../11_level_filtering/) for advanced filtering 