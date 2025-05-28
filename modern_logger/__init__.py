"""
Modern Logger - A flexible logging system with file, console, and GUI output options.

This package provides multiple logging options:
- Console logging with colored output
- File logging with rotation support
- GUI logging with a modern interface and progress indicators
- Multi-destination logging to any combination of outputs
- Log export in multiple formats (log, csv, xml, json)

Examples:
    # Basic console-only logger (default)
    logger = ModernLogger()
    logger.info("Console logging enabled by default")

    # Logger with custom file output
    logger = ModernLogger(file="path/to/logfile.log")
    logger.info("Logging to file")

    # Logger with GUI
    logger = ModernLogger(gui=True)
    widget = logger.get_gui_widget()  # Get widget for embedding in your app
    logger.info("GUI logging enabled")

    # Full logger with all outputs
    logger = ModernLogger(console=True, file="logs/app.log", gui=True)
    logger.info("Logging to all outputs")
    
    # Export logs in different formats
    logger.export_log("logs/export.json", "json")
    logger.export_log("logs/errors.csv", "csv", level_filter=Logger.ERROR)
"""

from typing import Optional

# Import core logger components (always available)
from .logger import Logger, FileLogger, ConsoleLogger, MultiLogger

__version__ = "1.0.0"

# Lazy import functions for GUI components
def _import_gui_components():
    """Lazy import of GUI components to avoid PySide6 dependency when not needed"""
    try:
        from .gui_logger import ModernLogger as GUIModernLogger
        from .gui_adapter import GUILogger
        return GUIModernLogger, GUILogger
    except ImportError as e:
        raise ImportError(
            f"GUI components require PySide6. Please install it with: pip install PySide6\n"
            f"Original error: {e}"
        )

class ModernLogger:
    def __init__(self, console=True, file=False, gui=False):
        """
        Initialize ModernLogger with specified outputs.
        
        Args:
            console (bool): Enable console output. Defaults to True.
            file (Union[bool, str]): Enable file output. If string, use as file path. Defaults to False.
            gui (bool): Enable GUI output. Defaults to False.
        """
        self.loggers = []
        self.multi_logger = MultiLogger()
        
        if console:
            self.loggers.append(ConsoleLogger())
            
        if file:
            filepath = "logs/app.log" if file is True else file
            self.loggers.append(FileLogger(filename=filepath))
            
        if gui:
            # Lazy import GUI components only when needed
            GUIModernLogger, GUILogger = _import_gui_components()
            self.gui_logger = GUIModernLogger()
            self.loggers.append(GUILogger(gui_logger=self.gui_logger))
            
        for logger in self.loggers:
            self.multi_logger.add_logger(logger)
    
    def debug(self, message):
        """Log debug message"""
        self.multi_logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self.multi_logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self.multi_logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.multi_logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.multi_logger.critical(message)
    
    def exception(self, message="Exception occurred"):
        """Log exception with traceback"""
        self.multi_logger.exception(message)
    
    def get_gui_widget(self):
        """Get the GUI widget if GUI logging is enabled"""
        # Import GUILogger class for isinstance check only when needed
        try:
            from .gui_adapter import GUILogger
            for logger in self.loggers:
                if isinstance(logger, GUILogger):
                    return logger.gui_logger
        except ImportError:
            pass
        return None
    
    def close(self):
        """Close all loggers and clean up resources"""
        if hasattr(self, 'multi_logger') and self.multi_logger:
            self.multi_logger.close()
    
    def export_log(self, filepath: str, format_type: str = "log", level_filter: Optional[int] = None, limit: Optional[int] = None) -> bool:
        """
        Export log records to file in specified format
        
        Args:
            filepath (str): Output file path
            format_type (str): Export format ('log', 'csv', 'xml', 'json')
            level_filter (Optional[int]): Minimum level to include (use Logger.DEBUG, Logger.INFO, etc.)
            limit (Optional[int]): Maximum number of records to export
            
        Returns:
            bool: True if export successful, False otherwise
            
        Examples:
            # Export all logs as JSON
            logger.export_log("logs/export.json", "json")
            
            # Export only ERROR and CRITICAL logs as CSV
            logger.export_log("logs/errors.csv", "csv", level_filter=Logger.ERROR)
            
            # Export last 100 logs as XML
            logger.export_log("logs/recent.xml", "xml", limit=100)
        """
        return self.multi_logger.export_log(filepath, format_type, level_filter, limit)
    
    def get_records(self, level_filter: Optional[int] = None, limit: Optional[int] = None):
        """
        Get stored log records with optional filtering
        
        Args:
            level_filter (Optional[int]): Minimum level to include
            limit (Optional[int]): Maximum number of records to return
            
        Returns:
            List: Filtered log records
        """
        return self.multi_logger.get_records(level_filter, limit)
    
    def clear_records(self):
        """Clear all stored log records"""
        self.multi_logger.clear_records()
    
    def set_max_records(self, max_records: int):
        """
        Set maximum number of records to keep in memory for export
        
        Args:
            max_records (int): Maximum number of records to keep
        """
        self.multi_logger.set_max_records(max_records)

# Function to get GUI components (for advanced users who want direct access)
def get_gui_components():
    """
    Get GUI components for advanced usage.
    
    Returns:
        tuple: (GUIModernLogger, GUILogger) classes
        
    Raises:
        ImportError: If PySide6 is not available
    """
    return _import_gui_components()

__all__ = [
    # Core loggers (always available)
    'Logger',
    'FileLogger',
    'ConsoleLogger',
    'MultiLogger',
    'ModernLogger',
    
    # Utility functions
    'get_gui_components',
] 