#!/usr/bin/env python3
"""
Console Colors Example - ModernLogger

This example demonstrates how to customize console colors
for different log levels.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from modern_logger import ConsoleLogger, Logger
from colorama import Fore, Back, Style

def main():
    print("🎨 Console Colors Example")
    print("=" * 30)
    
    # Create a console logger with default colors
    print("\n📺 Default Colors:")
    default_logger = ConsoleLogger()
    default_logger.debug("Debug message (cyan)")
    default_logger.info("Info message (green)")
    default_logger.warning("Warning message (yellow)")
    default_logger.error("Error message (red)")
    default_logger.critical("Critical message (bright red)")
    
    # Create a console logger with custom colors
    print("\n🎯 Custom Colors:")
    custom_logger = ConsoleLogger()
    
    # Customize colors for each log level
    custom_logger.set_color(Logger.DEBUG, Fore.MAGENTA)
    custom_logger.set_color(Logger.INFO, Fore.BLUE + Style.BRIGHT)
    custom_logger.set_color(Logger.WARNING, Fore.YELLOW + Back.BLACK)
    custom_logger.set_color(Logger.ERROR, Fore.WHITE + Back.RED)
    custom_logger.set_color(Logger.CRITICAL, Fore.RED + Back.YELLOW + Style.BRIGHT)
    
    custom_logger.debug("Debug message (magenta)")
    custom_logger.info("Info message (bright blue)")
    custom_logger.warning("Warning message (yellow on black)")
    custom_logger.error("Error message (white on red)")
    custom_logger.critical("Critical message (bright red on yellow)")
    
    # Disable colors
    print("\n⚫ No Colors:")
    no_color_logger = ConsoleLogger(use_colors=False)
    no_color_logger.info("Info message without colors")
    no_color_logger.error("Error message without colors")
    
    print("\n✅ Console colors example completed!")

if __name__ == "__main__":
    main() 