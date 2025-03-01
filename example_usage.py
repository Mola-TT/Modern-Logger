import sys
import time
import random
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QFrame, QSplitter, QScrollArea, QCheckBox
from PySide6.QtCore import QThread, Signal, QTimer, Qt

from modern_logger import ModernLogger

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

# Add a new worker thread for the simple loading operation
class LoadingWorker(QThread):
    """Simple worker thread for loading simulation"""
    finished = Signal()
    
    def __init__(self, duration=3):
        super().__init__()
        self.duration = duration
        self._stop_requested = False
        
    def run(self):
        start_time = time.time()
        while time.time() - start_time < self.duration and not self._stop_requested:
            time.sleep(0.1)  # Check for stop requests more frequently
        self.finished.emit()
        
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

# Add a new worker thread class for stress testing
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

# Add a direct messaging worker that doesn't use loading indicators
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

# Add a worker thread with more granular progress updates
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
        
        # Create main splitter to divide console and controls
        main_splitter = QSplitter(Qt.Horizontal)
        
        # --- LEFT SIDE: MODERN LOGGER ---
        logger_widget = QWidget()
        logger_layout = QVBoxLayout(logger_widget)
        logger_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for cleaner look
        
        # Add a label for the logger
        logger_label = QLabel("Log Output")
        logger_label.setStyleSheet("font-weight: bold; font-size: 12pt; color: #333; padding: 5px;")
        logger_layout.addWidget(logger_label)
        
        # Create modern logger with larger size
        self.console = ModernLogger()
        self.console.setMinimumWidth(500)  # Ensure reasonable width
        
        # Set a nicer font for the logger
        font = self.console.font()
        font.setPointSize(10)
        self.console.setFont(font)
        
        logger_layout.addWidget(self.console)
        main_splitter.addWidget(logger_widget)
        
        # --- RIGHT SIDE: CONTROLS ---
        # Create a scroll area for the controls in case they're too tall
        controls_scroll = QScrollArea()
        controls_scroll.setWidgetResizable(True)
        controls_scroll.setMinimumWidth(500)  # Increase minimum width for controls area
        
        # Container widget for all controls
        controls_widget = QWidget()
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        
        # Add a title for the controls section
        controls_title = QLabel("Test Controls")
        controls_title.setStyleSheet("font-weight: bold; font-size: 12pt; color: #333;")
        controls_layout.addWidget(controls_title)
        
        # 1. Simple Message Test
        self._add_group_label(controls_layout, "Simple Message Test", 
                             "Test receiving a single signal to display message on the TextEdit widget")
        
        message_buttons_layout = QHBoxLayout()
        self.add_message_btn = QPushButton("Send Single Message")
        self.add_message_btn.clicked.connect(self.add_message)
        
        # Add new button for sending 50 messages
        self.add_50_messages_btn = QPushButton("Send 50 Messages")
        self.add_50_messages_btn.clicked.connect(self.add_50_messages)
        
        # Add new Clear Messages button
        self.clear_messages_btn = QPushButton("Clear Messages")
        self.clear_messages_btn.clicked.connect(self.clear_messages)
        
        message_buttons_layout.addWidget(self.add_message_btn)
        message_buttons_layout.addWidget(self.add_50_messages_btn)
        message_buttons_layout.addWidget(self.clear_messages_btn)
        controls_layout.addLayout(message_buttons_layout)
        
        # Add separator between control groups
        controls_layout.addWidget(self._create_separator())
        
        # 2. Loading Test (renamed from "Loading Indicator Test")
        self._add_group_label(controls_layout, "Loading Test", 
                             "Test loading state with message queuing (runs for 5 seconds). New messages are queued during loading and displayed in sequence when loading completes. Try clicking 'Send Single Message' during loading to see messages being queued.")
        
        loading_layout = QHBoxLayout()
        self.start_loading_btn = QPushButton("Start Loading Test")  # Updated label
        self.start_loading_btn.clicked.connect(self.start_loading)
        self.stop_loading_btn = QPushButton("Stop Loading Test")  # Updated label
        self.stop_loading_btn.clicked.connect(self.stop_loading)
        self.stop_loading_btn.setEnabled(False)
        loading_layout.addWidget(self.start_loading_btn)
        loading_layout.addWidget(self.stop_loading_btn)
        controls_layout.addLayout(loading_layout)
        
        # Add separator
        controls_layout.addWidget(self._create_separator())
        
        # 3. Loading Test with Progress Updates (renamed from "Process Loading Test")
        self._add_group_label(controls_layout, "Loading Test with Progress Updates", 
                             "Test loading state with real-time progress updates. "
                             "Messages appear immediately (passthrough mode) rather than being queued, "
                             "showing progress as it happens. This simulates operations that need "
                             "to report progress while processing, such as file uploads, data imports, "
                             "or long calculations where you need to show interim results.")
        
        work_layout = QHBoxLayout()
        self.simulate_work_btn = QPushButton("Start Progress Loading Test")  # Updated button label
        self.simulate_work_btn.clicked.connect(self.simulate_work)
        self.stop_work_btn = QPushButton("Stop Progress Loading Test")  # Updated button label
        self.stop_work_btn.clicked.connect(self.stop_work)
        self.stop_work_btn.setEnabled(False)
        
        # Add new inline progress option
        self.inline_progress_check = QCheckBox("Use Inline Progress")
        self.inline_progress_check.setChecked(False)
        
        work_layout.addWidget(self.simulate_work_btn)
        work_layout.addWidget(self.stop_work_btn)
        work_layout.addWidget(self.inline_progress_check)
        controls_layout.addLayout(work_layout)
        
        # Add separator
        controls_layout.addWidget(self._create_separator())
        
        # 4. Concurrent Loading Test (Queued Mode) (renamed from "Multi-Thread Stress Test")
        self._add_group_label(controls_layout, "Concurrent Loading Test (Queued Mode)", 
                             "Test multiple threads sending messages during loading with message queuing. "
                             "Messages from all threads are queued and displayed in order when loading completes. "
                             "This simulates concurrent operations where results need to be processed in "
                             "batch after completion, such as multiple API requests or database queries.")
        
        stress_layout = QHBoxLayout()
        self.stress_test_btn = QPushButton("Start Concurrent Test (Queued)")
        self.stress_test_btn.clicked.connect(self.run_stress_test)
        self.stop_stress_test_btn = QPushButton("Stop Concurrent Test")
        self.stop_stress_test_btn.clicked.connect(self.stop_stress_test)
        self.stop_stress_test_btn.setEnabled(False)
        stress_layout.addWidget(self.stress_test_btn)
        stress_layout.addWidget(self.stop_stress_test_btn)
        controls_layout.addLayout(stress_layout)
        
        # Add separator
        controls_layout.addWidget(self._create_separator())
        
        # 5. Concurrent Loading Test (Passthrough Mode) (renamed from "Direct Message Test")
        self._add_group_label(controls_layout, "Concurrent Message Test (No Animation)", 
                             "Test multiple threads sending messages directly without loading indicators. "
                             "Each message appears immediately when received with no animation. "
                             "This simulates scenarios where multiple processes need to log information "
                             "simultaneously with immediate visibility, such as system monitoring, "
                             "parallel processing tasks, or diagnostic logging.")
        
        direct_msg_layout = QHBoxLayout()
        self.direct_msg_test_btn = QPushButton("Start Concurrent Test (No Animation)")
        self.direct_msg_test_btn.clicked.connect(self.run_direct_msg_test)
        self.stop_direct_msg_btn = QPushButton("Stop Concurrent Test")
        self.stop_direct_msg_btn.clicked.connect(self.stop_direct_msg_test)
        self.stop_direct_msg_btn.setEnabled(False)
        direct_msg_layout.addWidget(self.direct_msg_test_btn)
        direct_msg_layout.addWidget(self.stop_direct_msg_btn)
        controls_layout.addLayout(direct_msg_layout)
        
        # Add spacer at the bottom to push controls to the top
        controls_layout.addStretch(1)
        
        # Set the controls widget to the scroll area
        controls_scroll.setWidget(controls_widget)
        main_splitter.addWidget(controls_scroll)
        
        # Set the initial split proportion (55% console, 45% controls)
        main_splitter.setSizes([660, 540])
        
        # Set the splitter as the central widget
        self.setCentralWidget(main_splitter)
        
        # Initialize worker threads and state flags
        self.worker = None
        self.loading_worker = None
        
        # Add flags to track operation states
        self._loading_stop_requested = False
        self._work_stop_requested = False
        
        # For stress testing
        self._stress_workers = []
        self._active_workers = 0
        self._stress_stop_requested = False
        
        # For direct message testing
        self._direct_msg_workers = []
        self._active_direct_msg_workers = 0
        self._direct_msg_stop_requested = False
        
        # Initial message
        self.console.append_message("Application started")
        
    def _add_group_label(self, layout, title, description):
        """Helper method to add a labeled section with title and description"""
        # Add a bit of spacing before each group (except the first)
        if layout.count() > 1:
            layout.addSpacing(10)
            
        # Create title label with bold text
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        
        # Create description label with smaller text
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 9pt; color: #666666;")
        desc_label.setWordWrap(True)
        
        # Add to layout
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
    def _create_separator(self):
        """Create a horizontal separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        return separator
        
    def add_message(self):
        self.console.append_message("User sent a single message")
    
    def add_50_messages(self):
        """Add 50 numbered messages to the console"""
        try:
            self.console.append_message("Starting to add 50 messages...")
            
            # Add messages in small batches
            for i in range(1, 51):
                self.console.append_message(f"Message #{i} of 50")
                
                # We don't need these processEvents calls if the logger handles them
                # Small delay every 10 messages to prevent UI from becoming unresponsive
                if i % 10 == 0 and not self.console.handles_event_processing:
                    QApplication.processEvents()
                    
            self.console.append_message("Finished adding 50 messages")
        except Exception as e:
            import traceback
            print(f"Error adding messages: {traceback.format_exc()}")
        
    def start_loading(self):
        # Reset the stop flag at the start of a new operation
        self._loading_stop_requested = False
        
        self.console.append_message("Starting loading test (will run for 5 seconds)")
        
        # Update button states
        self.start_loading_btn.setEnabled(False)
        self.stop_loading_btn.setEnabled(True)
        
        # Start loading indicator AFTER appending the message
        self.console.set_loading_on()
        
        # Create a worker thread for the loading operation - now with 5 second duration
        self.loading_worker = LoadingWorker(duration=5)
        self.loading_worker.finished.connect(self.loading_finished)
        self.loading_worker.start()
    
    def stop_loading(self):
        """Stop the loading operation"""
        if self.loading_worker and self.loading_worker.isRunning():
            # Set the flag to indicate a manual stop was requested
            self._loading_stop_requested = True
            
            # First stop the worker thread
            self.loading_worker.stop()
            
            # Then stop the loading indicator with a custom message
            # This will process any queued messages first
            self.console.set_loading_off(completion_message="Loading operation stopped by user")
            
            # Wait for thread to finish
            self.loading_worker.wait(1000)  # Wait up to 1 second for thread to finish
            
            # Update button states
            self.start_loading_btn.setEnabled(True)
            self.stop_loading_btn.setEnabled(False)
    
    def loading_finished(self):
        # Only proceed if not already stopped manually
        if not self._loading_stop_requested:
            # Make sure we include a completion message
            self.console.set_loading_off(completion_message="Loading operation completed successfully")
            self.start_loading_btn.setEnabled(True)
            self.stop_loading_btn.setEnabled(False)
        
    def simulate_work(self):
        """Start a simulated work process with progress updates"""
        # Reset the stop flag at the start of a new operation
        self._work_stop_requested = False
        
        # Update button states
        self.simulate_work_btn.setEnabled(False)
        self.stop_work_btn.setEnabled(True)
        
        # Check if inline progress is enabled
        use_inline = self.inline_progress_check.isChecked()
        
        # First add message about which test is starting
        message_type = "Inline" if use_inline else "Standard"
        self.console.append_message(f"Starting {message_type} Progress Test")
        
        # Enable loading with appropriate mode
        if use_inline:
            # Turn on inline progress mode BEFORE starting the worker
            self.console.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
            
            # Process events to ensure loading state is fully updated
            QApplication.processEvents()
            
            # Create and configure inline worker - wait longer to start
            self.worker = InlineProgressWorker(steps=20)
            self.worker.progress.connect(self.on_inline_progress)
            self.worker.finished.connect(self.on_work_finished)
            self.worker.start()
        else:
            # Use standard passthrough mode (original implementation)
            self.console.set_loading_on(queue_messages=False, passthrough_messages=True)
            
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
            
            # First stop the worker thread
            self.worker.stop()
            
            # Then stop the loading indicator with a custom message
            # This will process queued messages first
            self.console.set_loading_off(completion_message="Work stopped by user")
            
            # Wait for thread to finish
            self.worker.wait(1000)  # Wait up to 1 second for thread to finish
            
            # Update button states
            self.simulate_work_btn.setEnabled(True)
            self.stop_work_btn.setEnabled(False)
        
    def on_progress(self, message):
        """Handle standard progress updates"""
        self.console.append_message(message)
    
    def on_inline_progress(self, current, total, message):
        """Handle inline progress updates"""
        self.console.update_progress(current, total, message)
        
    def on_work_finished(self):
        # Only proceed if not already stopped manually
        if not self._work_stop_requested:
            # Use a short delay to ensure any pending progress messages are processed first
            # This makes sure the last progress message appears before the completion message
            QTimer.singleShot(50, lambda: self._complete_work_operation())
        
    def _complete_work_operation(self):
        """Complete the work operation after ensuring all progress messages are processed"""
        # Add completion message directly as part of loading off
        self.console.set_loading_off(completion_message="Progress Loading Test completed successfully")
        
        # Update button states
        self.simulate_work_btn.setEnabled(True)
        self.stop_work_btn.setEnabled(False)
    
    def run_stress_test(self):
        """Start a stress test with multiple worker threads"""
        self.console.append_message("Starting Concurrent Loading Test with 4 threads (Queued Mode)")
        
        # Update button states
        self.stress_test_btn.setEnabled(False)
        self.stop_stress_test_btn.setEnabled(True)
        self._stress_stop_requested = False
        
        # Show loading indicator with message queuing
        self.console.set_loading_on(queue_messages=True)
        
        # Start 4 worker threads
        self._stress_workers = []
        self._active_workers = 4
        
        for i in range(4):
            # Create worker with different iteration counts
            worker = StressTestWorker(i+1, iterations=5+i*2)  # 5, 7, 9, 11 iterations
            worker.progress.connect(self.on_stress_progress)
            worker.finished.connect(self.on_stress_worker_finished)
            self._stress_workers.append(worker)
            worker.start()
    
    def stop_stress_test(self):
        """Stop all stress test worker threads"""
        self._stress_stop_requested = True
        
        # Stop all workers
        for worker in self._stress_workers:
            worker.stop()
        
        # Wait for them to finish
        for worker in self._stress_workers:
            worker.wait(1000)  # Wait up to 1 second for each thread
        
        # Turn off loading indicator (this will process queued messages first)
        self.console.set_loading_off(completion_message="Concurrent Loading Test (Queued Mode) stopped by user")
        
        # Update button states
        self.stress_test_btn.setEnabled(True)
        self.stop_stress_test_btn.setEnabled(False)
    
    def on_stress_progress(self, worker_id, message):
        """Handle progress updates from stress test workers"""
        self.console.append_message(f"Thread {worker_id}: {message}")
    
    def on_stress_worker_finished(self, worker_id):
        """Handle completion of a stress test worker"""
        if not self._stress_stop_requested:
            self.console.append_message(f"Thread {worker_id} completed")
            
            # Decrement active worker count
            self._active_workers -= 1
            
            # If all workers are done, finish the stress test
            if self._active_workers <= 0:
                self.console.set_loading_off()
                self.console.append_message("Concurrent Loading Test (Queued Mode) completed successfully")
                self.stress_test_btn.setEnabled(True)
                self.stop_stress_test_btn.setEnabled(False)
    
    def run_direct_msg_test(self):
        """Start a test with multiple threads sending direct messages without loading indicators"""
        self.console.append_message("Starting Concurrent Message Test (No Animation)")
        
        # Update button states
        self.direct_msg_test_btn.setEnabled(False)
        self.stop_direct_msg_btn.setEnabled(True)
        self._direct_msg_stop_requested = False
        
        # NOTE: We're intentionally NOT activating the loading indicator here
        # to demonstrate direct message handling without loading animation
        
        # Start 4 worker threads
        self._direct_msg_workers = []
        self._active_direct_msg_workers = 4
        
        for i in range(4):
            # Create worker with different message counts
            worker = DirectMessageWorker(i+1, messages=8+i*3)  # 8, 11, 14, 17 messages
            worker.message.connect(self.on_direct_message)
            worker.finished.connect(self.on_direct_msg_worker_finished)
            self._direct_msg_workers.append(worker)
            worker.start()
    
    def stop_direct_msg_test(self):
        """Stop all direct message worker threads"""
        self._direct_msg_stop_requested = True
        
        # Stop all workers
        for worker in self._direct_msg_workers:
            worker.stop()
        
        # Wait for them to finish
        for worker in self._direct_msg_workers:
            worker.wait(1000)  # Wait up to 1 second for each thread
        
        # Update button states
        self.direct_msg_test_btn.setEnabled(True)
        self.stop_direct_msg_btn.setEnabled(False)
        
        self.console.append_message("Concurrent Message Test (No Animation) stopped by user")
    
    def on_direct_message(self, message):
        """Handle direct messages from worker threads"""
        self.console.append_message(message)
    
    def on_direct_msg_worker_finished(self, worker_id):
        """Handle completion of a direct message worker"""
        if not self._direct_msg_stop_requested:
            self.console.append_message(f"Direct message thread {worker_id} completed")
            
            # Decrement active worker count
            self._active_direct_msg_workers -= 1
            
            # If all workers are done, finish the test
            if self._active_direct_msg_workers <= 0:
                self.console.append_message("Concurrent Message Test (No Animation) completed successfully")
                self.direct_msg_test_btn.setEnabled(True)
                self.stop_direct_msg_btn.setEnabled(False)
    
    def clear_messages(self):
        """Clear all messages from the console"""
        # Simply clear the console immediately without any messages
        self.console.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())