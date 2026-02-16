# iGuide Project - Setup Instructions

## ✅ What You've Already Done

1. ✅ Created virtual environment (`venv`)
2. ✅ Installed all Python dependencies
3. ✅ Created `.env` configuration file

---

## 🎯 What You Need to Do Next

### Step 1: Authenticate with Google Earth Engine

**Why:** You need GEE authentication to download satellite data.

**Command to run:**

```bash
earthengine authenticate
```

**What will happen:**

1. A browser window will open
2. Sign in with your Google account
3. Click "Allow" to grant permissions
4. You'll see a success message
5. Close the browser

**Note:** You only need to do this once. The credentials will be saved.

---

### Step 2: Get Your Google Earth Engine Project ID

**Why:** The scripts need to know which GEE project to use.

**Steps:**

1. Go to: https://console.cloud.google.com
2. Click on the project dropdown (top left)
3. Either:
    - Select an existing project, OR
    - Click "New Project" to create one
4. Copy the **Project ID** (not the project name!)
5. Make sure "Earth Engine API" is enabled for this project:
    - Go to: https://console.cloud.google.com/apis/library/earthengine.googleapis.com
    - Click "Enable" if it's not already enabled

---

### Step 3: Configure Your Environment File

**Why:** The scripts read configuration from the `.env` file.

**Steps:**

1. Open the `.env` file in your editor:

    ```bash
    notepad .env
    # or
    code .env
    ```

2. Replace `your-gee-project-id` with your actual Project ID from Step 2:

    ```env
    GEE_PROJECT_ID=your-actual-project-id-here
    ```

3. Save the file

**Optional configurations** (you can leave these as-is for now):

- `BATCH_SIZE=100` - How many municipalities to process at once
- `MAX_WORKERS=4` - Number of parallel workers
- `LOG_LEVEL=INFO` - How detailed the logs should be

---

### Step 4: Test Your Setup

**Why:** Verify everything is working before running the full pipeline.

**Command to run:**

```bash
python -c "import ee; ee.Initialize(project='your-gee-project-id'); print('✅ Success! Earth Engine is ready.')"
```

**Replace** `your-gee-project-id` with your actual project ID.

**Expected result:**

- You should see: `✅ Success! Earth Engine is ready.`

**If you get an error:**

- Make sure you completed Step 1 (authentication)
- Make sure your Project ID is correct
- Make sure Earth Engine API is enabled for your project

---

### Step 5: Run Your First Data Collection

**Why:** This will extract satellite embeddings for Brazilian municipalities.

**Recommended command** (memory-efficient streaming mode):

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

**Alternative commands:**

**Server-side processing** (processing happens on Google's servers):

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode server-side
```

**Standard mode** (for small datasets):

```bash
python src/1_collection/gee/extract_embeddings.py
```

**What will happen:**

1. Script connects to Google Earth Engine
2. Loads Brazilian municipality boundaries
3. Computes 64-dimensional embeddings for each municipality
4. Saves results to `data/raw/satellite/municipality_embeddings_YYYYMMDD_HHMMSS.csv`
5. Shows progress bar and logs

**How long it takes:**

- Depends on number of municipalities and your internet speed
- Could take from minutes to hours
- You'll see a progress bar

---

### Step 6: Verify Your Data

**Why:** Make sure the data was extracted correctly.

**Commands to run:**

**1. Check if the file was created:**

```bash
ls data/raw/satellite/
```

**2. View the first few rows:**

```bash
python -c "import pandas as pd; import glob; files = glob.glob('data/raw/satellite/*.csv'); df = pd.read_csv(files[0]) if files else None; print(df.head() if df is not None else 'No files found')"
```

**Expected output:**

- You should see columns like:
    - `municipality_id`
    - `municipality_name`
    - `state`
    - `embedding_0` through `embedding_63`
    - `extraction_date`

---

## 🔍 Important Notes

### Always Use the Virtual Environment

When running Python commands, make sure your virtual environment is active. You'll see `(venv)` at the start of your prompt:

```
(venv) PS C:\Users\jaian\OneDrive\Documentos\01 - In Progress\06 - SWE\iguide_project>
```

**If you don't see (venv)**, activate it first:

```bash
.\venv\Scripts\activate
```

### Check Logs

If something goes wrong, check the log file:

```bash
cat logs/extraction.log
# or
notepad logs/extraction.log
```

### Monitor Progress

The scripts will show:

- Progress bars
- Current municipality being processed
- Estimated time remaining
- Any errors or warnings

---

## 🆘 Troubleshooting

### "earthengine command not found"

**Solution:**

```bash
pip install earthengine-api --upgrade
```

### "Authentication required"

**Solution:**

```bash
earthengine authenticate --force
```

### "Project not found" or "Permission denied"

**Solution:**

- Double-check your Project ID in `.env`
- Make sure Earth Engine API is enabled
- Make sure you're signed in with the correct Google account

### "ModuleNotFoundError"

**Solution:**

- Make sure virtual environment is activated (you should see `(venv)`)
- If not: `.\venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

---

## 📊 What Happens After Data Collection?

Once you have the satellite data, you can proceed to:

1. **Data Integration** - Combine with other data sources (demographic, economic, etc.)
2. **Feature Engineering** - Create derived features
3. **Modeling** - Train machine learning models
4. **Analysis** - Perform statistical analysis
5. **Visualization** - Create maps and charts

But for now, focus on getting the satellite data first!

---

## ✅ Quick Checklist

- [ ] Run `earthengine authenticate`
- [ ] Get GEE Project ID from Google Cloud Console
- [ ] Edit `.env` file with your Project ID
- [ ] Test setup with `python -c "import ee; ee.Initialize(project='your-id'); print('✅ Success!')"`
- [ ] Run data collection: `python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming`
- [ ] Verify output in `data/raw/satellite/`

---

## 💡 Pro Tips

1. **Start with a test run**: Before processing all municipalities, you might want to test with a small subset
2. **Keep terminal open**: Don't close the terminal while the script is running
3. **Stable internet**: Make sure you have a stable internet connection
4. **Backup**: Once data is collected, consider backing it up

---

Good luck! 🚀
