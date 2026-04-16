"""
Setup script for iGuide Project

This script helps set up the project environment.
"""

import os
import sys
import subprocess
from pathlib import Path
from loguru import logger


def create_virtual_environment():
    """Create Python virtual environment."""
    logger.info("Creating virtual environment...")

    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        logger.success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install project dependencies."""
    logger.info("Installing dependencies...")

    # Determine pip path based on OS
    if sys.platform == "win32":
        pip_path = Path("venv") / "Scripts" / "pip.exe"
    else:
        pip_path = Path("venv") / "bin" / "pip"

    if not pip_path.exists():
        logger.error("Virtual environment not found. Please create it first.")
        return False

    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        logger.success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False


def create_env_file():
    """Create .env file from template."""
    logger.info("Setting up environment variables...")

    env_example = Path("config/.env.example")
    env_file = Path(".env")

    if env_file.exists():
        logger.warning(".env file already exists. Skipping...")
        return True

    if not env_example.exists():
        logger.error("config/.env.example not found")
        return False

    try:
        with open(env_example, "r") as src, open(env_file, "w") as dst:
            dst.write(src.read())

        logger.success(".env file created. Please update it with your credentials.")
        return True
    except Exception as e:
        logger.error(f"Failed to create .env file: {e}")
        return False


def create_directories():
    """Create necessary project directories."""
    logger.info("Creating project directories...")

    directories = ["data/raw", "data/processed", "logs", "notebooks", "output"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger.success("Project directories created")
    return True


def authenticate_gee():
    """Guide user through GEE authentication."""
    logger.info("\n" + "=" * 60)
    logger.info("Google Earth Engine Authentication")
    logger.info("=" * 60)

    print("\nTo use Google Earth Engine, you need to authenticate.")
    print("Please follow these steps:")
    print("\n1. Activate your virtual environment:")

    if sys.platform == "win32":
        print("   .\\venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")

    print("\n2. Run the authentication command:")
    print("   earthengine authenticate")

    print("\n3. Follow the prompts in your browser to authenticate")

    print("\n4. Update your .env file with your GEE project ID")

    logger.info("=" * 60 + "\n")


def main():
    """Main setup function."""
    logger.info("Starting Geolocate Project setup...")
    logger.info("=" * 60)

    # Create directories
    if not create_directories():
        logger.error("Setup failed at directory creation")
        return

    # Create virtual environment
    if not Path("venv").exists():
        if not create_virtual_environment():
            logger.error("Setup failed at virtual environment creation")
            return
    else:
        logger.info("Virtual environment already exists")

    # Install dependencies
    if not install_dependencies():
        logger.error("Setup failed at dependency installation")
        return

    # Create .env file
    if not create_env_file():
        logger.error("Setup failed at .env file creation")
        return

    # Show GEE authentication instructions
    authenticate_gee()

    logger.success("\n" + "=" * 60)
    logger.success("Setup completed successfully!")
    logger.success("=" * 60)

    print("\nNext steps:")
    print("1. Activate your virtual environment")
    print("2. Authenticate with Google Earth Engine")
    print("3. Update your .env file with credentials")
    print("4. Run: python src/satellite/extract_embeddings.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
