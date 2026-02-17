# Data Treatment and Integration

This module is responsible for cleaning, standardizing, and merging data from different sources into a unified dataset for analysis.

## Objectives

1.  **Standardization**: Ensure all municipality identifiers are consistent across sources (IBGE codes).
2.  **Cleaning**: Handle missing values and outliers in satellite and economic data.
3.  **Integration**: Join data from:
    - **Satellite**: Sentinel-2 spectral indices and Open Buildings embeddings.
    - **OSM**: Road density and POI counts.
    - **IBGE**: Municipality boundaries and demographic data.
    - **Receita Federal**: Economic and firm-level data (to be included).
4.  **Validation**: Verify spatial consistency and data integrity.

## Workflow

1.  Place raw data in `data/raw/`.
2.  Run source-specific treatment scripts (e.g., `treat_ibge.py`, `treat_satellite.py`).
3.  Run the master integration script to generate the final analytical dataset in `data/processed/`.

## Progress

- [x] Initial module structure.
- [ ] IBGE boundary treatment.
- [ ] Satellite data cleaning.
- [ ] Receita Federal integration.
- [ ] OSM feature aggregation.
