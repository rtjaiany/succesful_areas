# GEE API Reference

## Useful Google Earth Engine Resources

### Official Documentation

- [GEE Python API](https://developers.google.com/earth-engine/guides/python_install)
- [GEE Data Catalog](https://developers.google.com/earth-engine/datasets)
- [GEE Code Editor](https://code.earthengine.google.com/)

### Satellite Embedding Dataset

The Google Satellite Embedding V1 dataset provides pre-computed embeddings from satellite imagery.

**Key Features:**

- 64-dimensional embeddings
- Global coverage
- Based on deep learning models trained on satellite imagery
- Useful for environmental analysis, land use classification, and more

### Brazilian Municipality Boundaries

1. **IBGE Data** (Custom Upload)
    - Download from: [IBGE Downloads](https://www.ibge.gov.br/geociencias/downloads-geociencias.html)
    - Upload as GEE asset
    - Reference in your scripts

### Common GEE Operations

#### Reduce Region

```python
mean_value = image.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=geometry,
    scale=10,
    maxPixels=1e9
)
```

#### Export to Drive

```python
task = ee.batch.Export.table.toDrive(
    collection=feature_collection,
    description='export_description',
    folder='folder_name',
    fileFormat='CSV'
)
task.start()
```

#### Filter Collections

```python
filtered = collection.filter(
    ee.Filter.eq('property_name', 'value')
)
```

### Best Practices

1. **Batch Processing**: Process municipalities in batches to avoid timeouts
2. **Error Handling**: Always include try-catch blocks for GEE operations
3. **Scale**: Choose appropriate scale based on your analysis needs
4. **Max Pixels**: Set reasonable maxPixels to avoid memory errors
5. **Task Monitoring**: Check task status in GEE Code Editor

### Troubleshooting

**Issue**: "Computation timed out"

- **Solution**: Reduce batch size, increase scale, or simplify computation

**Issue**: "User memory limit exceeded"

- **Solution**: Reduce maxPixels or process smaller regions

**Issue**: "Asset not found"

- **Solution**: Verify asset path and permissions

### Example: Extract Mean NDVI

```python
import ee

# Initialize
ee.Initialize()

# Load Sentinel-2 image
image = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate('2023-01-01', '2023-12-31') \
    .median()

# Calculate NDVI
ndvi = image.normalizedDifference(['B8', 'B4'])

# Define region (municipality)
region = ee.Geometry.Point([-46.6333, -23.5505]).buffer(10000)

# Compute mean
mean_ndvi = ndvi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=region,
    scale=10
)

print(mean_ndvi.getInfo())
```

## Additional Resources

- [GEE Community Tutorials](https://developers.google.com/earth-engine/tutorials/community/intro)
- [Awesome GEE](https://github.com/giswqs/Awesome-GEE)
- [GEE Python Examples](https://github.com/google/earthengine-api/tree/master/python/examples)
