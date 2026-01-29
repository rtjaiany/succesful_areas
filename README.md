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

Run the main extraction script:

```bash
python src/gee/extract_embeddings.py
```

This will:

1. Connect to Google Earth Engine
2. Load Brazilian municipality boundaries
3. Compute mean 64-dimensional embeddings for each municipality
4. Export results to Google Drive as CSV

### Data Preprocessing

Process the exported CSV data:

```bash
python src/preprocessing/process_satellite_data.py
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

## Database Integration

The satellite data table infrastructure includes:

- **Table Schema**: Optimized for storing municipality embeddings
- **Indexing**: Efficient querying by municipality and state
- **Data Types**: Appropriate types for embeddings and metadata

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
