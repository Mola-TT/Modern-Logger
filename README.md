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

## Project Structure

```
Modern-Logger/
├── modern_logger/
│   ├── __init__.py          # Package initialization with lazy loading
│   ├── gui_logger.py        # GUI logger components
│   ├── logger.py            # Base logger components
│   └── gui_adapter.py       # Adapter to connect GUI logger with base logger
├── examples/
│   ├── cli_example.py       # Example of command-line application
│   └── gui_example.py       # Example of GUI logger usage
├── install.py               # Installation helper script
├── setup.py                 # Package installation configuration
└── README.md                # Project documentation
```

## Installation

### Easy Installation

The easiest way to install Modern Logger is to use the provided installation script:

```bash
# Install with GUI support (requires PySide6)
python install.py

# Install without GUI support
python install.py --no-gui

# Install in development mode
python install.py --dev

# Install without running tests
python install.py --no-test
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

### Dependencies

- **Required**: Python 3.7+, colorama
- **Optional (for GUI)**: PySide6

**Note**: PySide6 is only imported when GUI functionality is explicitly requested. This means you can use all CLI and file logging features without installing PySide6.

## Usage

### Simple ModernLogger Interface

```python
from modern_logger import ModernLogger

# CLI-only logger (no PySide6 required)
logger = ModernLogger(console=True, file="app.log", gui=False)
logger.info("This works without PySide6!")

# GUI logger (requires PySide6)
logger = ModernLogger(console=True, file="app.log", gui=True)
widget = logger.get_gui_widget()  # Get widget for embedding in your app
logger.info("This requires PySide6")

# Close when done
logger.close()
```

### Advanced Usage with Individual Components

```python
from modern_logger import Logger, FileLogger, ConsoleLogger, MultiLogger

# Create loggers
file_logger = FileLogger(filename="app.log", max_size=1024*1024, backup_count=5)
console_logger = ConsoleLogger(use_colors=True)

# Create a multi-logger that writes to both
logger = MultiLogger(loggers=[file_logger, console_logger])

# Log messages
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Log an exception
try:
    1/0
except Exception:
    logger.exception("An error occurred")

# Close loggers when done
logger.close()
```

### GUI Components (Lazy Loading)

```python
# GUI components are only imported when needed
from modern_logger import get_gui_components

try:
    # This will only import PySide6 when called
    GUIModernLogger, GUILogger = get_gui_components()
    
    # Use GUI components...
    gui_widget = GUIModernLogger()
    
except ImportError as e:
    print("PySide6 not available:", e)
    # Fall back to CLI-only functionality
```

### Full GUI Application Example

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from modern_logger import ModernLogger, GUILogger

app = QApplication([])
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

# Create GUI logger widget
gui_widget = ModernLogger()
layout.addWidget(gui_widget)

window.setCentralWidget(central_widget)
window.resize(800, 600)
window.show()

# Create logger that writes to the GUI
logger = GUILogger(gui_logger=gui_widget)

# Log messages
logger.info("This is an info message")
logger.warning("This is a warning message")

# Show progress
logger.start_progress("Starting a long operation...")
for i in range(10):
    # Simulate work
    import time
    time.sleep(0.5)
    # Update progress
    logger.update_progress(i+1, 10, f"Processing item {i+1}")
logger.end_progress("Operation completed successfully")

app.exec()
```

## Dependency Management

Modern Logger uses lazy loading to minimize dependencies:

- **CLI functionality**: Only requires `colorama` (automatically installed)
- **GUI functionality**: Requires `PySide6` (only imported when GUI features are used)

This means you can:
1. Use the library in CLI applications without installing PySide6
2. Add GUI functionality later by installing PySide6
3. Deploy lightweight CLI applications without GUI dependencies

```python
# This works without PySide6 installed
from modern_logger import ModernLogger
logger = ModernLogger(console=True, file="app.log")
logger.info("No GUI dependencies needed!")

# This will show a helpful error if PySide6 is not installed
try:
    logger = ModernLogger(gui=True)
except ImportError as e:
    print(f"GUI not available: {e}")
```

## Customization

### Customize Console Colors

```python
from modern_logger import ConsoleLogger, Logger
from colorama import Fore, Back, Style

console_logger = ConsoleLogger()

# Customize colors for different log levels
console_logger.set_color(Logger.DEBUG, Fore.BLUE)
console_logger.set_color(Logger.INFO, Fore.WHITE)
console_logger.set_color(Logger.WARNING, Fore.YELLOW + Style.BRIGHT)
console_logger.set_color(Logger.ERROR, Fore.RED + Style.BRIGHT)
console_logger.set_color(Logger.CRITICAL, Back.RED + Fore.WHITE + Style.BRIGHT)
```

### Customize GUI Logger

```python
from PySide6.QtGui import QFont
from modern_logger import ModernLogger

gui_logger = ModernLogger()

# Customize the scroll-to-bottom button
gui_logger.customize_scroll_button(
    size=40,
    background_color="rgba(100, 150, 200, 180)",
    hover_color="rgba(120, 170, 220, 220)",
    pressed_color="rgba(80, 130, 180, 220)",
    text="↓",
    font=QFont("Arial", 18, QFont.Bold),
    animation_duration=300,
    shadow_enabled=True,
    shadow_blur=8,
    shadow_offset=(0, 3)
)
```

## Examples

The package includes several examples in the `examples/` directory:

- `cli_example.py`: Shows how to use the loggers in a command-line application
- `gui_example.py`: Demonstrates the GUI logger in a PySide6 application

To run the examples:

```bash
# CLI example
python examples/cli_example.py --log-level DEBUG --messages 30

# GUI example (requires PySide6)
python examples/gui_example.py
```

### Troubleshooting Examples

If you encounter errors when running the examples:

1. Make sure you're running the examples from the project root directory
2. Ensure the package is installed or in your Python path
3. Check that all dependencies are installed
4. Look for error messages in the console output

The examples have been updated to provide better error handling and diagnostics.

## License

MIT License

