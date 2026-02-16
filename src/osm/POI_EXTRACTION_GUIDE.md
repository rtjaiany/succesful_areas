# POI Extraction Guide

This guide explains how to extract commercial Points of Interest (POIs) from OpenStreetMap data for economic analysis.

## Prerequisites

1. **OSM Data Downloaded**: You must have the Brazil OSM PBF file

    ```bash
    python src/1_collection/economic/collect_osm_data.py --source geofabrik
    ```

2. **Install osmium**: Required for parsing OSM PBF files
    ```bash
    pip install osmium
    ```

## Quick Start

### Option 1: Standalone Extraction

Run the POI extraction script directly:

```bash
python src/1_collection/economic/extract_pois.py
```

This will:

- Read `data/raw/economic/osm/raw/brazil-latest.osm.pbf`
- Extract all commercial POIs
- Save to `data/raw/economic/osm/pois/commercial_pois.geojson`
- Generate statistics in `commercial_pois_stats.json`

### Option 2: Integrated with Main Script

Run the main collection script (will auto-extract if osmium is installed):

```bash
python src/1_collection/economic/collect_osm_data.py --skip-download
```

## Command-Line Options

```bash
# Custom input file
python src/1_collection/economic/extract_pois.py \
  --input path/to/custom.osm.pbf

# Custom output location
python src/1_collection/economic/extract_pois.py \
  --output path/to/output.geojson

# Different output format
python src/1_collection/economic/extract_pois.py \
  --format gpkg  # Options: geojson, gpkg, csv

# Complete example
python src/1_collection/economic/extract_pois.py \
  --input data/raw/economic/osm/raw/brazil-latest.osm.pbf \
  --output data/raw/economic/osm/pois/commercial_pois.geojson \
  --format geojson
```

## What Gets Extracted

### Commercial Categories

The script extracts POIs from these OSM tag categories:

#### 1. Amenities (`amenity` tag)

- **Financial**: bank, atm, bureau_de_change, marketplace
- **Food & Drink**: restaurant, cafe, fast_food, bar, pub
- **Healthcare**: pharmacy, clinic, hospital, dentist, doctors
- **Automotive**: fuel, car_wash, car_rental, parking

#### 2. Shops (`shop` tag)

- **Retail**: supermarket, convenience, department_store, mall
- **Apparel**: clothes, shoes, jewelry
- **Electronics**: electronics, mobile_phone
- **Home**: furniture, hardware
- **Food**: bakery, butcher, beverages, alcohol
- **Services**: hairdresser, beauty, optician, florist
- **Other**: books, toys, gift, pet, bicycle, sports, kiosk

#### 3. Offices (`office` tag)

- company, government, insurance, financial
- lawyer, accountant, estate_agent, travel_agent
- employment_agency, consulting

#### 4. Tourism (`tourism` tag)

- hotel, motel, hostel, guest_house
- attraction, museum, gallery

### Extracted Attributes

For each POI, the following attributes are extracted (when available):

- **Location**: latitude, longitude, geometry
- **Identification**: osm_id, osm_type (node/way)
- **Classification**: category, type
- **Details**: name, brand, operator
- **Address**: street, city, postcode
- **Contact**: phone, website
- **Hours**: opening_hours

## Output Files

### 1. GeoJSON File (default)

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-46.6333, -23.5505]
            },
            "properties": {
                "osm_id": 123456789,
                "osm_type": "node",
                "category": "amenity",
                "type": "bank",
                "name": "Banco do Brasil",
                "brand": "Banco do Brasil",
                "address": "Rua XV de Novembro",
                "city": "São Paulo"
            }
        }
    ]
}
```

### 2. Statistics File (JSON)

```json
{
    "total_nodes_processed": 45000000,
    "total_ways_processed": 8000000,
    "total_pois_extracted": 250000,
    "pois_by_category": {
        "amenity": 120000,
        "shop": 95000,
        "office": 25000,
        "tourism": 10000
    }
}
```

## Performance

### Expected Processing Time

- **File Size**: ~1.5 GB (Brazil OSM PBF)
- **Processing Time**: 10-30 minutes (depends on CPU)
- **Memory Usage**: ~2-4 GB RAM
- **Expected Output**: 200,000-500,000 POIs

### Progress Tracking

The script shows real-time progress:

```text
Extracting POIs: 45.2M nodes [15:23, 48.9k nodes/s, POIs=245,123]
```

### Optimization Tips

1. **Use SSD**: Significantly faster than HDD
2. **Close other applications**: Free up RAM
3. **Run overnight**: For large extracts
4. **Process by state**: If memory is limited

## Troubleshooting

### osmium Installation Issues

**Windows**:

```bash
# Option 1: Install Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Option 2: Use conda
conda install -c conda-forge osmium-tool

# Option 3: Use pre-built wheel
pip install osmium --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/
```

**Linux**:

```bash
# Install system dependencies
sudo apt-get install libboost-python-dev libexpat1-dev zlib1g-dev libbz2-dev

# Then install osmium
pip install osmium
```

**macOS**:

```bash
# Install dependencies via Homebrew
brew install boost-python3

# Then install osmium
pip install osmium
```

### Memory Errors

If you encounter memory errors:

1. **Close other applications**
2. **Process by region**: Extract state-by-state instead of entire Brazil
3. **Use streaming mode**: The script already uses streaming, but you can reduce buffer sizes
4. **Upgrade RAM**: 8 GB minimum recommended, 16 GB ideal

### No POIs Extracted

If no POIs are extracted:

1. **Check OSM file**: Ensure the PBF file is valid and complete
2. **Verify tags**: OSM data might use different tagging schemes
3. **Check region**: Ensure you're processing the correct geographic area
4. **Review logs**: Check `poi_extraction.log` for details

### Slow Performance

If extraction is very slow:

1. **Check disk I/O**: Use `Task Manager` (Windows) or `htop` (Linux)
2. **Verify file isn't corrupted**: Re-download if necessary
3. **Use SSD**: Much faster than HDD for large file processing
4. **Reduce logging**: Comment out debug-level logging

## Next Steps

After POI extraction:

1. **Review the data**:

    ```python
    import geopandas as gpd
    pois = gpd.read_file('data/raw/economic/osm/pois/commercial_pois.geojson')
    print(pois.head())
    print(pois['category'].value_counts())
    ```

2. **Download municipality boundaries** (IBGE shapefiles)

3. **Perform spatial aggregation** (Point-in-Polygon)

4. **Calculate commercial density** per municipality

5. **Export to CSV** for integration with satellite data

## Example Workflow

```bash
# 1. Download OSM data (if not already done)
python src/1_collection/economic/collect_osm_data.py --download-only

# 2. Install osmium
pip install osmium

# 3. Extract POIs
python src/1_collection/economic/extract_pois.py

# 4. Check results
python -c "import geopandas as gpd; pois = gpd.read_file('data/raw/economic/osm/pois/commercial_pois.geojson'); print(f'Total POIs: {len(pois):,}'); print(pois['category'].value_counts())"

# 5. Proceed to aggregation (next phase)
```

## References

- [OSM Wiki - Map Features](https://wiki.openstreetmap.org/wiki/Map_features)
- [OSM Wiki - Amenity](https://wiki.openstreetmap.org/wiki/Key:amenity)
- [OSM Wiki - Shop](https://wiki.openstreetmap.org/wiki/Key:shop)
- [OSM Wiki - Office](https://wiki.openstreetmap.org/wiki/Key:office)
- [Osmium Documentation](https://osmcode.org/pyosmium/)
