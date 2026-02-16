# Phase 1: Data Collection

## Overview

This phase focuses on collecting data from various sources to build a comprehensive dataset for Brazilian municipalities.

## Data Sources

### 1. Satellite Data (✅ Implemented)

- **Source**: Google Earth Engine - Satellite Embedding V1
- **Script**: `gee/extract_embeddings_efficient.py`
- **Output**: 64-dimensional embeddings per municipality
- **Storage**: `data/raw/satellite/`

### 2. Demographic Data (🔄 To Implement)

- **Source**: IBGE Census API
- **Planned Data**:
    - Population
    - Age distribution
    - Education levels
    - Household composition
- **Storage**: `data/raw/demographic/`

### 3. Economic Data (🔄 In Progress)

- **Source**: OpenStreetMap (OSM), IBGE, Central Bank APIs
- **Implemented**:
    - ✅ OSM data download (Geofabrik)
    - ✅ Commercial POI extraction (banks, shops, amenities) - **IMPLEMENTED**
    - 🔄 Infrastructure (road network, density) - **IMPLEMENTED**
- **Planned Data**:
    - GDP per capita
    - Employment rates
    - Income distribution
    - Economic sectors
- **Storage**: `data/raw/economic/`
- **Scripts**:
    - `economic/collect_osm_data.py` - Main collection script
    - `economic/extract_pois.py` - POI extraction

### 4. Environmental Data (🔄 To Implement)

- **Source**: INPE, Climate APIs
- **Planned Data**:
    - Temperature
    - Precipitation
    - Vegetation indices (NDVI)
    - Deforestation rates
- **Storage**: `data/raw/environmental/`

### 5. Geographic Data (🔄 To Implement)

- **Source**: IBGE Geospatial Data
- **Planned Data**:
    - Municipality boundaries
    - Coordinates (lat/lon)
    - Area
    - Region classification
- **Storage**: `data/raw/geographic/`

## Usage

### Collect Satellite Data

```bash
# Memory-efficient extraction (recommended)
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming

# Standard extraction
python src/1_collection/gee/extract_embeddings.py
```

### Collect Demographic Data (Coming Soon)

```bash
python src/1_collection/demographic/collect_census_data.py
```

### Collect Economic Data (Coming Soon)

```bash
python src/1_collection/economic/collect_gdp_data.py
```

### Collect Environmental Data (Coming Soon)

```bash
python src/1_collection/environmental/collect_climate_data.py
```

## Output Format

All collectors should output CSV files with at least:

- `municipality_id` - IBGE municipality code
- `municipality_name` - Municipality name
- `state_code` - State abbreviation
- Data-specific columns

## Next Steps

1. Implement demographic data collector
2. Implement economic data collector
3. Implement environmental data collector
4. Create unified collection script
5. Add data validation

## Dependencies

See `requirements.txt` for Python dependencies.

Additional APIs may require:

- IBGE API credentials
- Climate data API keys
- GEE authentication (already configured)
