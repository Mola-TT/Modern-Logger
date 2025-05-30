from setuptools import setup, find_packages

setup(
    name="modern-logger",
    version="1.0.0",
    description="A flexible logging system with file, console, and GUI (PySide6) output options",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mola",
    author_email="mola@molamola.me",
    url="https://github.com/Mola-TT/Modern-Logger",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.4",
    ],
    extras_require={
        "gui": ["PySide6>=6.0.0"],
        "dev": ["PySide6>=6.0.0"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    keywords="logging, console, file, gui, qt, pyside6, modern",
    project_urls={
        "Homepage": "https://github.com/Mola-TT/Modern-Logger",
        "Repository": "https://github.com/Mola-TT/Modern-Logger",
        "Issues": "https://github.com/Mola-TT/Modern-Logger/issues",
    },
) 