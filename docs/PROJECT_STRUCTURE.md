# iGuide Project - Modular Data Science Pipeline

## Project Vision

This project implements a complete data science pipeline for environmental analysis of Brazilian municipalities:

1. **Data Collection** - Satellite embeddings from Google Earth Engine
2. **Data Integration** - Join satellite data with other datasets
3. **Feature Engineering** - Create derived features and transformations
4. **Modeling** - Train and evaluate machine learning models
5. **Analysis** - Statistical analysis and insights
6. **Visualization** - Interactive plots and dashboards

---

## Project Structure

```
iguide_project/
├── 📂 data/                          # Data storage
│   ├── raw/                          # Raw data sources
│   │   ├── satellite/                # Satellite embeddings
│   │   ├── demographic/              # Population, census data
│   │   ├── economic/                 # GDP, employment, etc.
│   │   ├── environmental/            # Climate, vegetation, etc.
│   │   └── geographic/               # Boundaries, coordinates
│   ├── processed/                    # Cleaned and processed data
│   ├── integrated/                   # Merged datasets
│   └── features/                     # Engineered features
│
├── 📂 src/                           # Source code
│   ├── 1_collection/                 # Phase 1: Data Collection
│   │   ├── gee/                      # Google Earth Engine
│   │   │   ├── extract_embeddings.py
│   │   │   └── extract_embeddings_efficient.py
│   │   ├── demographic/              # Demographic data collectors
│   │   ├── economic/                 # Economic data collectors
│   │   └── environmental/            # Environmental data collectors
│   │
│   ├── 2_integration/                # Phase 2: Data Integration
│   │   ├── merge_datasets.py         # Join multiple data sources
│   │   ├── data_validation.py        # Validate merged data
│   │   └── quality_checks.py         # Data quality assurance
│   │
│   ├── 3_features/                   # Phase 3: Feature Engineering
│   │   ├── feature_extraction.py     # Extract features
│   │   ├── transformations.py        # Data transformations
│   │   └── dimensionality_reduction.py  # PCA, t-SNE, etc.
│   │
│   ├── 4_modeling/                   # Phase 4: Machine Learning
│   │   ├── train.py                  # Model training
│   │   ├── evaluate.py               # Model evaluation
│   │   ├── predict.py                # Make predictions
│   │   └── models/                   # Model definitions
│   │       ├── clustering.py         # Clustering models
│   │       ├── regression.py         # Regression models
│   │       └── classification.py     # Classification models
│   │
│   ├── 5_analysis/                   # Phase 5: Statistical Analysis
│   │   ├── descriptive_stats.py      # Descriptive statistics
│   │   ├── correlation_analysis.py   # Correlation studies
│   │   ├── spatial_analysis.py       # Spatial statistics
│   │   └── time_series.py            # Temporal analysis
│   │
│   ├── 6_visualization/              # Phase 6: Visualization
│   │   ├── plots.py                  # Static plots
│   │   ├── maps.py                   # Geographic visualizations
│   │   ├── dashboards.py             # Interactive dashboards
│   │   └── reports.py                # Automated reports
│   │
│   ├── preprocessing/                # Data preprocessing utilities
│   │   ├── process_satellite_data.py
│   │   └── database_integration.py
│   │
│   └── utils/                        # Shared utilities
│       ├── gee_auth.py
│       ├── logger_config.py
│       ├── memory_utils.py
│       ├── database.py               # Database helpers
│       ├── file_io.py                # File I/O utilities
│       └── config_loader.py          # Configuration management
│
├── 📂 notebooks/                     # Jupyter notebooks
│   ├── 01_data_exploration/          # Exploratory data analysis
│   ├── 02_feature_analysis/          # Feature analysis
│   ├── 03_model_experiments/         # Model experimentation
│   └── 04_visualization_demos/       # Visualization examples
│
├── 📂 models/                        # Saved models
│   ├── trained/                      # Trained model files
│   ├── checkpoints/                  # Training checkpoints
│   └── configs/                      # Model configurations
│
├── 📂 outputs/                       # Analysis outputs
│   ├── figures/                      # Generated plots
│   ├── reports/                      # Analysis reports
│   ├── tables/                       # Result tables
│   └── exports/                      # Data exports
│
├── 📂 config/                        # Configuration files
│   ├── gee_config.yaml               # GEE settings
│   ├── database_config.yaml          # Database settings
│   ├── model_config.yaml             # Model parameters
│   └── visualization_config.yaml     # Viz settings
│
├── 📂 sql/                           # SQL scripts
│   ├── create_tables.sql
│   ├── sample_queries.sql
│   └── views.sql
│
├── 📂 scripts/                       # Automation scripts
│   ├── run_pipeline.py               # Run full pipeline
│   ├── run_collection.py             # Run data collection
│   ├── run_integration.py            # Run data integration
│   ├── run_modeling.py               # Run modeling
│   └── run_analysis.py               # Run analysis
│
├── 📂 tests/                         # Unit tests
│   ├── test_collection/
│   ├── test_integration/
│   ├── test_features/
│   ├── test_modeling/
│   └── test_visualization/
│
├── 📂 docs/                          # Documentation
│   ├── ARCHITECTURE.md
│   ├── QUICKSTART.md
│   ├── POSTGRESQL_SETUP.md
│   ├── MEMORY_OPTIMIZATION.md
│   ├── DATA_SOURCES.md               # Data source documentation
│   ├── MODELING_GUIDE.md             # Modeling guidelines
│   └── VISUALIZATION_GUIDE.md        # Visualization guide
│
├── 📄 README.md                      # Main documentation
├── 📄 requirements.txt               # Python dependencies
├── 📄 setup.py                       # Setup script
├── 📄 .env.example                   # Environment template
└── 📄 .gitignore                     # Git ignore rules
```

---

## Pipeline Phases

### **Phase 1: Data Collection** 🛰️

**Status**: ✅ Implemented

**Components:**

- Satellite embedding extraction (GEE)
- Memory-efficient processing
- PostgreSQL integration

**Next Steps:**

- Add demographic data collectors
- Add economic data collectors
- Add environmental data collectors

---

### **Phase 2: Data Integration** 🔗

**Status**: 🔄 To be implemented

**Purpose:**

- Merge satellite data with other datasets
- Handle missing values and inconsistencies
- Create unified dataset for analysis

**Key Files:**

- `src/2_integration/merge_datasets.py`
- `src/2_integration/data_validation.py`

---

### **Phase 3: Feature Engineering** ⚙️

**Status**: 🔄 To be implemented

**Purpose:**

- Extract meaningful features from raw data
- Apply transformations (normalization, scaling)
- Reduce dimensionality if needed

**Key Files:**

- `src/3_features/feature_extraction.py`
- `src/3_features/transformations.py`

---

### **Phase 4: Modeling** 🤖

**Status**: 🔄 To be implemented

**Purpose:**

- Train machine learning models
- Evaluate model performance
- Make predictions

**Potential Models:**

- Clustering (group similar municipalities)
- Regression (predict outcomes)
- Classification (categorize municipalities)

**Key Files:**

- `src/4_modeling/train.py`
- `src/4_modeling/evaluate.py`

---

### **Phase 5: Analysis** 📊

**Status**: 🔄 To be implemented

**Purpose:**

- Statistical analysis of results
- Correlation studies
- Spatial analysis

**Key Files:**

- `src/5_analysis/descriptive_stats.py`
- `src/5_analysis/spatial_analysis.py`

---

### **Phase 6: Visualization** 📈

**Status**: 🔄 To be implemented

**Purpose:**

- Create static plots
- Generate interactive maps
- Build dashboards
- Produce reports

**Key Files:**

- `src/6_visualization/plots.py`
- `src/6_visualization/maps.py`
- `src/6_visualization/dashboards.py`

---

## Workflow Example

```bash
# 1. Collect satellite data
python src/1_collection/gee/extract_embeddings_efficient.py --mode streaming

# 2. Collect other data sources
python src/1_collection/demographic/collect_census_data.py
python src/1_collection/economic/collect_gdp_data.py

# 3. Integrate all datasets
python src/2_integration/merge_datasets.py --output data/integrated/full_dataset.csv

# 4. Engineer features
python src/3_features/feature_extraction.py --input data/integrated/full_dataset.csv

# 5. Train models
python src/4_modeling/train.py --model clustering --config config/model_config.yaml

# 6. Analyze results
python src/5_analysis/descriptive_stats.py --results models/trained/clustering_results.pkl

# 7. Visualize
python src/6_visualization/maps.py --results models/trained/clustering_results.pkl

# Or run entire pipeline
python scripts/run_pipeline.py --config config/pipeline_config.yaml
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Collection Phase                         │
├─────────────────────────────────────────────────────────────────┤
│  Satellite → GEE Extraction → data/raw/satellite/               │
│  Demographics → Census API → data/raw/demographic/              │
│  Economic → IBGE/API → data/raw/economic/                       │
│  Environmental → Climate API → data/raw/environmental/          │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Data Integration Phase                         │
├─────────────────────────────────────────────────────────────────┤
│  Merge by municipality_id → data/integrated/                    │
│  Validate & Clean → Quality Checks                              │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Feature Engineering Phase                        │
├─────────────────────────────────────────────────────────────────┤
│  Extract Features → Transform → data/features/                  │
│  Normalize, Scale, PCA, etc.                                    │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Modeling Phase                              │
├─────────────────────────────────────────────────────────────────┤
│  Train Models → Evaluate → models/trained/                      │
│  Clustering, Regression, Classification                          │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Analysis Phase                              │
├─────────────────────────────────────────────────────────────────┤
│  Statistical Analysis → Insights → outputs/reports/             │
│  Correlations, Spatial Analysis, etc.                           │
└────────────────────────┬────────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Visualization Phase                            │
├─────────────────────────────────────────────────────────────────┤
│  Plots, Maps, Dashboards → outputs/figures/                     │
│  Interactive Reports → outputs/reports/                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### **1. Modularity**

- Each phase is independent
- Can run phases separately or together
- Easy to add new data sources or models

### **2. Scalability**

- Memory-efficient processing
- Database integration for large datasets
- Parallel processing where applicable

### **3. Reproducibility**

- Configuration files for all parameters
- Version control for code and configs
- Logging for all operations

### **4. Extensibility**

- Easy to add new data sources
- Pluggable model architectures
- Flexible visualization options

---

## Current Status

✅ **Completed:**

- Phase 1: Satellite data collection (GEE)
- Memory optimization
- PostgreSQL integration
- Documentation and testing framework

🔄 **Next Steps:**

1. Create directory structure for all phases
2. Add data integration module
3. Implement feature engineering
4. Set up modeling framework
5. Create visualization templates

---

## Technology Stack

### **Data Collection**

- Google Earth Engine API
- Requests (for APIs)
- BeautifulSoup (for web scraping)

### **Data Processing**

- pandas, numpy
- geopandas (spatial data)
- SQLAlchemy (database)

### **Modeling**

- scikit-learn (ML models)
- scipy (statistical analysis)
- statsmodels (time series)

### **Visualization**

- matplotlib, seaborn (static plots)
- plotly (interactive plots)
- folium (maps)
- dash (dashboards)

---

**Last Updated**: 2026-01-28
**Current Phase**: Data Collection (Phase 1)
**Next Phase**: Data Integration (Phase 2)
