# iGuide Project - Brazilian Successful Areas

## Overview

This project collects and analyzes geospatial data for Brazilian municipalities to identify successful areas using:

- **Satellite imagery** from Google Earth Engine (Spectral Indices & Building Embeddings)
- **OpenStreetMap (OSM)** data for infrastructure (Road Density, Intersections)
- **Economic Data** (Business Status, IBGE Demographic Metrics)

The data is unified into a master analytical dataset aligned with IBGE 2022 municipality boundaries.

**Current Status**:

- Data Collection ✅ Complete
- Data Treatment & Integration ✅ Complete

---

## Project Structure

```text
iguide_project/
├── 📂 src/                    # Source code
│   ├── satellite/             # Satellite data (Google Earth Engine)
│   ├── osm/                   # OpenStreetMap data (Download & Extraction)
│   ├── ibge/                  # IBGE data collection
│   ├── treatment/             # Data cleaning, spatial joins & integration
│   └── utils/                 # Shared utilities
├── 📂 data/                   # Data storage
│   ├── raw/                   # Raw source files (PBFs, CSVs, Shapefiles)
│   └── processed/             # Final analytical datasets
├── 📂 config/                 # Configuration files
├── 📂 docs/                   # Documentation
└── 📂 logs/                   # Log files
```

---

## Features

### Satellite Data

- **Spectral Features**: Extract band reflectance (RGB, NIR, SWIR) and indices (NDVI, EVI, NDBI) via Sentinel-2.
- **Building Embeddings**: 64-dimensional embeddings from Google Open Buildings dataset.

### OSM Data

- **Road Network Analysis**: Ultra-memory-efficient calculation of road density and intersection counts.
- **POI Extraction**: Comprehensive collection of commercial and social points of interest.
- **8GB RAM Optimized**: Custom "Endpoint-First" scan for processing large spatial networks on limited hardware.

### Data Integration

- **Master Unified Dataset**: Robust join logic using IBGE CD_MUN codes with name/UF fallback.
- **Spatial Alignment**: All indicators aggregated to IBGE 2022 municipality polygons.

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

---

## Usage Workflow

### 1. Foundation: IBGE Boundaries

Download the official IBGE municipality boundaries:

```bash
python src/ibge/collect_municipalities.py --year 2022
```

### 2. Satellite Data Collection

```bash
python src/satellite/extract_embeddings.py
```

### 3. OSM Data Processing

Download and extract all OSM data for Brazil:

```bash
python src/osm/collect_osm_data.py
```

Calculate road metrics (Density, Intersections, Highway Proximity):

```bash
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

_Note: Optimized for 8GB RAM machines._

### 4. Final Data Integration

Unify all sources (Satellite, Roads, Business, IBGE) into the final master dataset:

```bash
python src/treatment/integrate_final_dataset.py
```

---

## Output

### Final Integrated Dataset

Location: `data/processed/final_integrated_dataset.csv`

The final table includes over 5,500 municipalities with:

- **Geometry**: Municipality boundaries (from IBGE 2022)
- **Infrastructure**: Road density ($km/km^2$), intersection counts, highway presence.
- **Economic**: Active firm counts, branches, head offices (from Business Data).
- **Satellite**: Red/Blue/Green reflectance, NDVI, EVI (from Sentinel-2).
- **Demographic**: GDP per capita, HDI, Resident Population, etc.

### Metadata

- **Total Rows**: 5,572 (Brazilian municipalities)
- **Coordinate Reference System**: EPSG:4674 (SIRGAS 2000)

---

## Documentation

Additional documentation is available in the `docs/` folder:

- `memory_optimization.md` - Strategies for running the pipeline on 8GB RAM.
- `quickstart.md` - End-to-end execution guide.
- `src/treatment/README.md` - Details on the integration and calculation logic.

---

## Troubleshooting

### Memory Errors on Roads

If `calculate_road_metrics.py` fails with memory errors, reduce the `--chunk-size` or ensure no other Python processes are running.

---

## Contact

- Jaiany Rocha - <jaiany.trindade@ufrgs.br>
- Devika Jain - <kakkar@fas.harvard.edu>
- Vinicius Brei - <brei@ufrgs.br>
