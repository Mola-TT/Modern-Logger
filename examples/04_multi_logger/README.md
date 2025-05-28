# Multi-Logger Example

This example demonstrates how to combine multiple loggers to send messages to different destinations simultaneously, each with their own log level filtering.

## What it shows

- Creating individual loggers with different configurations
- Combining loggers using MultiLogger
- Different log levels for different destinations
- Adding loggers dynamically
- Automatic message routing based on log levels

## How to run

```bash
cd examples/04_multi_logger
python example.py
```

## Expected output

```
🔀 Multi-Logger Example
==============================

📝 Logging to multiple destinations:
   - Console (DEBUG and above)
   - multi_example.log (INFO and above)
   - errors.log (ERROR and above)

[2025-05-28 15:12:30] [DEBUG]    Debug message - only goes to console
[2025-05-28 15:12:30] [INFO]     Info message - goes to console and multi_example.log
[2025-05-28 15:12:30] [WARNING]  Warning message - goes to console and multi_example.log
[2025-05-28 15:12:30] [ERROR]    Error message - goes to all three destinations
[2025-05-28 15:12:30] [CRITICAL] Critical message - goes to all three destinations

➕ Adding another file logger...
[2025-05-28 15:12:30] [WARNING]  This warning goes to 4 destinations now!
[2025-05-28 15:12:30] [ERROR]    This error goes to 4 destinations too!

📄 File contents:

   multi_example.log:
      [2025-05-28 15:12:30] [INFO]     Info message - goes to console and multi_example.log
      [2025-05-28 15:12:30] [WARNING]  Warning message - goes to console and multi_example.log
      [2025-05-28 15:12:30] [ERROR]    Error message - goes to all three destinations
      [2025-05-28 15:12:30] [CRITICAL] Critical message - goes to all three destinations
      [2025-05-28 15:12:30] [WARNING]  This warning goes to 4 destinations now!
      [2025-05-28 15:12:30] [ERROR]    This error goes to 4 destinations too!

   errors.log:
      [2025-05-28 15:12:30] [ERROR]    Error message - goes to all three destinations
      [2025-05-28 15:12:30] [CRITICAL] Critical message - goes to all three destinations
      [2025-05-28 15:12:30] [ERROR]    This error goes to 4 destinations too!

   warnings.log:
      [2025-05-28 15:12:30] [WARNING]  This warning goes to 4 destinations now!
      [2025-05-28 15:12:30] [ERROR]    This error goes to 4 destinations too!

✅ Multi-logger example completed!
```

## Files created

After running this example, you'll find these log files:
- `multi_example.log` - INFO level and above
- `errors.log` - ERROR level and above  
- `warnings.log` - WARNING level and above

## Key features demonstrated

- **Message Routing**: Messages are sent to appropriate destinations based on log levels
- **Dynamic Configuration**: Loggers can be added/removed at runtime
- **Level Filtering**: Each destination can have its own minimum log level
- **Efficient Distribution**: Same message goes to multiple outputs without duplication

## Use cases

This pattern is useful for:
- **Separate Error Logging**: Keep errors in a dedicated file for monitoring
- **Debug vs Production**: Console shows debug info, files store important messages
- **Log Aggregation**: Send logs to multiple systems (files, databases, network)
- **Alert Systems**: Route critical messages to notification systems

## Configuration patterns

```python
from modern_logger import MultiLogger, ConsoleLogger, FileLogger, Logger

# Create specialized loggers
console = ConsoleLogger(level=Logger.DEBUG)      # All messages to console
general = FileLogger("app.log", level=Logger.INFO)  # General app log
errors = FileLogger("errors.log", level=Logger.ERROR)  # Errors only

# Combine them
multi = MultiLogger(loggers=[console, general, errors])

# Add more loggers dynamically
audit = FileLogger("audit.log", level=Logger.WARNING)
multi.add_logger(audit)

# Remove a logger if needed
multi.remove_logger(console)
```

## Next steps

- Learn about [Log Levels](../05_log_levels/) to understand filtering better
- Try [Export functionality](../06_export_log/) to convert logs to different formats
- Explore [Memory Management](../12_memory_management/) for high-volume logging 