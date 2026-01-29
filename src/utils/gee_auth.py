"""
Google Earth Engine Authentication Utilities

Handles authentication for Google Earth Engine API.
"""

import ee
import os
from loguru import logger


def authenticate_gee(project_id: str = None):
    """
    Authenticate and initialize Google Earth Engine.

    Args:
        project_id: GEE project ID
    """
    try:
        # Try to initialize with existing credentials
        if project_id:
            ee.Initialize(project=project_id)
        else:
            ee.Initialize()

        logger.info("Google Earth Engine initialized successfully")

    except Exception as e:
        logger.warning(f"Failed to initialize with existing credentials: {e}")
        logger.info("Attempting to authenticate...")

        try:
            # Authenticate
            ee.Authenticate()

            # Initialize after authentication
            if project_id:
                ee.Initialize(project=project_id)
            else:
                ee.Initialize()

            logger.success("Google Earth Engine authenticated and initialized")

        except Exception as auth_error:
            logger.error(f"Authentication failed: {auth_error}")
            raise


def check_gee_connection():
    """
    Check if GEE connection is working.

    Returns:
        bool: True if connection is successful
    """
    try:
        # Simple test - get image count from a known collection
        image_count = ee.ImageCollection("COPERNICUS/S2").size().getInfo()
        logger.info(
            f"GEE connection test successful. Sample collection size: {image_count}"
        )
        return True
    except Exception as e:
        logger.error(f"GEE connection test failed: {e}")
        return False
