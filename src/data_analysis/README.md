# Analysis & Modeling

This module contains the core analytics pipeline focusing on geolocation integration and advanced Bayesian Spatial Modeling.

## Directory Contents

- **`geolocate.ipynb`**: The integration and geolocation notebook. Used to merge external datasets and attach them properly to spatial data for specific municipality tracking.
  - *Dependencies:* Handled via `requirements_geolocate.txt`.
- **`eda_bayesian.ipynb`**: The main analytical notebook. Connects the pipeline’s processed dataset with high-performance exploratory analysis and rigorous site-selection models (BYM2) scaled for spatial distributions using PyMC and JAX.
- **`bayesian_old.ipynb`**: *Archived.* Legacy spatial analysis retained temporarily for reference; will be deleted.

## Usage

You should run these progressively based on the pipeline:

1. Setup geolocation environments using the specific constraints set in `requirements_geolocate.txt`.
2. Process location tagging with `geolocate.ipynb`.
3. Advance to `eda_bayesian.ipynb` to complete empirical reviews and MCMC evaluations.

Please refer to `docs/bayesian_modeling.md` for extended interpretation frameworks.
