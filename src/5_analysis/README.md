# Phase 5: Statistical Analysis

## Overview

This phase performs statistical analysis on model results and data.

## Purpose

- Descriptive statistics
- Correlation analysis
- Spatial analysis
- Temporal analysis
- Hypothesis testing

## Key Scripts

### `descriptive_stats.py` (To Implement)

Computes descriptive statistics.

**Outputs:**

- Mean, median, std for all features
- Distribution plots
- Summary tables

### `correlation_analysis.py` (To Implement)

Analyzes correlations between variables.

**Methods:**

- Pearson correlation
- Spearman correlation
- Partial correlation
- Correlation heatmaps

### `spatial_analysis.py` (To Implement)

Performs spatial statistical analysis.

**Methods:**

- Spatial autocorrelation (Moran's I)
- Hot spot analysis (Getis-Ord Gi\*)
- Spatial regression
- Cluster detection

### `time_series.py` (To Implement)

Analyzes temporal patterns (if applicable).

**Methods:**

- Trend analysis
- Seasonality detection
- Forecasting
- Change point detection

## Usage

```bash
# Descriptive statistics
python src/5_analysis/descriptive_stats.py \
    --data data/integrated/full_dataset.csv \
    --output outputs/reports/descriptive_stats.html

# Correlation analysis
python src/5_analysis/correlation_analysis.py \
    --data data/features/transformed_features.csv \
    --output outputs/figures/correlation_matrix.png

# Spatial analysis
python src/5_analysis/spatial_analysis.py \
    --data data/integrated/full_dataset.csv \
    --shapefile data/raw/geographic/municipalities.shp \
    --output outputs/reports/spatial_analysis.html
```

## Analysis Types

### 1. Descriptive Analysis

- Summary statistics
- Distribution analysis
- Outlier detection
- Data profiling

### 2. Inferential Analysis

- Hypothesis testing
- Confidence intervals
- Statistical significance
- Effect sizes

### 3. Spatial Analysis

- Spatial patterns
- Geographic clustering
- Spatial dependencies
- Regional comparisons

### 4. Comparative Analysis

- Group comparisons
- Before/after analysis
- Regional differences
- Temporal changes

## Output

**Location**: `outputs/reports/`

**Files:**

- `descriptive_stats.html` - Descriptive statistics report
- `correlation_report.html` - Correlation analysis
- `spatial_analysis.html` - Spatial analysis results
- `statistical_tests.csv` - Hypothesis test results

## Statistical Tests

### Parametric Tests

- t-test (group comparisons)
- ANOVA (multiple groups)
- Linear regression

### Non-Parametric Tests

- Mann-Whitney U test
- Kruskal-Wallis test
- Spearman correlation

### Spatial Tests

- Moran's I (spatial autocorrelation)
- Geary's C (spatial association)
- LISA (local spatial autocorrelation)

## Best Practices

1. **Check assumptions** - Verify test assumptions before applying
2. **Multiple testing correction** - Use Bonferroni or FDR correction
3. **Effect sizes** - Report effect sizes, not just p-values
4. **Visualization** - Always visualize before testing
5. **Interpretation** - Focus on practical significance

## Next Steps

1. Implement descriptive statistics module
2. Add spatial analysis capabilities
3. Create automated report generation
4. Build interactive analysis dashboard
