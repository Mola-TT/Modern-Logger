# Console Colors Example

This example demonstrates how to customize console output colors for different log levels.

## What it shows

- Default color scheme for log levels
- Customizing colors for individual log levels
- Using foreground and background colors
- Disabling colors completely
- Using colorama for cross-platform color support

## How to run

```bash
cd examples/03_console_colors
python example.py
```

## Expected output

The output will show colored text in your terminal (colors won't appear in plain text):

```
🎨 Console Colors Example
==============================

📺 Default Colors:
[2025-05-28 15:12:30] [DEBUG]    Debug message (cyan)
[2025-05-28 15:12:30] [INFO]     Info message (green)
[2025-05-28 15:12:30] [WARNING]  Warning message (yellow)
[2025-05-28 15:12:30] [ERROR]    Error message (red)
[2025-05-28 15:12:30] [CRITICAL] Critical message (bright red)

🎯 Custom Colors:
[2025-05-28 15:12:30] [DEBUG]    Debug message (magenta)
[2025-05-28 15:12:30] [INFO]     Info message (bright blue)
[2025-05-28 15:12:30] [WARNING]  Warning message (yellow on black)
[2025-05-28 15:12:30] [ERROR]    Error message (white on red)
[2025-05-28 15:12:30] [CRITICAL] Critical message (bright red on yellow)

⚫ No Colors:
[2025-05-28 15:12:30] [INFO]     Info message without colors
[2025-05-28 15:12:30] [ERROR]    Error message without colors

✅ Console colors example completed!
```

## Key features demonstrated

- **Default Colors**: Built-in color scheme that works well
- **Custom Colors**: How to set your own colors for each level
- **Color Combinations**: Foreground, background, and style combinations
- **Color Disable**: Option to turn off colors completely

## Available color options

### Foreground Colors
- `Fore.BLACK`, `Fore.RED`, `Fore.GREEN`, `Fore.YELLOW`
- `Fore.BLUE`, `Fore.MAGENTA`, `Fore.CYAN`, `Fore.WHITE`

### Background Colors
- `Back.BLACK`, `Back.RED`, `Back.GREEN`, `Back.YELLOW`
- `Back.BLUE`, `Back.MAGENTA`, `Back.CYAN`, `Back.WHITE`

### Styles
- `Style.BRIGHT` - Bright/bold text
- `Style.DIM` - Dim text
- `Style.RESET_ALL` - Reset to default

## Configuration examples

```python
from modern_logger import ConsoleLogger, Logger
from colorama import Fore, Back, Style

# Create logger
logger = ConsoleLogger()

# Set custom colors
logger.set_color(Logger.INFO, Fore.BLUE + Style.BRIGHT)
logger.set_color(Logger.ERROR, Fore.WHITE + Back.RED)
logger.set_color(Logger.CRITICAL, Fore.RED + Back.YELLOW + Style.BRIGHT)

# Disable colors
no_color_logger = ConsoleLogger(use_colors=False)
```

## Next steps

- Combine with [File Logging](../02_file_logging/) for colored console + file output
- Learn about [Log Levels](../05_log_levels/) to control which messages appear
- Try [Multi-Logger](../04_multi_logger/) for complex logging setups 