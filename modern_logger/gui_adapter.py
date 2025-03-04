"""
GUI Logger Adapter for Modern Logger.

This module provides an adapter to connect the GUI logger with the base logger system.
"""

from .logger import Logger
from .gui_logger import ModernLogger
from typing import Optional, Dict, Any
import traceback
import sys


class GUILogger(Logger):
    """Logger that writes to a ModernLogger GUI widget"""
    
    def __init__(self, 
                 name: str = "GUILogger", 
                 level: int = Logger.INFO,
                 gui_logger: Optional[ModernLogger] = None):
        """
        Initialize a GUI logger
        
        Args:
            name (str, optional): Logger name. Defaults to "GUILogger".
            level (int, optional): Minimum log level. Defaults to Logger.INFO.
            gui_logger (Optional[ModernLogger], optional): GUI logger widget. Defaults to None.
        """
        super().__init__(name, level)
        self.gui_logger = gui_logger
        
        # Level-specific formatting
        self._level_prefixes = {
            self.DEBUG: "🔍 ",
            self.INFO: "ℹ️ ",
            self.WARNING: "⚠️ ",
            self.ERROR: "❌ ",
            self.CRITICAL: "🔥 "
        }
    
    def set_gui_logger(self, gui_logger: ModernLogger) -> None:
        """
        Set the GUI logger widget
        
        Args:
            gui_logger (ModernLogger): GUI logger widget
        """
        self.gui_logger = gui_logger
    
    def _format_message(self, level: int, message: str) -> str:
        """
        Format a log message with level-specific prefix
        
        Args:
            level (int): Log level
            message (str): Log message
            
        Returns:
            str: Formatted log message
        """
        prefix = self._level_prefixes.get(level, "")
        return f"{prefix}{message}"
    
    def _write(self, message: str) -> None:
        """
        Write a message to the GUI logger
        
        Args:
            message (str): Formatted log message
        """
        if self.gui_logger:
            try:
                # The GUI logger will add its own timestamp
                # Extract just the level and message part
                parts = message.split("] ", 2)
                if len(parts) >= 3:
                    # Remove the timestamp part
                    message = parts[2]
                
                self.gui_logger.append_message(message)
            except Exception as e:
                print(f"Error writing to GUI logger: {e}", file=sys.stderr)
    
    def start_progress(self, message: str = "Starting operation...", queue_messages: bool = True) -> None:
        """
        Start a progress operation in the GUI logger
        
        Args:
            message (str, optional): Initial progress message. Defaults to "Starting operation...".
            queue_messages (bool, optional): Whether to queue messages during progress. Defaults to True.
        """
        if self.gui_logger:
            try:
                self.gui_logger.set_loading_on(queue_messages=queue_messages, inline_update=True)
                self.info(message)
            except Exception as e:
                print(f"Error starting progress in GUI logger: {e}", file=sys.stderr)
    
    def update_progress(self, current: int, total: int, message: Optional[str] = None) -> None:
        """
        Update progress in the GUI logger
        
        Args:
            current (int): Current progress value
            total (int): Total progress value
            message (Optional[str], optional): Progress message. Defaults to None.
        """
        if self.gui_logger:
            try:
                self.gui_logger.update_progress(current, total, message)
            except Exception as e:
                print(f"Error updating progress in GUI logger: {e}", file=sys.stderr)
    
    def end_progress(self, message: str = "Operation completed") -> None:
        """
        End a progress operation in the GUI logger
        
        Args:
            message (str, optional): Completion message. Defaults to "Operation completed".
        """
        if self.gui_logger:
            try:
                self.gui_logger.set_loading_off(completion_message=message)
            except Exception as e:
                print(f"Error ending progress in GUI logger: {e}", file=sys.stderr)
    
    def clear(self) -> None:
        """Clear the GUI logger"""
        if self.gui_logger:
            try:
                self.gui_logger.clear()
            except Exception as e:
                print(f"Error clearing GUI logger: {e}", file=sys.stderr) 