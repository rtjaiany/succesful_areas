# Quick Start Guide

## Initial Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd iguide_project
```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
GEE_PROJECT_ID=your-gee-project-id
GDRIVE_FOLDER_ID=your-google-drive-folder-id  # Optional
BATCH_SIZE=50
MAX_WORKERS=2
```

### 5. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

Follow the browser prompts to complete authentication.

---

## Running Data Collection

### 1. Extract Satellite Data

```bash
python src/satellite/extract_embeddings.py
```

This will:

1. Connect to Google Earth Engine
2. Load Brazilian municipality boundaries
3. Extract satellite features for each municipality
4. Save results to `data/processed/municipality_embeddings_YYYYMMDD_HHMMSS.csv`

### 2. Collect OSM Data

```bash
python src/osm/collect_osm_data.py
```

This will:

1. Download Brazil OSM PBF file
2. Extract road networks
3. Extract points of interest (POIs)
4. Save results to `data/processed/`

---

## Project Structure

```
iguide_project/
├── src/
│   ├── satellite/              # Satellite data extraction
│   │   └── extract_embeddings.py
│   ├── osm/                    # OSM data extraction
│   │   ├── collect_osm_data.py
│   │   ├── extract_pois.py
│   │   └── extract_roads.py
│   └── utils/                  # Shared utilities
├── data/
│   ├── raw/                    # Raw downloaded data
│   └── processed/              # Processed outputs
├── config/                     # Configuration files
├── docs/                       # Documentation
└── logs/                       # Log files
```

---

## Common Issues

### GEE Authentication Fails

If authentication fails, try:

```bash
earthengine authenticate --force
```

### Missing Dependencies

If you encounter import errors:

```bash
pip install -r requirements.txt --upgrade
```

### Memory Issues

If you run out of memory, reduce batch size in `.env`:

```env
BATCH_SIZE=25
MAX_WORKERS=1
```

### OSM Processing Issues

Check the log files in `logs/`:

- `osm_collection.log`
- `poi_extraction.log`
- `road_extraction.log`

---

## Output Files

### Satellite Data

Location: `data/processed/municipality_embeddings_*.csv`

Columns:

- `municipality_id` - Unique identifier
- `municipality_name` - Municipality name
- `state` - State code
- `embedding_0` to `embedding_63` - Satellite features
- `extraction_date` - When data was extracted

### OSM Data

Location: `data/processed/`

Files:

- `brazil_roads_*.geojson` - Road network
- `brazil_pois_*.geojson` - Points of interest

---

## Additional Documentation

- `README.md` - Main project documentation
- `docs/gee_api_reference.md` - Google Earth Engine reference
- `docs/memory_optimization.md` - Memory optimization tips
- `docs/gee_quota_optimization.md` - GEE quota management
- `src/osm/README.md` - OSM data collection guide

---

## Quick Commands Reference

```bash
# Activate environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run satellite extraction
python src/satellite/extract_embeddings.py

# Run OSM collection
python src/osm/collect_osm_data.py

# Extract only roads
python src/osm/extract_roads.py <path_to_pbf>

# Extract only POIs
python src/osm/extract_pois.py <path_to_pbf>
```

---

**Ready to start collecting data!** 🚀
