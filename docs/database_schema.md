# Database Schema for Satellite Embeddings

## Table: satellite_embeddings

This table stores the 64-dimensional satellite embeddings for Brazilian municipalities.

### Schema

```sql
CREATE TABLE IF NOT EXISTS satellite_embeddings (
    id SERIAL PRIMARY KEY,
    municipality_id VARCHAR(7) NOT NULL,
    municipality_name VARCHAR(255) NOT NULL,
    state_code VARCHAR(2) NOT NULL,
    state_name VARCHAR(100),

    -- 64-dimensional embedding columns
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
    data_source VARCHAR(100) DEFAULT 'Google Satellite Embedding V1',
    geometry GEOMETRY(MULTIPOLYGON, 4326),  -- Optional: municipality boundary

    -- Constraints
    UNIQUE(municipality_id, extraction_date),
    CHECK(state_code ~ '^[A-Z]{2}$')
);

-- Indexes for efficient querying
CREATE INDEX idx_municipality_id ON satellite_embeddings(municipality_id);
CREATE INDEX idx_state_code ON satellite_embeddings(state_code);
CREATE INDEX idx_extraction_date ON satellite_embeddings(extraction_date);
CREATE INDEX idx_geometry ON satellite_embeddings USING GIST(geometry);
```

### Column Descriptions

| Column                      | Type         | Description                               |
| --------------------------- | ------------ | ----------------------------------------- |
| id                          | SERIAL       | Primary key, auto-incrementing            |
| municipality_id             | VARCHAR(7)   | IBGE municipality code (7 digits)         |
| municipality_name           | VARCHAR(255) | Official municipality name                |
| state_code                  | VARCHAR(2)   | Two-letter state code (e.g., SP, RJ)      |
| state_name                  | VARCHAR(100) | Full state name                           |
| embedding_0 to embedding_63 | FLOAT        | 64-dimensional satellite embedding values |
| extraction_date             | TIMESTAMP    | Date and time of data extraction          |
| data_source                 | VARCHAR(100) | Source of the satellite data              |
| geometry                    | GEOMETRY     | Optional: municipality boundary polygon   |

### Indexes

- **idx_municipality_id**: Fast lookups by municipality
- **idx_state_code**: Filter by state
- **idx_extraction_date**: Time-based queries
- **idx_geometry**: Spatial queries (if geometry is stored)

### Usage Examples

```sql
-- Get embeddings for a specific municipality
SELECT * FROM satellite_embeddings
WHERE municipality_id = '3550308';  -- São Paulo

-- Get all municipalities in a state
SELECT municipality_name, embedding_0, embedding_1
FROM satellite_embeddings
WHERE state_code = 'SP';

-- Get most recent extraction
SELECT * FROM satellite_embeddings
ORDER BY extraction_date DESC
LIMIT 100;

-- Calculate similarity between municipalities (cosine similarity example)
-- This would require a custom function or extension
```

## Alternative: Array Storage

For more efficient storage, embeddings can be stored as arrays:

```sql
CREATE TABLE IF NOT EXISTS satellite_embeddings_array (
    id SERIAL PRIMARY KEY,
    municipality_id VARCHAR(7) NOT NULL,
    municipality_name VARCHAR(255) NOT NULL,
    state_code VARCHAR(2) NOT NULL,
    state_name VARCHAR(100),

    -- Store all embeddings as a single array
    embeddings FLOAT[64] NOT NULL,

    -- Metadata
    extraction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(100) DEFAULT 'Google Satellite Embedding V1',
    geometry GEOMETRY(MULTIPOLYGON, 4326),

    UNIQUE(municipality_id, extraction_date)
);
```

This approach is more compact and can be more efficient for certain operations.
