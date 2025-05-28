# Memory Management Example

This example demonstrates how ModernLogger efficiently manages memory when handling large volumes of log records, preventing memory leaks in long-running applications.

## What it shows

- Automatic memory management for log records
- How the logger maintains recent records while preventing memory growth
- Memory efficiency testing with different volumes
- Export functionality with memory-managed records
- Benefits of built-in memory management

## How to run

```bash
cd examples/12_memory_management
python example.py
```

## Expected output

```
💾 Memory Management Example
==============================

📝 Creating logger with default memory limit...
Initial records in memory: 0
Memory management: Automatic (default limit: 10,000 records)

🔄 Generating 50 log records to demonstrate memory handling...
   Generated 20 records, memory contains: 20
   Generated 40 records, memory contains: 40

📊 Memory state:
   Records generated: 50
   Records in memory: 50

🔍 Most recent records in memory:
   1. [INFO] Info #49: Processing item 49
   2. [ERROR] Error #40: Something went wrong
   3. [INFO] Info #48: Processing item 48
   4. [INFO] Info #47: Processing item 47
   5. [WARNING] Warning #45: Resource usage high

📈 Testing memory efficiency:
   Volume 10: 10 records stored in memory
   Volume 25: 25 records stored in memory
   Volume 50: 50 records stored in memory

💾 Testing export with current records...
   Export success: True
   Exported to multiple formats (log, csv, json)

📖 Sample of exported content:
   Total lines in export: 50
   Last few entries:
      [2025-05-28 15:12:30] [INFO]     Info #47: Processing item 47
      [2025-05-28 15:12:30] [INFO]     Info #48: Processing item 48
      [2025-05-28 15:12:30] [INFO]     Info #49: Processing item 49

💡 Memory Management Benefits:
   ✅ Prevents memory leaks in long-running applications
   ✅ Maintains recent logs for debugging and export
   ✅ Automatic cleanup of old records
   ✅ Configurable limits for different use cases

✅ Memory management example completed!
```

## Key features demonstrated

- **Automatic Management**: No manual memory cleanup required
- **Configurable Limits**: Default 10,000 record limit (adjustable)
- **Recent Record Retention**: Always keeps the most recent logs
- **Export Compatibility**: All records in memory can be exported
- **Performance Monitoring**: Track memory usage during operation

## Memory management strategy

The logger uses a circular buffer approach:
1. **Storage**: Keeps the most recent N records in memory (default: 10,000)
2. **Cleanup**: Automatically removes oldest records when limit is reached
3. **Access**: All memory operations are O(1) for recent records
4. **Export**: Current memory contents can be exported at any time

## Benefits for long-running applications

- **Memory Safety**: Prevents unbounded memory growth
- **Performance**: Maintains consistent memory footprint
- **Debugging**: Recent logs always available for troubleshooting
- **Export Ready**: Can export logs at any point without memory issues

## Configuration options

```python
from modern_logger import ModernLogger

# Default memory management (10,000 records)
logger = ModernLogger()

# Access memory management features
records = logger.get_records()  # Get all records in memory
recent = logger.get_records(limit=100)  # Get last 100 records

# Export current memory contents
logger.export_log("current.log", "log")
```

## Use cases

Perfect for:
- **Server Applications**: Long-running web servers
- **Background Services**: Continuous processing applications  
- **Monitoring Tools**: Real-time system monitoring
- **Development**: Debug info without memory concerns

## Next steps

- Combine with [Export functionality](../06_export_log/) for periodic log archiving
- Use with [Level Filtering](../11_level_filtering/) to manage different log priorities
- Integrate with [File Logging](../02_file_logging/) for persistent storage 