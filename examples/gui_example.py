"""GUI example for Modern Logger"""

import sys
import time
import random
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QCheckBox, QScrollArea, 
                            QFrame, QSizePolicy, QSpacerItem)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor

from modern_logger import ModernLogger, MultiLogger, ConsoleLogger, FileLogger

# Custom GUIModernLogger that doesn't add the "Preparing progress tracking..." message
class CustomGUILogger(ModernLogger):
    def __init__(self, *args, **kwargs):
        # Force GUI mode
        kwargs['gui'] = True
        super().__init__(*args, **kwargs)
    
    def set_loading_on(self, queue_messages=False, passthrough_messages=False, inline_update=False):
        """Override to prevent adding the 'Preparing progress tracking...' message"""
        # Store the current inline_update value
        original_inline_update = inline_update
        
        # Temporarily set inline_update to False to prevent adding the message
        if inline_update:
            inline_update = False
        
        # Get the GUI widget and call its method directly
        gui_widget = self.get_gui_widget()
        if gui_widget:
            gui_widget.set_loading_on(queue_messages, passthrough_messages, inline_update)
        
        # Restore the inline progress mode if it was originally enabled
        if original_inline_update and gui_widget:
            gui_widget._inline_progress_update = True
            gui_widget._progress_current = 0
            gui_widget._progress_total = 100
            gui_widget._progress_message_id = None

class WorkerThread(QThread):
    """Example worker thread that simulates long-running operations"""
    finished = Signal()
    progress = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._stop_requested = False
        
    def run(self):
        for i in range(5):
            if self._stop_requested:
                break
            time.sleep(1)  # Simulate work
            if self._stop_requested:
                break
            self.progress.emit(f"Task progress: {i+1}/5")
            
            # Make sure the last progress message is processed before sending finished
            if i == 4:  # Last iteration
                # Give UI thread time to process the progress message
                QThread.msleep(10)  # Small delay to ensure progress is processed first
        
        self.finished.emit()
        
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class LoadingWorker(QThread):
    """Worker thread that simulates loading with queued messages"""
    finished = Signal()
    message = Signal(str)
    
    def __init__(self, duration=5):
        super().__init__()
        self.duration = duration
        self._stop_requested = False
        
    def run(self):
        start_time = time.time()
        message_count = 0
        
        while time.time() - start_time < self.duration and not self._stop_requested:
            # Emit a message every 0.5 seconds
            if time.time() - start_time > message_count * 0.5:
                self.message.emit(f"Loading message #{message_count + 1}")
                message_count += 1
            time.sleep(0.1)  # Check for stop requests frequently
            
        # Just emit the finished signal
        self.finished.emit()
        
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class StressTestWorker(QThread):
    """Worker thread that simulates random operations for stress testing"""
    finished = Signal(int)  # Include worker ID in signal
    progress = Signal(int, str)  # Worker ID and message
    
    def __init__(self, worker_id, iterations=10):
        super().__init__()
        self.worker_id = worker_id
        self.iterations = iterations
        self._stop_requested = False
        
    def run(self):
        for i in range(self.iterations):
            if self._stop_requested:
                break
            
            # Random sleep time between 0.1 and 1 second
            sleep_time = random.uniform(0.1, 1.0)
            time.sleep(sleep_time)
            
            if self._stop_requested:
                break
                
            # Emit progress with worker ID
            self.progress.emit(self.worker_id, f"Worker {self.worker_id}: Step {i+1}/{self.iterations}")
        
        # Signal completion with worker ID
        self.finished.emit(self.worker_id)
    
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class DirectMessageWorker(QThread):
    """Worker thread that sends messages directly to the console without loading indicator"""
    finished = Signal(int)  # Include worker ID in signal
    message = Signal(str)  # Message to display
    
    def __init__(self, worker_id, messages=10):
        super().__init__()
        self.worker_id = worker_id
        self.message_count = messages
        self._stop_requested = False
        
    def run(self):
        for i in range(self.message_count):
            if self._stop_requested:
                break
            
            # Random sleep time between 0.1 and 0.5 seconds
            sleep_time = random.uniform(0.1, 0.5)
            time.sleep(sleep_time)
            
            if self._stop_requested:
                break
                
            # Emit message directly
            self.message.emit(f"Direct message from Thread {self.worker_id}: #{i+1}/{self.message_count}")
        
        # Signal completion with worker ID
        self.finished.emit(self.worker_id)
    
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class InlineProgressWorker(QThread):
    """Worker thread that provides more granular progress updates"""
    finished = Signal()
    progress = Signal(int, int, str)  # current, total, message
    
    def __init__(self, steps=20):
        super().__init__()
        self._steps = steps
        self._stop_requested = False
        
    def run(self):
        # Wait a moment to ensure UI is updated before starting progress updates
        time.sleep(0.3)  # Increased delay
        
        # Send progress updates for each step
        for i in range(self._steps + 1):  # +1 to include 100%
            if self._stop_requested:
                break
                
            # Fixed message for all progress updates
            message = "Processing task" 
            self.progress.emit(i, self._steps, message)
            
            # Calculate a realistic delay that varies slightly
            delay = 0.2 + random.uniform(-0.1, 0.1)  # 0.1-0.3 second delay
            time.sleep(delay)
            
        self.finished.emit()
        
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Logger Example")
        self.resize(1200, 800)  # Increase window size for better content display
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
        main_layout.setSpacing(0)  # Remove spacing
        
        # --- LEFT SIDE: MODERN LOGGER ---
        logger_widget = QWidget()
        logger_layout = QVBoxLayout(logger_widget)
        logger_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for cleaner look
        
        # Add a label for the logger
        logger_label = QLabel("Log Output")
        logger_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #333; padding: 5px;")
        logger_layout.addWidget(logger_label)
        
        # Create modern logger with GUI
        self.logger = CustomGUILogger(
            console=True,  # Also log to console
            file="logs/gui_example.log"  # Also log to file
        )
        
        # Get the GUI widget
        self.gui_widget = self.logger.get_gui_widget()
        
        # Add the GUI widget to our window
        logger_layout.addWidget(self.gui_widget)
            
        # --- RIGHT SIDE: CONTROLS ---
        # Create a scroll area for the controls in case they're too tall
        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        controls_scroll.setFixedWidth(550)  # Set exact width for controls area
        
        # Container widget for all controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(10, 0, 10, 10)  # Remove top margin
        controls_layout.setSpacing(0)  # Remove spacing completely
        
        # Create a container for the title and first card with no spacing
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        # Add a title for the controls section
        controls_title = QLabel("Test Controls")
        controls_title.setStyleSheet("font-weight: bold; font-size: 14pt; color: #333; margin: 0; padding-bottom: 0;")
        title_layout.addWidget(controls_title)
        
        # Create first card directly in the title container
        simple_msg_card = self._create_test_card_widget(
            "Simple Message Test", 
            "Test receiving a single signal to display message on the TextEdit widget",
            self._create_simple_message_controls())
        title_layout.addWidget(simple_msg_card)
        
        # Add the title container to the main layout
        controls_layout.addWidget(title_container)
        
        # Add remaining cards with small spacing
        controls_layout.addSpacing(5)
        
        self._create_test_card(controls_layout, 
                              "Loading Test", 
                              "Test loading state with message queuing (runs for 5 seconds). New messages are queued during loading and displayed in sequence when loading completes. Try clicking 'Send Single Message' during loading to see messages being queued.",
                              self._create_loading_controls())
        
        self._create_test_card(controls_layout, 
                              "Loading Test with Progress Updates", 
                              "Test loading state with real-time progress updates. Messages appear immediately (passthrough mode) rather than being queued, showing progress as it happens. This simulates operations that need to report progress while processing, such as file uploads, data imports, or long calculations where you need to show interim results.",
                              self._create_progress_controls())
        
        self._create_test_card(controls_layout, 
                              "Concurrent Loading Test (Queued Mode)", 
                              "Test multiple worker threads sending messages simultaneously. This simulates concurrent operations where results need to be processed in batch after completion, such as multiple API requests or database queries.",
                              self._create_stress_controls())
        
        self._create_test_card(controls_layout, 
                              "Concurrent Message Test (No Animation)", 
                              "Test multiple threads sending messages directly without loading indicators. Each message appears immediately when received with no animation. This simulates scenarios where multiple processes need to log information simultaneously with immediate visibility, such as system monitoring, parallel processing tasks, or diagnostic logging.",
                              self._create_direct_msg_controls())
        
        # Set up the controls scroll area
        controls_scroll.setWidget(controls_widget)
        
        # Add widgets to main layout
        main_layout.addWidget(logger_widget, 1)  # Logger takes remaining space
        main_layout.addWidget(controls_scroll, 0)  # Controls have fixed width
        
        # Set up the main window
        self.setCentralWidget(main_widget)
        
        # Initialize worker threads
        self.worker = None
        self.loading_worker = None
        self.stress_workers = []
        self.direct_msg_workers = []
        self._active_workers = 0
        self._active_direct_msg_workers = 0
        self._stop_requested = False
        self._direct_msg_stop_requested = False
        self._stress_stop_requested = False
        self._work_stop_requested = False
        self._loading_stop_requested = False
        
        # Log initial message
        self.logger.info("GUI Example started!")
    
    def _create_test_card_widget(self, title, description, controls_widget):
        """Create a card widget without adding it to a layout"""
        # Create card container
        card = QFrame()
        card.setFrameShape(QFrame.NoFrame)  # Remove frame
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 4px;
                border: none;  /* Remove border */
                margin-top: 0;  /* Remove top margin */
            }
        """)
        
        # Create card layout
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        card_layout.setSpacing(5)
        
        # Add title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 11pt;")
        card_layout.addWidget(title_label)
        
        # Add description
        if description:
            desc_label = QLabel(description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #7f8c8d; font-size: 10pt;")
            card_layout.addWidget(desc_label)
        
        # Add controls
        card_layout.addWidget(controls_widget)
        
        return card
        
    def _create_test_card(self, parent_layout, title, description, controls_widget):
        """Create a card-style container for a test section and add it to the parent layout"""
        card = self._create_test_card_widget(title, description, controls_widget)
        parent_layout.addWidget(card)
    
    def _create_simple_message_controls(self):
        """Create controls for simple message test"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)
        
        self.add_message_btn = QPushButton("Send Single Message")
        self.add_message_btn.clicked.connect(self.log_test_messages)
        
        # Add new button for sending 50 messages
        self.add_50_messages_btn = QPushButton("Send 50 Messages")
        self.add_50_messages_btn.clicked.connect(self.add_50_messages)
        
        # Add new Clear Messages button
        self.clear_messages_btn = QPushButton("Clear Messages")
        self.clear_messages_btn.clicked.connect(self.clear_messages)
        
        layout.addWidget(self.add_message_btn)
        layout.addWidget(self.add_50_messages_btn)
        layout.addWidget(self.clear_messages_btn)
        
        return widget
    
    def _create_loading_controls(self):
        """Create controls for loading test"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)
        
        self.start_loading_btn = QPushButton("Start Loading Test")
        self.start_loading_btn.clicked.connect(self.start_loading)
        self.stop_loading_btn = QPushButton("Stop Loading Test")
        self.stop_loading_btn.clicked.connect(self.stop_loading)
        self.stop_loading_btn.setEnabled(False)
        
        layout.addWidget(self.start_loading_btn)
        layout.addWidget(self.stop_loading_btn)
        
        return widget
    
    def _create_progress_controls(self):
        """Create controls for progress test"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)
        
        self.start_progress_btn = QPushButton("Start Progress Loading Test")
        self.start_progress_btn.clicked.connect(self.simulate_work)
        self.stop_progress_btn = QPushButton("Stop Progress Loading Test")
        self.stop_progress_btn.clicked.connect(self.stop_work)
        self.stop_progress_btn.setEnabled(False)
        
        # Add inline progress option
        self.inline_progress_check = QCheckBox("Use Inline Progress")
        self.inline_progress_check.setChecked(False)
        
        layout.addWidget(self.start_progress_btn)
        layout.addWidget(self.stop_progress_btn)
        layout.addWidget(self.inline_progress_check)
        
        return widget
    
    def _create_stress_controls(self):
        """Create controls for stress test"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)
        
        self.start_stress_btn = QPushButton("Start Concurrent Test (Queued)")
        self.start_stress_btn.clicked.connect(self.run_stress_test)
        self.stop_stress_btn = QPushButton("Stop Concurrent Test")
        self.stop_stress_btn.clicked.connect(self.stop_stress_test)
        self.stop_stress_btn.setEnabled(False)
        
        layout.addWidget(self.start_stress_btn)
        layout.addWidget(self.stop_stress_btn)
        
        return widget
    
    def _create_direct_msg_controls(self):
        """Create controls for direct message test"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 5, 0, 0)
        
        self.start_direct_msg_btn = QPushButton("Start Concurrent Test (No Animation)")
        self.start_direct_msg_btn.clicked.connect(self.run_direct_msg_test)
        self.stop_direct_msg_btn = QPushButton("Stop Concurrent Test")
        self.stop_direct_msg_btn.clicked.connect(self.stop_direct_msg_test)
        self.stop_direct_msg_btn.setEnabled(False)
        
        layout.addWidget(self.start_direct_msg_btn)
        layout.addWidget(self.stop_direct_msg_btn)
        
        return widget
    
    def log_test_messages(self):
        """Log test messages at different levels"""
        self.logger.debug("This is a debug message")
        self.logger.info("This is an info message")
        self.logger.warning("This is a warning message")
        self.logger.error("This is an error message")
        self.logger.critical("This is a critical message")
    
    def add_50_messages(self):
        """Add 50 test messages"""
        self.logger.info("Starting to send 50 messages...")
        for i in range(50):
            level = random.choice(['debug', 'info', 'warning', 'error', 'critical'])
            getattr(self.logger, level)(f"Test message #{i+1}: This is a {level} message")
        self.logger.info("Finished sending 50 messages")
    
    def start_loading(self):
        """Start the loading test with message queuing"""
        # First log the start message with information icon
        self.logger.info("Starting loading test...")
        
        # Set loading state AFTER the message is displayed
        self.gui_widget.set_loading_on(queue_messages=True)
        
        # Reset flags
        self._loading_stop_requested = False
        self._loading_finished_called = False
        
        # Create and start the loading worker
        self.loading_worker = LoadingWorker()
        self.loading_worker.message.connect(lambda msg: self.logger.info(msg))
        self.loading_worker.finished.connect(self.loading_finished)
        self.loading_worker.start()
        
        # Update button states
        self.start_loading_btn.setEnabled(False)
        self.stop_loading_btn.setEnabled(True)
    
    def stop_loading(self):
        """Stop the loading test"""
        if self.loading_worker and self.loading_worker.isRunning():
            # Set flag to prevent completion message
            self._loading_stop_requested = True
            
            # Signal worker to stop (non-blocking)
            self.loading_worker.stop()
            
            # Use a timer to check for completion without blocking
            self._loading_cleanup_timer = QTimer()
            self._loading_cleanup_timer.setSingleShot(True)
            self._loading_cleanup_timer.timeout.connect(self._cleanup_loading_worker)
            self._loading_cleanup_timer.start(100)
            
            # Immediately turn off loading and update UI
            self.gui_widget.set_loading_off()
            self.logger.warning("Loading test stopped by user")
            
            # Update button states to show stopping
            self.start_loading_btn.setEnabled(False)
            self.stop_loading_btn.setText("Stopping...")
            self.stop_loading_btn.setEnabled(False)
        else:
            # No worker running, just reset buttons
            self.start_loading_btn.setEnabled(True)
            self.stop_loading_btn.setEnabled(False)
    
    def _cleanup_loading_worker(self):
        """Clean up loading worker after it has stopped"""
        if self.loading_worker and self.loading_worker.isRunning():
            # Still running, check again
            self._loading_cleanup_timer.start(50)
        else:
            # Worker has stopped, reset button states
            self.start_loading_btn.setEnabled(True)
            self.stop_loading_btn.setText("Stop Loading Test")
            self.stop_loading_btn.setEnabled(False)
    
    def loading_finished(self):
        """Handle loading test completion"""
        # Prevent multiple calls
        if not hasattr(self, '_loading_finished_called') or not self._loading_finished_called:
            self._loading_finished_called = True
            
            if not self._loading_stop_requested:
                # Log the completion message to the console first
                completion_message = "Loading test completed successfully"
                self.logger.info(completion_message)
                
                # Then turn off the loading indicator without a completion message
                # since we've already logged it
                self.gui_widget.set_loading_off()
                
                # Update button states
                self.start_loading_btn.setEnabled(True)
                self.stop_loading_btn.setEnabled(False)
    
    def simulate_work(self):
        """Start a simulated work process with progress updates"""
        # Reset the stop flag at the start of a new operation
        self._work_stop_requested = False
        
        # Update button states
        self.start_progress_btn.setEnabled(False)
        self.stop_progress_btn.setEnabled(True)
        
        # Check if inline progress is enabled
        use_inline = self.inline_progress_check.isChecked()
        
        # First add message about which test is starting
        message_type = "Inline" if use_inline else "Standard"
        self.logger.info(f"Starting {message_type} Progress Test")
        
        # Enable loading with appropriate mode
        if use_inline:
            # Add preparing message through the logger first
            self.logger.info("Preparing progress tracking...")
            
            # Turn on inline progress mode AFTER the preparing message is displayed
            self.gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
            
            # Create and configure inline worker - wait longer to start
            self.worker = InlineProgressWorker(steps=20)
            self.worker.progress.connect(self.on_inline_progress)
            self.worker.finished.connect(self.on_work_finished)
            self.worker.start()
        else:
            # Use standard passthrough mode (original implementation)
            self.gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)
            
            # Create and configure standard worker
            self.worker = WorkerThread()
            self.worker.progress.connect(self.on_progress)
            self.worker.finished.connect(self.on_work_finished)
            self.worker.start()
    
    def stop_work(self):
        """Stop the work simulation"""
        if self.worker and self.worker.isRunning():
            # Set the flag to indicate a manual stop was requested
            self._work_stop_requested = True
            
            # Signal worker to stop (non-blocking)
            self.worker.stop()
            
            # Use a timer to check for completion without blocking
            self._work_cleanup_timer = QTimer()
            self._work_cleanup_timer.setSingleShot(True)
            self._work_cleanup_timer.timeout.connect(self._cleanup_work_worker)
            self._work_cleanup_timer.start(100)
            
            # Immediately stop the loading indicator and update UI
            self.gui_widget.set_loading_off()
            self.logger.warning("Progress test stopped by user")
            
            # Update button states to show stopping
            self.start_progress_btn.setEnabled(False)
            self.stop_progress_btn.setText("Stopping...")
            self.stop_progress_btn.setEnabled(False)
        else:
            # No worker running, just reset buttons
            self.start_progress_btn.setEnabled(True)
            self.stop_progress_btn.setEnabled(False)
    
    def _cleanup_work_worker(self):
        """Clean up work worker after it has stopped"""
        if self.worker and self.worker.isRunning():
            # Still running, check again
            self._work_cleanup_timer.start(50)
        else:
            # Worker has stopped, reset button states
            self.start_progress_btn.setEnabled(True)
            self.stop_progress_btn.setText("Stop Progress Loading Test")
            self.stop_progress_btn.setEnabled(False)
    
    def on_progress(self, message):
        """Handle standard progress updates"""
        # No need to add the icon - the logger.info will add it automatically
        self.logger.info(message)
    
    def on_inline_progress(self, current, total, message):
        """Handle progress updates from the inline progress worker"""
        # The update_progress method doesn't automatically add icons, so we need to add it here
        # but only if it doesn't already have one
        if message and not message.startswith("ℹ️"):
            message = f"ℹ️ {message}"
        self.gui_widget.update_progress(current, total, message)
    
    def on_work_finished(self):
        """Handle completion of the progress test"""
        # Only proceed if not already stopped manually
        if not self._work_stop_requested:
            # Use a short delay to ensure any pending progress messages are processed first
            QTimer.singleShot(50, self._complete_work_operation)
            
            # Set a flag to prevent multiple completion calls
            self._work_stop_requested = True
    
    def _complete_work_operation(self):
        """Complete the work operation after ensuring all progress messages are processed"""
        # Turn off loading and add completion message
        self.gui_widget.set_loading_off()
        self.logger.info("Progress test completed successfully")
        
        # Reset button states
        self.start_progress_btn.setEnabled(True)
        self.stop_progress_btn.setEnabled(False)
    
    def run_stress_test(self):
        """Start a stress test with multiple worker threads"""
        self.logger.info("Starting Concurrent Loading Test with 4 threads (Queued Mode)")
        
        # Update button states
        self.start_stress_btn.setEnabled(False)
        self.stop_stress_btn.setEnabled(True)
        
        # Reset worker tracking
        self.stress_workers = []
        self._active_workers = 0
        self._stress_stop_requested = False
        
        # Show loading indicator with message queuing
        self.gui_widget.set_loading_on(queue_messages=True)
        
        # Start 4 worker threads
        for i in range(4):
            worker = StressTestWorker(i, iterations=10)
            worker.progress.connect(self.on_stress_progress)
            worker.finished.connect(self.on_stress_worker_finished)
            self.stress_workers.append(worker)
            worker.start()
            self._active_workers += 1
    
    def stop_stress_test(self):
        """Stop the stress test"""
        self._stress_stop_requested = True
        
        # Signal all workers to stop (non-blocking)
        for worker in self.stress_workers:
            if worker.isRunning():
                worker.stop()
        
        # Use a timer to check for thread completion without blocking the GUI
        self._cleanup_timer = QTimer()
        self._cleanup_timer.setSingleShot(True)
        self._cleanup_timer.timeout.connect(self._cleanup_stress_workers)
        self._cleanup_timer.start(100)  # Check after 100ms
        
        # Immediately update UI to show stopping state
        self.start_stress_btn.setEnabled(False)  # Keep disabled until cleanup
        self.stop_stress_btn.setText("Stopping...")
        self.stop_stress_btn.setEnabled(False)
        
        # Turn off loading indicator immediately (this will process queued messages first)
        self.gui_widget.set_loading_off(completion_message="⚠️ Concurrent Loading Test (Queued Mode) stopped by user")
    
    def _cleanup_stress_workers(self):
        """Clean up stress test workers after they've had time to stop"""
        # Check if any workers are still running
        still_running = []
        for worker in self.stress_workers:
            if worker.isRunning():
                still_running.append(worker)
        
        if still_running:
            # If some workers are still running, wait a bit more
            self._cleanup_timer.start(50)  # Check again in 50ms
        else:
            # All workers have stopped, complete the cleanup
            self.stress_workers.clear()
            self._active_workers = 0
            
            # Reset button states
            self.start_stress_btn.setEnabled(True)
            self.stop_stress_btn.setText("Stop Concurrent Test")
            self.stop_stress_btn.setEnabled(False)
    
    def on_stress_progress(self, worker_id, message):
        """Handle progress updates from stress test workers"""
        self.logger.info(f"Thread {worker_id}: {message}")
    
    def on_stress_worker_finished(self, worker_id):
        """Handle completion of a stress test worker"""
        if not self._stress_stop_requested:
            self.logger.info(f"Thread {worker_id} completed")
            
            # Decrement active worker count
            self._active_workers -= 1
            
            # If all workers are done, finish the stress test
            if self._active_workers <= 0:
                self.gui_widget.set_loading_off()
                self.logger.info("Concurrent Loading Test (Queued Mode) completed successfully")
                self.start_stress_btn.setEnabled(True)
                self.stop_stress_btn.setEnabled(False)
    
    def run_direct_msg_test(self):
        """Start a test with multiple threads sending direct messages without loading indicators"""
        self.logger.info("Starting Concurrent Message Test (No Animation)")
        
        # Update button states
        self.start_direct_msg_btn.setEnabled(False)
        self.stop_direct_msg_btn.setEnabled(True)
        self._direct_msg_stop_requested = False
        
        # NOTE: We're intentionally NOT activating the loading indicator here
        # to demonstrate direct message handling without loading animation
        
        # Start 4 worker threads
        self.direct_msg_workers = []
        self._active_direct_msg_workers = 4
        
        for i in range(4):
            # Create worker with different message counts
            worker = DirectMessageWorker(i+1, messages=8+i*3)  # 8, 11, 14, 17 messages
            worker.message.connect(self.on_direct_message)
            worker.finished.connect(self.on_direct_msg_worker_finished)
            self.direct_msg_workers.append(worker)
            worker.start()
    
    def stop_direct_msg_test(self):
        """Stop all direct message worker threads"""
        self._direct_msg_stop_requested = True
        
        # Signal all workers to stop (non-blocking)
        for worker in self.direct_msg_workers:
            worker.stop()
        
        # Use a timer to check for thread completion without blocking the GUI
        self._direct_cleanup_timer = QTimer()
        self._direct_cleanup_timer.setSingleShot(True)
        self._direct_cleanup_timer.timeout.connect(self._cleanup_direct_msg_workers)
        self._direct_cleanup_timer.start(100)  # Check after 100ms
        
        # Immediately update UI to show stopping state
        self.start_direct_msg_btn.setEnabled(False)  # Keep disabled until cleanup
        self.stop_direct_msg_btn.setText("Stopping...")
        self.stop_direct_msg_btn.setEnabled(False)
        
        self.logger.info("Concurrent Message Test (No Animation) stopped by user")
    
    def _cleanup_direct_msg_workers(self):
        """Clean up direct message workers after they've had time to stop"""
        # Check if any workers are still running
        still_running = []
        for worker in self.direct_msg_workers:
            if worker.isRunning():
                still_running.append(worker)
        
        if still_running:
            # If some workers are still running, wait a bit more
            self._direct_cleanup_timer.start(50)  # Check again in 50ms
        else:
            # All workers have stopped, complete the cleanup
            self.direct_msg_workers.clear()
            
            # Reset button states
            self.start_direct_msg_btn.setEnabled(True)
            self.stop_direct_msg_btn.setText("Stop Concurrent Test")
            self.stop_direct_msg_btn.setEnabled(False)
    
    def on_direct_message(self, message):
        """Handle direct messages from worker threads"""
        self.logger.info(message)
    
    def on_direct_msg_worker_finished(self, worker_id):
        """Handle completion of a direct message worker"""
        if not self._direct_msg_stop_requested:
            self.logger.info(f"Direct message thread {worker_id} completed")
            
            # Decrement active worker count
            self._active_direct_msg_workers -= 1
            
            # If all workers are done, finish the test
            if self._active_direct_msg_workers <= 0:
                self.logger.info("Concurrent Message Test (No Animation) completed successfully")
                self.start_direct_msg_btn.setEnabled(True)
                self.stop_direct_msg_btn.setEnabled(False)
    
    def clear_messages(self):
        """Clear all messages from the console"""
        # Clear the GUI widget directly
        self.gui_widget.clear()
        # Log that messages were cleared
        self.logger.info("Log cleared")

def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 