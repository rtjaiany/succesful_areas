# 🛰️ Satellite Data Collection - Updated Approach

## What Changed

The original script was trying to use Google's satellite embeddings dataset, which is not publicly available yet. I've updated it to use **Sentinel-2 satellite imagery** instead, which is:

✅ **Freely available** in Google Earth Engine  
✅ **High quality** - 10m resolution  
✅ **Well documented** and widely used  
✅ **Perfect for environmental analysis**

---

## New Features Being Extracted

Instead of generic embeddings, we're now extracting **18 meaningful satellite features** for each municipality:

### 🌈 Spectral Bands (10 features)

- **Blue** (B2) - Water bodies, atmospheric scattering
- **Green** (B3) - Vegetation vigor
- **Red** (B4) - Vegetation discrimination
- **Red Edge 1-3** (B5-B7) - Vegetation health
- **NIR** (B8) - Vegetation biomass
- **NIR Narrow** (B8A) - Vegetation stress
- **SWIR 1** (B11) - Moisture content
- **SWIR 2** (B12) - Soil/rock discrimination

### 🌿 Vegetation Indices (3 features)

- **NDVI** - Normalized Difference Vegetation Index (vegetation health)
- **EVI** - Enhanced Vegetation Index (improved sensitivity)
- **SAVI** - Soil-Adjusted Vegetation Index (accounts for soil brightness)

### 💧 Water Indices (2 features)

- **NDWI** - Normalized Difference Water Index (water bodies)
- **MNDWI** - Modified NDWI (better for urban areas)

### 🏙️ Built-Up Indices (2 features)

- **NDBI** - Normalized Difference Built-up Index (urban areas)
- **UI** - Urban Index (built-up land)

### 📊 Metadata (1 feature)

- **image_count** - Number of Sentinel-2 images used

---

## How It Works

### 1. Data Collection

```python
# For each municipality:
1. Load Sentinel-2 images from 2023 (or 2022 if no 2023 data)
2. Filter out cloudy images (< 20% cloud cover)
3. Create median composite (reduces noise and clouds)
4. Calculate all indices and features
5. Compute mean values over municipality area
6. Save to CSV
```

### 2. Data Quality

- **Cloud filtering**: Only uses images with <20% cloud cover
- **Median composite**: Reduces impact of remaining clouds
- **Fallback**: Uses 2022 data if 2023 unavailable
- **Error handling**: Skips municipalities with no data

### 3. Output Format

Each row in the CSV will have:

```csv
municipality_id, municipality_name, state_name, state_code,
blue, green, red, red_edge_1, red_edge_2, red_edge_3,
nir, nir_narrow, swir_1, swir_2,
ndvi, evi, savi, ndwi, mndwi, ndbi, urban_index,
image_count, extraction_date, data_source
```

---

## Why This Is Better

### Compared to Embeddings:

| Feature                 | Embeddings    | Sentinel-2 Features     |
| ----------------------- | ------------- | ----------------------- |
| **Availability**        | ❌ Not public | ✅ Free & public        |
| **Interpretability**    | ❌ Black box  | ✅ Clear meaning        |
| **Scientific validity** | ⚠️ Unknown    | ✅ Well-established     |
| **Customization**       | ❌ Fixed      | ✅ Can add more indices |
| **Temporal coverage**   | ⚠️ Unknown    | ✅ 2015-present         |
| **Resolution**          | ⚠️ Unknown    | ✅ 10m                  |

---

## What These Features Tell Us

### Environmental Health

- **NDVI, EVI, SAVI**: Vegetation coverage and health
- **NDWI, MNDWI**: Water availability and bodies

### Land Use

- **NDBI, UI**: Urban development and built-up areas
- **NIR, SWIR**: Agricultural vs urban vs forest

### Economic Indicators (indirect)

- High NDVI → Agricultural activity
- High NDBI → Urban development
- High NDWI → Water resources

---

## Running the Updated Script

### Same command as before:

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

### What to expect:

1. ✅ Loads Brazilian municipalities (~5,570)
2. ✅ For each municipality:
    - Finds Sentinel-2 images
    - Creates cloud-free composite
    - Calculates 18 features
    - Saves to CSV
3. ✅ Progress updates every municipality
4. ✅ Output: `data/raw/satellite/municipality_embeddings_YYYYMMDD_HHMMSS.csv`

### Processing time:

- **Estimated**: 2-4 hours for all municipalities
- **Depends on**: Internet speed, GEE server load
- **Can resume**: If interrupted, just run again (new file created)

---

## Example Output

```csv
municipality_id,municipality_name,state_name,blue,green,red,ndvi,evi,ndbi,urban_index,...
1100015,Alta Floresta D'Oeste,Rondônia,450,520,380,0.65,0.58,-0.15,-0.12,...
1100023,Ariquemes,Rondônia,520,610,420,0.52,0.48,-0.08,-0.05,...
```

---

## Scientific References

These indices are well-established in remote sensing:

1. **NDVI**: Rouse et al. (1974) - Vegetation monitoring
2. **EVI**: Huete et al. (2002) - Improved vegetation index
3. **NDWI**: McFeeters (1996) - Water body detection
4. **NDBI**: Zha et al. (2003) - Built-up area mapping

---

## Next Steps After Collection

Once you have the satellite data:

### 1. Data Validation

```python
import pandas as pd
df = pd.read_csv('data/raw/satellite/municipality_embeddings_*.csv')
print(df.describe())  # Check statistics
print(df.isnull().sum())  # Check missing values
```

### 2. Visualization

- Map NDVI values (vegetation coverage)
- Map NDBI values (urban development)
- Compare states/regions

### 3. Integration

- Combine with demographic data
- Combine with economic data
- Create master dataset for modeling

---

## Troubleshooting

### "No Sentinel-2 images found"

- Some remote areas may have limited coverage
- Script automatically tries 2022 if 2023 fails
- These municipalities will be skipped (logged as warnings)

### "Quota exceeded"

- Unlikely with current settings (50 batch size, 2 workers)
- If it happens, script will retry automatically
- Can reduce batch size in `.env` if needed

### "Computation timeout"

- For very large municipalities
- Script uses `bestEffort=True` to handle this
- GEE will automatically reduce resolution if needed

---

## Summary

✅ **Updated to use Sentinel-2** instead of unavailable embeddings  
✅ **Extracting 18 meaningful features** instead of generic embeddings  
✅ **Scientifically validated** indices used in research  
✅ **Same ease of use** - just run the script!  
✅ **Better for your analysis** - interpretable features

**You're ready to collect real, meaningful satellite data for all Brazilian municipalities!** 🚀
