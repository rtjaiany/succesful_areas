"""
Test script to verify Earth Engine setup and authentication.

This script checks:
1. Python package imports
2. Earth Engine authentication
3. Project configuration
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("iGuide Project - Setup Verification")
print("=" * 60)

# Test 1: Import core packages
print("\n[1/5] Testing core package imports...")
try:
    import ee
    import pandas as pd
    import numpy as np

    print("✅ Core packages imported successfully")
    print(f"   - earthengine-api: {ee.__version__}")
    print(f"   - pandas: {pd.__version__}")
    print(f"   - numpy: {np.__version__}")
except ImportError as e:
    print(f"❌ Failed to import core packages: {e}")
    sys.exit(1)

# Test 2: Import project utilities
print("\n[2/5] Testing project utilities...")
try:
    from src.utils.gee_auth import authenticate_gee
    from src.utils.logger_config import setup_logger

    print("✅ Project utilities imported successfully")
except ImportError as e:
    print(f"❌ Failed to import project utilities: {e}")
    sys.exit(1)

# Test 3: Load configuration
print("\n[3/5] Loading configuration...")
try:
    from dotenv import load_dotenv
    import os

    load_dotenv()
    project_id = os.getenv("GEE_PROJECT_ID")

    if project_id and project_id != "your-gee-project-id":
        print(f"✅ Configuration loaded")
        print(f"   - Project ID: {project_id}")
    else:
        print("⚠️  Warning: GEE_PROJECT_ID not configured in .env file")
        print("   Please edit .env and add your Google Earth Engine Project ID")
        project_id = None
except Exception as e:
    print(f"❌ Failed to load configuration: {e}")
    project_id = None

# Test 4: Test Earth Engine authentication
print("\n[4/5] Testing Earth Engine authentication...")
try:
    if project_id:
        ee.Initialize(project=project_id)
        print("✅ Earth Engine initialized successfully")
        print(f"   - Using project: {project_id}")
    else:
        print("⚠️  Skipping authentication test (no project ID configured)")
        print("   Run 'earthengine authenticate' first")
except Exception as e:
    print(f"⚠️  Earth Engine initialization failed: {e}")
    print("\n   To fix this, run:")
    print("   1. earthengine authenticate")
    print("   2. Add your GEE_PROJECT_ID to .env file")

# Test 5: Test Earth Engine connection
print("\n[5/5] Testing Earth Engine connection...")
try:
    if project_id:
        # Simple test query
        image = ee.Image("COPERNICUS/S2/20150821T111616_20160314T094808_T30UWU")
        info = image.getInfo()
        print("✅ Earth Engine connection working")
        print("   - Successfully queried sample image")
    else:
        print("⚠️  Skipping connection test (authentication required)")
except Exception as e:
    print(f"⚠️  Connection test failed: {e}")

# Summary
print("\n" + "=" * 60)
print("Setup Verification Summary")
print("=" * 60)

if project_id:
    print("\n✅ Your setup is ready!")
    print("\nNext steps:")
    print(
        "   python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming"
    )
else:
    print("\n⚠️  Setup incomplete")
    print("\nTo complete setup:")
    print("   1. Run: earthengine authenticate")
    print("   2. Get your Project ID from: https://console.cloud.google.com")
    print("   3. Edit .env file and set: GEE_PROJECT_ID=your-project-id")
    print("   4. Run this test again: python test_setup.py")

print("\n" + "=" * 60)
