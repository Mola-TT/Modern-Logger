# GUI Progress Tracking Example

This example demonstrates advanced progress tracking features including inline updates, percentage tracking, and real-time completion status.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Advanced progress monitoring with inline updates
- Real-time percentage calculation and display
- Progress message updates with custom status
- Completion tracking and status updates
- Integration with GUI loading animations

## How to run

```bash
cd examples/17_gui_progress_tracking
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Inline Progress Updates**: Real-time progress on a single updating line
- **Percentage Tracking**: Automatic calculation and display of completion percentage
- **Custom Messages**: Each progress step can include custom status messages
- **Completion Handling**: Proper completion status and cleanup
- **Visual Feedback**: Loading animation with progress indicator

## Usage patterns

```python
from modern_logger import ModernLogger

logger = ModernLogger(gui=True)
gui_widget = logger.get_gui_widget()

# Start progress tracking
gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)

# Update progress in real-time
for i in range(1, 101):
    gui_widget.update_progress(i, 100, f"Processing item {i}")
    time.sleep(0.1)

# Complete the operation
gui_widget.set_loading_off("Processing completed successfully!")
```

## Progress API

- `update_progress(current, total, message)` - Update progress with custom message
- `set_loading_on(inline_update=True)` - Enable inline progress mode
- `set_loading_off(completion_message)` - Complete with status message

## When to use

Perfect for:
- **File Processing**: Track progress through large files
- **Data Import/Export**: Monitor database operations
- **Downloads/Uploads**: Show transfer progress
- **Batch Operations**: Process multiple items with status
- **Long Calculations**: Track computational progress

## Next steps

- Try [GUI Inline Mode](../14_gui_inline_mode/) for more inline examples
- Explore [GUI Scroll Management](../18_gui_scroll_management/) for large volumes 