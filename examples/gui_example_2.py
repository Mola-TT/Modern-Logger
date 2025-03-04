"""
GUI Logger example for Modern Logger (with log levels).

This example demonstrates how to use the GUI logger in a PySide6 application,
including log level functionality.
"""

import sys
import os
import time
import threading
import random
import traceback

# Add the parent directory to the path so we can import the package
try:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)
    print(f"Added {parent_dir} to Python path")
except Exception as e:
    print(f"Warning: Could not add parent directory to path: {e}")

# Try to import PySide6
try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
        QWidget, QPushButton, QComboBox, QLabel, QSpinBox, QMessageBox,
        QFrame, QSplitter, QScrollArea, QCheckBox
    )
    from PySide6.QtCore import Qt, QTimer, QThread, Signal, QEvent
    from PySide6.QtGui import QFont
    print("Successfully imported PySide6")
except ImportError as e:
    print(f"Error importing PySide6: {e}")
    print("\nPlease install PySide6 with: pip install PySide6")
    sys.exit(1)

# Try to import modern_logger
try:
    from modern_logger import Logger, FileLogger, MultiLogger, ModernLogger, GUILogger
    print("Successfully imported modern_logger package")
except ImportError as e:
    print(f"Error importing modern_logger: {e}")
    print("\nPossible solutions:")
    print("1. Make sure you're running this script from the examples directory")
    print("2. Install the package with: pip install -e ..")
    print("3. Check if the modern_logger directory exists in the parent directory")
    sys.exit(1)

class ProgressWorker(QThread):
    """Worker thread for progress operations"""
    progress = Signal(int, int, str)  # current, total, message
    finished = Signal()
    
    def __init__(self, steps):
        super().__init__()
        self.steps = steps
        self._stop_requested = False
    
    def run(self):
        try:
            for i in range(self.steps):
                if self._stop_requested:
                    break
                    
                # Random delay between 0.1 and 0.5 seconds
                time.sleep(random.uniform(0.1, 0.5))
                
                # Update progress
                self.progress.emit(i + 1, self.steps, f"Processing step {i + 1}/{self.steps}")
            
            self.finished.emit()
            
        except Exception as e:
            print(f"Error in progress worker: {e}")
            traceback.print_exc()
    
    def stop(self):
        """Request the worker to stop"""
        self._stop_requested = True

class LoggerDemoWindow(QMainWindow):
    """Demo window for the Modern Logger"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Modern Logger Demo")
        self.resize(900, 700)
        
        # Initialize worker threads
        self.worker = None
        self.progress_worker = None
        
        try:
            # Create log directory if it doesn't exist
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Create central widget and layout
            central_widget = QWidget()
            main_layout = QVBoxLayout(central_widget)
            
            # Create controls
            controls_layout = QHBoxLayout()
            
            # Log level selector
            level_layout = QVBoxLayout()
            level_layout.addWidget(QLabel("Log Level:"))
            self.level_combo = QComboBox()
            self.level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
            self.level_combo.setCurrentIndex(1)  # INFO by default
            self.level_combo.currentIndexChanged.connect(self.update_log_level)
            level_layout.addWidget(self.level_combo)
            controls_layout.addLayout(level_layout)
            
            # Log message buttons
            log_buttons_layout = QVBoxLayout()
            log_buttons_layout.addWidget(QLabel("Log Messages:"))
            buttons_layout = QHBoxLayout()
            
            self.debug_button = QPushButton("Debug")
            self.debug_button.clicked.connect(lambda: self.log_message(Logger.DEBUG))
            buttons_layout.addWidget(self.debug_button)
            
            self.info_button = QPushButton("Info")
            self.info_button.clicked.connect(lambda: self.log_message(Logger.INFO))
            buttons_layout.addWidget(self.info_button)
            
            self.warning_button = QPushButton("Warning")
            self.warning_button.clicked.connect(lambda: self.log_message(Logger.WARNING))
            buttons_layout.addWidget(self.warning_button)
            
            self.error_button = QPushButton("Error")
            self.error_button.clicked.connect(lambda: self.log_message(Logger.ERROR))
            buttons_layout.addWidget(self.error_button)
            
            self.critical_button = QPushButton("Critical")
            self.critical_button.clicked.connect(lambda: self.log_message(Logger.CRITICAL))
            buttons_layout.addWidget(self.critical_button)
            
            log_buttons_layout.addLayout(buttons_layout)
            controls_layout.addLayout(log_buttons_layout)
            
            # Progress controls
            progress_layout = QVBoxLayout()
            progress_layout.addWidget(QLabel("Progress:"))
            progress_buttons_layout = QHBoxLayout()
            
            self.progress_count = QSpinBox()
            self.progress_count.setRange(1, 100)
            self.progress_count.setValue(10)
            self.progress_count.setPrefix("Steps: ")
            progress_buttons_layout.addWidget(self.progress_count)
            
            self.start_progress_button = QPushButton("Start Progress")
            self.start_progress_button.clicked.connect(self.start_progress)
            progress_buttons_layout.addWidget(self.start_progress_button)
            
            progress_layout.addLayout(progress_buttons_layout)
            controls_layout.addLayout(progress_layout)
            
            # Exception and clear buttons
            actions_layout = QVBoxLayout()
            actions_layout.addWidget(QLabel("Actions:"))
            actions_buttons_layout = QHBoxLayout()
            
            self.exception_button = QPushButton("Log Exception")
            self.exception_button.clicked.connect(self.log_exception)
            actions_buttons_layout.addWidget(self.exception_button)
            
            self.clear_button = QPushButton("Clear Log")
            self.clear_button.clicked.connect(self.clear_log)
            actions_buttons_layout.addWidget(self.clear_button)
            
            actions_layout.addLayout(actions_buttons_layout)
            controls_layout.addLayout(actions_layout)
            
            # Add controls to main layout
            main_layout.addLayout(controls_layout)
            
            # Create the logger
            self.logger = ModernLogger(
                console=True,
                file=os.path.join(log_dir, "demo.log"),
                gui=True
            )
            
            # Get and add the GUI widget
            gui_widget = self.logger.get_gui_widget()
            if gui_widget:
                main_layout.addWidget(gui_widget)
                
                # Customize the scroll button
                gui_widget.customize_scroll_button(
                    size=40,
                    background_color="rgba(100, 150, 200, 180)",
                    hover_color="rgba(120, 170, 220, 220)",
                    pressed_color="rgba(80, 130, 180, 220)",
                    text="↓",
                    font=QFont("Arial", 18, QFont.Bold),
                    animation_duration=300,
                    shadow_enabled=True,
                    shadow_blur=8,
                    shadow_offset=(0, 3)
                )
            else:
                print("Error: Could not get GUI widget from logger")
                sys.exit(1)
            
            # Set central widget
            self.setCentralWidget(central_widget)
            
            # Log initial message
            self.logger.info("Modern Logger Demo started")
            self.logger.info(f"Python version: {sys.version}")
            self.logger.info(f"Log file: {os.path.abspath(os.path.join(log_dir, 'demo.log'))}")
            self.logger.info("Click the buttons above to test different logging features")
            
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", 
                                f"Error initializing the application: {str(e)}\n\n{traceback.format_exc()}")
            raise
    
    def update_log_level(self):
        """Update the log level based on the combo box selection"""
        try:
            level_name = self.level_combo.currentText()
            level = getattr(Logger, level_name)
            self.logger.set_level(level)
            self.logger.info(f"Log level set to {level_name}")
        except Exception as e:
            self.logger.error(f"Error updating log level: {e}")
            traceback.print_exc()
    
    def log_message(self, level):
        """Log a message at the specified level"""
        try:
            level_name = Logger.LEVEL_NAMES.get(level, "UNKNOWN")
            message = f"This is a {level_name.lower()} message (timestamp: {time.time()})"
            
            if level == Logger.DEBUG:
                self.logger.debug(message)
            elif level == Logger.INFO:
                self.logger.info(message)
            elif level == Logger.WARNING:
                self.logger.warning(message)
            elif level == Logger.ERROR:
                self.logger.error(message)
            elif level == Logger.CRITICAL:
                self.logger.critical(message)
        except Exception as e:
            self.logger.error(f"Error logging message: {e}")
    
    def start_progress(self):
        """Start a progress operation"""
        try:
            if self.progress_worker and self.progress_worker.isRunning():
                return
            
            steps = self.progress_count.value()
            self.logger.info(f"Starting progress operation with {steps} steps...")
            
            self.progress_worker = ProgressWorker(steps)
            self.progress_worker.progress.connect(self._on_progress_update)
            self.progress_worker.finished.connect(self._on_progress_finished)
            self.progress_worker.start()
            
            self.start_progress_button.setEnabled(False)
            
        except Exception as e:
            self.logger.error(f"Error starting progress: {e}")
    
    def _on_progress_update(self, current, total, message):
        """Handle progress updates"""
        self.logger.info(f"Progress: {message} ({current}/{total})")
    
    def _on_progress_finished(self):
        """Handle progress completion"""
        self.logger.info("Progress operation completed")
        self.start_progress_button.setEnabled(True)
        
        if self.progress_worker:
            self.progress_worker.deleteLater()
            self.progress_worker = None
    
    def log_exception(self):
        """Log a test exception"""
        try:
            raise ValueError("This is a test exception")
        except Exception:
            self.logger.exception("An error occurred")
    
    def clear_log(self):
        """Clear the log display"""
        gui_widget = self.logger.get_gui_widget()
        if gui_widget:
            gui_widget.clear()
            self.logger.info("Log cleared")
    
    def closeEvent(self, event):
        """Handle window close event"""
        try:
            # Stop any running workers
            if self.progress_worker and self.progress_worker.isRunning():
                self.progress_worker.stop()
                self.progress_worker.wait()
            
            self.logger.info("Application closing")
            
        except Exception as e:
            print(f"Error during close: {e}")
        finally:
            super().closeEvent(event)


def main():
    """Main function"""
    print("Starting Modern Logger GUI Example...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        app = QApplication(sys.argv)
        window = LoggerDemoWindow()
        window.show()
        return app.exec()
    except Exception as e:
        print(f"Error in GUI example: {e}")
        traceback.print_exc()
        
        # Show error in GUI if possible
        try:
            if QApplication.instance():
                QMessageBox.critical(None, "Application Error", 
                                    f"Error starting the application: {str(e)}\n\n{traceback.format_exc()}")
        except:
            pass
            
        return 1


if __name__ == "__main__":
    sys.exit(main()) 