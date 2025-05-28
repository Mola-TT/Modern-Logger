# GUI Non-Queue Mode Example

This example demonstrates the GUI logger's non-queue (passthrough) mode functionality, where messages appear immediately as they are sent, even during loading operations.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Immediate message display during loading operations
- Real-time streaming of messages
- Passthrough mode with loading animations
- No animation mode for direct messaging
- Burst message handling

## How to run

```bash
cd examples/15_gui_non_queue_mode
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Immediate Display**: Messages appear instantly when sent
- **Real-time Feedback**: Perfect for monitoring live operations
- **Loading Animation**: Visual indicator while messages stream
- **High-frequency Messages**: Handles rapid message streams
- **No Queuing**: Messages never wait to be displayed

## Non-Queue Mode Benefits

- **Real-time Monitoring**: See operations as they happen
- **Debugging**: Immediate feedback for troubleshooting
- **Live Data**: Perfect for streaming data visualization
- **User Feedback**: Instant status updates
- **No Delays**: Messages never wait in queue

## Usage patterns

```python
from modern_logger import ModernLogger

logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Enable passthrough mode with loading animation
gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)

# Messages appear immediately
logger.info("This appears right away")
logger.warning("So does this warning")
logger.error("And this error")

# End loading
gui_widget.set_loading_off("Operation completed!")
```

## When to use Non-Queue Mode

Perfect for:
- **System Monitoring**: Real-time system status updates
- **Live Data Streams**: Network traffic, sensor data, etc.
- **Debugging Sessions**: Immediate feedback during development
- **Interactive Operations**: User-driven processes with instant feedback
- **Log Tailing**: Monitoring log files in real-time

## Demonstration Modes

The example provides several demonstrations:

### 1. Passthrough Demo
- Messages appear immediately during loading
- Loading animation continues while messages stream
- Simulates typical monitoring scenario

### 2. Streaming Demo
- High-frequency message stream (50 messages in 5 seconds)
- Tests performance with rapid updates
- Shows different message types streaming

### 3. No Animation Demo
- Direct message display without loading animation
- Pure immediate messaging
- Simplest form of real-time logging

### 4. Burst Messages
- Manual burst of 8 rapid messages
- Tests immediate display capability
- Shows different log levels in quick succession

## Performance Characteristics

- **Immediate Display**: Zero delay between send and display
- **High Throughput**: Handles rapid message streams smoothly
- **Concurrent Safety**: Thread-safe for multiple workers
- **Memory Efficient**: No message queuing overhead

## Interactive Features

The example provides buttons to:
- **Start Passthrough Demo**: Standard real-time messaging with animation
- **Streaming Demo**: High-frequency message stream test
- **No Animation Demo**: Direct messaging without loading indicator
- **Burst Messages**: Send rapid burst of different message types
- **Stop Demo**: Cancel any running operation
- **Clear Messages**: Reset the display

## Comparison with Queue Mode

| Feature | Non-Queue Mode | Queue Mode |
|---------|----------------|------------|
| Message Display | Immediate | Batch on completion |
| User Feedback | Real-time | End of operation |
| Performance | Direct updates | Batch processing |
| Use Case | Monitoring, debugging | File processing, imports |

## Thread Safety

Non-queue mode is thread-safe and works with:
- Multiple QThread workers
- Concurrent message generation
- High-frequency updates
- Real-time data streams

## Visual Features

- Loading animation during operations
- Immediate message appearance
- Smooth scrolling with rapid updates
- Color-coded message levels
- Real-time timestamp display

## Next steps

- Compare with [GUI Queue Mode](../13_gui_queue_mode/) for batch processing
- Try [GUI Multithread](../16_gui_multithread/) for complex threading scenarios
- Explore [GUI Scroll Management](../18_gui_scroll_management/) for handling large message volumes 