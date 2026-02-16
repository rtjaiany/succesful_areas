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

### Step 1: Download OSM Data (~5-10 minutes)

Download the Brazil OSM extract from Geofabrik:

```bash
python src/1_collection/economic/collect_osm_data.py --source geofabrik
```

**What happens:**

- Downloads `brazil-latest.osm.pbf` (~1-2 GB)
- Saves to `data/raw/economic/osm/raw/`
- Shows progress bar during download
- Prompts before re-downloading if file exists

**Expected output:**

```text
INFO - Starting Brazil OSM download from geofabrik...
INFO - Downloading from: https://download.geofabrik.de/south-america/brazil-latest.osm.pbf
Downloading Brazil OSM: 100%|██████████| 1.5GB/1.5GB [05:23<00:00, 4.6MB/s]
INFO - Download complete: data/raw/economic/osm/raw/brazil-latest.osm.pbf
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

### Step 3: Extract Features (Coming Soon)

Once osmium is installed, run extraction:

```bash
python src/1_collection/economic/collect_osm_data.py --skip-download
```

**Note:** Feature extraction is currently under development. The script will:

- Parse the PBF file
- Extract commercial POIs (banks, shops, offices)
- Extract road networks
- Save as GeoJSON files

## Troubleshooting

### Download is slow

- Geofabrik servers can be slow during peak hours
- Try downloading during off-peak times
- Download typically takes 5-10 minutes on a good connection

### Not enough disk space

- Ensure at least 5 GB free space
- Raw PBF: ~1.5 GB
- Extracted features: ~1-2 GB
- Processing temp files: ~1-2 GB

### osmium installation fails

**Windows:**

```bash
# Option 1: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Option 2: Use pre-built wheel
pip install osmium --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/
```

**Linux:**

```bash
# Install system dependencies first
sudo apt-get install libboost-python-dev libexpat1-dev zlib1g-dev libbz2-dev
pip install osmium
```

## What's Next?

After collecting OSM data, the next phase is aggregation:

1. **Download municipality boundaries** from IBGE
2. **Perform spatial joins** (Point-in-Polygon)
3. **Calculate statistics** per municipality:
    - Commercial density (POIs per km²)
    - Road density (km of roads per km²)
    - Infrastructure scores
4. **Export to CSV** for integration with satellite data

## File Structure After Collection

```text
iguide_project/
├── data/
│   └── raw/
│       └── economic/
│           └── osm/
│               ├── raw/
│               │   └── brazil-latest.osm.pbf    # Downloaded OSM data
│               ├── pois/                         # (Future) Extracted POIs
│               └── roads/                        # (Future) Extracted roads
└── src/
    └── 1_collection/
        └── economic/
            ├── collect_osm_data.py              # Main collection script
            └── README.md                         # Detailed documentation
```

## Command Reference

```bash
# Download OSM data
python src/1_collection/economic/collect_osm_data.py --source geofabrik

# Download only (skip extraction)
python src/1_collection/economic/collect_osm_data.py --download-only

# Use existing download (skip re-downloading)
python src/1_collection/economic/collect_osm_data.py --skip-download

# Specify custom output directory
python src/1_collection/economic/collect_osm_data.py --output-dir custom/path

# Get help
python src/1_collection/economic/collect_osm_data.py --help
```

## Need Help?

- Check the detailed [README.md](README.md) in this directory
- Review the [OSM Wiki](https://wiki.openstreetmap.org/)
- Check [Geofabrik documentation](https://download.geofabrik.de/)
