# Memory Optimization Guide

## Overview

This guide explains memory optimization strategies for satellite data extraction.

---

## 🚀 Current Extraction Approach

### **Satellite Data Extraction** (`extract_embeddings.py`)

**Features:**

- Memory-efficient processing with batch operations
- Incremental CSV writes to minimize memory usage
- Automatic garbage collection
- Progress tracking and error handling
- Retry logic for failed operations

**Memory Usage:**

- Constant memory footprint (~200-500MB)
- Processes municipalities in batches
- Writes results incrementally to CSV

**Best for:**

- All dataset sizes
- Production environments
- Long-running extractions
- Systems with any RAM configuration

---

## 📊 Memory Optimization Techniques

### 1. **Batch Processing**

The script processes municipalities in configurable batches:

```python
# Process in batches to control memory
for batch in batches:
    results = process_batch(batch)
    write_to_csv(results)
    clear_memory()
```

### 2. **Incremental Writes**

Results are written to CSV immediately, not accumulated in memory:

```python
# Write each result immediately
with open('output.csv', 'a') as f:
    writer.writerow(result)
    # Result is freed from memory
```

### 3. **Garbage Collection**

Automatic garbage collection after each batch:

```python
import gc

# After processing batch
del batch_results
gc.collect()  # Force garbage collection
```

### 4. **Server-Side Processing**

Google Earth Engine performs heavy computation on their servers:

```python
# Processing happens on GEE servers
result = ee_image.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=municipality_geometry
)
```

---

## ⚙️ Configuration

### Recommended Settings (`config/gee_config.yaml`)

```yaml
processing:
    batch_size: 50 # Municipalities per batch
    max_workers: 2 # Parallel workers
    chunk_size: 10 # Write frequency

memory:
    max_memory_mb: 1000 # Memory limit
    gc_interval: 50 # Garbage collection frequency
    monitor_enabled: true # Enable monitoring
```

**Key Parameters:**

- **batch_size**: Number of municipalities processed together
    - Smaller = less memory, slower processing
    - Larger = more memory, faster processing
    - Recommended: 25-100

- **max_workers**: Parallel processing threads
    - More workers = faster but more memory
    - Recommended: 2-4

- **chunk_size**: How often to flush results to disk
    - Smaller = more frequent writes, less memory
    - Recommended: 10-25

---

## 🎯 Recommendations by Scenario

### Scenario 1: Testing (< 100 municipalities)

```yaml
processing:
    batch_size: 25
    max_workers: 2
```

**Expected:** Fast processing, minimal memory usage

---

### Scenario 2: Production - Full Brazil (~5,500 municipalities)

```yaml
processing:
    batch_size: 50
    max_workers: 2
    chunk_size: 10

memory:
    max_memory_mb: 1000
    gc_interval: 50
    monitor_enabled: true
```

**Expected:** 1-3 hours, ~500MB memory usage

---

### Scenario 3: Limited Memory (< 4GB RAM)

```yaml
processing:
    batch_size: 25
    max_workers: 1
    chunk_size: 5

memory:
    max_memory_mb: 500
    gc_interval: 25
```

**Expected:** Slower but very safe

---

### Scenario 4: High Performance (16GB+ RAM)

```yaml
processing:
    batch_size: 100
    max_workers: 4
    chunk_size: 25
```

**Expected:** Fastest processing, higher memory usage

---

## 📈 Monitoring Memory

The script automatically logs memory usage:

```
2026-02-16 17:00:00 | INFO | Memory: 180.5 MB (2.3% of system)
2026-02-16 17:00:30 | INFO | Processing batch 1: municipalities 0-50
2026-02-16 17:01:00 | INFO | Memory: 205.3 MB (2.6% of system) [Δ +24.8 MB]
2026-02-16 17:01:00 | INFO | Garbage collection freed 15.2 MB
2026-02-16 17:01:30 | INFO | Progress: 10.0% (500/5000)
```

---

## 🔍 Troubleshooting

### Issue: Out of Memory Error

**Solutions:**

1. Reduce batch size:

    ```yaml
    processing:
        batch_size: 10
    ```

2. Reduce workers:

    ```yaml
    processing:
        max_workers: 1
    ```

3. Enable aggressive garbage collection:
    ```yaml
    memory:
        gc_interval: 10
    ```

---

### Issue: Slow Processing

**Solutions:**

1. Increase batch size (if memory allows):

    ```yaml
    processing:
        batch_size: 100
    ```

2. Increase workers:

    ```yaml
    processing:
        max_workers: 4
    ```

3. Reduce write frequency:
    ```yaml
    processing:
        chunk_size: 50
    ```

---

### Issue: Process Killed by OS

**Cause:** Memory limit exceeded

**Solutions:**

1. Set strict memory limit:

    ```yaml
    memory:
        max_memory_mb: 500
    ```

2. Use minimal batch size:
    ```yaml
    processing:
        batch_size: 10
        max_workers: 1
    ```

---

## 📝 Best Practices

1. **Start conservative** - Use small batches first
2. **Monitor logs** - Watch memory usage patterns
3. **Test with subset** - Process 100 municipalities first
4. **Adjust gradually** - Increase batch size if stable
5. **Enable monitoring** - Always track memory usage
6. **Check GEE quota** - Avoid rate limits

---

## 🎓 Memory Optimization Checklist

- [ ] Configure appropriate batch size for your RAM
- [ ] Enable memory monitoring
- [ ] Set reasonable chunk size
- [ ] Test with small dataset first
- [ ] Monitor logs for memory warnings
- [ ] Adjust settings based on performance
- [ ] Keep batch size under control

---

## 📚 Resources

- **Extraction Script**: `src/satellite/extract_embeddings.py`
- **Configuration**: `config/gee_config.yaml`
- **Utilities**: `src/utils/`

---

**Last Updated**: 2026-02-16
**Recommended**: Use default settings for most cases
