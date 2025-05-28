#!/usr/bin/env python3
"""
GUI Scroll Management Example - ModernLogger

This example demonstrates how the GUI logger manages scrolling
when handling large volumes of messages.
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
        print("Skipping GUI scroll management example - PySide6 not available")
        return
        
    print("📜 GUI Scroll Management Example")
    print("=" * 35)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Scroll Management")
    window.setGeometry(300, 300, 700, 500)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Scroll Management Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Scroll Management: Intelligent scrolling behavior for high-volume logging. "
        "Features auto-scroll, scroll-to-bottom button, and scroll position preservation "
        "for optimal user experience with large message volumes."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #fffaf0; border-radius: 5px;")
    description.setWordWrap(True)
    layout.addWidget(description)
    
    # Create logger with GUI
    try:
        logger = ModernLogger(console=True, gui=True)
        gui_widget = logger.get_gui_widget()
        
        if gui_widget:
            layout.addWidget(gui_widget)
            
            timer = QTimer()
            message_count = 0
            
            def send_volume_messages():
                nonlocal message_count
                
                logger.info("📜 Starting high-volume message demonstration...")
                logger.info("💡 Try scrolling up while messages are being added")
                app.processEvents()
                
                message_count = 0
                
                def add_message():
                    nonlocal message_count
                    message_count += 1
                    
                    if message_count <= 100:
                        if message_count % 10 == 0:
                            logger.warning(f"High volume message #{message_count}")
                        else:
                            logger.info(f"Message #{message_count} - scroll behavior test")
                    else:
                        timer.stop()
                        logger.info("📜 High-volume demonstration completed!")
                        volume_button.setEnabled(True)
                
                timer.timeout.connect(add_message)
                timer.start(100)  # Send message every 100ms
                volume_button.setEnabled(False)
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Messages cleared - scroll position reset")
            
            # Control buttons
            volume_button = QPushButton("Send 100 Messages")
            volume_button.clicked.connect(send_volume_messages)
            layout.addWidget(volume_button)
            
            clear_button = QPushButton("Clear Messages")
            clear_button.clicked.connect(clear_messages)
            layout.addWidget(clear_button)
            
            # Initial messages
            logger.info("📜 Scroll Management ready")
            logger.info("💡 Send volume messages and try scrolling to test behavior")
            logger.info("🔍 Notice the scroll-to-bottom button when you scroll up")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 Scroll Management window opened")
    
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