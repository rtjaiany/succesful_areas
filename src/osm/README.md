# Economic Data Collection

This module handles collection of economic indicators from various sources to complement satellite data analysis.

## Phase 3: OpenStreetMap (OSM) Data Acquisition

### Goal

Extract economic indicators from OpenStreetMap data to complement satellite-based analysis.

### 3.1 Collection & Aggregation (Current Phase)

#### Data Source

- **Primary**: Geofabrik OSM extracts for Brazil
- **Alternative**: Overpass API (for smaller queries)
- **Update Frequency**: Daily extracts available

#### Economic Indicators

1. **Commercial Density**
    - Banks and ATMs
    - Shops (supermarkets, malls, retail)
    - Marketplaces
    - Offices (companies, financial institutions)

2. **Infrastructure**
    - Road network (highways, primary, secondary roads)
    - Road density per municipality
    - Total road length per municipality

## Usage

### Step 1: Download OSM Data for Brazil

```bash
# Download Brazil OSM data from Geofabrik (~1-2 GB)
python src/1_collection/economic/collect_osm_data.py --source geofabrik

# Download only (skip extraction)
python src/1_collection/economic/collect_osm_data.py --download-only

# Use existing download
python src/1_collection/economic/collect_osm_data.py --skip-download
```

### Step 2: Extract Features (Requires Additional Setup)

The feature extraction step requires the `osmium` library:

```bash
# Install osmium
pip install osmium

# Run extraction
python src/1_collection/economic/collect_osm_data.py --skip-download
```

## Output Structure

```text
data/raw/economic/osm/
├── raw/
│   └── brazil-latest.osm.pbf          # Raw OSM data (~1-2 GB)
├── pois/
│   └── commercial_pois.geojson        # Extracted POIs (future)
└── roads/
    └── road_network.geojson           # Extracted roads (future)
```

## Data Processing Pipeline

### Phase 3.1: Collection (Current)

1. ✅ Download Brazil OSM data from Geofabrik
2. ✅ Extract commercial POIs (banks, shops, amenities)
3. ✅ Extract road network (highways, roads)
4. ✅ Save as GeoJSON/GeoPackage

### Phase 3.2: Aggregation (Next)

1. Load municipality boundaries (IBGE)
2. Perform Point-in-Polygon operations
3. Calculate commercial density per municipality
4. Calculate road length and density per municipality
5. Export aggregated statistics to CSV

## Dependencies

### Required

- `requests` - HTTP downloads
- `geopandas` - Geospatial data processing
- `pandas` - Data manipulation
- `tqdm` - Progress bars
- `shapely` - Geometric operations

### Optional (for extraction)

- `osmium` - OSM PBF file parsing
- Alternative: `ogr2ogr` (GDAL command-line tool)

## Data Sources

### Geofabrik

- **URL**: <https://download.geofabrik.de/south-america/brazil.html>
- **Format**: PBF (Protocol Buffer Format)
- **Size**: ~1-2 GB compressed
- **Update**: Daily
- **License**: ODbL (Open Database License)

### Overpass API

- **URL**: <https://overpass-api.de/>
- **Use Case**: Smaller, targeted queries
- **Limitation**: Not suitable for entire Brazil download

## OSM Tag Reference

### Commercial Tags

```python
COMMERCIAL_TAGS = {
    'amenity': ['bank', 'atm', 'bureau_de_change', 'marketplace'],
    'shop': ['supermarket', 'convenience', 'department_store', 'mall', ...],
    'office': ['company', 'government', 'insurance', 'financial']
}
```

### Infrastructure Tags

```python
INFRASTRUCTURE_TAGS = {
    'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', ...]
}
```

## Next Steps

1. **Install osmium**: `pip install osmium`
2. **Implement OSM parsing**: Create osmium handlers for POI and road extraction
3. **Download municipality boundaries**: Get IBGE municipality shapefiles
4. **Implement aggregation**: Point-in-Polygon operations for statistics
5. **Create unified output**: CSV with municipality-level economic indicators

## Troubleshooting

### Download Issues

- **Slow download**: Geofabrik servers may be slow. Be patient or try later.
- **Connection timeout**: Increase timeout or check internet connection.
- **Disk space**: Ensure at least 5 GB free space (2 GB download + processing).

### Extraction Issues

- **osmium not found**: Install with `pip install osmium`
- **Memory errors**: OSM data is large. Consider processing by state/region.
- **Missing features**: Verify OSM tags match expected categories.

## References

- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
- [Geofabrik Downloads](https://download.geofabrik.de/)
- [OSM Tag Reference](https://wiki.openstreetmap.org/wiki/Map_features)
- [Osmium Documentation](https://osmcode.org/pyosmium/)
