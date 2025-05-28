# GUI Multithread Example

This example demonstrates how the GUI logger safely handles messages from multiple threads simultaneously with proper thread safety and message ordering.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Thread-safe message handling from multiple concurrent threads
- Proper message ordering in multithreaded scenarios
- QThread integration with GUI logger
- Real-time display of messages from different threads
- Safe thread termination and cleanup

## How to run

```bash
cd examples/16_gui_multithread
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Thread Safety**: Multiple threads can safely send messages
- **Message Ordering**: Messages appear in the order they are received
- **Concurrent Operations**: Threads run independently
- **Visual Identification**: Each thread's messages are clearly marked
- **Safe Termination**: Proper cleanup when stopping threads

## Usage patterns

```python
from modern_logger import ModernLogger
from PySide6.QtCore import QThread, Signal

class WorkerThread(QThread):
    message_ready = Signal(str)
    
    def run(self):
        # Thread-safe logging
        self.message_ready.emit("Message from worker thread")

# In main thread
logger = ModernLogger(gui=True)
worker = WorkerThread()
worker.message_ready.connect(logger.info)
worker.start()
```

## Thread Safety Features

- **Signal-Slot Connection**: Qt's thread-safe signal system
- **Message Queuing**: Internal message queue handles concurrent access
- **GUI Thread Safety**: All GUI updates happen in the main thread
- **Resource Protection**: Thread-safe resource management

## When to use

Perfect for:
- **Parallel Processing**: Multiple workers processing data simultaneously
- **Background Tasks**: Long-running operations that need to report progress
- **Server Applications**: Handling multiple client connections
- **Data Processing**: Concurrent data analysis or transformation
- **System Monitoring**: Multiple monitoring threads

## Next steps

- Try [GUI Queue Mode](../13_gui_queue_mode/) for batch processing
- Explore [GUI Progress Tracking](../17_gui_progress_tracking/) for progress monitoring
- Learn about [GUI Scroll Management](../18_gui_scroll_management/) for high-volume scenarios 