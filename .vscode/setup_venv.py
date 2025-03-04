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
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    venv_path = os.path.join(workspace_root, venv_path)
    
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
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        pip_path = os.path.join(venv_path, 'bin', 'pip')
        python_path = os.path.join(venv_path, 'bin', 'python')
    
    # Upgrade pip
    try:
        subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
        print("Pip upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upgrade pip: {e}")
    
    # Install the package in development mode
    print("Installing the package in development mode...")
    try:
        subprocess.run([pip_path, 'install', '-e', workspace_root], check=True)
        print("Package installed successfully in development mode.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install package: {e}")
        
        # Fallback to manual installation of dependencies
        print("Attempting to install dependencies directly...")
        requirements = ['colorama>=0.4.4', 'PySide6>=6.0.0']
        try:
            subprocess.run([pip_path, 'install'] + requirements, check=True)
            print("Dependencies installed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
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
