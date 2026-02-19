# IBGE Data Collection

This module is responsible for collecting official territorial boundaries and demographic data from the Brazilian Institute of Geography and Statistics (IBGE).

## Features

- **Territorial Boundaries**: Automated download and extraction of 2022 municipality boundary shapefiles (latest official mesh).
- **Standardized Formats**: Downloads the national mesh as a single unified shapefile for consistent cross-referencing.

## Usage

### Collect Municipality Boundaries

To download and extract the official boundaries for a specific year (default 2022):

```bash
python src/ibge/collect_municipalities.py --year 2022
```

## Data Source

Data is fetched from the [IBGE Geosciences Portal](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/).

- **Base URL**: `https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/`

## Output Structure

The collector saves data to `data/raw/ibge/`:

```text
data/raw/ibge/
└── BR_Municipios_2022/
    ├── BR_Municipios_2022.shp
    ├── BR_Municipios_2022.dbf
    ├── BR_Municipios_2022.prj
    └── ...
```

## Next Steps

These shapefiles serve as the spatial backbone for the entire project. They are used in:

1. `src/treatment/calculate_road_metrics.py`: To aggregate road network data per municipality.
2. `src/treatment/integrate_final_dataset.py`: To provide the geometries for the master analytical dataset.
