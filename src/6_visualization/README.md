# Phase 6: Visualization

## Overview

This phase creates visualizations, maps, dashboards, and reports.

## Purpose

- Create static plots for publications
- Generate interactive visualizations
- Build geographic maps
- Develop dashboards for exploration
- Produce automated reports

## Key Scripts

### `plots.py` (To Implement)

Creates static plots using matplotlib/seaborn.

**Plot Types:**

- Histograms and distributions
- Scatter plots
- Box plots
- Heatmaps
- Time series plots

### `maps.py` (To Implement)

Creates geographic visualizations using folium/geopandas.

**Map Types:**

- Choropleth maps (colored by variable)
- Point maps (municipality locations)
- Heat maps (density visualization)
- Interactive maps with popups

### `dashboards.py` (To Implement)

Builds interactive dashboards using Plotly Dash.

**Dashboard Features:**

- Interactive filters
- Multiple linked plots
- Real-time updates
- Export capabilities

### `reports.py` (To Implement)

Generates automated reports.

**Report Types:**

- PDF reports
- HTML reports
- PowerPoint presentations
- Jupyter notebooks

## Usage

### Static Plots

```bash
python src/6_visualization/plots.py \
    --data data/integrated/full_dataset.csv \
    --type scatter \
    --x gdp_per_capita \
    --y satellite_embedding_0 \
    --output outputs/figures/gdp_vs_embedding.png
```

### Interactive Maps

```bash
python src/6_visualization/maps.py \
    --data data/integrated/full_dataset.csv \
    --variable population_density \
    --shapefile data/raw/geographic/municipalities.shp \
    --output outputs/figures/population_map.html
```

### Dashboard

```bash
python src/6_visualization/dashboards.py \
    --data data/integrated/full_dataset.csv \
    --port 8050
```

### Reports

```bash
python src/6_visualization/reports.py \
    --template templates/analysis_report.html \
    --data outputs/reports/analysis_results.json \
    --output outputs/reports/final_report.pdf
```

## Visualization Libraries

### Static Plots

- **matplotlib** - Basic plotting
- **seaborn** - Statistical visualizations
- **plotly** - Interactive plots (static export)

### Maps

- **folium** - Interactive maps
- **geopandas** - Spatial data visualization
- **contextily** - Basemaps

### Dashboards

- **Plotly Dash** - Web-based dashboards
- **Streamlit** - Quick prototyping
- **Panel** - Flexible dashboards

## Visualization Types

### 1. Exploratory Visualizations

- Data distributions
- Correlation matrices
- Pair plots
- Missing data patterns

### 2. Analytical Visualizations

- Model results
- Cluster visualizations
- Feature importance
- Prediction vs actual

### 3. Geographic Visualizations

- Choropleth maps
- Spatial patterns
- Regional comparisons
- Interactive maps

### 4. Presentation Visualizations

- Publication-ready plots
- Infographics
- Slide decks
- Executive summaries

## Output

**Location**: `outputs/figures/`

**File Types:**

- `.png` - Static images (high resolution)
- `.svg` - Vector graphics
- `.html` - Interactive plots/maps
- `.pdf` - Reports

## Style Guidelines

### Colors

- Use colorblind-friendly palettes
- Consistent color scheme across plots
- Meaningful color mapping

### Fonts

- Clear, readable fonts
- Consistent font sizes
- Proper axis labels

### Layout

- Clear titles and labels
- Legends when needed
- Proper aspect ratios
- White space for clarity

## Best Practices

1. **Know your audience** - Tailor visualizations to viewers
2. **Start simple** - Begin with basic plots before complex ones
3. **Tell a story** - Visualizations should have a clear message
4. **Be accurate** - Don't mislead with scale or truncation
5. **Iterate** - Refine based on feedback

## Example Visualizations

### Cluster Map

```python
import folium
import geopandas as gpd

# Load data
gdf = gpd.read_file('data/raw/geographic/municipalities.shp')
gdf = gdf.merge(clusters, on='municipality_id')

# Create map
m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)

# Add choropleth
folium.Choropleth(
    geo_data=gdf,
    data=gdf,
    columns=['municipality_id', 'cluster'],
    key_on='feature.properties.municipality_id',
    fill_color='YlOrRd',
    legend_name='Cluster'
).add_to(m)

m.save('outputs/figures/cluster_map.html')
```

### Feature Importance Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Feature Importance')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('outputs/figures/feature_importance.png', dpi=300)
```

## Next Steps

1. Implement basic plotting functions
2. Create map templates
3. Build interactive dashboard
4. Set up automated report generation
5. Create visualization style guide
