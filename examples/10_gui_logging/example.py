#!/usr/bin/env python3
"""
GUI Logging Example - ModernLogger

This example demonstrates how to use the GUI logger
for visual log monitoring and management.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from modern_logger import ModernLogger
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
    from PySide6.QtCore import QTimer
    import time
    
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"❌ GUI dependencies not available: {e}")
    print("💡 Install PySide6 with: pip install PySide6")
    GUI_AVAILABLE = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI example - PySide6 not available")
        return
        
    print("🖥️ GUI Logging Example")
    print("=" * 30)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Example")
    window.setGeometry(300, 300, 600, 400)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title
    title = QLabel("ModernLogger GUI Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    # Create logger with GUI
    try:
        logger = ModernLogger(console=True, gui=True)
        gui_widget = logger.get_gui_widget()
        
        if gui_widget:
            layout.addWidget(gui_widget)
            
            # Add control buttons
            def log_sample_messages():
                logger.info("GUI logging started")
                logger.warning("This is a warning in the GUI")
                logger.error("Error message displayed in GUI")
                logger.critical("Critical issue logged to GUI")
                logger.info("GUI logging demonstration complete")
            
            log_button = QPushButton("Generate Sample Logs")
            log_button.clicked.connect(log_sample_messages)
            layout.addWidget(log_button)
            
            # Generate initial logs
            logger.info("GUI logger initialized successfully")
            logger.info("Click the button to generate more logs")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error creating GUI logger: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 GUI window opened - close it to end the example")
    
    # Run the application
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n⚠️ GUI example interrupted")
    finally:
        if 'logger' in locals():
            logger.close()
        print("✅ GUI logging example completed!")

if __name__ == "__main__":
    main() 