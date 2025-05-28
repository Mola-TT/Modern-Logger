#!/usr/bin/env python3
"""
GUI Non-Queue Mode Example - ModernLogger

This example demonstrates how to use the GUI logger in non-queue mode,
where messages appear immediately as they are sent, even during loading operations.
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

class ImmediateWorkerThread(QThread):
    """Worker thread that generates immediate messages"""
    message_ready = Signal(str, str)  # level, message
    
    def __init__(self, message_count=15):
        super().__init__()
        self.running = True
        self.message_count = message_count
    
    def run(self):
        """Generate messages with immediate display"""
        for i in range(self.message_count):
            if not self.running:
                break
            
            # Simulate work with variable timing
            time.sleep(0.4)
            
            # Generate different types of messages
            if i % 5 == 0:
                self.message_ready.emit("info", f"Starting batch {i//5 + 1}")
            elif i % 5 == 1:
                self.message_ready.emit("info", f"Processing item {i}")
            elif i % 5 == 2:
                self.message_ready.emit("warning", f"Resource usage high during item {i}")
            elif i % 5 == 3:
                self.message_ready.emit("info", f"Validating item {i}")
            else:
                self.message_ready.emit("info", f"Completed batch {i//5 + 1}")
    
    def stop(self):
        self.running = False

class StreamingWorkerThread(QThread):
    """Worker thread that generates rapid streaming messages"""
    message_ready = Signal(str, str)  # level, message
    
    def __init__(self):
        super().__init__()
        self.running = True
    
    def run(self):
        """Generate rapid stream of messages"""
        data_types = ["user_data", "system_info", "network_stats", "database_query", "cache_update"]
        
        for i in range(50):
            if not self.running:
                break
            
            # Rapid messages
            time.sleep(0.1)
            
            data_type = data_types[i % len(data_types)]
            
            if i % 10 == 0:
                self.message_ready.emit("warning", f"High frequency data: {data_type} #{i}")
            elif i % 7 == 0:
                self.message_ready.emit("error", f"Error processing {data_type} #{i}")
            else:
                self.message_ready.emit("info", f"Processed {data_type} #{i}")
    
    def stop(self):
        self.running = False

def main():
    if not GUI_AVAILABLE:
        print("Skipping GUI non-queue mode example - PySide6 not available")
        return
        
    print("⚡ GUI Non-Queue Mode Example")
    print("=" * 30)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create main window
    window = QWidget()
    window.setWindowTitle("ModernLogger GUI Non-Queue Mode Example")
    window.setGeometry(300, 300, 700, 600)
    
    # Create layout
    layout = QVBoxLayout()
    
    # Add title and description
    title = QLabel("GUI Non-Queue Mode Example")
    title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
    layout.addWidget(title)
    
    description = QLabel(
        "Non-Queue Mode (Passthrough): Messages appear immediately as they are sent, "
        "even during loading operations. This provides real-time feedback and is perfect "
        "for monitoring live operations, debugging, or streaming data."
    )
    description.setStyleSheet("margin: 10px; padding: 10px; background-color: #fff4e6; border-radius: 5px;")
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
            
            def start_passthrough_demo():
                nonlocal worker
                
                logger.info("⚡ Starting Non-Queue Mode demonstration...")
                logger.info("Messages will appear immediately as they are generated")
                
                # Process events to show initial messages
                app.processEvents()
                
                # Start loading in passthrough mode (no queuing)
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)
                
                # Create and start worker thread
                worker = ImmediateWorkerThread(message_count=15)
                
                def on_worker_message(level, message):
                    # Messages appear immediately
                    if level == "info":
                        logger.info(f"🔄 {message}")
                    elif level == "warning":
                        logger.warning(f"⚠️ {message}")
                    elif level == "error":
                        logger.error(f"❌ {message}")
                
                def on_worker_finished():
                    # End loading
                    gui_widget.set_loading_off("✅ Non-queue mode demonstration completed!")
                    start_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                worker.message_ready.connect(on_worker_message)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                start_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def start_streaming_demo():
                nonlocal worker
                
                logger.info("🌊 Starting Streaming Mode demonstration...")
                logger.info("Rapid messages will stream in real-time")
                
                # Process events to show initial messages
                app.processEvents()
                
                # Start loading in passthrough mode for streaming
                gui_widget.set_loading_on(queue_messages=False, passthrough_messages=True)
                
                # Create and start streaming worker
                worker = StreamingWorkerThread()
                
                def on_worker_message(level, message):
                    # Messages stream immediately
                    if level == "info":
                        logger.info(f"📊 {message}")
                    elif level == "warning":
                        logger.warning(f"⚠️ {message}")
                    elif level == "error":
                        logger.error(f"🚨 {message}")
                
                def on_worker_finished():
                    # End loading
                    gui_widget.set_loading_off("🌊 Streaming demonstration completed!")
                    stream_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                worker.message_ready.connect(on_worker_message)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                stream_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def start_no_animation_demo():
                nonlocal worker
                
                logger.info("📝 Starting No Animation demonstration...")
                logger.info("Messages without any loading animation")
                
                # No loading state - just direct messages
                worker = ImmediateWorkerThread(message_count=10)
                
                def on_worker_message(level, message):
                    # Direct messages without animation
                    if level == "info":
                        logger.info(f"💬 {message}")
                    elif level == "warning":
                        logger.warning(f"⚠️ {message}")
                    elif level == "error":
                        logger.error(f"❌ {message}")
                
                def on_worker_finished():
                    logger.info("📝 No animation demonstration completed!")
                    no_anim_button.setEnabled(True)
                    stop_button.setEnabled(False)
                
                worker.message_ready.connect(on_worker_message)
                worker.finished.connect(on_worker_finished)
                worker.start()
                
                no_anim_button.setEnabled(False)
                stop_button.setEnabled(True)
            
            def stop_demo():
                nonlocal worker
                if worker and worker.isRunning():
                    worker.stop()
                    worker.wait()
                    
                    # Only turn off loading if it was on
                    try:
                        gui_widget.set_loading_off("⚠️ Demonstration stopped by user")
                    except:
                        pass
                    
                    logger.warning("Non-queue mode demonstration stopped")
                
                start_button.setEnabled(True)
                stream_button.setEnabled(True)
                no_anim_button.setEnabled(True)
                stop_button.setEnabled(False)
            
            def burst_messages():
                logger.info("💥 Sending burst of immediate messages...")
                
                # Send multiple messages rapidly
                for i in range(8):
                    if i % 3 == 0:
                        logger.info(f"📦 Burst message {i+1}: Data packet received")
                    elif i % 3 == 1:
                        logger.warning(f"⚠️ Burst message {i+1}: Warning condition")
                    else:
                        logger.error(f"🚨 Burst message {i+1}: Error detected")
                    
                    # Small delay to see the real-time effect
                    app.processEvents()
                    time.sleep(0.1)
                
                logger.info("💥 Burst complete - all messages appeared immediately")
            
            def clear_messages():
                gui_widget.clear()
                logger.info("🗑️ Messages cleared")
            
            # Control buttons
            button_widget = QWidget()
            button_layout = QVBoxLayout(button_widget)
            
            # Row 1: Main demo buttons
            row1 = QWidget()
            row1_layout = QHBoxLayout(row1)
            
            start_button = QPushButton("Start Passthrough Demo")
            start_button.clicked.connect(start_passthrough_demo)
            row1_layout.addWidget(start_button)
            
            stream_button = QPushButton("Streaming Demo")
            stream_button.clicked.connect(start_streaming_demo)
            row1_layout.addWidget(stream_button)
            
            stop_button = QPushButton("Stop Demo")
            stop_button.clicked.connect(stop_demo)
            stop_button.setEnabled(False)
            row1_layout.addWidget(stop_button)
            
            button_layout.addWidget(row1)
            
            # Row 2: Additional functions
            row2 = QWidget()
            row2_layout = QHBoxLayout(row2)
            
            no_anim_button = QPushButton("No Animation Demo")
            no_anim_button.clicked.connect(start_no_animation_demo)
            row2_layout.addWidget(no_anim_button)
            
            burst_button = QPushButton("Burst Messages")
            burst_button.clicked.connect(burst_messages)
            row2_layout.addWidget(burst_button)
            
            clear_button = QPushButton("Clear Messages")
            clear_button.clicked.connect(clear_messages)
            row2_layout.addWidget(clear_button)
            
            button_layout.addWidget(row2)
            
            layout.addWidget(button_widget)
            
            # Initial messages
            logger.info("⚡ GUI Non-Queue Mode ready")
            logger.info("📝 Messages will appear immediately - try the different demos")
            logger.info("💡 Notice how messages appear in real-time without waiting")
            
        else:
            error_label = QLabel("❌ Failed to get GUI widget")
            layout.addWidget(error_label)
            
    except Exception as e:
        error_label = QLabel(f"❌ Error creating GUI logger: {e}")
        layout.addWidget(error_label)
    
    window.setLayout(layout)
    window.show()
    
    print("🚀 GUI Non-Queue Mode window opened")
    print("💡 Try the different demo buttons to see immediate message display")
    
    # Run the application
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\n⚠️ GUI non-queue mode example interrupted")
    finally:
        if 'logger' in locals():
            logger.close()
        print("✅ GUI non-queue mode example completed!")

if __name__ == "__main__":
    main() 