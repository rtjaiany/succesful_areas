# 🏛️ Socioeconomic & Business Data

This module handles the integration of disparate government datasets (IBGE, RAIS, Receita Federal) to create a robust socioeconomic profile for each municipality.

## Data Integration Workflow

The integration is performed by `src/treatment/preprocess_cities.py`.

### 1. Dictionary-Driven Extraction

Instead of hardcoding column names for every source file, we use a mapping dictionary (`data/raw/cities_data/dictionary_city.xlsx`).

- **Input**: Multiple `.xlsx` files in `data/raw/cities_data/`.
- **Mapping**: The dictionary maps specific columns in raw files to standardized variables in our dataset (e.g., `Valor Adicionado` → `GDP_val_added`).
- **Merging**: All datasets are joined on the 7-digit **IBGE Municipality Code** (`cod_ibge`).

---

## Key Variables

### 💰 Economy

- **GDP per Capita**: Gross Domestic Product divided by population.
- **Average Salary**: Monthly average salary of formal workers (source: RAIS).
- **HDI**: Human Development Index (Income, Longevity, Education).

### 🏢 Business Activity (CNPJ Data)

Data sourced from **Receita Federal** public records.

- **Active Firms**: Count of companies with `STATUS = ATIVA`.
- **Failed Firms**: Count of companies with `STATUS = BAIXADA`.
- **Head Offices (Matriz)**: Companies that are headquarters.
- **Branches (Filial)**: Companies that are operational branches.

#### Derived Density Metrics

These metrics are calculated during the **Analysis phase** (`src/data_analysis/eda_bayesian.ipynb`) to normalize for municipality size:

| Metric             | Formula                      | Interpretation                               |
| :----------------- | :--------------------------- | :------------------------------------------- |
| **Active Density** | `Active Firms / Area_km2`    | Intensity of economic activity.              |
| **HQ Density**     | `Head Offices / Area_km2`    | Concentration of decision-making centers.    |
| **Branch Density** | `Branches / Area_km2`        | Spread of retail/service operations.         |
| **Failure Rate**   | `Failed / (Active + Failed)` | Municipal business survival (or churn) rate. |

### 👥 Demographics

- **Population**: Resident population (IBGE Census/Estimates).
- **Population Density**: `Population / Area_km2`.

---

## Usage

To re-process the raw socioeconomic files:

```bash
python src/treatment/preprocess_cities.py
```

This will produce `data/processed/integrated_cities_data.csv`, which is later merged with Road and Satellite data in the final integration step.
