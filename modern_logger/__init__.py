"""
Modern Logger - A flexible logging system with file, console, and GUI output options.

This package provides multiple logging options:
- Console logging with colored output
- File logging with rotation support
- GUI logging with a modern interface and progress indicators
- Multi-destination logging to any combination of outputs

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
"""

# Import core logger components
from .logger import Logger, FileLogger, ConsoleLogger, MultiLogger

# Import GUI components
from .gui_logger import ModernLogger as GUIModernLogger

# Import GUI adapter
from .gui_adapter import GUILogger

__version__ = "1.0.0"

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
        for logger in self.loggers:
            if isinstance(logger, GUILogger):
                return logger.gui_logger
        return None

__all__ = [
    # Core loggers
    'Logger',
    'FileLogger',
    'ConsoleLogger',
    'MultiLogger',
    
    # GUI components
    'ModernLogger',
    
    # GUI adapter
    'GUILogger'
] 