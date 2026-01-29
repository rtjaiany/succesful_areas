# Memory Optimization Guide

## Overview

This guide explains the memory optimizations implemented for satellite data extraction and provides recommendations for different scenarios.

---

## 🔄 Two Extraction Approaches

### 1. **Standard Extraction** (`extract_embeddings.py`)

**Best for:**

- Small to medium datasets (< 1000 municipalities)
- Systems with ample RAM (8GB+)
- When you need the full DataFrame in memory for immediate processing

**Memory Usage:**

- Loads all results into a pandas DataFrame
- Memory grows linearly with number of municipalities
- ~500MB - 2GB for full Brazil dataset

**Pros:**

- Simple and straightforward
- Easy to manipulate data in memory
- Good for exploratory analysis

**Cons:**

- High memory usage for large datasets
- Risk of out-of-memory errors
- Slower for very large datasets

---

### 2. **Memory-Efficient Extraction** (`extract_embeddings_efficient.py`) ⭐ **RECOMMENDED**

**Best for:**

- Large datasets (1000+ municipalities)
- Systems with limited RAM (< 8GB)
- Production environments
- Long-running extractions

**Memory Usage:**

- Constant memory footprint (~100-200MB)
- Writes results incrementally to CSV
- Aggressive garbage collection

**Pros:**

- Minimal memory usage
- Can handle unlimited dataset sizes
- More reliable for long-running tasks
- Better error recovery

**Cons:**

- Results not immediately available in memory
- Slightly more complex code

---

## 📊 Memory Comparison

| Feature              | Standard       | Memory-Efficient |
| -------------------- | -------------- | ---------------- |
| **Peak Memory**      | ~2GB           | ~200MB           |
| **Memory Growth**    | Linear         | Constant         |
| **Processing Speed** | Fast           | Moderate         |
| **Reliability**      | Good           | Excellent        |
| **Max Dataset Size** | Limited by RAM | Unlimited        |
| **Error Recovery**   | Poor           | Good             |

---

## 🚀 Usage

### Standard Extraction

```bash
# Run standard extraction
python src/gee/extract_embeddings.py
```

### Memory-Efficient Extraction

```bash
# Streaming mode (local processing, incremental writes)
python src/gee/extract_embeddings_efficient.py --mode streaming

# Server-side mode (processing on GEE servers)
python src/gee/extract_embeddings_efficient.py --mode server-side

# Both modes
python src/gee/extract_embeddings_efficient.py --mode both
```

---

## 🔧 Memory Optimization Techniques

### 1. **Streaming CSV Writes**

Instead of accumulating all results in memory:

```python
# ❌ Memory-intensive (standard approach)
results = []
for municipality in municipalities:
    result = process(municipality)
    results.append(result)
df = pd.DataFrame(results)  # All data in memory!
df.to_csv('output.csv')

# ✅ Memory-efficient (streaming approach)
with open('output.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()

    for municipality in municipalities:
        result = process(municipality)
        writer.writerow(result)  # Write immediately
        del result  # Free memory
```

### 2. **Chunked Processing with Garbage Collection**

```python
import gc

for i in range(0, total, batch_size):
    batch = process_batch(i, i + batch_size)
    write_batch(batch)

    # Clear memory
    del batch
    gc.collect()  # Force garbage collection
```

### 3. **Server-Side Processing**

Let GEE servers do the heavy lifting:

```python
# Processing happens on GEE servers, not locally
municipalities_with_embeddings = municipalities.map(compute_embedding)

# Export directly from GEE to Google Drive
task = ee.batch.Export.table.toDrive(
    collection=municipalities_with_embeddings,
    # ... export parameters
)
```

### 4. **Memory Monitoring**

```python
from src.utils.memory_utils import MemoryMonitor

monitor = MemoryMonitor()
monitor.log_memory_usage("before processing")

# ... your code ...

monitor.log_memory_usage("after processing")
monitor.force_garbage_collection()
```

---

## 📈 Configuration Optimization

### Updated `config/gee_config.yaml`

```yaml
processing:
    batch_size: 50 # Reduced from 100
    max_workers: 2 # Reduced from 4
    chunk_size: 10 # Write every 10 records

memory:
    max_memory_mb: 1000
    gc_interval: 50
    monitor_enabled: true
    log_interval: 25
```

**Key Changes:**

- **Smaller batch size**: Processes fewer municipalities at once
- **Fewer workers**: Reduces parallel processing overhead
- **Chunk size**: Flushes to disk more frequently
- **Memory monitoring**: Tracks usage in real-time

---

## 🎯 Recommendations by Scenario

### Scenario 1: Testing with Small Dataset (< 100 municipalities)

```bash
# Use standard extraction
python src/gee/extract_embeddings.py
```

**Config:**

```yaml
processing:
    batch_size: 25
```

---

### Scenario 2: Production - Full Brazil Dataset (~5,500 municipalities)

```bash
# Use memory-efficient streaming
python src/gee/extract_embeddings_efficient.py --mode streaming
```

**Config:**

```yaml
processing:
    batch_size: 50
    chunk_size: 10

memory:
    max_memory_mb: 1000
    gc_interval: 50
    monitor_enabled: true
```

---

### Scenario 3: Limited Memory System (< 4GB RAM)

```bash
# Use server-side processing
python src/gee/extract_embeddings_efficient.py --mode server-side
```

**Config:**

```yaml
processing:
    batch_size: 25 # Very small batches
    chunk_size: 5 # Frequent writes

memory:
    max_memory_mb: 500
    gc_interval: 25
```

---

### Scenario 4: Maximum Speed (with 16GB+ RAM)

```bash
# Use standard extraction with larger batches
python src/gee/extract_embeddings.py
```

**Config:**

```yaml
processing:
    batch_size: 200
    max_workers: 8
```

---

## 🛠️ Memory Profiling Tools

### 1. **Built-in Memory Monitor**

```python
from src.utils.memory_utils import MemoryMonitor, log_system_memory

# Log system memory
log_system_memory()

# Monitor specific code
monitor = MemoryMonitor()
monitor.log_memory_usage("start")
# ... your code ...
monitor.log_memory_usage("end")
```

### 2. **Memory Profiling Decorator**

```python
from src.utils.memory_utils import memory_profile

@memory_profile
def my_function():
    # Function will be automatically profiled
    pass
```

### 3. **Memory Guard**

```python
from src.utils.memory_utils import MemoryGuard

with MemoryGuard(max_memory_mb=500):
    # Code will raise exception if memory exceeds 500MB
    process_data()
```

---

## 📊 Monitoring Memory During Extraction

The memory-efficient extractor automatically logs memory usage:

```
2026-01-28 21:00:00 | INFO | Memory before: 150.23 MB (2.1% of system) [Δ +0.00 MB]
2026-01-28 21:00:30 | INFO | Processing batch 1: municipalities 0 to 50
2026-01-28 21:01:00 | INFO | Memory after batch: 175.45 MB (2.5% of system) [Δ +25.22 MB]
2026-01-28 21:01:00 | INFO | Garbage collection freed 15.30 MB
2026-01-28 21:01:30 | INFO | Progress: 10.0% (500/5000)
```

---

## 🔍 Troubleshooting Memory Issues

### Issue: Out of Memory Error

**Solutions:**

1. Use memory-efficient extraction:

    ```bash
    python src/gee/extract_embeddings_efficient.py --mode streaming
    ```

2. Reduce batch size in `config/gee_config.yaml`:

    ```yaml
    processing:
        batch_size: 25 # or even 10
    ```

3. Use server-side processing:
    ```bash
    python src/gee/extract_embeddings_efficient.py --mode server-side
    ```

---

### Issue: Slow Processing

**Solutions:**

1. Increase batch size (if memory allows):

    ```yaml
    processing:
        batch_size: 100
    ```

2. Reduce chunk size for more frequent writes:

    ```yaml
    processing:
        chunk_size: 5
    ```

3. Use standard extraction if you have enough RAM

---

### Issue: Process Killed by OS

**Cause:** Memory limit exceeded

**Solutions:**

1. Use memory-efficient extraction
2. Enable memory monitoring:
    ```yaml
    memory:
        monitor_enabled: true
        max_memory_mb: 500 # Set lower limit
    ```

---

## 📝 Best Practices

1. **Always monitor memory** during first run
2. **Start with small batches** and increase gradually
3. **Use streaming mode** for production
4. **Enable garbage collection** for long-running tasks
5. **Test with subset** before processing full dataset
6. **Monitor GEE quota** to avoid rate limits
7. **Use server-side processing** when possible

---

## 🎓 Memory Optimization Checklist

- [ ] Choose appropriate extraction mode
- [ ] Configure batch size based on available RAM
- [ ] Enable memory monitoring
- [ ] Set appropriate chunk size
- [ ] Test with small dataset first
- [ ] Monitor logs for memory warnings
- [ ] Use garbage collection for large datasets
- [ ] Consider server-side processing for very large datasets

---

## 📚 Additional Resources

- **Memory Utils**: `src/utils/memory_utils.py`
- **Standard Extraction**: `src/gee/extract_embeddings.py`
- **Efficient Extraction**: `src/gee/extract_embeddings_efficient.py`
- **Configuration**: `config/gee_config.yaml`

---

**Last Updated**: 2026-01-28
**Recommended Approach**: Memory-Efficient Streaming for production use
