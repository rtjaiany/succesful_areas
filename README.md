# iGuide Project - Satellite Data Collection

## Overview

This project extracts environmental features from satellite imagery for Brazilian municipalities using Google Earth Engine (GEE) without downloading raw imagery.

## Project Structure

```
iguide_project/
├── data/
│   ├── raw/              # Raw data (gitignored)
│   └── processed/        # Processed CSV outputs
├── src/
│   ├── gee/              # Google Earth Engine scripts
│   ├── preprocessing/    # Data preprocessing modules
│   └── utils/            # Utility functions
├── config/               # Configuration files
├── notebooks/            # Jupyter notebooks for exploration
├── tests/                # Unit tests
├── docs/                 # Additional documentation
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## Features

- **Satellite Data Extraction**: Compute mean 64-dimensional embeddings from Google Satellite Embedding V1
- **Municipality Coverage**: Process all Brazilian municipalities
- **Automated Pipeline**: Python/GEE integration for seamless data extraction
- **Cloud Storage**: Direct output to Google Drive

## Prerequisites

- Python 3.8+
- Google Earth Engine account
- Google Cloud Project (for GEE authentication)
- Google Drive access
- **PostgreSQL 12+** (for database storage)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd iguide_project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

- Google Earth Engine project ID
- Google Drive folder ID
- Other necessary credentials

### 5. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

## Usage

### Extract Satellite Embeddings

#### Option 1: Memory-Efficient Extraction (⭐ Recommended for Production)

For large datasets or systems with limited memory:

```bash
# Streaming mode (incremental writes, minimal memory)
python src/gee/extract_embeddings_efficient.py --mode streaming

# Server-side mode (processing on GEE servers)
python src/gee/extract_embeddings_efficient.py --mode server-side

# Both modes
python src/gee/extract_embeddings_efficient.py --mode both
```

**Benefits:**

- Constant memory usage (~200MB)
- Can handle unlimited dataset sizes
- Writes results incrementally
- Better for long-running tasks

#### Option 2: Standard Extraction

For small datasets or systems with ample RAM:

```bash
python src/gee/extract_embeddings.py
```

**Note:** See `docs/MEMORY_OPTIMIZATION.md` for detailed comparison and recommendations.

### What the Extraction Does

1. Connect to Google Earth Engine
2. Load Brazilian municipality boundaries
3. Compute mean 64-dimensional embeddings for each municipality
4. Export results to CSV (and optionally Google Drive)

### Data Preprocessing

Process the exported CSV data:

```bash
python src/preprocessing/process_satellite_data.py data/processed/municipality_embeddings_*.csv
```

## Configuration

Configuration files are located in the `config/` directory:

- `gee_config.yaml`: Google Earth Engine settings
- `municipalities.yaml`: Municipality boundary settings
- `export_config.yaml`: Export and output settings

## Output

The main output is a CSV file with the following structure:

| Column                      | Description                               |
| --------------------------- | ----------------------------------------- |
| municipality_id             | Unique identifier for the municipality    |
| municipality_name           | Name of the municipality                  |
| state                       | State code                                |
| embedding_0 to embedding_63 | 64-dimensional satellite embedding values |
| extraction_date             | Date of data extraction                   |

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Format code using:

```bash
black src/
flake8 src/
```

## Database Integration (PostgreSQL)

### Setup PostgreSQL

**Detailed guide**: See `docs/POSTGRESQL_SETUP.md`

#### Quick Setup

1. **Install PostgreSQL** (if not already installed)
    - Download from [postgresql.org](https://www.postgresql.org/download/)
    - Or use package manager: `choco install postgresql` (Windows)

2. **Create Database and User**

    ```bash
    # Connect as postgres superuser
    psql -U postgres

    # In psql, run:
    CREATE DATABASE iguide_db;
    CREATE USER iguide_user WITH PASSWORD 'your_secure_password';
    GRANT ALL PRIVILEGES ON DATABASE iguide_db TO iguide_user;
    \q
    ```

3. **Configure Environment Variables**

    Edit `.env` file:

    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=iguide_db
    DB_USER=iguide_user
    DB_PASSWORD=your_secure_password
    ```

4. **Create Database Tables**

    ```bash
    python src/preprocessing/database_integration.py --create-tables
    ```

5. **Test Connection**
    ```bash
    python test_db_connection.py
    ```

### Database Operations

#### Ingest Data

```bash
python src/preprocessing/database_integration.py --ingest data/processed/your_file.csv
```

#### View Statistics

```bash
python src/preprocessing/database_integration.py --stats
```

#### Query Data

Use the sample queries in `sql/sample_queries.sql` or connect with any PostgreSQL client:

```bash
psql -U iguide_user -d iguide_db
```

### Database Schema

The satellite data table infrastructure includes:

- **Table Schema**: Optimized for storing municipality embeddings (64 dimensions)
- **Indexing**: Efficient querying by municipality, state, and date
- **Data Types**: Appropriate types for embeddings and metadata
- **Views**: Pre-built views for common queries
- **Functions**: Utility functions for data analysis

See `docs/database_schema.md` for detailed schema information.

## Troubleshooting

### GEE Authentication Issues

If you encounter authentication errors:

```bash
earthengine authenticate --force
```

### Memory Errors

For large-scale processing, adjust batch size in `config/gee_config.yaml`

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[Specify your license here]

## Contact

[Your contact information]

## Acknowledgments

- Google Earth Engine for satellite data access
- IBGE for Brazilian municipality boundaries
