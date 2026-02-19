# OSM Data Collection

This module handles collection of infrastructure and points of interest data from OpenStreetMap to complement satellite data analysis.

## OpenStreetMap (OSM) Data Acquisition

### Goal

Extract economic indicators from OpenStreetMap data to complement satellite-based analysis.

### Features

1. **Road Network Analysis**:
    - Total road length per municipality (km).
    - Road density (km per km²).
    - Intersection counts (junctions with degree $\ge$ 3).
    - Highway proximity presence.
2. **POI Analysis**:
    - Commercial density (Banks, Shops, Offices).
    - Social infrastructure (Schools, Hospitals).

## Usage

### Step 1: Download OSM Data for Brazil

```bash
python src/osm/collect_osm_data.py --source geofabrik
```

Downloads `brazil-latest.osm.pbf` to `data/raw/osm/raw/`.

### Step 2: Extract Features

Extract raw geometries and nodes for processing:

**Extract Roads:**

```bash
python src/osm/extract_roads.py
```

**Extract POIs:**

```bash
python src/osm/extract_pois.py
```

### Step 3: Calculate Metrics

Aggregate the extracted roads into municipality-level predictors:

```bash
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

_Note: This script uses an optimized endpoint-first scan to run on 8GB RAM._

## Data Processing Pipeline

### Status

- [x] Download Brazil OSM data from Geofabrik
- [x] Extract commercial POIs
- [x] Extract road network geometry
- [x] Calculate road density and intersections per municipality
- [x] Integrate with final master dataset

## Output Structure

```text
data/raw/osm/
├── raw/
│   └── brazil-latest.osm.pbf          # Raw OSM data (~1.5 GB)
├── pois/
│   └── commercial_pois.geojson        # Extracted POI geometries
└── roads/
    └── road_network.geojson           # Extracted road geometries
```

## Dependencies

- `osmium` - High-performance OSM PBF parsing.
- `geopandas` - Spatial joins and GeoJSON manipulation.
- `fiona` - Optimized GeoJSON streaming.
- `tqdm` - Progress monitoring.

## References

- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
- [Geofabrik Downloads](https://download.geofabrik.de/)
- [pyosmium](https://osmcode.org/pyosmium/)
