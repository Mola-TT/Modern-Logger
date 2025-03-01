# Modern Logger

A PySide6-based modern logger widget that displays timestamped messages and supports non-blocking loading indicators.

## Features

- Real-time message display with timestamps
- Animated loading indicators
- Auto-scrolling with user override
- Message batching for performance
- Threaded operation support

## Usage

### Basic Message Display

Display simple messages with automatic timestamps:

```python
# Create the logger widget
console = ModernLogger()

# Add a message
console.append_message("Operation started")
```

### Loading Indicators

Show a loading animation while performing background operations:

```python
# Start a loading operation
console.set_loading_on()

# Perform some work in a background thread
worker_thread = WorkerThread()
worker_thread.start()

# When done, turn off loading and show completion message
def on_worker_finished():
    console.set_loading_off(completion_message="Operation completed successfully")

worker_thread.finished.connect(on_worker_finished)
```

### Progress Updates

Display real-time progress updates during loading operations:

```python
# Enable loading with message passthrough (don't queue messages)
console.set_loading_on(queue_messages=False, passthrough_messages=True)

# Connect progress signals from worker
def on_progress(message):
    console.append_message(message)

worker.progress.connect(on_progress)
```

### Inline Progress Updates

Show a dynamic progress bar for operations with percentage-based progress:

```python
# Enable inline progress mode
console.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)

# Update progress from worker thread
def on_progress(current, total, message):
    console.update_progress(current, total, message)

worker.progress.connect(on_progress)
```

### Multiple Concurrent Operations

Handle messages from multiple threads with queuing:

```python
# Start loading with message queuing
console.set_loading_on(queue_messages=True)

# Start multiple worker threads
workers = [WorkerThread() for _ in range(4)]
for worker in workers:
    worker.progress.connect(lambda msg: console.append_message(msg))
    worker.start()

# Complete when all workers are done
def check_completion():
    if all(not w.isRunning() for w in workers):
        console.set_loading_off(completion_message="All operations completed")
```

### Direct Messages without Loading Animation

Send messages directly to the console without loading indicators:

```python
# Without calling set_loading_on(), messages appear immediately
for worker in workers:
    worker.message.connect(lambda msg: console.append_message(msg))
    worker.start()
```

### Clearing Messages

Clear the console:

```python
console.clear()

