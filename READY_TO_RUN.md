# ✅ Setup Complete - Ready to Run!

## 🎉 Your iGuide Project is Ready!

All setup steps are complete. You can now start collecting satellite data!

---

## 📋 What's Been Configured

✅ **Virtual environment** - Created and activated  
✅ **Dependencies** - All packages installed  
✅ **Project structure** - All `__init__.py` files created  
✅ **Configuration** - `.env` file optimized for free tier  
✅ **Output directory** - `data/raw/satellite/` ready  
✅ **Import paths** - Fixed and tested

---

## 🚀 How to Run the Data Collection

### Step 1: Make sure your virtual environment is active

You should see `(venv)` in your terminal prompt:

```
(venv) PS C:\Users\jaian\OneDrive\Documentos\01 - In Progress\06 - SWE\iguide_project>
```

If not, activate it:

```bash
.\venv\Scripts\activate
```

### Step 2: Run the extraction script

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

---

## 📊 What Will Happen

1. **Authentication** - Script will authenticate with Google Earth Engine
2. **Loading** - Loads Brazilian municipality boundaries (~5,570 municipalities)
3. **Processing** - Processes in batches of 50 municipalities
4. **Progress** - Shows progress bar and logs
5. **Output** - Saves to `data/raw/satellite/municipality_embeddings_YYYYMMDD_HHMMSS.csv`

**Estimated time:** 1-2 hours  
**Quota usage:** ~5% of your daily limit  
**Memory usage:** ~200MB (constant)

---

## 📁 Output Location

Your data will be saved to:

```
c:\Users\jaian\OneDrive\Documentos\01 - In Progress\06 - SWE\iguide_project\data\raw\satellite\
```

File format:

```
municipality_embeddings_20260202_143000.csv
```

---

## 📈 Monitoring Progress

### In the Terminal:

- Progress percentage
- Current municipality being processed
- Batch completion messages
- Success/failure counts

### In the Log File:

```bash
cat logs/extraction.log
```

---

## ⚙️ Current Configuration

From your `.env` file:

| Setting       | Value                | Description              |
| ------------- | -------------------- | ------------------------ |
| `BATCH_SIZE`  | 50                   | Municipalities per batch |
| `MAX_WORKERS` | 2                    | Parallel workers         |
| `OUTPUT_DIR`  | `data/raw/satellite` | Where data is saved      |

These are **optimized for your GEE free tier**!

---

## 🔧 If Something Goes Wrong

### "Authentication required"

```bash
earthengine authenticate
```

### "Project not found"

Check line 2 of `.env` file - make sure `GEE_PROJECT_ID` is set correctly

### "ModuleNotFoundError"

Make sure virtual environment is activated:

```bash
.\venv\Scripts\activate
```

### "Rate limit exceeded"

The script will automatically retry - no action needed!

---

## 📚 Next Steps After Data Collection

Once you have the satellite data:

1. **Verify the output**

    ```bash
    python -c "import pandas as pd; df = pd.read_csv('data/raw/satellite/municipality_embeddings_*.csv'); print(df.head())"
    ```

2. **Check data quality**
    - Number of rows should match number of municipalities
    - All embedding columns (embedding_0 to embedding_63) should have values
    - No missing data

3. **Proceed to Phase 2: Data Integration**
    - Combine with demographic data
    - Combine with economic data
    - Combine with environmental data

---

## 🎯 Quick Command Reference

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run data collection (streaming mode - recommended)
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming

# Run data collection (server-side mode)
python src/1_collection/gee/extract_embeddings_efficient.py --mode server-side

# Run both modes
python src/1_collection/gee/extract_embeddings_efficient.py --mode both

# Test setup
python test_setup.py

# View logs
cat logs/extraction.log

# Check output
ls data/raw/satellite/
```

---

## ✅ You're Ready!

Everything is configured and ready to go. Just run:

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

And let it run! The script will handle everything automatically.

---

**Good luck with your data collection!** 🚀

If you encounter any issues, check the troubleshooting section above or review the logs.
