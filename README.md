# Modern Logger

A flexible logging system with file, console, and GUI output options.

## Features

- **Multiple Output Options**: Log to files, console, GUI, or any combination
- **File Logging**: Write logs to files with automatic rotation
- **Console Logging**: Colorful console output with customizable colors
- **GUI Logging**: Modern Qt-based GUI with progress indicators and scroll-to-bottom button
- **Multi-Logger**: Send logs to multiple destinations simultaneously
- **Lazy Loading**: PySide6 is only imported when GUI functionality is explicitly requested
- **Optional Dependencies**: CLI functionality works without installing PySide6
- **Log Export**: Export logs in multiple formats (LOG, CSV, XML, JSON) with filtering options

## Project Structure

```
Modern-Logger/
├── modern_logger/
│   ├── __init__.py          # Package initialization with lazy loading
│   ├── gui_logger.py        # GUI logger components
│   ├── logger.py            # Base logger components with export functionality
│   └── gui_adapter.py       # Adapter to connect GUI logger with base logger
├── examples/
│   ├── cli_example.py       # Example of command-line application
│   ├── gui_example.py       # Example of GUI logger usage
│   └── export_example.py    # Example of log export functionality
├── install.py               # Installation helper script
├── setup.py                 # Package installation configuration
├── pyproject.toml           # Modern Python packaging configuration
├── LICENSE                  # MIT license
├── MANIFEST.in              # Package manifest for distribution
└── README.md                # Project documentation
```

## Installation

### Using the Installation Script (Recommended)

```bash
# Run the automated installation script
python install.py

# For development installation (editable)
python install.py --dev

# Install without GUI dependencies
python install.py --no-gui
```

### Manual Installation

You can also install the package manually:

```bash
# Install CLI-only version (no GUI dependencies)
pip install modern-logger

# Install with GUI support
pip install modern-logger[gui]

# Install from source (CLI-only)
git clone https://github.com/yourusername/modern-logger.git
cd modern-logger
pip install -e .

# Install from source with GUI support
pip install -e .[gui]
```

## Usage Examples

### Basic Usage

```python
from modern_logger import ModernLogger

# Create a logger (console output by default)
logger = ModernLogger()

# Log some messages
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### File Logging

```python
from modern_logger import ModernLogger

# Log to file
logger = ModernLogger(file="logs/app.log")
logger.info("This will be written to the file")

# Both console and file
logger = ModernLogger(console=True, file="logs/app.log")
logger.info("This goes to both console and file")
```

### GUI Logging

```python
from modern_logger import ModernLogger

# Create logger with GUI
logger = ModernLogger(gui=True)
widget = logger.get_gui_widget()

# In your application, add the widget to your layout
# layout.addWidget(widget)

logger.info("This appears in the GUI logger")
```

### Log Export

```python
from modern_logger import ModernLogger, Logger

# Create logger and generate some logs
logger = ModernLogger()
logger.info("Application started")
logger.warning("High memory usage")
logger.error("Connection failed")
logger.critical("System overload")

# Export all logs as JSON
logger.export_log("logs/export.json", "json")

# Export only errors and critical logs as CSV
logger.export_log("logs/errors.csv", "csv", level_filter=Logger.ERROR)

# Export last 10 logs as XML
logger.export_log("logs/recent.xml", "xml", limit=10)

# Export warnings and above as standard log format
logger.export_log("logs/warnings.log", "log", level_filter=Logger.WARNING)
```

### Advanced Usage

```python
from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger

# Create individual loggers
console_logger = ConsoleLogger(level=Logger.DEBUG)
file_logger = FileLogger("app.log", level=Logger.INFO)

# Combine multiple loggers
multi_logger = MultiLogger(loggers=[console_logger, file_logger])
multi_logger.info("This goes to both console and file")

# Export functionality
multi_logger.export_log("export.json", "json")
```

## Export Formats

ModernLogger supports exporting logs in four formats:

### 1. LOG Format (.log)
Standard log format with aligned timestamps and levels:
```
[2025-05-28 14:56:50] [INFO]     Application started
[2025-05-28 14:56:50] [WARNING]  High memory usage detected
[2025-05-28 14:56:50] [ERROR]    Connection failed
```

### 2. CSV Format (.csv)
Comma-separated values for Excel/spreadsheet analysis:
```csv
Timestamp,Level,Level_Name,Logger_Name,Message
2025-05-28T14:56:50.123456,20,INFO,MultiLogger,Application started
2025-05-28T14:56:50.234567,30,WARNING,MultiLogger,High memory usage
```

### 3. XML Format (.xml)
Structured XML for system integration:
```xml
<?xml version='1.0' encoding='utf-8'?>
<logs exported_at="2025-05-28T14:56:51.000000" total_records="3">
  <log>
    <timestamp>2025-05-28T14:56:50.123456</timestamp>
    <level>20</level>
    <level_name>INFO</level_name>
    <logger_name>MultiLogger</logger_name>
    <message>Application started</message>
  </log>
</logs>
```

### 4. JSON Format (.json)
JSON format with metadata for API integration:
```json
{
  "metadata": {
    "exported_at": "2025-05-28T14:56:51.000000",
    "total_records": 3,
    "logger_name": "MultiLogger"
  },
  "logs": [
    {
      "timestamp": "2025-05-28T14:56:50.123456",
      "level": 20,
      "level_name": "INFO",
      "message": "Application started",
      "logger_name": "MultiLogger"
    }
  ]
}
```

## Export Options

- **format_type**: `"log"`, `"csv"`, `"xml"`, or `"json"`
- **level_filter**: Export only logs at or above specified level (use `Logger.DEBUG`, `Logger.INFO`, `Logger.WARNING`, `Logger.ERROR`, `Logger.CRITICAL`)
- **limit**: Maximum number of records to export (most recent logs)

## Examples

The package includes several examples in the `examples/` directory:

- `cli_example.py`: Shows how to use the loggers in a command-line application
- `gui_example.py`: Demonstrates GUI logger usage in a PySide6 application
- `export_example.py`: Comprehensive demonstration of log export functionality

Run any example:
```bash
python examples/export_example.py
```

## License

MIT License

