# ModernLogger Examples

This directory contains minimized examples showcasing individual functions of the ModernLogger library. Each example is designed to demonstrate a specific feature with clean, focused code.

## 📁 Example Structure

Each example is contained in its own directory with:
- `example.py` - Minimal, focused demonstration script
- `README.md` - Detailed documentation and usage guide

## 🚀 Quick Start Examples

### Basic Functionality
- **[01_basic_logging](01_basic_logging/)** - Simple console logging with colored output
- **[02_file_logging](02_file_logging/)** - Saving logs to files with dual console/file output
- **[05_log_levels](05_log_levels/)** - Understanding and using different log levels

### Advanced Features
- **[03_console_colors](03_console_colors/)** - Customizing console colors for different log levels
- **[04_multi_logger](04_multi_logger/)** - Combining multiple loggers for complex routing
- **[10_gui_logging](10_gui_logging/)** - Visual log monitoring with PySide6 GUI

### Export Functionality
- **[06_export_log](06_export_log/)** - Exporting to standard .log format
- **[07_export_csv](07_export_csv/)** - Exporting to CSV for spreadsheet analysis  
- **[08_export_xml](08_export_xml/)** - Exporting to XML for system integration
- **[09_export_json](09_export_json/)** - Exporting to JSON for API integration

### GUI Functionality
- **[13_gui_queue_mode](13_gui_queue_mode/)** - Message queuing during loading operations
- **[14_gui_inline_mode](14_gui_inline_mode/)** - Real-time progress updates on single line
- **[15_gui_non_queue_mode](15_gui_non_queue_mode/)** - Immediate message display mode
- **[16_gui_multithread](16_gui_multithread/)** - Thread-safe multi-threaded messaging
- **[17_gui_progress_tracking](17_gui_progress_tracking/)** - Advanced progress monitoring
- **[18_gui_scroll_management](18_gui_scroll_management/)** - Intelligent scroll behavior

### Filtering and Management
- **[11_level_filtering](11_level_filtering/)** - Filtering exports by log level
- **[12_memory_management](12_memory_management/)** - Automatic memory management for long-running apps

## 🎯 Example Categories

### 🆕 Beginner Examples
Start here if you're new to ModernLogger:

1. **[Basic Logging](01_basic_logging/)** - Your first logger
2. **[File Logging](02_file_logging/)** - Saving logs to files
3. **[Log Levels](05_log_levels/)** - Understanding severity levels

### 🎨 Customization Examples
Learn how to customize the logger appearance and behavior:

1. **[Console Colors](03_console_colors/)** - Custom color schemes
2. **[Multi-Logger](04_multi_logger/)** - Complex routing setups

### 📊 Export Examples
Learn how to export and analyze your logs:

1. **[Log Export](06_export_log/)** - Standard log format
2. **[CSV Export](07_export_csv/)** - Spreadsheet-friendly format
3. **[JSON Export](09_export_json/)** - API-ready format
4. **[XML Export](08_export_xml/)** - Structured data format

### 🖥️ GUI Examples
Explore visual logging with advanced GUI features:

1. **[Basic GUI Logging](10_gui_logging/)** - Introduction to GUI logging
2. **[GUI Queue Mode](13_gui_queue_mode/)** - Batch message processing
3. **[GUI Inline Mode](14_gui_inline_mode/)** - Real-time progress updates
4. **[GUI Non-Queue Mode](15_gui_non_queue_mode/)** - Immediate message display
5. **[GUI Multithread](16_gui_multithread/)** - Thread-safe concurrent messaging
6. **[GUI Progress Tracking](17_gui_progress_tracking/)** - Advanced progress monitoring
7. **[GUI Scroll Management](18_gui_scroll_management/)** - Smart scrolling for high volume

### 🔧 Advanced Examples
Advanced features for production applications:

1. **[Level Filtering](11_level_filtering/)** - Selective log processing
2. **[Memory Management](12_memory_management/)** - Performance optimization

## 🏃‍♂️ Quick Run Guide

Each example can be run independently:

```bash
# Navigate to any example directory
cd examples/01_basic_logging

# Run the example
python example.py
```

## 🔗 Example Dependencies

Most examples only require:
- Python 3.7+
- ModernLogger library
- colorama (included in dependencies)

**GUI Examples require:**
- PySide6: `pip install PySide6`

## 📖 Learning Path

### For Beginners
1. Start with **Basic Logging** to understand core concepts
2. Try **File Logging** to see persistent storage
3. Explore **Log Levels** to understand message priorities

### For Developers
1. Check **Multi-Logger** for complex applications
2. Review **Console Colors** for better debugging experience
3. Study **Memory Management** for production deployments

### For GUI Applications
1. Start with **Basic GUI Logging** to understand GUI integration
2. Try **GUI Queue Mode** for batch operations
3. Explore **GUI Inline Mode** for real-time progress
4. Test **GUI Multithread** for concurrent applications

### For Data Analysis
1. Learn **Export Log** for human-readable formats
2. Try **CSV Export** for spreadsheet analysis
3. Use **JSON Export** for programmatic processing

### For System Integration
1. Explore **XML Export** for structured data exchange
2. Study **Level Filtering** for selective processing
3. Consider **GUI Logging** for monitoring interfaces

## 🛠️ Common Patterns

### Basic Usage Pattern
```python
from modern_logger import ModernLogger

logger = ModernLogger()
logger.info("Hello, World!")
logger.close()
```

### File + Console Pattern
```python
logger = ModernLogger(console=True, file="app.log")
logger.info("Message goes to both console and file")
logger.close()
```

### GUI Pattern
```python
logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()
# Add gui_widget to your application layout
logger.info("Message appears in GUI")
logger.close()
```

### Export Pattern
```python
logger = ModernLogger()
# ... generate logs ...
logger.export_log("export.csv", "csv")
logger.close()
```

### Multi-Destination Pattern
```python
from modern_logger import MultiLogger, ConsoleLogger, FileLogger, Logger

console = ConsoleLogger(level=Logger.DEBUG)
file_log = FileLogger("app.log", level=Logger.INFO)
multi = MultiLogger(loggers=[console, file_log])

multi.info("Goes to both destinations")
multi.close()
```

### GUI Queue Mode Pattern
```python
logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Start queue mode
gui_widget.set_loading_on(queue_messages=True)
logger.info("This message is queued")
gui_widget.set_loading_off("Processing complete!")
```

### GUI Progress Pattern
```python
logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Start progress mode
gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)

for i in range(1, 101):
    gui_widget.update_progress(i, 100, f"Processing {i}%")
    time.sleep(0.1)

gui_widget.set_loading_off("Complete!")
```

## 🚀 Next Steps

After exploring these examples:

1. **Read the main [README.md](../README.md)** for complete documentation
2. **Check [setup.py](../setup.py)** for installation options
3. **Review the source code** in [modern_logger/](../modern_logger/) for implementation details
4. **Build your own application** using the patterns from these examples

## 💡 Tips

- Each example is self-contained and can be run independently
- Examples include both basic usage and edge cases
- All examples include proper cleanup with `logger.close()`
- Check the README in each example directory for detailed explanations
- Most examples generate output files that you can examine
- GUI examples provide interactive demonstrations of features

## 🐛 Troubleshooting

**Import Errors:**
- Make sure you're running from the example directory
- Check that ModernLogger is installed or accessible via Python path

**GUI Example Issues:**
- Install PySide6: `pip install PySide6`
- GUI examples will gracefully skip if PySide6 is not available

**File Permission Issues:**
- Examples create files in their directories
- Ensure write permissions in the example directories

## 📞 Support

If you have questions about any example:
1. Check the example's individual README file
2. Review the main project documentation
3. Look at similar examples for patterns
4. Check the source code for implementation details

Happy logging! 🎉 