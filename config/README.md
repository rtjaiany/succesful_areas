# Configuration Reference

This directory contains YAML configuration files for external APIs and data processing parameters.

## Files

- **`gee_config.yaml`**: Configuration for Google Earth Engine (GEE) extractions.
    - `scale`: Spatial resolution for reduction (default: 100m).
    - `max_pixels`: Maximum pixels allowed in a single reduction operation.

- **`.env.example`**: Template for environment variables. Copy this out to the root directory as `.env` and fill it in.

## Environment Variables

The project requires a `.env` file at the root containing:
- `GEE_PROJECT_ID`: Your Google Earth Engine project identifier.
- `GDRIVE_FOLDER_ID`: (Optional) Folder ID for server-side exports.
