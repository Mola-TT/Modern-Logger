# Modern Logger

A high-performance, flexible logging system with file, console, and GUI output options designed for modern Python applications.

## ✨ Features

- **🚀 High Performance**: Optimized for minimal overhead and efficient memory usage
- **🎯 Multiple Output Options**: Log to files, console, GUI, or any combination
- **📁 Smart File Logging**: Automatic file creation and intelligent directory handling  
- **🎨 Colorful Console**: Rich console output with customizable colors using colorama
- **🖥️ Modern GUI**: Advanced Qt-based interface with progress indicators, scroll management, and real-time updates
- **🔀 Multi-Logger**: Send logs to multiple destinations simultaneously with intelligent routing
- **⚡ Lazy Loading**: PySide6 only imported when GUI functionality is requested
- **📦 Optional Dependencies**: Full CLI functionality without installing GUI dependencies
- **📊 Advanced Export**: Export logs in multiple formats (LOG, CSV, XML, JSON) with filtering and metadata
- **🧵 Thread-Safe**: Fully thread-safe for multithreaded applications
- **💾 Memory Management**: Automatic memory management for long-running applications

## 🏗️ Project Structure

```
ModernLogger/
├── modern_logger/              # Core package
│   ├── __init__.py            # Package initialization with lazy loading
│   ├── logger.py              # Base logger with export functionality  
│   ├── gui_logger.py          # Advanced GUI logger components
│   └── gui_adapter.py         # GUI-logger integration adapter
├── examples/                   # 18 comprehensive examples
│   ├── 01_basic_logging/      # Simple console logging
│   ├── 02_file_logging/       # File logging with dual output
│   ├── 03_console_colors/     # Custom console colors
│   ├── 04_multi_logger/       # Multiple logger routing
│   ├── 05_log_levels/         # Log level filtering
│   ├── 06_export_log/         # Standard .log export
│   ├── 07_export_csv/         # CSV format export
│   ├── 08_export_xml/         # XML format export  
│   ├── 09_export_json/        # JSON format export
│   ├── 10_gui_logging/        # Basic GUI integration
│   ├── 11_level_filtering/    # Advanced filtering
│   ├── 12_memory_management/  # Memory optimization
│   ├── 13_gui_queue_mode/     # GUI message queuing
│   ├── 14_gui_inline_mode/    # Real-time progress updates
│   ├── 15_gui_non_queue_mode/ # Immediate message display
│   ├── 16_gui_multithread/    # Thread-safe GUI logging
│   ├── 17_gui_progress_tracking/ # Advanced progress monitoring
│   ├── 18_gui_scroll_management/ # Intelligent scroll behavior
│   ├── cli_example.py         # Command-line application demo
│   ├── gui_example.py         # Comprehensive GUI demo
│   ├── export_example.py      # Export functionality demo
│   └── README.md              # Complete examples documentation
├── logs/                       # Generated log files
├── exports/                    # Exported log files
├── .venv/                      # Python virtual environment
├── install.py                  # Automated installation script
├── setup.py                   # Package configuration
├── pyproject.toml             # Modern Python packaging
├── LICENSE                    # MIT license
└── README.md                  # This file
```

## 🚀 Installation

### Automated Installation (Recommended)

```bash
# Full installation with GUI support
python install.py

# Development installation (editable)
python install.py --dev

# CLI-only installation (no GUI dependencies)
python install.py --no-gui
```

### Manual Installation

```bash
# Install from PyPI (CLI-only)
pip install modern-logger

# Install with GUI support
pip install modern-logger[gui]

# Install from source
git clone https://github.com/yourusername/modern-logger.git
cd modern-logger
pip install -e .[gui]  # With GUI support
# or
pip install -e .       # CLI-only
```

## 📖 Quick Start

### Basic Logging
```python
from modern_logger import ModernLogger

# Simple console logging
logger = ModernLogger()
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")
```

### File Logging
```python
# Log to file with automatic directory creation
logger = ModernLogger(file="logs/app.log")
logger.info("This will be written to the file")

# Both console and file
logger = ModernLogger(console=True, file="logs/app.log")
logger.info("This goes to both console and file")
```

### GUI Logging
```python
# Modern GUI with advanced features
logger = ModernLogger(gui=True)
widget = logger.get_gui_widget()

# Add to your application layout
# layout.addWidget(widget)

logger.info("This appears in the GUI logger")

# Advanced GUI features
gui_widget = logger.get_gui_widget()
gui_widget.set_loading_on(queue_messages=True)
logger.info("This message will be queued")
gui_widget.set_loading_off("Operation completed!")
```

## 🔧 Advanced Usage

### Multi-Logger Configuration
```python
from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger

# Create specialized loggers
console = ConsoleLogger(level=Logger.DEBUG)
file_log = FileLogger("app.log", level=Logger.INFO)

# Combine multiple destinations
multi = MultiLogger(loggers=[console, file_log])
multi.info("Goes to both console and file")
```

### Log Export & Analysis
```python
# Generate comprehensive logs
logger = ModernLogger()
logger.info("Application started")
logger.warning("High memory usage")
logger.error("Connection failed")
logger.critical("System overload")

# Export in multiple formats
logger.export_log("logs/all.json", "json")                    # All logs as JSON
logger.export_log("logs/errors.csv", "csv", level_filter=Logger.ERROR)  # Errors only
logger.export_log("logs/recent.xml", "xml", limit=10)         # Last 10 logs
logger.export_log("logs/warnings.log", "log", level_filter=Logger.WARNING) # Warnings+
```

### Thread-Safe GUI Logging
```python
import threading
from modern_logger import ModernLogger

logger = ModernLogger(gui=True)

def worker_function(worker_id):
    for i in range(10):
        logger.info(f"Worker {worker_id}: Processing item {i}")
        time.sleep(0.1)

# Start multiple threads safely
threads = []
for i in range(4):
    thread = threading.Thread(target=worker_function, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
```

## 🎨 GUI Features

The ModernLogger GUI provides advanced features for real-time monitoring:

### **Queue Mode** - Batch Processing
```python
gui_widget.set_loading_on(queue_messages=True)
# Messages are queued during loading
logger.info("Processing item 1...")
logger.info("Processing item 2...")
gui_widget.set_loading_off("All items processed!")  # Messages appear at once
```

### **Inline Mode** - Real-time Progress
```python
gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
for i in range(1, 101):
    gui_widget.update_progress(i, 100, f"Processing {i}%")
    time.sleep(0.1)
gui_widget.set_loading_off("Processing complete!")
```

### **Non-Queue Mode** - Immediate Display
```python
gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)
# Messages appear immediately as they're sent
logger.info("Real-time message 1")
logger.info("Real-time message 2")
```

### **Smart Scroll Management**
- **Auto-scroll**: Automatically follows new messages when at bottom
- **Scroll Button**: Convenient scroll-to-bottom button with centered arrow
- **Position Memory**: Preserves scroll position during operations
- **High Volume**: Handles rapid message streams smoothly

## 📊 Export Formats

### LOG Format (.log)
```
[2025-05-28 14:56:50] [INFO]     Application started
[2025-05-28 14:56:50] [WARNING]  High memory usage detected
[2025-05-28 14:56:50] [ERROR]    Connection failed
```

### CSV Format (.csv)
```csv
Timestamp,Level,Level_Name,Logger_Name,Message
2025-05-28T14:56:50.123456,20,INFO,MultiLogger,Application started
2025-05-28T14:56:50.234567,30,WARNING,MultiLogger,High memory usage
```

### XML Format (.xml)
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

### JSON Format (.json)
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

## 🔧 Export Options

- **format_type**: `"log"`, `"csv"`, `"xml"`, or `"json"`
- **level_filter**: Export only specific levels (`Logger.DEBUG`, `Logger.INFO`, `Logger.WARNING`, `Logger.ERROR`, `Logger.CRITICAL`)
- **limit**: Maximum number of records (most recent logs)

## 📚 Examples

The project includes **18 comprehensive examples** in the `examples/` directory:

### **Foundational Examples (01-05)**
- Basic logging, file logging, console colors, multi-logger, log levels

### **Export Examples (06-09)**  
- Export to .log, .csv, .xml, .json with filtering and metadata

### **Advanced Examples (10-12)**
- GUI integration, level filtering, memory management

### **GUI Functionality Examples (13-18)**
- Queue mode, inline mode, non-queue mode, multithreading, progress tracking, scroll management

### **Running Examples**
```bash
# Run any example
python examples/01_basic_logging/example.py

# Or run the comprehensive demos
python examples/gui_example.py      # Full GUI demonstration
python examples/export_example.py  # Export functionality demo
python examples/cli_example.py     # Command-line usage
```

Each example includes:
- ✅ Self-contained demonstration script
- ✅ Comprehensive README with documentation
- ✅ Interactive features and real-world scenarios
- ✅ Cross-references to related examples

## 🔄 Recent Updates

### **Version 2.1.0** - Enhanced GUI & Examples
- ✅ **18 Complete Examples**: Comprehensive coverage of all functionality
- ✅ **GUI Enhancements**: Queue mode, inline mode, non-queue mode
- ✅ **Thread Safety**: Full multithreading support for GUI
- ✅ **Progress Tracking**: Real-time progress updates with percentage
- ✅ **Scroll Management**: Intelligent auto-scroll with centered arrow button
- ✅ **Memory Management**: Automatic cleanup for long-running applications
- ✅ **Export Improvements**: Enhanced filtering and metadata support

### **Bug Fixes**
- ✅ **Import Error Fix**: Resolved `GUIModernLogger` import issues
- ✅ **Arrow Centering**: Fixed scroll-to-bottom button arrow alignment
- ✅ **Thread Safety**: Improved concurrent logging reliability
- ✅ **Memory Leaks**: Fixed GUI animation memory management

## 🧪 Testing

```bash
# Test basic functionality
python examples/01_basic_logging/example.py

# Test file logging
python examples/02_file_logging/example.py

# Test GUI functionality (requires PySide6)
python examples/10_gui_logging/example.py

# Test export functionality
python examples/export_example.py

# Test high-volume scenarios
python examples/18_gui_scroll_management/example.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Add tests for new functionality
4. Ensure all examples work correctly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PySide6** for the modern GUI framework
- **Colorama** for cross-platform colored terminal output
- **Qt Framework** for robust GUI components
- **Python Community** for excellent logging standards

---

**ModernLogger** - *Efficient, Beautiful, Modern Logging for Python* 🚀

