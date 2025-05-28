# Basic Logging Example

This example demonstrates the most basic usage of ModernLogger for console output.

## What it shows

- Creating a ModernLogger instance with default settings
- Logging messages at different levels (INFO, WARNING, ERROR, CRITICAL)
- Basic console output with colored log levels
- Proper logger cleanup

## How to run

```bash
cd examples/01_basic_logging
python example.py
```

## Expected output

```
🚀 Basic Logging Example
==============================
[2025-05-28 15:12:30] [INFO]     Application started successfully
[2025-05-28 15:12:30] [WARNING]  This is a warning message
[2025-05-28 15:12:30] [ERROR]    This is an error message
[2025-05-28 15:12:30] [CRITICAL] This is a critical message

✅ Basic logging example completed!
```

## Key features demonstrated

- **Console Logging**: Messages are displayed in the terminal with colors
- **Log Levels**: Different severity levels are shown with appropriate formatting
- **Timestamp**: Each log entry includes a timestamp
- **Clean Output**: Proper alignment and formatting for readability

## Next steps

- Try [File Logging](../02_file_logging/) to save logs to files
- Explore [Console Colors](../03_console_colors/) to customize log colors
- Learn about [Log Levels](../05_log_levels/) for filtering messages 