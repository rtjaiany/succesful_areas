# Phase 2: Data Integration

## Overview

This phase merges data from multiple sources into unified datasets for analysis.

## Purpose

- Combine satellite, demographic, economic, environmental, and geographic data
- Handle missing values and data inconsistencies
- Validate merged datasets
- Create analysis-ready data files

## Key Scripts

### `merge_datasets.py` (To Implement)

Merges multiple data sources by municipality ID.

**Usage:**

```bash
python src/2_integration/merge_datasets.py \
    --satellite data/raw/satellite/embeddings.csv \
    --demographic data/raw/demographic/census.csv \
    --economic data/raw/economic/gdp.csv \
    --output data/integrated/full_dataset.csv
```

### `data_validation.py` (To Implement)

Validates the integrated dataset.

**Checks:**

- No duplicate municipality IDs
- All required columns present
- Data types correct
- Value ranges valid
- No excessive missing data

### `quality_checks.py` (To Implement)

Performs data quality assurance.

**Checks:**

- Completeness
- Consistency
- Accuracy
- Timeliness

## Output

**Location**: `data/integrated/`

**Files:**

- `full_dataset.csv` - Complete merged dataset
- `validation_report.txt` - Validation results
- `quality_report.html` - Quality assessment

## Data Integration Strategy

### 1. Primary Key

- Use `municipality_id` (IBGE code) as primary key
- All datasets must have this column

### 2. Join Type

- Left join from satellite data (base)
- Preserve all municipalities with satellite data

### 3. Missing Data Handling

- Document missing data patterns
- Impute where appropriate
- Flag municipalities with excessive missing data

### 4. Data Types

- Standardize column names
- Convert data types
- Handle categorical variables

## Next Steps

1. Implement merge_datasets.py
2. Implement data_validation.py
3. Create data quality dashboard
4. Add automated testing
