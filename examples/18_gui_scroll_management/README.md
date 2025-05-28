# GUI Scroll Management Example

This example demonstrates the GUI logger's intelligent scrolling behavior for handling large volumes of messages with optimal user experience.

## Requirements

- PySide6: `pip install PySide6`

## What it shows

- Intelligent auto-scroll behavior for new messages
- Scroll-to-bottom button when user scrolls up
- Scroll position preservation during user interaction
- High-volume message handling
- Smooth scrolling performance

## How to run

```bash
cd examples/18_gui_scroll_management
pip install PySide6  # if not already installed
python example.py
```

## Key features demonstrated

- **Auto-scroll**: Automatically scrolls to show newest messages
- **User Control**: Respects user scroll position when manually scrolled
- **Scroll Button**: Convenient button to return to bottom
- **Position Memory**: Preserves scroll position during operations
- **High Volume**: Handles rapid message streams smoothly

## Scroll Behavior

- **At Bottom**: New messages auto-scroll to remain visible
- **Scrolled Up**: Messages added without changing user's view
- **Scroll Button**: Appears when not at bottom, allows quick return
- **Smart Detection**: Automatically detects user scroll intent

## When to use

Perfect for:
- **High-volume Logging**: Applications with many log messages
- **Real-time Monitoring**: Live data streams and system monitoring
- **Debug Sessions**: Long debugging sessions with many messages
- **Server Logs**: Monitoring server applications with continuous output
- **Data Processing**: Operations that generate many status messages

## Interactive Features

The example demonstrates:
- **High-volume Test**: Sends 100 messages rapidly to test scroll behavior
- **Manual Scrolling**: User can scroll up/down to test position preservation
- **Auto-scroll Toggle**: Behavior changes based on user scroll position
- **Clear Function**: Resets scroll position when clearing messages

## Next steps

- Combine with [GUI Multithread](../16_gui_multithread/) for complex scenarios
- Try [GUI Non-Queue Mode](../15_gui_non_queue_mode/) for real-time streaming 