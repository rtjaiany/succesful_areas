# 🎯 Quick Reference - GEE Quota Limits

## Your Free Tier Limits

✅ **Requests per day:** 1,260,000  
✅ **Requests per minute:** 6,000  
✅ **Compute time:** Unlimited  
✅ **Processing time:** Unlimited

---

## Your Project Needs

📊 **Total municipalities:** ~5,570  
📊 **Requests needed:** ~16,710  
📊 **Quota usage:** ~1.3% of daily limit

**Result:** ✅ You can process ALL municipalities in ONE run!

---

## Optimized Settings (Already Configured!)

Your `.env` file is now set to **BALANCED** mode:

```
BATCH_SIZE=50    ← Process 50 municipalities per batch
MAX_WORKERS=2    ← Use 2 parallel workers
```

**This will:**

- ✅ Complete in 1-2 hours
- ✅ Use only ~5% of your quota
- ✅ Stay well under rate limits
- ✅ Handle errors automatically

---

## What You Need to Do

### 1. Edit `.env` file

```bash
notepad .env
```

**Change this line:**

```
GEE_PROJECT_ID=your-gee-project-id
```

**To your actual Project ID from Google Cloud Console**

### 2. Authenticate

```bash
earthengine authenticate
```

### 3. Test

```bash
python -c "import ee; ee.Initialize(project='your-project-id'); print('✅ Ready!')"
```

### 4. Run

```bash
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming
```

---

## Settings Comparison

| Mode            | BATCH_SIZE | MAX_WORKERS | Time   | Quota | Risk     |
| --------------- | ---------- | ----------- | ------ | ----- | -------- |
| **Safe**        | 25         | 1           | 2-3h   | 1%    | Very Low |
| **Balanced** ⭐ | 50         | 2           | 1-2h   | 5%    | Low      |
| **Fast**        | 100        | 4           | 30-60m | 15%   | Medium   |

⭐ = Your current setting (recommended!)

---

## Need to Change Settings?

Edit `.env` file and change:

```bash
# For SAFE mode (slower, safest)
BATCH_SIZE=25
MAX_WORKERS=1

# For BALANCED mode (recommended) ⭐
BATCH_SIZE=50
MAX_WORKERS=2

# For FAST mode (faster, more aggressive)
BATCH_SIZE=100
MAX_WORKERS=4
```

---

## Monitoring

**During run, watch for:**

- Progress bar showing percentage
- Current municipality being processed
- Success/failure counts

**Check logs:**

```bash
cat logs/extraction.log
```

---

## Troubleshooting

**"Rate limit exceeded"**
→ Script will automatically retry, no action needed

**"Authentication error"**
→ Run: `earthengine authenticate --force`

**"Project not found"**
→ Check your Project ID in `.env` file

---

**Full details:** See `docs/GEE_QUOTA_OPTIMIZATION.md`
