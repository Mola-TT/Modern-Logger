# GUI Inline Mode Example

This example demonstrates the GUI logger's inline mode functionality, where progress updates are displayed in real-time by updating a single line in the interface.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Real-time progress updates on a single line
- Inline progress tracking with percentage and custom messages
- Fast update performance testing
- Static progress demonstration
- Clean interface with immediate feedback

## How to run

```bash
cd examples/14_gui_inline_mode
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Real-time Updates**: Progress shown immediately as it happens
- **Single Line Display**: Progress updates replace the previous line
- **Custom Messages**: Each progress update can include custom text
- **Percentage Tracking**: Built-in current/total progress calculation
- **Performance**: Handles rapid updates smoothly

## Inline Mode Benefits

- **Immediate Feedback**: Users see progress as it happens
- **Clean Interface**: Single line prevents message spam
- **Accurate Progress**: Real-time percentage and status updates
- **Resource Efficient**: Updates existing content instead of adding new
- **User Friendly**: Clear visual indication of operation progress

## Usage patterns

```python
from modern_logger import ModernLogger

logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Enable inline mode
gui_widget.set_loading_on(
    queue_messages=False, 
    passthrough_messages=True, 
    inline_update=True
)

# Update progress in real-time
for i in range(1, 101):
    gui_widget.update_progress(i, 100, f"Processing item {i}")
    time.sleep(0.1)

# Complete the operation
gui_widget.set_loading_off("Processing completed!")
```

## When to use Inline Mode

Perfect for:
- **File Uploads**: Show upload progress with bytes transferred
- **Data Processing**: Display current item being processed
- **Downloads**: Real-time download progress
- **Calculations**: Progress through computational steps
- **Import/Export**: Database or file processing progress

## Interactive Features

The example provides buttons to:
- **Start Inline Demo**: Standard inline progress demonstration
- **Fast Updates Demo**: High-frequency update testing (100 updates)
- **Static Progress Demo**: Manual step-by-step progress
- **Stop Demo**: Cancel any running operation
- **Clear Messages**: Reset the display

## Performance Testing

The example includes performance tests:
- **Standard Updates**: 20 steps over 6 seconds (moderate speed)
- **Fast Updates**: 100 steps over 5 seconds (rapid updates)
- **Static Updates**: Manual 5-step demonstration

## Progress Update API

```python
# Update progress with current/total and message
gui_widget.update_progress(current, total, message)

# Examples
gui_widget.update_progress(25, 100, "Processing data...")
gui_widget.update_progress(50, 100, "Validating results...")
gui_widget.update_progress(100, 100, "Operation complete")
```

## Thread Safety

Inline mode works safely with:
- QThread workers
- Background processing
- Real-time data streams
- Concurrent operations

## Visual Features

- Animated loading indicator during progress
- Real-time percentage calculation
- Custom message display
- Smooth progress line updates
- Loading animation overlay

## Next steps

- Try [GUI Queue Mode](../13_gui_queue_mode/) for batch message processing
- Explore [GUI Non-Queue Mode](../15_gui_non_queue_mode/) for immediate messages
- Learn about [GUI Progress Tracking](../17_gui_progress_tracking/) for advanced progress features 