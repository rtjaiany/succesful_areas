# Google Earth Engine Quota Optimization Guide

## 📊 Your Free Tier Quotas

Based on your GEE account limits:

| Quota                                 | Limit     | What It Means                        |
| ------------------------------------- | --------- | ------------------------------------ |
| **Requests per day**                  | 1,260,000 | Total API calls you can make per day |
| **Compute time (EECU)**               | Unlimited | Processing time on GEE servers       |
| **Seconds per month**                 | Unlimited | Total processing time per month      |
| **Read requests per minute**          | 6,000     | API calls per minute                 |
| **Read requests per minute per user** | 6,000     | Same as above (single user)          |

**Good news:** These limits are **very generous** for your project! ✅

---

## 🧮 Calculating Your Usage

### For Brazilian Municipalities:

- **Total municipalities:** ~5,570
- **Requests per municipality:** ~2-3 (boundary + embedding calculation)
- **Total requests needed:** ~11,140 - 16,710
- **Percentage of daily quota:** ~1.3%

**Conclusion:** You can easily process all municipalities in a single run! 🎉

---

## ⚙️ Optimized Configuration

### Current Configuration (Already Optimized!)

Your `config/gee_config.yaml` is already well-configured:

```yaml
processing:
    batch_size: 50 # Process 50 municipalities at a time
    max_workers: 2 # Use 2 parallel workers
    retry_attempts: 3 # Retry failed requests 3 times
    retry_delay: 5 # Wait 5 seconds between retries
    chunk_size: 10 # Write to disk every 10 records
```

### Why These Settings Work Well:

1. **Batch size: 50**
    - Processes 50 municipalities per batch
    - ~100-150 requests per batch
    - Well under the 6,000 requests/minute limit

2. **Max workers: 2**
    - 2 parallel threads
    - Total: ~200-300 requests/minute
    - Only 5% of your quota!

3. **Retry logic**
    - Handles temporary failures gracefully
    - Prevents data loss

---

## 🎯 Recommended Settings for Different Scenarios

### Scenario 1: Conservative (Safest, Slowest)

**Best for:** First-time users, unstable internet

Edit `.env`:

```env
BATCH_SIZE=25
MAX_WORKERS=1
```

**Estimated time:** 2-3 hours
**Quota usage:** ~1% of limits

---

### Scenario 2: Balanced (Recommended) ✅

**Best for:** Most users, stable internet

Edit `.env`:

```env
BATCH_SIZE=50
MAX_WORKERS=2
```

**Estimated time:** 1-2 hours
**Quota usage:** ~5% of limits

**This is your current setting!**

---

### Scenario 3: Aggressive (Fastest)

**Best for:** Experienced users, very stable internet

Edit `.env`:

```env
BATCH_SIZE=100
MAX_WORKERS=4
```

**Estimated time:** 30-60 minutes
**Quota usage:** ~15% of limits

**Note:** Still well within quota, but may hit rate limits occasionally

---

## 🚦 Rate Limit Management

The script automatically handles rate limits:

1. **Exponential backoff:** Waits longer after each retry
2. **Automatic retry:** Retries failed requests up to 3 times
3. **Error logging:** Logs all failures for debugging

### If You Hit Rate Limits:

You'll see messages like:

```
WARNING: Rate limit exceeded, retrying in 5 seconds...
```

**Solution:** The script will automatically retry. No action needed!

---

## 📈 Monitoring Your Usage

### During Execution:

The script shows:

- ✅ Progress bar with percentage
- ✅ Current municipality being processed
- ✅ Estimated time remaining
- ✅ Success/failure counts

### After Execution:

Check the log file:

```bash
cat logs/extraction.log
```

Look for:

- Total requests made
- Failed requests
- Rate limit warnings

---

## 🔧 Adjusting Configuration

### To Change Settings:

**Option 1: Edit `.env` file (Recommended)**

```bash
notepad .env
```

Change these values:

```env
BATCH_SIZE=50      # Number of municipalities per batch
MAX_WORKERS=2      # Number of parallel workers
```

**Option 2: Edit `config/gee_config.yaml`**

```bash
notepad config/gee_config.yaml
```

Change:

```yaml
processing:
    batch_size: 50
    max_workers: 2
```

---

## 💡 Best Practices

### 1. Start Conservative

For your first run:

```env
BATCH_SIZE=25
MAX_WORKERS=1
```

Monitor the logs and adjust if needed.

### 2. Monitor Progress

Keep an eye on:

- Progress bar
- Log file (`logs/extraction.log`)
- Memory usage (Task Manager)

### 3. Test with Small Subset First

Before processing all municipalities, test with a small subset:

```python
# Edit extract_embeddings_efficient.py
# Line ~300, add:
municipality_list = municipality_list.slice(0, 10)  # Test with 10 municipalities
```

### 4. Run During Off-Peak Hours

For best performance:

- Run during night/early morning (your local time)
- Less competition for GEE resources
- More stable internet

---

## 🎯 Quota Usage Calculator

### Formula:

```
Total Requests = Municipalities × Requests per Municipality
               = 5,570 × 3
               = 16,710 requests

Percentage of Daily Quota = (16,710 / 1,260,000) × 100
                          = 1.33%
```

### Time Estimates:

**With current settings (batch_size=50, max_workers=2):**

```
Batches = 5,570 / 50 = 112 batches
Time per batch = ~30-60 seconds
Total time = 112 × 45 seconds = ~84 minutes
```

---

## ⚠️ What to Do If You Exceed Quotas

### Daily Request Limit (1,260,000)

**Unlikely to happen** with this project, but if it does:

1. **Wait 24 hours** for quota to reset
2. **Reduce batch_size** and **max_workers**
3. **Process in multiple days** (split municipalities)

### Per-Minute Rate Limit (6,000)

**More likely** if using aggressive settings:

1. **Script will automatically retry**
2. **Reduce max_workers** to 1 or 2
3. **Add delays** between batches

---

## 📊 Recommended Configuration Summary

For **5,570 Brazilian municipalities**:

| Setting          | Value | Reason                       |
| ---------------- | ----- | ---------------------------- |
| `BATCH_SIZE`     | 50    | Balances speed and safety    |
| `MAX_WORKERS`    | 2     | Stays well under rate limits |
| `retry_attempts` | 3     | Handles temporary failures   |
| `retry_delay`    | 5     | Gives GEE time to recover    |

**Expected results:**

- ✅ Completes in 1-2 hours
- ✅ Uses only ~5% of quotas
- ✅ Minimal risk of rate limits
- ✅ Automatic error recovery

---

## ✅ Quick Checklist

Before running:

- [ ] Check your `.env` file has `BATCH_SIZE=50` and `MAX_WORKERS=2`
- [ ] Ensure stable internet connection
- [ ] Have at least 2 hours of uninterrupted time
- [ ] Check disk space (need ~100MB for output)
- [ ] Review `config/gee_config.yaml` settings

During run:

- [ ] Monitor progress bar
- [ ] Watch for error messages
- [ ] Check `logs/extraction.log` periodically

After run:

- [ ] Verify output file in `data/raw/satellite/`
- [ ] Check log for any errors
- [ ] Review quota usage (should be ~1-5%)

---

## 🚀 You're Ready!

Your current configuration is **optimal** for the free tier. Just run:

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

And let it run! The script will handle everything automatically. ✨

---

**Questions?** Check the troubleshooting section in `SETUP_INSTRUCTIONS.md`
