-- ============================================================================
-- iGuide Project - Sample SQL Queries
-- ============================================================================
-- Description: Useful queries for analyzing satellite embedding data
-- Author: iGuide Project Team
-- Created: 2026-01-28
-- ============================================================================

-- ============================================================================
-- Basic Queries
-- ============================================================================

-- 1. Count total records
SELECT COUNT(*) as total_records 
FROM satellite_embeddings;

-- 2. View first 10 records
SELECT 
    municipality_id,
    municipality_name,
    state_code,
    extraction_date
FROM satellite_embeddings
LIMIT 10;

-- 3. Get unique municipalities
SELECT COUNT(DISTINCT municipality_id) as unique_municipalities
FROM satellite_embeddings;

-- 4. Get unique states
SELECT DISTINCT state_code, state_name
FROM satellite_embeddings
ORDER BY state_code;

-- ============================================================================
-- Filtering Queries
-- ============================================================================

-- 5. Get embeddings for a specific municipality (São Paulo)
SELECT *
FROM satellite_embeddings
WHERE municipality_id = '3550308';

-- 6. Get all municipalities in São Paulo state
SELECT 
    municipality_name,
    municipality_id,
    extraction_date
FROM satellite_embeddings
WHERE state_code = 'SP'
ORDER BY municipality_name;

-- 7. Get recent extractions (last 7 days)
SELECT 
    municipality_name,
    state_code,
    extraction_date
FROM satellite_embeddings
WHERE extraction_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY extraction_date DESC;

-- 8. Find municipalities with specific name pattern
SELECT 
    municipality_name,
    state_code,
    municipality_id
FROM satellite_embeddings
WHERE municipality_name ILIKE '%São%'
ORDER BY municipality_name;

-- ============================================================================
-- Aggregation Queries
-- ============================================================================

-- 9. Count municipalities by state
SELECT 
    state_code,
    state_name,
    COUNT(*) as municipality_count
FROM satellite_embeddings
GROUP BY state_code, state_name
ORDER BY municipality_count DESC;

-- 10. Average embeddings by state (first 5 dimensions)
SELECT 
    state_code,
    AVG(embedding_0) as avg_emb_0,
    AVG(embedding_1) as avg_emb_1,
    AVG(embedding_2) as avg_emb_2,
    AVG(embedding_3) as avg_emb_3,
    AVG(embedding_4) as avg_emb_4
FROM satellite_embeddings
GROUP BY state_code
ORDER BY state_code;

-- 11. Extraction statistics by date
SELECT 
    DATE(extraction_date) as extraction_day,
    COUNT(*) as records_extracted,
    COUNT(DISTINCT municipality_id) as unique_municipalities
FROM satellite_embeddings
GROUP BY DATE(extraction_date)
ORDER BY extraction_day DESC;

-- ============================================================================
-- Statistical Queries
-- ============================================================================

-- 12. Get min, max, avg for first embedding dimension
SELECT 
    MIN(embedding_0) as min_value,
    MAX(embedding_0) as max_value,
    AVG(embedding_0) as avg_value,
    STDDEV(embedding_0) as std_dev
FROM satellite_embeddings;

-- 13. Find municipalities with extreme embedding values
SELECT 
    municipality_name,
    state_code,
    embedding_0
FROM satellite_embeddings
WHERE embedding_0 = (SELECT MAX(embedding_0) FROM satellite_embeddings)
   OR embedding_0 = (SELECT MIN(embedding_0) FROM satellite_embeddings);

-- 14. Percentile analysis for embedding_0
SELECT 
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY embedding_0) as q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY embedding_0) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY embedding_0) as q3
FROM satellite_embeddings;

-- ============================================================================
-- Time-based Queries
-- ============================================================================

-- 15. Get latest embedding for each municipality
SELECT DISTINCT ON (municipality_id)
    municipality_id,
    municipality_name,
    state_code,
    extraction_date,
    embedding_0,
    embedding_1
FROM satellite_embeddings
ORDER BY municipality_id, extraction_date DESC;

-- 16. Compare embeddings over time (if multiple extractions exist)
SELECT 
    municipality_id,
    municipality_name,
    extraction_date,
    embedding_0,
    LAG(embedding_0) OVER (PARTITION BY municipality_id ORDER BY extraction_date) as previous_embedding_0,
    embedding_0 - LAG(embedding_0) OVER (PARTITION BY municipality_id ORDER BY extraction_date) as change
FROM satellite_embeddings
WHERE municipality_id = '3550308'
ORDER BY extraction_date;

-- ============================================================================
-- Data Quality Queries
-- ============================================================================

-- 17. Check for NULL values in embeddings
SELECT 
    COUNT(*) as total_records,
    COUNT(embedding_0) as non_null_emb_0,
    COUNT(*) - COUNT(embedding_0) as null_emb_0,
    COUNT(embedding_1) as non_null_emb_1,
    COUNT(*) - COUNT(embedding_1) as null_emb_1
FROM satellite_embeddings;

-- 18. Find records with any NULL embeddings
SELECT 
    municipality_id,
    municipality_name,
    CASE 
        WHEN embedding_0 IS NULL THEN 'embedding_0'
        WHEN embedding_1 IS NULL THEN 'embedding_1'
        -- Add more checks as needed
        ELSE 'other'
    END as null_column
FROM satellite_embeddings
WHERE embedding_0 IS NULL 
   OR embedding_1 IS NULL 
   OR embedding_2 IS NULL;

-- 19. Check for duplicate municipalities (same extraction date)
SELECT 
    municipality_id,
    extraction_date,
    COUNT(*) as duplicate_count
FROM satellite_embeddings
GROUP BY municipality_id, extraction_date
HAVING COUNT(*) > 1;

-- ============================================================================
-- Advanced Queries
-- ============================================================================

-- 20. Calculate Euclidean distance between two municipalities (first 5 dimensions)
WITH municipality_a AS (
    SELECT embedding_0, embedding_1, embedding_2, embedding_3, embedding_4
    FROM satellite_embeddings
    WHERE municipality_id = '3550308'  -- São Paulo
    LIMIT 1
),
municipality_b AS (
    SELECT embedding_0, embedding_1, embedding_2, embedding_3, embedding_4
    FROM satellite_embeddings
    WHERE municipality_id = '3304557'  -- Rio de Janeiro
    LIMIT 1
)
SELECT 
    SQRT(
        POWER(a.embedding_0 - b.embedding_0, 2) +
        POWER(a.embedding_1 - b.embedding_1, 2) +
        POWER(a.embedding_2 - b.embedding_2, 2) +
        POWER(a.embedding_3 - b.embedding_3, 2) +
        POWER(a.embedding_4 - b.embedding_4, 2)
    ) as euclidean_distance
FROM municipality_a a, municipality_b b;

-- 21. Find top 10 municipalities with highest embedding_0 values
SELECT 
    municipality_name,
    state_code,
    embedding_0,
    RANK() OVER (ORDER BY embedding_0 DESC) as rank
FROM satellite_embeddings
ORDER BY embedding_0 DESC
LIMIT 10;

-- 22. Get embedding statistics by state
SELECT 
    state_code,
    COUNT(*) as municipality_count,
    AVG(embedding_0) as avg_emb_0,
    STDDEV(embedding_0) as stddev_emb_0,
    MIN(embedding_0) as min_emb_0,
    MAX(embedding_0) as max_emb_0
FROM satellite_embeddings
GROUP BY state_code
ORDER BY state_code;

-- ============================================================================
-- Export Queries
-- ============================================================================

-- 23. Export data for specific state to CSV (run in psql)
-- \copy (SELECT * FROM satellite_embeddings WHERE state_code = 'SP') TO 'sp_embeddings.csv' CSV HEADER;

-- 24. Export summary statistics to CSV
-- \copy (SELECT state_code, COUNT(*) as count, AVG(embedding_0) as avg_emb FROM satellite_embeddings GROUP BY state_code) TO 'state_summary.csv' CSV HEADER;

-- ============================================================================
-- Maintenance Queries
-- ============================================================================

-- 25. Check table size
SELECT 
    pg_size_pretty(pg_total_relation_size('satellite_embeddings')) as total_size,
    pg_size_pretty(pg_relation_size('satellite_embeddings')) as table_size,
    pg_size_pretty(pg_indexes_size('satellite_embeddings')) as indexes_size;

-- 26. Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE tablename = 'satellite_embeddings';

-- 27. Analyze table statistics (run to update query planner)
ANALYZE satellite_embeddings;

-- 28. Vacuum table (cleanup and optimize)
VACUUM ANALYZE satellite_embeddings;

-- ============================================================================
-- Using Views
-- ============================================================================

-- 29. Query the latest_embeddings view
SELECT * FROM latest_embeddings
WHERE state_code = 'SP'
ORDER BY municipality_name;

-- 30. Query the state_summary view
SELECT * FROM state_summary
ORDER BY municipality_count DESC;

-- ============================================================================
-- Custom Analysis Examples
-- ============================================================================

-- 31. Find municipalities with similar embeddings (cosine similarity - simplified)
-- Note: This is a simplified version. For production, consider using pgvector extension
WITH target AS (
    SELECT embedding_0, embedding_1, embedding_2
    FROM satellite_embeddings
    WHERE municipality_id = '3550308'
    LIMIT 1
)
SELECT 
    s.municipality_name,
    s.state_code,
    (s.embedding_0 * t.embedding_0 + 
     s.embedding_1 * t.embedding_1 + 
     s.embedding_2 * t.embedding_2) as similarity_score
FROM satellite_embeddings s, target t
WHERE s.municipality_id != '3550308'
ORDER BY similarity_score DESC
LIMIT 10;

-- 32. Identify outliers using z-score (embedding_0)
WITH stats AS (
    SELECT 
        AVG(embedding_0) as mean,
        STDDEV(embedding_0) as stddev
    FROM satellite_embeddings
)
SELECT 
    municipality_name,
    state_code,
    embedding_0,
    (embedding_0 - stats.mean) / stats.stddev as z_score
FROM satellite_embeddings, stats
WHERE ABS((embedding_0 - stats.mean) / stats.stddev) > 3
ORDER BY ABS((embedding_0 - stats.mean) / stats.stddev) DESC;

-- ============================================================================
-- End of Sample Queries
-- ============================================================================
