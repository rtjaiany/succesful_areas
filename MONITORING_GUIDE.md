# 📊 Progress Monitoring Guide

## How to Monitor Your Data Collection

### Quick Start

**Open a NEW terminal window** (keep the extraction running in the first one) and run:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run the monitor
python monitor_progress.py
```

---

## What You'll See

The monitor displays a **live dashboard** that updates every 2 seconds:

```
🛰️  SATELLITE DATA COLLECTION MONITOR
================================================================================
📁 Output File: municipality_embeddings_20260202_183507.csv
⏰ Started: 2026-02-02 18:35:07
================================================================================

📊 Progress: [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 15.2%

📈 Statistics:
   Municipalities Processed: 847 / 5,570
   Remaining: 4,723
   File Size: 2.45 MB
   Elapsed Time: 12m 34s

⚡ Performance:
   Processing Rate: 1.12 municipalities/second
   Estimated Time Remaining: 1h 10m
   Estimated Completion: 2026-02-02 19:48:41

📝 Recent Activity:
   • Processing [847]: São Paulo, São Paulo
   • Extracted 18 features for São Paulo
   • Processing [848]: Guarulhos, São Paulo
   • No Sentinel-2 images found for Guarulhos, trying 2022
   • Processing [849]: Campinas, São Paulo

💡 Status:
   ✅ Running smoothly

================================================================================
Press Ctrl+C to stop monitoring (extraction will continue)
================================================================================
```

---

## Features

### 📊 Visual Progress Bar

- Shows completion percentage
- Updates in real-time

### 📈 Statistics

- **Municipalities Processed**: How many completed
- **Remaining**: How many left to process
- **File Size**: Current output file size
- **Elapsed Time**: How long it's been running

### ⚡ Performance Metrics

- **Processing Rate**: Municipalities per second
- **Estimated Time Remaining**: How much longer
- **Estimated Completion**: When it will finish

### 📝 Recent Activity

- Shows last 5 log entries
- See which municipality is being processed
- Spot any warnings or errors

### 💡 Status Indicators

- ✅ **Running smoothly**: Everything working
- ⏳ **Initializing**: Just started
- ⚠️ **Waiting for updates**: Might be processing a large municipality

---

## Tips

### 1. Run in Separate Terminal

Keep the extraction running in one terminal, monitor in another.

### 2. Stop Monitoring Anytime

Press **Ctrl+C** to stop the monitor. The extraction keeps running!

### 3. Resume Monitoring

You can close and reopen the monitor anytime:

```bash
python monitor_progress.py
```

### 4. Check Output File

The monitor shows you which file is being written to.

---

## Troubleshooting

### "No active extraction found"

**Solution**: Make sure the extraction script is running first:

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

### Monitor shows 0 municipalities

**Solution**: Wait a few seconds. The first municipality takes longer to process.

### Rate is 0

**Solution**: Normal at the start. Rate will stabilize after a few municipalities.

---

## Example Session

### Terminal 1 (Extraction):

```bash
(venv) PS> python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
2026-02-02 18:35:07 | INFO | Initializing...
2026-02-02 18:35:10 | INFO | Processing [1]: Água Branca, Alagoas
...
```

### Terminal 2 (Monitor):

```bash
(venv) PS> python monitor_progress.py
🛰️  Satellite Data Collection Monitor
================================================================================
✅ Found active extraction: municipality_embeddings_20260202_183507.csv
Monitoring progress... (Press Ctrl+C to stop)
...
```

---

## What to Do While It Runs

### Option 1: Watch the Monitor ✅

Keep the monitor open and watch progress in real-time.

### Option 2: Let It Run 🌙

Close the monitor, come back in a few hours.

### Option 3: Check Periodically 📱

Open monitor occasionally to check progress.

---

## When It's Done

The extraction script will show:

```
✅ Extraction complete! Successfully processed 5,570/5,570 municipalities
📁 Output saved to: data/raw/satellite/municipality_embeddings_20260202_183507.csv
```

The monitor will show:

```
📊 Progress: [██████████████████████████████████████████████████] 100.0%
```

---

## Next Steps After Completion

1. **Verify the data**:

    ```bash
    python -c "import pandas as pd; df = pd.read_csv('data/raw/satellite/municipality_embeddings_*.csv'); print(df.head()); print(df.shape)"
    ```

2. **Check for missing values**:

    ```bash
    python -c "import pandas as pd; df = pd.read_csv('data/raw/satellite/municipality_embeddings_*.csv'); print(df.isnull().sum())"
    ```

3. **View statistics**:
    ```bash
    python -c "import pandas as pd; df = pd.read_csv('data/raw/satellite/municipality_embeddings_*.csv'); print(df.describe())"
    ```

---

**Happy monitoring!** 📊🛰️
