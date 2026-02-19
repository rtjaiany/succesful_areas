# Satellite Data Collection

This module handles the extraction of geospatial features and embeddings from satellite imagery using Google Earth Engine (GEE).

## Features

- **Spectral Indices**: Extraction of mean values for various spectral bands and indices across municipality geometries.
    - **Bands**: Blue, Green, Red, Red Edge (1, 2, 3), NIR, SWIR (1, 2).
    - **Vegetation Indices**: NDVI (Normalized Difference Vegetation Index), EVI (Enhanced Vegetation Index), SAVI (Soil Adjusted Vegetation Index).
    - **Water Indices**: NDWI, MNDWI.
    - **Built-up Indices**: NDBI (Normalized Difference Build-up Index), Urban Index.
- **Building Embeddings**: Extraction of 64-dimensional embeddings from the Google Open Buildings dataset (V1).

## Implementation Details

The extraction process is highly optimized for performance and memory efficiency:

1. **Streaming CSV Writes**: Results are written directly to disk in small chunks, avoiding large DataFrames in memory.
2. **Chunked Processing**: Municipalities are processed in batches with manual garbage collection (`gc.collect()`) to prevent memory leaks during long-running GEE requests.
3. **Server-Side Export**: Supports GEE's server-side export to Google Drive for massive datasets, which offloads processing to Google's infrastructure.
4. **Cloud Masking**: Automatically filters Sentinel-2 images with >20% cloud cover and creates median composites for the year.

## Configuration

The module uses `config/gee_config.yaml` for GEE-specific parameters:

- `scale`: Spatial resolution for reduction (default: 100m).
- `max_pixels`: Maximum pixels allowed in a reduction operation.

Requires a `.env` file with:

- `GEE_PROJECT_ID`: Your Google Earth Engine project identifier.
- `GDRIVE_FOLDER_ID`: (Optional) Folder ID for server-side exports.

## Usage

### 1. Extract Spectral Indices (Local Streaming)

```bash
python src/satellite/extract_embeddings.py --mode streaming
```

### 2. Export Building Embeddings (Server-side to Drive)

```bash
python src/satellite/extract_embeddings.py --mode server-side
```

### 3. Both

```bash
python src/satellite/extract_embeddings.py --mode both
```

## Output

The local extraction saves a timestamped CSV in `data/processed/`:

- `municipality_embeddings_YYYYMMDD_HHMMSS.csv`
