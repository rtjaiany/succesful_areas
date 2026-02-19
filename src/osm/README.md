# OSM Data Collection

This module handles the extraction and processing of infrastructure and POIs from OpenStreetMap.

## Usage

### Step 1: Download

```bash
python src/osm/collect_osm_data.py --source geofabrik
```

### Step 2: Extract Geometries

```bash
# Extract Roads
python src/osm/extract_roads.py

# Extract POIs
python src/osm/extract_pois.py
```

### Step 3: Analytical Metrics

Aggregation to municipality level is handled by the treatment module:

```bash
# See docs/MEMORY_OPTIMIZATION.md for 8GB RAM tips
python src/treatment/calculate_road_metrics.py
```

## Features

- **Road Network Analysis**: Connectivity, density, and intersection counts.
- **POI Density**: Extraction of commercial and social infrastructure.
- **Optimized PBF Parsing**: High-performance extraction using `osmium`.

## Data Pipeline Status

- [x] Geofabrik Brazil download
- [x] Road geometry extraction
- [x] POI geometry extraction
- [x] Municipality-level aggregation (Roads)
- [ ] Municipality-level aggregation (POIs)

## Dependencies

- `osmium`: PBF parsing
- `geopandas`: Spatial analysis
- `fiona`, `shapely`: Geometry handling
- `tqdm`: Progress monitoring
