#!/usr/bin/env python3
"""
GUI Multithread Example - ModernLogger

This example demonstrates how the GUI logger handles multiple threads
sending messages simultaneously with thread-safe operations.
"""

import sys
import os
import time
import random

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modern_logger import ModernLogger
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
    from PySide6.QtCore import QThread, Signal
    import time
    
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"❌ GUI dependencies not available: {e}")
    print("💡 Install PySide6 with: pip install PySide6")
    GUI_AVAILABLE = False

class MultiWorkerThread(QThread):
    """Worker thread for multithread demonstration"""
    message_ready = Signal(str, str, int)  # level, message, thread_id
    
    def __init__(self, thread_id, task_type="general", message_count=10):
        super().__init__()
        self.thread_id = thread_id
        self.task_type = task_type
        self.message_count = message_count
        self.running = True
    
    def run(self):
        """Generate messages from this thread"""
        for i in range(self.message_count):
            if not self.running:
                break
            
            # Variable delay to simulate different work patterns
            delay = random.uniform(0.1, 0.8)
            time.sleep(delay)
            
            # Generate messages based on task type
            if self.task_type == "database":
                level = "info" if i % 3 != 2 else "warning"
                message = f"DB operation {i+1}"
            elif self.task_type == "api":
                level = "info" if i % 4 != 3 else "warning"
                message = f"API call {i+1}"
            else:
                level = random.choice(["info", "warning"])
                message = f"Task {i+1}"
            
            self.message_ready.emit(level, message, self.thread_id)
    
    def stop(self):
        self.running = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI multithread example - PySide6 not available")
        return
        
    print("🧵 GUI Multithread Example")
    print("=" * 30)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Multithread Example")
    window.setGeometry(300, 300, 800, 600)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Multithread Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Multithread Support: The GUI logger safely handles messages from multiple "
        "threads simultaneously. Each thread can send messages independently while "
        "the GUI maintains thread safety and proper message ordering."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f8ff; border-radius: 5px;")
    description.setWordWrap(True)
    layout.addWidget(description)
    
    # Create logger with GUI
    try:
        logger = ModernLogger(console=True, gui=True)
        gui_widget = logger.get_gui_widget()
        
        if gui_widget:
            layout.addWidget(gui_widget)
            
            # Thread management
            workers = []
            active_workers = 0
            
            def start_concurrent_demo():
                nonlocal workers, active_workers
                
                logger.info("🧵 Starting 4 concurrent threads...")
                app.processEvents()
                
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)
                
                workers = []
                active_workers = 4
                
                for i in range(4):
                    worker = MultiWorkerThread(i+1, "database", 8)
                    
                    def on_message(level, message, thread_id):
                        if level == "info":
                            logger.info(f"🔵 [T{thread_id}] {message}")
                        else:
                            logger.warning(f"🟡 [T{thread_id}] {message}")
                    
                    def on_finished():
                        nonlocal active_workers
                        active_workers -= 1
                        if active_workers <= 0:
                            gui_widget.set_loading_off("🧵 All threads completed!")
                            concurrent_button.setEnabled(True)
                            stop_button.setEnabled(False)
                    
                    worker.message_ready.connect(on_message)
                    worker.finished.connect(on_finished)
                    workers.append(worker)
                    worker.start()
                
                concurrent_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def stop_all():
                nonlocal workers
                for worker in workers:
                    if worker.isRunning():
                        worker.stop()
                        worker.wait()
                
                workers.clear()
                gui_widget.set_loading_off("⚠️ Stopped by user")
                
                concurrent_button.setEnabled(True)
                stop_button.setEnabled(False)
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Cleared")
            
            # Control buttons
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            
            concurrent_button = QPushButton("Start 4 Threads")
            concurrent_button.clicked.connect(start_concurrent_demo)
            button_layout.addWidget(concurrent_button)
            
            stop_button = QPushButton("Stop All")
            stop_button.clicked.connect(stop_all)
            stop_button.setEnabled(False)
            button_layout.addWidget(stop_button)
            
            clear_button = QPushButton("Clear")
            clear_button.clicked.connect(clear_messages)
            button_layout.addWidget(clear_button)
            
            layout.addWidget(button_widget)
            
            # Initial messages
            logger.info("🧵 Multithread demo ready")
            logger.info("💡 Click 'Start 4 Threads' to see concurrent messaging")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 Multithread window opened")
    
    # Run the application
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted")
    finally:
        if 'logger' in locals():
            logger.close()
        print("✅ Completed!")

if __name__ == "__main__":
    main() 