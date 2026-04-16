# OSM Data Collection

This module handles the extraction and processing of infrastructure and POIs from OpenStreetMap using the `osmium` backend.

## 🚀 Usage

```bash
# 1. Download Brazil Data
python src/osm/collect_osm_data.py --source geofabrik

# 2. Extract Road Geometries
python src/osm/extract_roads.py

# 3. Extract Points of Interest (POIs)
python src/osm/extract_pois.py
```

## 📚 Detailed Documentation

For a full reference on extraction logic, road types, and aggregation methods, see:
👉 **[docs/osm_data.md](../../docs/osm_data.md)**
