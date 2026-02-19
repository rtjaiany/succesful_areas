# 🛰️ Satellite Data Collection

This module leverages **Google Earth Engine (GEE)** to extract high-resolution environmental and structural features for all Brazilian municipalities. We combine traditional spectral analysis with modern deep learning embeddings.

## Data Sources

1.  **Sentinel-2 (L2A)**:
    - ✅ **Freely available** 10m-30m resolution imagery.
    - ✅ **Spectral Vigor**: Excellent for vegetation, water, and soil analysis.
    - ✅ **Temporal Coverage**: 2015-present.
2.  **Google Open Buildings Embeddings (V1)**:
    - ✅ **Structural Insights**: 64-dimensional embeddings representing building patterns and urban density.
    - ✅ **Deep Learning Based**: Derived from models trained on the Open Buildings dataset.

---

## Features Extracted

We extract a comprehensive set of features for each municipality:

### 🌈 Spectral Bands (Sentinel-2)

- **Blue (B2), Green (B3), Red (B4)**: Visible spectrum.
- **Red Edge 1-3 (B5-B7)**: Critical for vegetation health monitoring.
- **NIR (B8) & NIR Narrow (B8A)**: Vegetation biomass and stress.
- **SWIR 1-2 (B11-B12)**: Moisture content and soil discrimination.

### 🌿 Vegetation Indices

- **NDVI**: Standard vegetation health index.
- **EVI**: Enhanced index, less sensitive to atmospheric noise.
- **SAVI**: Soil-Adjusted index for areas with sparse vegetation.

### 🏙️ Built-Up & Water Indices

- **NDBI**: Highlights urban and built-up land.
- **Urban Index (UI)**: Differentiates structural density.
- **NDWI / MNDWI**: Water body detection and moisture mapping.

### 🏢 Structural Embeddings (Google Open Buildings)

- **Embedding 0-63**: 64 latent features capturing the "visual signature" of urban structures, density, and building types.

---

## How It Works

### 1. Spectral Extraction (Local Streaming)

- **Timeframe**: Uses 2023 median composites (auto-fallback to 2022).
- **Quality**: Filters for <20% cloud cover.
- **Memory Optimization**: Uses a streaming approach to write records directly to CSV, allowing the process to run on low-RAM (8GB) systems.

### 2. Embedding Extraction (Server-side)

- **Large-scale**: Since embeddings are heavy, the script supports GEE's server-side export to Google Drive.
- **Consistency**: Uses the same municipality boundaries (GAUL level 2 or IBGE 2022).

---

## Configuration & Usage

### Setup

Ensure your `.env` has:

```bash
GEE_PROJECT_ID=your-project-id
GDRIVE_FOLDER_ID=your-drive-folder-id (optional)
```

### Running the Script

```bash
# Extract spectral indices locally (saves to data/processed/)
python src/satellite/extract_embeddings.py --mode streaming

# Export structural embeddings to Google Drive
python src/satellite/extract_embeddings.py --mode server-side
```

---

## Output Format

The final processed CSVs are saved in `data/processed/` with the following structure:

```csv
municipality_id, municipality_name, state_name, state_code,
blue, green, red, ..., ndvi, evi, ..., nbdwi,
image_count, extraction_date, data_source
```

---

## Why This Multi-Source Approach?

| Feature              | Spectral Indices (Sentinel-2)      | Building Embeddings                  |
| :------------------- | :--------------------------------- | :----------------------------------- |
| **Interpretability** | ✅ High (We know what NDVI means)  | ⚠️ Low (Model-derived)               |
| **Structure**        | ⚠️ Moderate (Based on reflectance) | ✅ High (Based on shapes/density)    |
| **Scalability**      | ✅ Direct Streaming                | ✅ Server-side Export                |
| **Use Case**         | Agriculture, Environmental Change  | Urban Planning, Economic Development |

---

## Troubleshooting

- **Quota Exceeded**: The script uses `batch_size: 50` to respect GEE's free tier quotas.
- **Memory Issues**: Ensure you use `--mode streaming` for local runs.
- **Missing Municipalities**: Check logs for municipalities with 100% cloud cover or no coverage in the selected year.

---

## Scientific References

1. **Sentinel-2 Indices**: Well-established indices like NDVI (Rouse, 1974) and EVI (Huete, 2002).
2. **Open Buildings**: Sirko et al. (2021) - Continental-Scale Building Extraction.
