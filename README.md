# iGuide Project - Brazilian Successful Areas

## Overview

This project collects and analyzes geospatial data for Brazilian municipalities to identify successful areas using:

- **Satellite imagery** from Google Earth Engine
- **OpenStreetMap (OSM)** data for infrastructure and points of interest

The data collected can be used for environmental analysis, urban planning, and machine learning applications.

**Current Status**: Data Collection ✅ Complete

---

## Project Structure

```text
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
│   ├── data_analysis/         # Exploratory Data Analysis
│   │   ├── eda.ipnyb          # Interactive Notebook
│   │   └── eda.py             # Script version of EDA
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

### Analysis & Visualization

- **Business Density**: Analysis of firm concentration (Active/Failed per km²) and HQ clustering.
- **Quality of Life Correlation**: Investigating links between green areas (NDVI), wealth, and infrastructure.
- **Regional Profiling**: Comparative radar charts for the 5 Brazilian macro-regions.

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

### Step 5: Exploratory Data Analysis

Run the EDA notebook to generate insights, visualizations, and the enhanced dataset with density metrics.

```bash
# Run via Jupyter
jupyter notebook src/data_analysis/eda.ipynb

# Or execute the script directly
python src/data_analysis/eda.py
```

---

## Output

### Final Integrated Dataset

## Location: `data/processed/final_integrated_dataset.csv`

## 📚 Detailed Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)**: Extended setup and execution instructions.
- **[Satellite Data](docs/satellite_data.md)**: Deep dive into GEE extraction, indices, and embeddings.
- **[Socioeconomic Data](docs/socioeconomic_data.md)**: Business data sources, variables, and processing.
- **[Memory Optimization](docs/MEMORY_OPTIMIZATION.md)**: How we handle 8GB+ road networks on standard RAM.
- **[GEE Quota Management](docs/gee_quota_optimization.md)**: Strategies for handling Earth Engine limits.

---

## Contact

- Jaiany Rocha - <jaiany.trindade@ufrgs.br>
- Devika Jain - <kakkar@fas.harvard.edu>
- Vinicius Brei - <brei@ufrgs.br>
