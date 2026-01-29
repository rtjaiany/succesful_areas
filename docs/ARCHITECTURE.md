# iGuide Project - Data Flow Architecture

## System Architecture

````
┌─────────────────────────────────────────────────────────────────────┐
│                     iGuide Satellite Data Pipeline                   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: Data Extraction (Google Earth Engine)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐         ┌─────────────────┐                       │
│  │   GEE API    │────────▶│  Municipality   │                       │
│  │ Authenticate │         │   Boundaries    │                       │
│  └──────────────┘         │   (IBGE/FAO)    │                       │
│                           └────────┬────────┘                        │
│                                    │                                 │
│                                    ▼                                 │
│                           ┌─────────────────┐                        │
│                           │  Google Sat.    │                        │
│                           │  Embedding V1   │                        │
│                           │  (64-dim)       │                        │
│                           └────────┬────────┘                        │
│                                    │                                 │
│                                    ▼                                 │
│                           ┌─────────────────┐                        │
│                           │  Compute Mean   │                        │
│                           │  Embeddings     │                        │
│                           │  Per Municip.   │                        │
│                           └────────┬────────┘                        │
│                                    │                                 │
│                    ┌───────────────┴───────────────┐                 │
│                    ▼                               ▼                 │
│           ┌─────────────────┐           ┌──────────────────┐        │
│           │  Local CSV      │           │  Google Drive    │        │
│           │  data/processed/│           │  Export          │        │
│           └─────────────────┘           └──────────────────┘        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: Data Preprocessing                                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐                                                    │
│  │  Raw CSV     │                                                    │
│  │  Input       │                                                    │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐                                                    │
│  │  Validation  │  ◀── Check dimensions, missing values, types      │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐                                                    │
│  │  Cleaning    │  ◀── Remove duplicates, handle NaN/Inf            │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐                                                    │
│  │  Add         │  ◀── Timestamps, data source, metadata            │
│  │  Metadata    │                                                    │
│  └──────┬───────┘                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────┐                                                    │
│  │  Processed   │                                                    │
│  │  CSV Output  │                                                    │
│  └──────────────┘                                                    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: Database Integration (Optional)                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐         ┌─────────────────┐                       │
│  │  Processed   │────────▶│  PostgreSQL     │                       │
│  │  CSV         │         │  Database       │                       │
│  └──────────────┘         └────────┬────────┘                        │
│                                    │                                 │
│                           ┌────────▼────────┐                        │
│                           │ satellite_      │                        │
│                           │ embeddings      │                        │
│                           │ table           │                        │
│                           ├─────────────────┤                        │
│                           │ - id            │                        │
│                           │ - municipality  │                        │
│                           │ - embeddings    │                        │
│                           │ - metadata      │                        │
│                           └─────────────────┘                        │
│                                    │                                 │
│                           ┌────────▼────────┐                        │
│                           │  Indexes:       │                        │
│                           │  - municipality │                        │
│                           │  - state        │                        │
│                           │  - date         │                        │
│                           └─────────────────┘                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  Data Output Structure                                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  CSV Columns:                                                        │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │ municipality_id     │ "3550308"                             │     │
│  │ municipality_name   │ "São Paulo"                           │     │
│  │ state_code          │ "SP"                                  │     │
│  │ state_name          │ "São Paulo"                           │     │
│  │ embedding_0         │ 0.1234                                │     │
│  │ embedding_1         │ -0.5678                               │     │
│  │ ...                 │ ...                                   │     │
│  │ embedding_63        │ 0.9012                                │     │
│  │ extraction_date     │ "2026-01-28T20:57:18"                 │     │
│  │ data_source         │ "Google Satellite Embedding V1"       │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

## Key Components

### 1. GEE Extraction (`src/gee/extract_embeddings.py`)
   - Authenticates with Google Earth Engine
   - Loads municipality boundaries
   - Computes mean embeddings for each municipality
   - Exports to CSV and Google Drive

### 2. Preprocessing (`src/preprocessing/process_satellite_data.py`)
   - Validates data quality
   - Cleans and standardizes data
   - Adds metadata
   - Generates summary statistics

### 3. Database Integration (`src/preprocessing/database_integration.py`)
   - Creates database schema
   - Ingests CSV data
   - Provides query functions
   - Manages indexes

### 4. Utilities (`src/utils/`)
   - GEE authentication
   - Logging configuration
   - Helper functions

## Workflow Execution

```bash
# 1. Setup environment
python setup.py

# 2. Activate virtual environment
.\venv\Scripts\activate  # Windows

# 3. Authenticate GEE
earthengine authenticate

# 4. Extract satellite data
python src/gee/extract_embeddings.py

# 5. Preprocess data
python src/preprocessing/process_satellite_data.py data/processed/municipality_embeddings_*.csv

# 6. (Optional) Ingest to database
python src/preprocessing/database_integration.py --create-tables
python src/preprocessing/database_integration.py --ingest data/processed/processed_embeddings_*.csv
````

## Technology Stack

- **Language**: Python 3.8+
- **GEE**: Google Earth Engine API
- **Data Processing**: pandas, numpy, geopandas
- **Database**: PostgreSQL + SQLAlchemy
- **Testing**: pytest
- **Logging**: loguru
- **Configuration**: python-dotenv, PyYAML

## Data Sources

- **Satellite Embeddings**: Google Satellite Embedding V1 (GEE)
- **Boundaries**: IBGE (Instituto Brasileiro de Geografia e Estatística)
- **Alternative Boundaries**: FAO GAUL (Global Administrative Unit Layers)
