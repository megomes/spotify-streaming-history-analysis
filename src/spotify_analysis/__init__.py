"""
Spotify Analysis Sleep Apnea Project

A comprehensive data science project analyzing Spotify streaming history 
with focus on sleep-related listening patterns.

This package provides tools for:
- Loading and processing Spotify streaming data
- Analyzing temporal patterns and sleep-related behaviors
- Creating interactive visualizations
- Generating insights about music listening habits
"""

__version__ = "1.0.0"
__author__ = "Spotify Analysis Team"
__email__ = "your-email@example.com"

from .core import *
from .utils import *
from .visualization import *

__all__ = [
    # Core functionality
    "load_spotify_data",
    "transform_data", 
    "analyze_patterns",
    
    # Utilities
    "validate_data",
    "export_results",
    
    # Visualization
    "create_dashboard",
    "generate_charts"
] 