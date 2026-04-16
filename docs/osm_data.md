# OpenStreetMap (OSM) Data Pipeline

This document details the extraction and processing of infrastructure and Points of Interest (POI) from OpenStreetMap.

## 1. Data Collection

The project uses Geofabrik as the primary source for Brazilian OSM data (`.osm.pbf`).

### Commands

```bash
# Download fresh Brazil data
python src/osm/collect_osm_data.py --source geofabrik

# Use existing download only
python src/osm/collect_osm_data.py --skip-download
```

## 2. Infrastructure Extraction

The `extract_roads.py` script parses the PBF file and calculates metrics for the road network.

### Extracted Road Types
- **Highways**: motorway, trunk, primary, secondary, tertiary.
- **Service/Access**: unclassified, residential, service, living_street.

### Attributes Captured
- Road type, name, and reference (e.g., "BR-101").
- Surface, lanes, and max speed.
- **Calculated Length**: Accurate metric measurement in Kilometers (projected).

## 3. POI Extraction

The `extract_pois.py` script captures commercial and social infrastructure points.

### Categories
- **Economy**: banks, ATMs, shops, marketplaces.
- **Services**: hospitals, schools, pharmacies, restaurants.

## 4. Technical Implementation

The extraction process is built using the `osmium` C++ backend for Python, which allows for memory-efficient streaming of massive PBF files.

### Key Features
- **Projected Geometry**: All lengths and areas are calculated after projecting to a metric CRS (SIRGAS 2000).
- **Format Support**: Exports to GeoJSON, GeoPackage, or Shapefile.
- **Diagnostics**: Generates a `*_stats.json` file for every extraction run.

## 5. Municipality Aggregation

Final metrics (e.g., Road Density $km/km^2$) are aggregated to the municipality level in the **Treatment** phase using `src/treatment/calculate_road_metrics.py`.
