"""
Base logger components for Modern Logger.

This module provides the core logging functionality including:
- Base Logger class with export capabilities
- File Logger for logging to files with rotation
- Console Logger for logging to the console with color support
- Multi Logger for logging to multiple destinations
"""

import os
import sys
import time
import logging
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional, Union, TextIO, Dict, Any
import traceback
import inspect
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init()


class LogRecord:
    """Class to store individual log records for export functionality"""
    
    def __init__(self, timestamp: datetime, level: int, level_name: str, message: str, logger_name: str = ""):
        self.timestamp = timestamp
        self.level = level
        self.level_name = level_name
        self.message = message
        self.logger_name = logger_name
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert log record to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level,
            'level_name': self.level_name,
            'message': self.message,
            'logger_name': self.logger_name
        }


class Logger:
    """Base logger class that all other loggers inherit from"""
    
    # Log levels
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    
    # Level names mapping
    LEVEL_NAMES = {
        DEBUG: "DEBUG",
        INFO: "INFO",
        WARNING: "WARNING",
        ERROR: "ERROR",
        CRITICAL: "CRITICAL"
    }
    
    def __init__(self, name: str = "ModernLogger", level: int = INFO):
        """
        Initialize the logger
        
        Args:
            name (str, optional): Logger name. Defaults to "ModernLogger".
            level (int, optional): Minimum log level to record. Defaults to INFO.
        """
        self.name = name
        self.level = level
        self._timestamp_format = "%Y-%m-%d %H:%M:%S"
        self._records: List[LogRecord] = []  # Store log records for export
        self._max_records = 10000  # Maximum records to keep in memory
    
    def set_level(self, level: int) -> None:
        """
        Set the minimum log level
        
        Args:
            level (int): Minimum log level to record
        """
        self.level = level
    
    def set_timestamp_format(self, format_str: str) -> None:
        """
        Set the timestamp format string
        
        Args:
            format_str (str): Format string for datetime.strftime()
        """
        self._timestamp_format = format_str
    
    def set_max_records(self, max_records: int) -> None:
        """
        Set maximum number of records to keep in memory for export
        
        Args:
            max_records (int): Maximum number of records to keep
        """
        self._max_records = max_records
        # Trim records if current count exceeds new limit
        if len(self._records) > max_records:
            self._records = self._records[-max_records:]
    
    def _format_message(self, level: int, message: str) -> str:
        """
        Format a log message with timestamp and level
        
        Args:
            level (int): Log level
            message (str): Log message
            
        Returns:
            str: Formatted log message
        """
        timestamp = datetime.now().strftime(self._timestamp_format)
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        return f"[{timestamp}] [{level_name}] {message}"
    
    def _log(self, level: int, message: str) -> None:
        """
        Log a message if level is sufficient
        
        Args:
            level (int): Log level
            message (str): Log message
        """
        if level >= self.level:
            timestamp = datetime.now()
            level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
            
            # Store record for export functionality
            record = LogRecord(timestamp, level, level_name, message, self.name)
            self._records.append(record)
            
            # Limit memory usage by keeping only recent records
            if len(self._records) > self._max_records:
                self._records.pop(0)
            
            formatted = self._format_message(level, message)
            self._write(formatted)
    
    def _write(self, message: str) -> None:
        """
        Write a message to the log destination
        
        Args:
            message (str): Formatted log message
        """
        # Base implementation does nothing
        # Subclasses should override this
        pass
    
    def get_records(self, level_filter: Optional[int] = None, limit: Optional[int] = None) -> List[LogRecord]:
        """
        Get stored log records with optional filtering
        
        Args:
            level_filter (Optional[int]): Minimum level to include
            limit (Optional[int]): Maximum number of records to return
            
        Returns:
            List[LogRecord]: Filtered log records
        """
        records = self._records
        
        if level_filter is not None:
            records = [r for r in records if r.level >= level_filter]
        
        if limit is not None:
            records = records[-limit:]
        
        return records
    
    def clear_records(self) -> None:
        """Clear all stored log records"""
        self._records.clear()
    
    def export_log(self, filepath: str, format_type: str = "log", level_filter: Optional[int] = None, limit: Optional[int] = None) -> bool:
        """
        Export log records to file in specified format
        
        Args:
            filepath (str): Output file path
            format_type (str): Export format ('log', 'csv', 'xml', 'json')
            level_filter (Optional[int]): Minimum level to include
            limit (Optional[int]): Maximum number of records to export
            
        Returns:
            bool: True if export successful, False otherwise
        """
        format_type = format_type.lower()
        
        if format_type not in ['log', 'csv', 'xml', 'json']:
            raise ValueError(f"Unsupported format: {format_type}. Supported formats: log, csv, xml, json")
        
        records = self.get_records(level_filter, limit)
        if not records:
            return False
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            
            if format_type == 'log':
                return self._export_log_format(filepath, records)
            elif format_type == 'csv':
                return self._export_csv_format(filepath, records)
            elif format_type == 'xml':
                return self._export_xml_format(filepath, records)
            elif format_type == 'json':
                return self._export_json_format(filepath, records)
        except Exception as e:
            print(f"Error exporting logs: {e}", file=sys.stderr)
            return False
        
        return False
    
    def _export_log_format(self, filepath: str, records: List[LogRecord]) -> bool:
        """Export records in standard log format"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for record in records:
                    timestamp_str = record.timestamp.strftime(self._timestamp_format)
                    # Calculate padding for alignment
                    padding = " " * (8 - len(record.level_name))
                    f.write(f"[{timestamp_str}] [{record.level_name}]{padding} {record.message}\n")
            return True
        except Exception:
            return False
    
    def _export_csv_format(self, filepath: str, records: List[LogRecord]) -> bool:
        """Export records in CSV format"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(['Timestamp', 'Level', 'Level_Name', 'Logger_Name', 'Message'])
                # Write records
                for record in records:
                    writer.writerow([
                        record.timestamp.isoformat(),
                        record.level,
                        record.level_name,
                        record.logger_name,
                        record.message
                    ])
            return True
        except Exception:
            return False
    
    def _export_xml_format(self, filepath: str, records: List[LogRecord]) -> bool:
        """Export records in XML format"""
        try:
            root = ET.Element("logs")
            root.set("exported_at", datetime.now().isoformat())
            root.set("total_records", str(len(records)))
            
            for record in records:
                log_elem = ET.SubElement(root, "log")
                
                timestamp_elem = ET.SubElement(log_elem, "timestamp")
                timestamp_elem.text = record.timestamp.isoformat()
                
                level_elem = ET.SubElement(log_elem, "level")
                level_elem.text = str(record.level)
                
                level_name_elem = ET.SubElement(log_elem, "level_name")
                level_name_elem.text = record.level_name
                
                logger_elem = ET.SubElement(log_elem, "logger_name")
                logger_elem.text = record.logger_name
                
                message_elem = ET.SubElement(log_elem, "message")
                message_elem.text = record.message
            
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return True
        except Exception:
            return False
    
    def _export_json_format(self, filepath: str, records: List[LogRecord]) -> bool:
        """Export records in JSON format"""
        try:
            export_data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_records": len(records),
                    "logger_name": self.name
                },
                "logs": [record.to_dict() for record in records]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def debug(self, message: str) -> None:
        """
        Log a debug message
        
        Args:
            message (str): Debug message
        """
        self._log(self.DEBUG, message)
    
    def info(self, message: str) -> None:
        """
        Log an info message
        
        Args:
            message (str): Info message
        """
        self._log(self.INFO, message)
    
    def warning(self, message: str) -> None:
        """
        Log a warning message
        
        Args:
            message (str): Warning message
        """
        self._log(self.WARNING, message)
    
    def error(self, message: str) -> None:
        """
        Log an error message
        
        Args:
            message (str): Error message
        """
        self._log(self.ERROR, message)
    
    def critical(self, message: str) -> None:
        """
        Log a critical message
        
        Args:
            message (str): Critical message
        """
        self._log(self.CRITICAL, message)
    
    def exception(self, message: str = "Exception occurred") -> None:
        """
        Log an exception with traceback
        
        Args:
            message (str, optional): Message to log with the exception. Defaults to "Exception occurred".
        """
        exc_info = traceback.format_exc()
        self._log(self.ERROR, f"{message}\n{exc_info}")


class FileLogger(Logger):
    """Logger that writes to a file with optional rotation"""
    
    def __init__(self, 
                 name: str = "FileLogger", 
                 level: int = Logger.INFO,
                 filename: str = "log.txt",
                 mode: str = "a",
                 encoding: str = "utf-8",
                 max_size: int = 0,
                 backup_count: int = 0):
        """
        Initialize a file logger
        
        Args:
            name (str, optional): Logger name. Defaults to "FileLogger".
            level (int, optional): Minimum log level. Defaults to Logger.INFO.
            filename (str, optional): Log file path. Defaults to "log.txt".
            mode (str, optional): File open mode. Defaults to "a" (append).
            encoding (str, optional): File encoding. Defaults to "utf-8".
            max_size (int, optional): Maximum file size in bytes before rotation. Defaults to 0 (no rotation).
            backup_count (int, optional): Number of backup files to keep. Defaults to 0.
        """
        super().__init__(name, level)
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.max_size = max_size
        self.backup_count = backup_count
        self._file = None
        self._open_file()
    
    def _open_file(self) -> None:
        """Open the log file"""
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(self.filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # Open the file
            self._file = open(self.filename, self.mode, encoding=self.encoding)
        except Exception as e:
            print(f"Error opening log file: {e}", file=sys.stderr)
            self._file = None
    
    def _format_message(self, level: int, message: str) -> str:
        """
        Format a log message with timestamp, level, and padding for alignment
        
        Args:
            level (int): Log level
            message (str): Log message
            
        Returns:
            str: Formatted log message
        """
        timestamp = datetime.now().strftime(self._timestamp_format)
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        
        # Calculate padding needed after the bracket (CRITICAL is 8 chars)
        padding = " " * (8 - len(level_name))
        
        return f"[{timestamp}] [{level_name}]{padding} {message}"
    
    def _rotate_if_needed(self) -> None:
        """Rotate the log file if it exceeds max_size"""
        if not self.max_size or not self._file:
            return
            
        try:
            # Check current file size
            self._file.flush()
            size = os.path.getsize(self.filename)
            
            if size >= self.max_size:
                # Close current file
                self._file.close()
                self._file = None
                
                # Rotate backup files
                for i in range(self.backup_count - 1, 0, -1):
                    src = f"{self.filename}.{i}"
                    dst = f"{self.filename}.{i+1}"
                    if os.path.exists(src):
                        if os.path.exists(dst):
                            os.remove(dst)
                        os.rename(src, dst)
                
                # Rename current file
                if self.backup_count > 0:
                    if os.path.exists(f"{self.filename}.1"):
                        os.remove(f"{self.filename}.1")
                    os.rename(self.filename, f"{self.filename}.1")
                
                # Open new file
                self._open_file()
        except Exception as e:
            print(f"Error rotating log file: {e}", file=sys.stderr)
            # Try to reopen the file
            if not self._file:
                self._open_file()
    
    def _write(self, message: str) -> None:
        """
        Write a message to the log file
        
        Args:
            message (str): Formatted log message
        """
        if not self._file:
            self._open_file()
            
        if self._file:
            try:
                self._file.write(message + "\n")
                self._file.flush()
                self._rotate_if_needed()
            except Exception as e:
                print(f"Error writing to log file: {e}", file=sys.stderr)
    
    def close(self) -> None:
        """Close the log file"""
        if self._file:
            try:
                self._file.close()
            except Exception:
                pass
            self._file = None
    
    def __del__(self) -> None:
        """Ensure file is closed when object is deleted"""
        self.close()


class ConsoleLogger(Logger):
    """Logger that writes to the console with color support"""
    
    # Default colors for different log levels
    DEFAULT_COLORS = {
        Logger.DEBUG: Fore.CYAN,
        Logger.INFO: Fore.GREEN,
        Logger.WARNING: Fore.YELLOW,
        Logger.ERROR: Fore.RED,
        Logger.CRITICAL: Fore.RED + Style.BRIGHT
    }
    
    def __init__(self, 
                 name: str = "ConsoleLogger", 
                 level: int = Logger.INFO,
                 use_colors: bool = True,
                 stream: TextIO = sys.stdout,
                 colors: Optional[Dict[int, str]] = None):
        """
        Initialize a console logger
        
        Args:
            name (str, optional): Logger name. Defaults to "ConsoleLogger".
            level (int, optional): Minimum log level. Defaults to Logger.INFO.
            use_colors (bool, optional): Whether to use colors. Defaults to True.
            stream (TextIO, optional): Output stream. Defaults to sys.stdout.
            colors (Optional[Dict[int, str]], optional): Custom colors for log levels. Defaults to None.
        """
        super().__init__(name, level)
        self.use_colors = use_colors
        self.stream = stream
        self.colors = colors or self.DEFAULT_COLORS.copy()
    
    def _format_message(self, level: int, message: str) -> str:
        """
        Format a log message with timestamp, level, and optional color
        
        Args:
            level (int): Log level
            message (str): Log message
            
        Returns:
            str: Formatted log message
        """
        timestamp = datetime.now().strftime(self._timestamp_format)
        level_name = self.LEVEL_NAMES.get(level, "UNKNOWN")
        
        # Calculate padding needed after the bracket (CRITICAL is 8 chars)
        padding = " " * (8 - len(level_name))
        
        if self.use_colors and level in self.colors:
            color = self.colors[level]
            reset = Style.RESET_ALL
            return f"[{timestamp}] [{color}{level_name}{reset}]{padding} {message}"
        else:
            return f"[{timestamp}] [{level_name}]{padding} {message}"
    
    def _write(self, message: str) -> None:
        """
        Write a message to the console
        
        Args:
            message (str): Formatted log message
        """
        print(message, file=self.stream)
    
    def set_color(self, level: int, color: str) -> None:
        """
        Set the color for a specific log level
        
        Args:
            level (int): Log level
            color (str): ANSI color code (from colorama)
        """
        self.colors[level] = color


class MultiLogger(Logger):
    """Logger that writes to multiple destinations"""
    
    def __init__(self, 
                 name: str = "MultiLogger", 
                 level: int = Logger.INFO,
                 loggers: Optional[List[Logger]] = None):
        """
        Initialize a multi-destination logger
        
        Args:
            name (str, optional): Logger name. Defaults to "MultiLogger".
            level (int, optional): Minimum log level. Defaults to Logger.INFO.
            loggers (Optional[List[Logger]], optional): List of loggers to write to. Defaults to None.
        """
        super().__init__(name, level)
        self.loggers = loggers or []
    
    def add_logger(self, logger: Logger) -> None:
        """
        Add a logger to the multi-logger
        
        Args:
            logger (Logger): Logger to add
        """
        if logger not in self.loggers:
            self.loggers.append(logger)
    
    def remove_logger(self, logger: Logger) -> None:
        """
        Remove a logger from the multi-logger
        
        Args:
            logger (Logger): Logger to remove
        """
        if logger in self.loggers:
            self.loggers.remove(logger)
    
    def _write(self, message: str) -> None:
        """
        Write a message to all loggers
        
        Args:
            message (str): Formatted log message
        """
        for logger in self.loggers:
            # Use the original message format for each logger
            level_start = message.find("[", message.find("]") + 1) + 1
            level_end = message.find("]", level_start)
            level_name = message[level_start:level_end]
            level = next((k for k, v in self.LEVEL_NAMES.items() if v == level_name), self.INFO)
            
            # Extract the raw message without timestamp and level
            raw_message = message[level_end + 2:]
            
            # Log with the appropriate level
            if level >= logger.level:
                logger._log(level, raw_message)
    
    def close(self) -> None:
        """Close all loggers that support closing"""
        for logger in self.loggers:
            if hasattr(logger, 'close') and callable(logger.close):
                logger.close() 