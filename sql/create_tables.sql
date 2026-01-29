-- ============================================================================
-- iGuide Project - Database Schema Creation
-- ============================================================================
-- Description: Creates tables and indexes for satellite embedding data
-- Author: iGuide Project Team
-- Created: 2026-01-28
-- ============================================================================

-- Drop existing table if exists (use with caution in production!)
-- DROP TABLE IF EXISTS satellite_embeddings CASCADE;

-- ============================================================================
-- Main Table: satellite_embeddings
-- ============================================================================

CREATE TABLE IF NOT EXISTS satellite_embeddings (
    -- Primary Key
    id SERIAL PRIMARY KEY,
    
    -- Municipality Identifiers
    municipality_id VARCHAR(7) NOT NULL,
    municipality_name VARCHAR(255) NOT NULL,
    state_code VARCHAR(2),
    state_name VARCHAR(100),
    
    -- 64-dimensional Satellite Embeddings
    embedding_0 FLOAT,
    embedding_1 FLOAT,
    embedding_2 FLOAT,
    embedding_3 FLOAT,
    embedding_4 FLOAT,
    embedding_5 FLOAT,
    embedding_6 FLOAT,
    embedding_7 FLOAT,
    embedding_8 FLOAT,
    embedding_9 FLOAT,
    embedding_10 FLOAT,
    embedding_11 FLOAT,
    embedding_12 FLOAT,
    embedding_13 FLOAT,
    embedding_14 FLOAT,
    embedding_15 FLOAT,
    embedding_16 FLOAT,
    embedding_17 FLOAT,
    embedding_18 FLOAT,
    embedding_19 FLOAT,
    embedding_20 FLOAT,
    embedding_21 FLOAT,
    embedding_22 FLOAT,
    embedding_23 FLOAT,
    embedding_24 FLOAT,
    embedding_25 FLOAT,
    embedding_26 FLOAT,
    embedding_27 FLOAT,
    embedding_28 FLOAT,
    embedding_29 FLOAT,
    embedding_30 FLOAT,
    embedding_31 FLOAT,
    embedding_32 FLOAT,
    embedding_33 FLOAT,
    embedding_34 FLOAT,
    embedding_35 FLOAT,
    embedding_36 FLOAT,
    embedding_37 FLOAT,
    embedding_38 FLOAT,
    embedding_39 FLOAT,
    embedding_40 FLOAT,
    embedding_41 FLOAT,
    embedding_42 FLOAT,
    embedding_43 FLOAT,
    embedding_44 FLOAT,
    embedding_45 FLOAT,
    embedding_46 FLOAT,
    embedding_47 FLOAT,
    embedding_48 FLOAT,
    embedding_49 FLOAT,
    embedding_50 FLOAT,
    embedding_51 FLOAT,
    embedding_52 FLOAT,
    embedding_53 FLOAT,
    embedding_54 FLOAT,
    embedding_55 FLOAT,
    embedding_56 FLOAT,
    embedding_57 FLOAT,
    embedding_58 FLOAT,
    embedding_59 FLOAT,
    embedding_60 FLOAT,
    embedding_61 FLOAT,
    embedding_62 FLOAT,
    embedding_63 FLOAT,
    
    -- Metadata
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_date TIMESTAMP,
    data_source VARCHAR(100) DEFAULT 'Google Satellite Embedding V1',
    
    -- Optional: Geometry column (requires PostGIS extension)
    -- geometry GEOMETRY(MULTIPOLYGON, 4326),
    
    -- Constraints
    CONSTRAINT unique_municipality_extraction UNIQUE(municipality_id, extraction_date),
    CONSTRAINT valid_state_code CHECK(state_code ~ '^[A-Z]{2}$' OR state_code IS NULL)
);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================

-- Index on municipality_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_municipality_id 
ON satellite_embeddings(municipality_id);

-- Index on state_code for filtering by state
CREATE INDEX IF NOT EXISTS idx_state_code 
ON satellite_embeddings(state_code);

-- Index on extraction_date for time-based queries
CREATE INDEX IF NOT EXISTS idx_extraction_date 
ON satellite_embeddings(extraction_date DESC);

-- Composite index for common queries
CREATE INDEX IF NOT EXISTS idx_state_municipality 
ON satellite_embeddings(state_code, municipality_id);

-- Index on municipality_name for text searches
CREATE INDEX IF NOT EXISTS idx_municipality_name 
ON satellite_embeddings(municipality_name);

-- Optional: Spatial index (requires PostGIS)
-- CREATE INDEX IF NOT EXISTS idx_geometry 
-- ON satellite_embeddings USING GIST(geometry);

-- ============================================================================
-- Comments for Documentation
-- ============================================================================

COMMENT ON TABLE satellite_embeddings IS 
'Stores 64-dimensional satellite embeddings for Brazilian municipalities extracted from Google Earth Engine';

COMMENT ON COLUMN satellite_embeddings.municipality_id IS 
'IBGE municipality code (7 digits)';

COMMENT ON COLUMN satellite_embeddings.municipality_name IS 
'Official municipality name';

COMMENT ON COLUMN satellite_embeddings.state_code IS 
'Two-letter state code (e.g., SP, RJ, BA)';

COMMENT ON COLUMN satellite_embeddings.extraction_date IS 
'Date and time when the data was extracted from GEE';

COMMENT ON COLUMN satellite_embeddings.data_source IS 
'Source of the satellite embedding data';

-- ============================================================================
-- Alternative Table Structure: Using Array for Embeddings
-- ============================================================================

-- Uncomment below if you prefer to store embeddings as an array
-- This is more compact and can be more efficient for certain operations

/*
CREATE TABLE IF NOT EXISTS satellite_embeddings_array (
    id SERIAL PRIMARY KEY,
    municipality_id VARCHAR(7) NOT NULL,
    municipality_name VARCHAR(255) NOT NULL,
    state_code VARCHAR(2),
    state_name VARCHAR(100),
    
    -- Store all 64 embeddings as a single array
    embeddings FLOAT[64] NOT NULL,
    
    -- Metadata
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_date TIMESTAMP,
    data_source VARCHAR(100) DEFAULT 'Google Satellite Embedding V1',
    
    CONSTRAINT unique_municipality_extraction_array UNIQUE(municipality_id, extraction_date),
    CONSTRAINT valid_embeddings_length CHECK(array_length(embeddings, 1) = 64)
);

-- Indexes for array version
CREATE INDEX IF NOT EXISTS idx_municipality_id_array 
ON satellite_embeddings_array(municipality_id);

CREATE INDEX IF NOT EXISTS idx_state_code_array 
ON satellite_embeddings_array(state_code);

CREATE INDEX IF NOT EXISTS idx_extraction_date_array 
ON satellite_embeddings_array(extraction_date DESC);
*/

-- ============================================================================
-- Utility Views
-- ============================================================================

-- View: Latest embeddings for each municipality
CREATE OR REPLACE VIEW latest_embeddings AS
SELECT DISTINCT ON (municipality_id) *
FROM satellite_embeddings
ORDER BY municipality_id, extraction_date DESC;

COMMENT ON VIEW latest_embeddings IS 
'Shows the most recent embedding for each municipality';

-- View: Summary by state
CREATE OR REPLACE VIEW state_summary AS
SELECT 
    state_code,
    state_name,
    COUNT(*) as municipality_count,
    MAX(extraction_date) as latest_extraction,
    MIN(extraction_date) as earliest_extraction
FROM satellite_embeddings
GROUP BY state_code, state_name
ORDER BY state_code;

COMMENT ON VIEW state_summary IS 
'Summary statistics grouped by state';

-- ============================================================================
-- Functions
-- ============================================================================

-- Function: Get embedding vector as array
CREATE OR REPLACE FUNCTION get_embedding_array(rec satellite_embeddings)
RETURNS FLOAT[] AS $$
BEGIN
    RETURN ARRAY[
        rec.embedding_0, rec.embedding_1, rec.embedding_2, rec.embedding_3,
        rec.embedding_4, rec.embedding_5, rec.embedding_6, rec.embedding_7,
        rec.embedding_8, rec.embedding_9, rec.embedding_10, rec.embedding_11,
        rec.embedding_12, rec.embedding_13, rec.embedding_14, rec.embedding_15,
        rec.embedding_16, rec.embedding_17, rec.embedding_18, rec.embedding_19,
        rec.embedding_20, rec.embedding_21, rec.embedding_22, rec.embedding_23,
        rec.embedding_24, rec.embedding_25, rec.embedding_26, rec.embedding_27,
        rec.embedding_28, rec.embedding_29, rec.embedding_30, rec.embedding_31,
        rec.embedding_32, rec.embedding_33, rec.embedding_34, rec.embedding_35,
        rec.embedding_36, rec.embedding_37, rec.embedding_38, rec.embedding_39,
        rec.embedding_40, rec.embedding_41, rec.embedding_42, rec.embedding_43,
        rec.embedding_44, rec.embedding_45, rec.embedding_46, rec.embedding_47,
        rec.embedding_48, rec.embedding_49, rec.embedding_50, rec.embedding_51,
        rec.embedding_52, rec.embedding_53, rec.embedding_54, rec.embedding_55,
        rec.embedding_56, rec.embedding_57, rec.embedding_58, rec.embedding_59,
        rec.embedding_60, rec.embedding_61, rec.embedding_62, rec.embedding_63
    ];
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMENT ON FUNCTION get_embedding_array IS 
'Converts the 64 individual embedding columns into a single array';

-- ============================================================================
-- Grant Permissions
-- ============================================================================

-- Grant permissions to iguide_user (adjust username as needed)
-- GRANT ALL PRIVILEGES ON TABLE satellite_embeddings TO iguide_user;
-- GRANT ALL PRIVILEGES ON SEQUENCE satellite_embeddings_id_seq TO iguide_user;
-- GRANT SELECT ON latest_embeddings TO iguide_user;
-- GRANT SELECT ON state_summary TO iguide_user;

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Check if table was created
SELECT 
    table_name, 
    table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
    AND table_name = 'satellite_embeddings';

-- Check indexes
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'satellite_embeddings';

-- Check constraints
SELECT 
    constraint_name, 
    constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'satellite_embeddings';

-- ============================================================================
-- End of Script
-- ============================================================================

-- Display success message
DO $$
BEGIN
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Table: satellite_embeddings';
    RAISE NOTICE 'Indexes: 5 created';
    RAISE NOTICE 'Views: 2 created';
    RAISE NOTICE 'Functions: 1 created';
END $$;
