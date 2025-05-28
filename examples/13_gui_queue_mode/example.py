#!/usr/bin/env python3
"""
GUI Queue Mode Example - ModernLogger

This example demonstrates how to use the GUI logger in queue mode,
where messages are queued during loading and displayed in batch when loading ends.
"""

import sys
import os
import time
import threading

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modern_logger import ModernLogger
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
    from PySide6.QtCore import QTimer, QThread, Signal
    import time
    
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"❌ GUI dependencies not available: {e}")
    print("💡 Install PySide6 with: pip install PySide6")
    GUI_AVAILABLE = False

class WorkerThread(QThread):
    """Worker thread that generates messages during loading"""
    message_ready = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """Simulate work that generates messages"""
        for i in range(10):
            if not self.running:
                break
            
            # Simulate work
            time.sleep(0.5)
            
            # Generate different types of messages
            if i % 3 == 0:
                self.message_ready.emit(f"Processing item {i+1}/10...")
            elif i % 3 == 1:
                self.message_ready.emit(f"Validating data for item {i+1}...")
            else:
                self.message_ready.emit(f"Completed processing item {i+1}")
    
    def stop(self):
        self.running = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI queue mode example - PySide6 not available")
        return
        
    print("📥 GUI Queue Mode Example")
    print("=" * 30)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Queue Mode Example")
    window.setGeometry(300, 300, 700, 500)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Queue Mode Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Queue Mode: Messages are collected during loading operations and displayed "
        "in batch when loading completes. This prevents UI updates during intensive "
        "operations and provides smooth user experience."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
    description.setWordWrap(True)
    layout.addWidget(description)
    
    # Create logger with GUI
    try:
        logger = ModernLogger(console=True, gui=True)
        gui_widget = logger.get_gui_widget()
        
        if gui_widget:
            layout.addWidget(gui_widget)
            
            # Variables for worker management
            worker = None
            
            def start_queue_mode_demo():
                nonlocal worker
                
                logger.info("🚀 Starting Queue Mode demonstration...")
                logger.info("Messages during loading will be queued and shown when complete")
                
                # Process events to show initial messages
                app.processEvents()
                
                # Start loading in queue mode (default)
                gui_widget.set_loading_on(queue_messages=True)
                logger.info("⏳ Loading started - messages are now being queued")
                
                # Create and start worker thread
                worker = WorkerThread()
                
                def on_worker_message(message):
                    logger.info(f"📦 {message}")  # These messages will be queued
                
                def on_worker_finished():
                    # End loading - this will display all queued messages at once
                    gui_widget.set_loading_off("✅ Loading completed - all queued messages displayed!")
                    start_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                worker.message_ready.connect(on_worker_message)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                start_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def stop_queue_mode_demo():
                nonlocal worker
                if worker and worker.isRunning():
                    worker.stop()
                    worker.wait()
                    gui_widget.set_loading_off("⚠️ Operation stopped by user")
                    logger.warning("Queue mode demonstration stopped")
                
                start_button.setEnabled(True)
                stop_button.setEnabled(False)
            
            def show_immediate_messages():
                logger.info("💬 Immediate message 1")
                logger.warning("💬 Immediate message 2")
                logger.error("💬 Immediate message 3")
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Messages cleared")
            
            # Control buttons
            button_widget = QWidget()
            button_layout = QVBoxLayout(button_widget)
            
            start_button = QPushButton("Start Queue Mode Demo")
            start_button.clicked.connect(start_queue_mode_demo)
            button_layout.addWidget(start_button)
            
            stop_button = QPushButton("Stop Demo")
            stop_button.clicked.connect(stop_queue_mode_demo)
            stop_button.setEnabled(False)
            button_layout.addWidget(stop_button)
            
            immediate_button = QPushButton("Send Immediate Messages")
            immediate_button.clicked.connect(show_immediate_messages)
            button_layout.addWidget(immediate_button)
            
            clear_button = QPushButton("Clear Messages")
            clear_button.clicked.connect(clear_messages)
            button_layout.addWidget(clear_button)
            
            layout.addWidget(button_widget)
            
            # Initial messages
            logger.info("🎯 GUI Queue Mode ready")
            logger.info("📝 Click 'Start Queue Mode Demo' to see queued messaging in action")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error creating GUI logger: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 GUI Queue Mode window opened")
    print("💡 Try the 'Start Queue Mode Demo' button to see messages queued during loading")
    
    # Run the application
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n⚠️ GUI queue mode example interrupted")
    finally:
        if 'logger' in locals():
            logger.close()
        print("✅ GUI queue mode example completed!")

if __name__ == "__main__":
    main() 