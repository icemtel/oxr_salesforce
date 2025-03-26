import sys
import os

# Append the parent directory to the Python path - to make sure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))