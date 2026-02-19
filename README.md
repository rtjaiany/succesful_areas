# iGuide Project - Brazilian Successful Areas

## Overview

This project collects and analyzes geospatial data for Brazilian municipalities to identify successful areas using:

- **Satellite imagery** from Google Earth Engine
- **OpenStreetMap (OSM)** data for infrastructure and points of interest

The data collected can be used for environmental analysis, urban planning, and machine learning applications.

**Current Status**: Data Collection ✅ Complete

---

## Project Structure

```
iguide_project/
├── 📂 src/                    # Source code
│   ├── satellite/             # Satellite data (Google Earth Engine)
│   │   ├── extract_embeddings.py
│   │   └── __init__.py
│   ├── osm/                   # OpenStreetMap data
│   │   ├── collect_osm_data.py
│   │   ├── extract_pois.py
│   │   ├── extract_roads.py
│   │   └── __init__.py
│   ├── ibge/                  # IBGE data collection
│   │   ├── collect_municipalities.py
│   │   └── __init__.py
│   └── utils/                 # Shared utilities
├── 📂 data/                   # Data storage
│   ├── raw/                   # Raw data
│   └── processed/             # Processed data
├── 📂 config/                 # Configuration files
├── 📂 docs/                   # Documentation
└── 📂 logs/                   # Log files
```

---

## Features

### Satellite Data

- **Satellite Data Extraction**: Compute mean 64-dimensional embeddings from Google Satellite Embedding V1
- **Municipality Coverage**: Process all Brazilian municipalities
- **Automated Pipeline**: Python/GEE integration for seamless data extraction
- **Cloud Storage**: Direct output to Google Drive

### OSM Data

- **Road Network Extraction**: Extract road infrastructure from OpenStreetMap
- **POI Extraction**: Collect points of interest (amenities, shops, services)
- **Infrastructure Mapping**: Analyze commercial density and urban features
- **PBF Processing**: Efficient processing of large OSM PBF files

---

## Prerequisites

- Python 3.8+
- Google Earth Engine account (for satellite data)
- Google Cloud Project (for GEE authentication)
- Google Drive access (optional, for cloud storage)
- **osmium** library (for OSM data processing)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd iguide_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

- Google Earth Engine project ID
- Google Drive folder ID (optional)
- Other necessary credentials

### 5. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

---

## Usage

### 1. IBGE Municipality Boundaries

Before extracting satellite or OSM data, download the official IBGE municipality boundaries:

```bash
python src/ibge/collect_municipalities.py --year 2022
```

### 2. Satellite Data Collection

Extract satellite embeddings for Brazilian municipalities:

```bash
python src/satellite/extract_embeddings.py
```

**What it does:**

1. Connect to Google Earth Engine
2. Load Brazilian municipality boundaries
3. Compute mean 64-dimensional embeddings for each municipality
4. Export results to CSV (and optionally Google Drive)

**Features:**

- Memory-efficient processing
- Batch processing support
- Progress tracking
- Error handling and retry logic

### 3. OSM Data Collection

#### Collect OSM Data (Roads + POIs)

```bash
# Download and extract all OSM data for Brazil
python src/osm/collect_osm_data.py

# This will:
# 1. Download Brazil OSM PBF file
# 2. Extract road networks
# 3. Extract points of interest (POIs)
# 4. Save results to data/processed/
```

#### Extract Only Roads

```bash
python src/osm/extract_roads.py <path_to_pbf_file>
```

#### Extract Only POIs

```bash
python src/osm/extract_pois.py <path_to_pbf_file>
```

**For detailed OSM extraction guides, see:**

- `src/osm/README.md` - Overview
- `src/osm/QUICKSTART.md` - Quick start guide
- `src/osm/road_extraction_summary.md` - Road extraction details
- `src/osm/poi_extraction_guide.md` - POI extraction details

---

## Configuration

Configuration files are located in the `config/` directory:

- `gee_config.yaml`: Google Earth Engine settings

---

## Output

### Satellite Data Output

The output structure depends on the extraction mode used:

#### 1. Local Streaming (Sentinel-2 Features)

This mode extracts spectral bands and vegetation indices. CSV file structure:

| Column            | Description                                  |
| ----------------- | -------------------------------------------- |
| municipality_id   | Unique code for the municipality             |
| municipality_name | Name of the municipality                     |
| state_name        | Full name of the state                       |
| state_code        | Numeric state code                           |
| blue, green, red  | Spectral bands (B2, B3, B4)                  |
| nir, swir_1, etc. | Near-infrared and Short-wave infrared bands  |
| ndvi, evi, savi   | Vegetation and soil indices                  |
| ndwi, mndwi       | Water indices                                |
| ndbi, urban_index | Built-up area indices                        |
| image_count       | Number of scenes used for the composite      |
| extraction_date   | Date and time of extraction                  |
| data_source       | Data source and year (e.g., Sentinel-2 2023) |

#### 2. Server-side Export (Building Embeddings)

This mode (using `--mode server-side`) exports the 64-dimensional embeddings from the Google Open Buildings dataset.

| Column                      | Description                               |
| --------------------------- | ----------------------------------------- |
| municipality_id             | Unique identifier for the municipality    |
| municipality_name           | Name of the municipality                  |
| embedding_0 to embedding_63 | 64-dimensional satellite embedding values |
| extraction_date             | Date of data extraction                   |
| data_source                 | Google Satellite Embedding V1             |

### OSM Data Output

- **Roads**: GeoJSON/CSV with road network features
- **POIs**: GeoJSON/CSV with points of interest

---

## Documentation

Additional documentation is available in the `docs/` folder:

- `gee_api_reference.md` - Google Earth Engine API reference
- `gee_quota_optimization.md` - Tips for optimizing GEE quota usage
- `memory_optimization.md` - Memory optimization strategies
- `quickstart.md` - Quick start guide
- `satellite_data_update.md` - Satellite data update procedures

---

## Troubleshooting

### GEE Authentication Issues

If you encounter authentication errors:

```bash
earthengine authenticate --force
```

### Memory Errors

For large-scale processing, adjust batch size in `config/gee_config.yaml`

### OSM Processing Issues

Check the log files in the `logs/` directory:

- `osm_collection.log`
- `poi_extraction.log`
- `road_extraction.log`

---

## Acknowledgments (Review in the end)

- Google Earth Engine for satellite data access

---

## Contact

- Jaiany Rocha - jaiany.trindade@ufrgs.br
- Devika Jain
- Vinicius Brei - brei@ufrgs.br
