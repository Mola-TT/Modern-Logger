#!/usr/bin/env python3
"""
GUI Progress Tracking Example - ModernLogger

This example demonstrates advanced progress tracking features
including inline updates, progress bars, and completion tracking.
"""

import sys
import os
import time

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modern_logger import ModernLogger
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
    from PySide6.QtCore import QTimer
    
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"❌ GUI dependencies not available: {e}")
    print("💡 Install PySide6 with: pip install PySide6")
    GUI_AVAILABLE = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI progress tracking example - PySide6 not available")
        return
        
    print("📊 GUI Progress Tracking Example")
    print("=" * 35)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Progress Tracking")
    window.setGeometry(300, 300, 700, 500)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Progress Tracking Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Progress Tracking: Advanced progress monitoring with inline updates, "
        "percentage tracking, and real-time completion status. Perfect for "
        "operations with measurable progress and detailed status updates."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0fff0; border-radius: 5px;")
    description.setWordWrap(True)
    layout.addWidget(description)
    
    # Create logger with GUI
    try:
        logger = ModernLogger(console=True, gui=True)
        gui_widget = logger.get_gui_widget()
        
        if gui_widget:
            layout.addWidget(gui_widget)
            
            timer = QTimer()
            progress_step = 0
            
            def start_progress_demo():
                nonlocal progress_step
                
                logger.info("📊 Starting Progress Tracking demonstration...")
                app.processEvents()
                
                # Start inline progress mode
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True, inline_update=True)
                
                progress_step = 0
                
                def update_progress():
                    nonlocal progress_step
                    progress_step += 1
                    
                    if progress_step <= 20:
                        message = f"Processing step {progress_step}"
                        gui_widget.update_progress(progress_step, 20, message)
                    else:
                        timer.stop()
                        gui_widget.set_loading_off("📊 Progress tracking completed!")
                        start_button.setEnabled(True)
                
                timer.timeout.connect(update_progress)
                timer.start(200)  # Update every 200ms
                start_button.setEnabled(False)
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Progress cleared")
            
            # Control buttons
            start_button = QPushButton("Start Progress Demo")
            start_button.clicked.connect(start_progress_demo)
            layout.addWidget(start_button)
            
            clear_button = QPushButton("Clear Messages")
            clear_button.clicked.connect(clear_messages)
            layout.addWidget(clear_button)
            
            # Initial messages
            logger.info("📊 Progress Tracking ready")
            logger.info("💡 Click 'Start Progress Demo' to see real-time progress")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 Progress Tracking window opened")
    
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