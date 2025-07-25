#!/usr/bin/env python3
"""
Launcher script for the Repo Manager application
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main application
from repo_manager import main

if __name__ == "__main__":
    main() 