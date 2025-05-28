# GUI Queue Mode Example

This example demonstrates the GUI logger's queue mode functionality, where messages are collected during loading operations and displayed in batch when loading completes.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- How queue mode collects messages during loading
- Batch display of messages when loading ends
- Smooth UI experience during intensive operations
- Worker thread integration with queue mode
- Loading animation with message queuing

## How to run

```bash
cd examples/13_gui_queue_mode
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Message Queuing**: Messages sent during loading are queued
- **Batch Display**: All queued messages appear at once when loading ends
- **Loading Animation**: Visual indicator shows operation in progress
- **Thread Safety**: Worker threads can safely send messages
- **Smooth UI**: No interruption of loading animation by individual messages

## Queue Mode Benefits

- **Performance**: Prevents UI updates during intensive operations
- **User Experience**: Smooth loading animation without interruption
- **Batch Processing**: Messages displayed efficiently in one update
- **Thread Safety**: Safe for multithreaded applications
- **Resource Efficiency**: Reduces GUI update overhead

## Usage patterns

```python
from modern_logger import ModernLogger

logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Start queue mode
gui_widget.set_loading_on(queue_messages=True)

# These messages will be queued
logger.info("Processing item 1...")
logger.info("Processing item 2...")
logger.info("Processing item 3...")

# End loading - all messages appear at once
gui_widget.set_loading_off("Operation completed!")
```

## When to use Queue Mode

Perfect for:
- **File Processing**: Large file operations where many status updates are generated
- **Data Import**: Database imports with progress messages
- **Batch Operations**: Processing multiple items with status for each
- **API Calls**: Multiple API requests with individual status messages
- **Background Tasks**: Long-running operations with periodic updates

## Interactive Features

The example provides buttons to:
- **Start Queue Mode Demo**: Begin a simulation with worker thread
- **Stop Demo**: Cancel the operation in progress
- **Send Immediate Messages**: Send messages outside of queue mode
- **Clear Messages**: Reset the message display

## Thread Safety

Queue mode is thread-safe and works well with:
- QThread workers
- Python threading
- Concurrent operations
- Multiple worker threads

## Next steps

- Try [GUI Inline Mode](../14_gui_inline_mode/) for real-time progress updates
- Explore [GUI Non-Queue Mode](../15_gui_non_queue_mode/) for immediate message display
- Learn about [GUI Multithread](../16_gui_multithread/) for complex threading scenarios 