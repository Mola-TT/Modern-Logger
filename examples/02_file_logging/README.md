# File Logging Example

This example demonstrates how to save log messages to files using ModernLogger.

## What it shows

- Logging to both console and file simultaneously
- Creating file-only loggers (no console output)
- Automatic log file creation
- Reading and displaying log file contents

## How to run

```bash
cd examples/02_file_logging
python example.py
```

## Expected output

```
📁 File Logging Example
==============================
[2025-05-28 15:12:30] [INFO]     This message goes to both console and file
[2025-05-28 15:12:30] [WARNING]  File logging is working!
[2025-05-28 15:12:30] [ERROR]    Error messages are saved to file

📄 Log files created:
   - example.log
   - file_only.log

📖 Contents of example.log:
   [2025-05-28 15:12:30] [INFO]     This message goes to both console and file
   [2025-05-28 15:12:30] [WARNING]  File logging is working!
   [2025-05-28 15:12:30] [ERROR]    Error messages are saved to file

✅ File logging example completed!
```

## Files created

After running this example, you'll find these log files:
- `example.log` - Contains logs from the dual console/file logger
- `file_only.log` - Contains logs from the file-only logger

## Key features demonstrated

- **Dual Output**: Messages can go to both console and file
- **File-Only Logging**: Some loggers can write only to files
- **Automatic File Creation**: Log files are created automatically
- **Persistent Storage**: Log messages are saved for later analysis

## Configuration options

```python
# Basic file logging
logger = ModernLogger(file="app.log")

# Both console and file
logger = ModernLogger(console=True, file="app.log")

# File-only (no console output)
logger = ModernLogger(console=False, file="app.log")
```

## Next steps

- Learn about [Log Levels](../05_log_levels/) to filter what gets written
- Try [Export functionality](../06_export_log/) to convert logs to different formats
- Explore [Multi-Logger](../04_multi_logger/) for advanced file management 