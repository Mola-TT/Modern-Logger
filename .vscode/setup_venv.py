import os
import sys
import subprocess
import platform
import time

def is_venv_setup(venv_path='.venv'):
    """Check if virtual environment exists and is set up correctly"""
    venv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), venv_path)
    
    if not os.path.isdir(venv_path):
        return False
    
    # Check for activation script which indicates a proper venv
    if platform.system() == 'Windows':
        activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
    
    return os.path.isfile(activate_script)

def setup_venv(venv_path='.venv'):
    """Set up a virtual environment"""
    venv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), venv_path)
    
    print(f"Setting up virtual environment in '{venv_path}'...")
    
    # Create the virtual environment
    try:
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment. Is the venv module installed?")
        print("Try: pip install virtualenv")
        return False
    
    print("Virtual environment created successfully.")
    
    # Get the path to the pip binary in the virtual environment
    if platform.system() == 'Windows':
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
    else:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
    
    # Install requirements
    requirements = ['PySide6']
    print(f"Installing required packages: {', '.join(requirements)}")
    
    try:
        subprocess.run([pip_path, 'install'] + requirements, check=True)
        print("Packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        return False

def main():
    """Check for virtual environment and set up if needed"""
    if not is_venv_setup():
        print("Virtual environment not found or incomplete.")
        setup_venv()
        # Small delay to let VS Code detect the new environment
        time.sleep(1)
    else:
        print("Virtual environment already set up.")

if __name__ == "__main__":
    main()
