# OSM Data Collection

**Date**: 2026-02-15

## What Was Implemented

### 1. OSM Data Download Module

Created a comprehensive Python script for downloading OpenStreetMap data for Brazil:

**File**: `src/osm/collect_osm_data.py`

**Command-Line Options**:

```bash
--source {geofabrik,overpass}  # Data source
--output-dir PATH              # Custom output directory
--download-only                # Skip extraction
--skip-download                # Use existing download
```

### 2. Documentation

Created three documentation files:

#### a. README.md

- Comprehensive guide to OSM data collection
- Economic indicators explanation
- Data sources and licensing
- OSM tag reference
- Troubleshooting guide

#### b. QUICKSTART.md

- Step-by-step quick start guide
- Prerequisites and setup
- Expected outputs
- Common issues and solutions

#### c. Module **init**.py

- Package initialization
- Export definitions

### 3. Dependencies

Updated `requirements.txt` to include:

- `osmium>=3.6.0` - For OSM PBF file parsing

### 4. Project Structure Updates

Updated `src/1_collection/README.md` to reflect:

- Economic data collection status
- OSM data download
- Commercial density extraction
- Infrastructure extraction

## File Structure Created

```text
src/osm/
├── __init__.py                 # Module initialization
├── collect_osm_data.py         # Main collection script (370 lines)
├── README.md                   # Comprehensive documentation
└── QUICKSTART.md               # Quick start guide

data/raw/osm/          # Created on first run
├── raw/                        # Raw OSM data
│   └── brazil-latest.osm.pbf  # Downloaded file (~1-2 GB)
├── pois/                       # Future: Extracted POIs
└── roads/                      # Future: Extracted roads
```

## Economic Indicators Targeted

### 1. Commercial Density

**OSM Tags**:

- `amenity`: bank, atm, bureau_de_change, marketplace
- `shop`: supermarket, convenience, department_store, mall, clothes, electronics, etc.
- `office`: company, government, insurance, financial

**Metrics** (to be calculated):

- Count of commercial POIs per municipality
- Commercial density (POIs per km²)
- Distribution by type

### 2. Infrastructure

**OSM Tags**:

- `highway`: motorway, trunk, primary, secondary, tertiary, residential, service

**Metrics** (to be calculated):

- Total road length per municipality (km)
- Road density (km per km²)
- Road network complexity

## How to Use

### Basic Usage

1. **Download OSM data**:

    ```bash
    python src/osm/collect_osm_data.py --source geofabrik
    ```

2. **Install osmium** (for future extraction):

    ```bash
    pip install osmium
    ```

3. **Run extraction** (when implemented):

    ```bash
    python src/osm/collect_osm_data.py --skip-download
    ```

## What's Next: Aggregation

### Immediate Next Steps

1. **Implement OSM Parsing**
    - Create osmium handler for POI extraction
    - Create osmium handler for road extraction
    - Filter features by relevant tags
    - Convert to GeoDataFrames

2. **Download Municipality Boundaries**
    - Get IBGE municipality shapefiles
    - Load as GeoDataFrame
    - Ensure CRS compatibility

3. **Spatial Aggregation**
    - Implement Point-in-Polygon for POIs
    - Calculate road lengths within polygons
    - Aggregate statistics per municipality

4. **Export Results**
    - Create CSV with municipality-level metrics
    - Include: municipality_id, commercial_density, road_density, etc.
    - Save to `data/processed/osm/`

### Technical Implementation Notes

**For POI Extraction**:

```python
import osmium

class POIHandler(osmium.SimpleHandler):
    def node(self, n):
        # Check if node has commercial tags
        # Extract coordinates and attributes
        # Store in list/GeoDataFrame
```

**For Road Extraction**:

```python
class RoadHandler(osmium.SimpleHandler):
    def way(self, w):
        # Check if way has highway tag
        # Extract geometry and attributes
        # Calculate length
        # Store in list/GeoDataFrame
```

## Data Sources

### Geofabrik

- **URL**: <https://download.geofabrik.de/south-america/brazil.html>
- **Format**: PBF (Protocol Buffer Format)
- **Size**: ~1-2 GB compressed
- **Update Frequency**: Daily
- **License**: ODbL (Open Database License)

### OpenStreetMap

- **License**: ODbL - Open Database License
- **Attribution**: © OpenStreetMap contributors
- **Data Quality**: Community-maintained, varies by region

## Known Limitations

1. **Feature Extraction Not Implemented**
    - POI and road extraction require osmium handlers
    - Currently shows placeholder messages
    - Planned for next development phase

2. **No Aggregation Yet**
    - Municipality-level statistics not calculated
    - Requires municipality boundaries
    - Planned for Phase 3.2

3. **Windows osmium Installation**
    - May require Visual C++ Build Tools
    - Alternative: use pre-built wheels

## Success Criteria

### Collection ✅

- [x] Download Brazil OSM data from Geofabrik
- [x] Create organized directory structure
- [x] Implement progress tracking
- [x] Add comprehensive documentation
- [x] Test script functionality

### Extraction and Aggregation 🔄

- [ ] Implement POI extraction with osmium
- [ ] Implement road network extraction
- [ ] Download IBGE municipality boundaries
- [ ] Perform spatial aggregation
- [ ] Export municipality-level CSV
- [ ] Validate data quality

## References

- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
- [Geofabrik Downloads](https://download.geofabrik.de/)
- [OSM Tag Reference](https://wiki.openstreetmap.org/wiki/Map_features)
- [Osmium Documentation](https://osmcode.org/pyosmium/)
- [ODbL License](https://opendatacommons.org/licenses/odbl/)

## Conclusion

Phase 3.1 successfully implements the data collection infrastructure for OSM economic indicators. The download mechanism is fully functional and ready to use. The next phase will focus on extracting and aggregating the features to create municipality-level economic metrics that complement the satellite data analysis.
