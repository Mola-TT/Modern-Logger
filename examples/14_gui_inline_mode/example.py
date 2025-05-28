#!/usr/bin/env python3
"""
GUI Inline Mode Example - ModernLogger

This example demonstrates how to use the GUI logger in inline mode,
where progress updates are shown in real-time by updating a single line.
"""

import sys
import os
import time

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modern_logger import ModernLogger
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
    from PySide6.QtCore import QTimer, QThread, Signal
    import time
    
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"❌ GUI dependencies not available: {e}")
    print("💡 Install PySide6 with: pip install PySide6")
    GUI_AVAILABLE = False

class ProgressWorkerThread(QThread):
    """Worker thread that generates progress updates"""
    progress_update = Signal(int, int, str)  # current, total, message
    
    def __init__(self, total_steps=20):
        super().__init__()
        self.running = True
        self.total_steps = total_steps
    
    def run(self):
        """Simulate work with progress updates"""
        for i in range(self.total_steps):
            if not self.running:
                break
            
            # Simulate work
            time.sleep(0.3)
            
            # Generate progress update
            current = i + 1
            percentage = int((current / self.total_steps) * 100)
            
            if i < 5:
                message = f"Initializing step {current}"
            elif i < 15:
                message = f"Processing data chunk {current-5}"
            else:
                message = f"Finalizing step {current-15}"
            
            self.progress_update.emit(current, self.total_steps, message)
    
    def stop(self):
        self.running = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI inline mode example - PySide6 not available")
        return
        
    print("📊 GUI Inline Mode Example")
    print("=" * 30)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Inline Mode Example")
    window.setGeometry(300, 300, 700, 500)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Inline Mode Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Inline Mode: Progress updates are displayed in real-time by updating a single "
        "line in the GUI. This provides immediate feedback while maintaining a clean "
        "interface. Perfect for operations with measurable progress."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #e8f4fd; border-radius: 5px;")
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
            
            def start_inline_demo():
                nonlocal worker
                
                logger.info("🚀 Starting Inline Mode demonstration...")
                logger.info("Progress will be shown in real-time on a single updating line")
                
                # Process events to show initial messages
                app.processEvents()
                
                # Start loading in inline mode
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
                
                # Create and start worker thread
                worker = ProgressWorkerThread(total_steps=20)
                
                def on_progress_update(current, total, message):
                    # Update the progress line in real-time
                    gui_widget.update_progress(current, total, message)
                
                def on_worker_finished():
                    # End loading
                    gui_widget.set_loading_off("✅ Inline progress completed successfully!")
                    start_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                worker.progress_update.connect(on_progress_update)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                start_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def start_fast_demo():
                nonlocal worker
                
                logger.info("⚡ Starting Fast Inline Mode demonstration...")
                logger.info("Rapid progress updates to test real-time performance")
                
                # Process events to show initial messages
                app.processEvents()
                
                # Start loading in inline mode
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
                
                # Create and start worker thread with more steps and faster updates
                worker = ProgressWorkerThread(total_steps=100)
                
                def on_progress_update(current, total, message):
                    # Update the progress line in real-time
                    percentage = int((current / total) * 100)
                    gui_widget.update_progress(current, total, f"Fast processing {percentage}% - {message}")
                
                def on_worker_finished():
                    # End loading
                    gui_widget.set_loading_off("⚡ Fast inline progress completed!")
                    fast_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                # Override run method for faster updates
                def fast_run(self):
                    for i in range(self.total_steps):
                        if not self.running:
                            break
                        time.sleep(0.05)  # Much faster updates
                        current = i + 1
                        message = f"Item {current}"
                        self.progress_update.emit(current, self.total_steps, message)
                
                worker.run = fast_run.__get__(worker, ProgressWorkerThread)
                
                worker.progress_update.connect(on_progress_update)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                fast_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def stop_demo():
                nonlocal worker
                if worker and worker.isRunning():
                    worker.stop()
                    worker.wait()
                    gui_widget.set_loading_off("⚠️ Inline progress stopped by user")
                    logger.warning("Inline mode demonstration stopped")
                
                start_button.setEnabled(True)
                fast_button.setEnabled(True)
                stop_button.setEnabled(False)
            
            def show_static_progress():
                logger.info("📈 Demonstrating static progress updates...")
                
                # Enable inline mode
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
                
                # Show a series of manual progress updates
                app.processEvents()
                for i in range(1, 6):
                    time.sleep(0.5)
                    gui_widget.update_progress(i, 5, f"Manual step {i}/5")
                    app.processEvents()
                
                # End with completion
                gui_widget.set_loading_off("📈 Static progress demonstration completed")
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Messages cleared")
            
            # Control buttons
            button_widget = QWidget()
            button_layout = QVBoxLayout(button_widget)
            
            # Row 1: Main demo buttons
            row1 = QWidget()
            row1_layout = QHBoxLayout(row1)
            
            start_button = QPushButton("Start Inline Demo")
            start_button.clicked.connect(start_inline_demo)
            row1_layout.addWidget(start_button)
            
            fast_button = QPushButton("Fast Updates Demo")
            fast_button.clicked.connect(start_fast_demo)
            row1_layout.addWidget(fast_button)
            
            stop_button = QPushButton("Stop Demo")
            stop_button.clicked.connect(stop_demo)
            stop_button.setEnabled(False)
            row1_layout.addWidget(stop_button)
            
            button_layout.addWidget(row1)
            
            # Row 2: Additional functions
            row2 = QWidget()
            row2_layout = QHBoxLayout(row2)
            
            static_button = QPushButton("Static Progress Demo")
            static_button.clicked.connect(show_static_progress)
            row2_layout.addWidget(static_button)
            
            clear_button = QPushButton("Clear Messages")
            clear_button.clicked.connect(clear_messages)
            row2_layout.addWidget(clear_button)
            
            button_layout.addWidget(row2)
            
            layout.addWidget(button_widget)
            
            # Initial messages
            logger.info("📊 GUI Inline Mode ready")
            logger.info("📝 Click buttons to see different inline progress demonstrations")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error creating GUI logger: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 GUI Inline Mode window opened")
    print("💡 Try the different demo buttons to see inline progress in action")
    
    # Run the application
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n⚠️ GUI inline mode example interrupted")
    finally:
        if 'logger' in locals():
            logger.close()
        print("✅ GUI inline mode example completed!")

if __name__ == "__main__":
    main() 