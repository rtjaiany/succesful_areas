"""
Utility functions for the iGuide project.

This module provides common utilities including:
- Google Earth Engine authentication
- Logging configuration
- Memory management utilities
"""

from .gee_auth import authenticate_gee, check_gee_connection
from .logger_config import setup_logger

__all__ = [
    "authenticate_gee",
    "check_gee_connection",
    "setup_logger",
]
