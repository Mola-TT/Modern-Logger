#!/usr/bin/env python3
"""
Installation script for Modern Logger.

This script helps users install the Modern Logger package and its dependencies.
"""

import os
import sys
import subprocess
import argparse
import platform


def check_python_version():
    """Check if the Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current Python version: {platform.python_version()}")
        return False
    return True


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return False


def install_dependencies(gui=True):
    """Install the required dependencies"""
    # Install base dependencies
    if not run_command("pip install colorama", "Installing colorama"):
        return False
    
    # Install GUI dependencies if requested
    if gui:
        if not run_command("pip install PySide6", "Installing PySide6"):
            print("Warning: Failed to install PySide6. GUI features will not be available.")
            print("You can try installing it manually with: pip install PySide6")
    
    return True


def install_package(dev_mode=False):
    """Install the Modern Logger package"""
    if dev_mode:
        return run_command("pip install -e .", "Installing Modern Logger in development mode")
    else:
        return run_command("pip install .", "Installing Modern Logger")


def run_tests():
    """Run the example scripts to test the installation"""
    print("\nRunning basic usage example...")
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Run the basic usage example
        subprocess.run([sys.executable, "examples/basic_usage.py"], check=True)
        print("Basic usage example completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Install Modern Logger")
    parser.add_argument("--no-gui", action="store_true", help="Skip installing GUI dependencies")
    parser.add_argument("--dev", action="store_true", help="Install in development mode")
    parser.add_argument("--no-test", action="store_true", help="Skip running tests")
    args = parser.parse_args()
    
    print("Modern Logger Installation Script")
    print("================================")
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies(gui=not args.no_gui):
        print("Warning: Some dependencies could not be installed")
    
    # Install the package
    if not install_package(dev_mode=args.dev):
        print("Error: Failed to install Modern Logger")
        return 1
    
    # Run tests if requested
    if not args.no_test:
        if not run_tests():
            print("Warning: Tests failed")
    
    print("\nInstallation completed successfully!")
    print("\nYou can now use Modern Logger in your projects:")
    print("  - Import the package: from modern_logger import Logger, FileLogger, ConsoleLogger")
    print("  - Run the examples: python examples/basic_usage.py")
    if not args.no_gui:
        print("  - Run the GUI example: python examples/gui_example.py")
    print("  - Run the CLI example: python examples/cli_example.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 