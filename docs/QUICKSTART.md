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

## Running the Pipeline

### 1. Foundation: IBGE Boundaries

```bash
python src/ibge/collect_municipalities.py --year 2022
```

### 2. Physical Evidence: Satellite Data

```bash
python src/satellite/extract_embeddings.py
```

Extracts spectral indices from Sentinel-2 for all municipalities.

### 3. Infrastructure: OSM Data

```bash
# A. Download
python src/osm/collect_osm_data.py

# B. Extract Geometries
python src/osm/extract_roads.py
python src/osm/extract_pois.py

# C. Calculate Metrics (8GB RAM Optimized)
python src/treatment/calculate_road_metrics.py --chunk-size 150000
```

### 4. Convergence: Final Integration

```bash
python src/treatment/integrate_final_dataset.py
```

Unifies Roads, Business, Satellite, and IBGE data into one master CSV.

---

## Project Structure

```text
iguide_project/
├── src/
│   ├── satellite/       # GEE extraction scripts
│   ├── osm/             # PBF processing & geometry extraction
│   ├── ibge/            # Boundary collection
│   ├── treatment/       # Road metrics & final integration
│   └── utils/           # Shared helpers
├── data/
│   ├── raw/             # Raw GeoJSONs, PBFs, and CSVs
│   └── processed/       # Final Unified Dataset & Metrics
```

## Output Files

### Final Master Dataset

Location: `data/processed/final_integrated_dataset.csv`
Contains: Road density, intersection counts, spectral indices (NDVI/EVI), and business status for 5,572 municipalities.

---

## Quick Commands Reference

```bash
# Run everything (simplified workflow)
python src/ibge/collect_municipalities.py
python src/satellite/extract_embeddings.py
python src/osm/collect_osm_data.py
python src/osm/extract_roads.py
python src/treatment/calculate_road_metrics.py
python src/treatment/integrate_final_dataset.py
```

---

**Ready to start collecting data!** 🚀
