# Quick Start Guide

This guide provides a step-by-step workflow to reproduce the master analytical dataset for Brazilian municipalities.

## Initial Setup

### 1. Environment

```bash
git clone <repository-url>
cd iguide_project
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

Alternatively, if you prefer **Conda**:

```bash
conda env create -f environment.yml
conda activate iguide
```

### 2. Configuration

Copy `.env.example` to `.env` and set your `GEE_PROJECT_ID`.

---

## The Data Pipeline

### Step 1: Boundaries (IBGE)

Download the official 2022 municipality boundaries from IBGE:

```bash
python src/ibge/collect_municipalities.py --year 2022
```

### Step 2: Physical Data Collection

Extract satellite features and download OSM data:

```bash
# A. Satellite Spectral Indices
python src/satellite/extract_embeddings.py

# B. OpenStreetMap geometries
python src/osm/collect_osm_data.py
```

### Step 3: Infrastructure Analytics

Calculate road network metrics. This step is optimized for **8GB RAM** using an endpoint-first topology scan.

```bash
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

### Step 4: Final Integration

Unify all collected sources (OSM, GEE, IBGE, Socioeconomic) into one master CSV:

```bash
python src/treatment/integrate_final_dataset.py
```

---

## Project Structure

```text
iguide_project/
├── src/
│   ├── ibge/            # Boundary collection
│   ├── satellite/       # GEE extraction
│   ├── osm/             # PBF processing
│   ├── treatment/       # Metrics & Integration
│   └── utils/           # Shared helpers
├── data/
│   ├── raw/             # Raw source datasets
│   └── processed/       # Final Unified Dataset
```

## Output

The final goal of this pipeline is:
`data/processed/final_integrated_dataset.csv`

This file contains over 5,500 municipalities with:

- Road density ($km/km^2$)
- Intersection counts
- Spectral Indices (NDVI, EVI, NDBI)
- Socioeconomic indicators (Active firms, average salary)
