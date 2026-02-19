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
│   │   └── extract_embeddings.py
│   ├── osm/                   # OpenStreetMap data
│   │   ├── collect_osm_data.py
│   │   ├── extract_pois.py
│   │   └── extract_roads.py
│   ├── ibge/                  # IBGE data collection
│   │   └── collect_municipalities.py
│   ├── treatment/             # Data cleaning and integration
│   │   ├── calculate_road_metrics.py
│   │   ├── integrate_final_dataset.py
│   │   └── preprocess_cities.py
│   └── utils/                 # Shared utilities
├── 📂 data/                   # Data storage
│   ├── raw/                   # Raw datasets (Shapes, Business, etc.)
│   └── processed/             # Final analytical datasets
├── 📂 config/                 # Configuration files
├── 📂 docs/                   # Documentation
└── 📂 logs/                   # Log files
```

---

## Features

### Satellite Data

- **Spectral Indices**: Extract NDVI, EVI, NDBI for all Brazilian municipalities.
- **Building Embeddings**: 64-dimensional embeddings from Google Open Buildings.
- **Automated Workflow**: Python/GEE integration for large-scale extraction.

### OSM Data

- **Road Network Analysis**: Optimized extraction of density and intersections.
- **8GB RAM Optimized**: Custom "Endpoint-First" scan for processing Brazil-scale networks.
- **Point of Interest (POI)**: Extraction of commercial and social infrastructure.

### Data Treatment

- **Unified Integration**: Robust join logic (CD_MUN + Name/UF) to merge all sources.
- **Socioeconomic Preprocessing**: Standardization of diverse municipality-level metrics.

---

## Prerequisites

- Python 3.8+
- Google Earth Engine account
- **osmium** library (for OSM processing)

---

## Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd iguide_project
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Alternative: Setup with Conda

```bash
conda env create -f environment.yml
conda activate iguide
```

### 3. Configure

Copy `.env.example` to `.env` and configure your GEE Project ID.

---

## Usage Workflow

The project is designed as a sequential pipeline:

### Step 1: Boundaries (IBGE)

```bash
python src/ibge/collect_municipalities.py --year 2022
```

### Step 2: Collection (Satellite & OSM)

```bash
# Satellite indices
python src/satellite/extract_embeddings.py

# OSM Data
python src/osm/collect_osm_data.py
```

### Step 3: Infrastructure Calculation

```bash
# Memory-optimized road metrics
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

### Step 4: Final Integration

```bash
# Unifies all data into one master CSV
python src/treatment/integrate_final_dataset.py
```

---

## Output

### Final Integrated Dataset

Location: `data/processed/final_integrated_dataset.csv`
Contains: Unified indicators for all 5,500+ Brazilian municipalities (Roads, Indices, Business metrics).

---

## Contact

- Jaiany Rocha - <jaiany.trindade@ufrgs.br>
- Devika Jain - <kakkar@fas.harvard.edu>
- Vinicius Brei - <brei@ufrgs.br>
