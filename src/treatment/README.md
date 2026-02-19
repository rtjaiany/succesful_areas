# Data Treatment and Integration

This module is responsible for cleaning, standardizing, and merging data from different sources into a unified dataset for analysis.

## Objectives

1. **Standardization**: Ensure all municipality identifiers are consistent across sources (IBGE codes).
2. **Cleaning**: Handle missing values and outliers in satellite and economic data.
3. **Integration**: Join data from:
    - **Satellite**: Sentinel-2 spectral indices and Open Buildings embeddings.
    - **OSM**: Road density and POI counts.
    - **IBGE**: Municipality boundaries and demographic data.
    - **Receita Federal**: Economic and firm-level data (to be included).
4. **Validation**: Verify spatial consistency and data integrity.

## Workflow

1. Place raw data in `data/raw/`.
2. Run source-specific treatment scripts (e.g., `treat_ibge.py`, `treat_satellite.py`).
3. Run the master integration script to generate the final analytical dataset in `data/processed/`.

## Progress

- [x] Initial module structure and base utilities (`DataTreater`).
- [x] Physical infrastructure calculation (`calculate_road_metrics.py`).
- [x] External indicators integration (`preprocess_cities.py`).
- [x] Final unified dataset integration (`integrate_final_dataset.py`).
- [x] 8GB RAM optimization for national road network processing.
- [ ] Detailed IBGE demographic and socioeconomic cleaning.
- [ ] Receita Federal (Firm-level) data integration.
- [ ] Commercial/Social POI spatial aggregation.

## Key Scripts

- `calculate_road_metrics.py`: Calculates road density ($km/km^2$), intersection counts, and highway proximity. Uses a two-pass "endpoint-first" scan to process 6.4M roads using less than 1.5GB RAM.
- `preprocess_cities.py`: Standardizes and Renames multiple indicators from diverse Excel sources (Economic, Demographic) into a unified CSV.
- `integrate_final_dataset.py`: The master join script. Merges IBGE boundaries, Road Metrics, City Data, and Satellite Embeddings using robust CD_MUN codes with fallback name-matching.
- `base_treatment.py`: Core utility class for ID standardization and logging.
