# Quick Start Guide

## Initial Setup

### 1. Run Setup Script

The easiest way to get started is to run the automated setup script:

```bash
python setup.py
```

This will:

- Create a Python virtual environment
- Install all dependencies
- Create necessary directories
- Set up your `.env` file

### 2. Activate Virtual Environment

**Windows:**

```bash
.\venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

Follow the browser prompts to complete authentication.

### 4. Configure Environment Variables

Edit the `.env` file and add your credentials:

```env
GEE_PROJECT_ID=your-actual-project-id
GDRIVE_FOLDER_ID=your-google-drive-folder-id
```

## Running the Extraction

### Extract Satellite Embeddings

```bash
python src/gee/extract_embeddings.py
```

This will:

1. Connect to Google Earth Engine
2. Load Brazilian municipality boundaries
3. Extract 64-dimensional embeddings for each municipality
4. Save results locally and to Google Drive

### Process the Data

```bash
python src/preprocessing/process_satellite_data.py data/processed/municipality_embeddings_*.csv
```

This will:

1. Validate the data
2. Clean any issues
3. Add metadata
4. Generate summary statistics

### Database Integration (Optional)

#### Create Database Tables

```bash
python src/preprocessing/database_integration.py --create-tables
```

#### Ingest Data

```bash
python src/preprocessing/database_integration.py --ingest data/processed/processed_embeddings_*.csv
```

#### View Statistics

```bash
python src/preprocessing/database_integration.py --stats
```

## Common Issues

### GEE Authentication Fails

If authentication fails, try:

```bash
earthengine authenticate --force
```

### Missing Dependencies

If you encounter import errors:

```bash
pip install -r requirements.txt --upgrade
```

### Database Connection Issues

Make sure PostgreSQL is running and your `.env` file has correct credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iguide_db
DB_USER=your_username
DB_PASSWORD=your_password
```

## Project Structure

```
iguide_project/
├── src/
│   ├── gee/                    # GEE extraction scripts
│   │   └── extract_embeddings.py
│   ├── preprocessing/          # Data processing
│   │   ├── process_satellite_data.py
│   │   └── database_integration.py
│   └── utils/                  # Utilities
│       ├── gee_auth.py
│       └── logger_config.py
├── data/
│   ├── raw/                    # Raw data (gitignored)
│   └── processed/              # Processed outputs
├── config/                     # Configuration files
├── tests/                      # Unit tests
├── docs/                       # Documentation
└── notebooks/                  # Jupyter notebooks
```

## Next Steps

1. **Explore the data**: Use Jupyter notebooks to analyze the extracted embeddings
2. **Integrate with database**: Set up PostgreSQL and ingest the data
3. **Build visualizations**: Create maps and charts of the embeddings
4. **Train models**: Use the embeddings as features for ML models

For detailed documentation, see `README.md` and files in the `docs/` directory.
