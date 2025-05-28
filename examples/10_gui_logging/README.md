# GUI Logging Example

This example demonstrates how to use the GUI logger for visual log monitoring and management in Qt-based applications.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Creating a logger with GUI output
- Embedding the GUI widget in your application
- Interactive log generation
- Visual log display with colors and formatting
- Real-time log updates

## How to run

```bash
cd examples/10_gui_logging
pip install PySide6  # if not already installed
python example.py
```

## Features demonstrated

- **Visual Interface**: Modern Qt-based log viewer
- **Real-time Updates**: Logs appear immediately in the GUI
- **Color Coding**: Different colors for different log levels
- **Interactive**: Button to generate sample logs
- **Embeddable**: GUI widget can be added to your application

## Key benefits

- **Visual Monitoring**: See logs in real-time with colors
- **User Friendly**: Better than console for end users
- **Integration**: Easy to embed in existing Qt applications
- **Professional**: Modern look and feel

## Integration in your app

```python
from modern_logger import ModernLogger
from PySide6.QtWidgets import QVBoxLayout

# Create logger with GUI
logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Add to your layout
layout = QVBoxLayout()
layout.addWidget(gui_widget)

# Log messages appear in the GUI
logger.info("This appears in the GUI!")
```

## Next steps

- Combine with [File Logging](../02_file_logging/) for dual output
- Try [Level Filtering](../11_level_filtering/) to control GUI display 