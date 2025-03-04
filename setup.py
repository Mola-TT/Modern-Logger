from setuptools import setup, find_packages

setup(
    name="modern-logger",
    version="1.0.0",
    description="A flexible logging system with file, console, and GUI output options",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/modern-logger",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.4",
        "PySide6>=6.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
) 