# Quick Start: OSM Data Collection

This guide will help you quickly get started with collecting OpenStreetMap data for Brazil.

## Prerequisites

1. **Python Environment**: Ensure your virtual environment is activated

    ```bash
    # Windows
    .\venv\Scripts\activate

    # Linux/Mac
    source venv/bin/activate
    ```

2. **Install Dependencies**: Update your packages

    ```bash
    pip install -r requirements.txt
    ```

## Step-by-Step Guide

### Step 1: Download OSM Data

Download the Brazil OSM extract from Geofabrik:

```bash
python src/osm/collect_osm_data.py --source geofabrik
```

**What happens:**

- Downloads `brazil-latest.osm.pbf` (~1-2 GB)
- Saves to `data/raw/osm/raw/`
- Shows progress bar during download
- Prompts before re-downloading if file exists

**Expected output:**

```text
INFO - Starting Brazil OSM download from geofabrik...
INFO - Downloading from: https://download.geofabrik.de/south-america/brazil-latest.osm.pbf
Downloading Brazil OSM: 100%|██████████| 1.5GB/1.5GB [05:23<00:00, 4.6MB/s]
INFO - Download complete: data/raw/osm/raw/brazil-latest.osm.pbf
INFO - File size: 1.45 GB
```

### Step 2: Install OSM Processing Tools

For feature extraction, you'll need the `osmium` library:

```bash
pip install osmium
```

**Note:** If you encounter issues installing osmium on Windows, you may need:

- Visual C++ Build Tools
- Or use a pre-built wheel from <https://www.lfd.uci.edu/~gohlke/pythonlibs/>

### Step 3: Extract Geometries

Run the extraction scripts to convert the raw PBF into GeoJSON files:

```bash
# Extract road segments
python src/osm/extract_roads.py

# Extract points of interest
python src/osm/extract_pois.py
```

### Step 4: Calculate Analytical Metrics

Generate the vulnerability/infrastructure predictors per municipality:

```bash
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

**What it does:**

- Scans `road_network.geojson` for junctions and road lengths.
- Performs a spatial join with IBGE municipality polygons.
- Outputs `road_predictors_muni_final.csv`.

---

## File Structure After Processing

```text
iguide_project/
├── data/
│   ├── raw/
│   │   ├── osm/
│   │   │   ├── raw/
│   │   │   │   └── brazil-latest.osm.pbf    # Raw PBF
│   │   │   ├── pois/
│   │   │   │   └── commercial_pois.geojson # Extracted POIs
│   │   │   └── roads/
│   │   │       └── road_network.geojson    # Extracted Roads
│   ├── processed/
│   │   └── road_predictors_muni_final.csv  # Final Infrastructure Metrics
```

## Troubleshooting

### Memory Errors during Metrics Calculation

Processing 6.4 million roads requires a lot of RAM. The script is optimized for **8GB RAM** by using a two-pass scan. If you still have issues:

1. Close all other programs (including VS Code if necessary).
2. Run with a smaller chunk size: `--chunk-size 50000`.

### osmium installation fails

...

## Command Reference

```bash
# Download OSM data
python src/osm/collect_osm_data.py --source geofabrik

# Download only (skip extraction)
python src/osm/collect_osm_data.py --download-only

# Use existing download (skip re-downloading)
python src/osm/collect_osm_data.py --skip-download

# Specify custom output directory
python src/osm/collect_osm_data.py --output-dir custom/path

# Get help
python src/osm/collect_osm_data.py --help
```

## Need Help?

- Check the detailed [README.md](README.md) in this directory
- Review the [OSM Wiki](https://wiki.openstreetmap.org/)
- Check [Geofabrik documentation](https://download.geofabrik.de/)
