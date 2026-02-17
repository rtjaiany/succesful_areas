"""
Integrate Business Status with Cities Data.

This script merges the processed cities features with the business status data
to create a final analytical dataset.
"""

import pandas as pd
from pathlib import Path
from loguru import logger


class DataIntegrator:
    def __init__(
        self,
        cities_path: str = "data/processed/integrated_cities_data.csv",
        business_path: str = "data/raw/business_data/business_status.csv",
        output_path: str = "data/processed/final_integrated_data.csv",
    ):
        self.cities_path = Path(cities_path)
        self.business_path = Path(business_path)
        self.output_path = Path(output_path)

    def _standardize_id(self, series):
        """Standardizes IDs to 7-digit strings."""
        return series.astype(str).str.split(".").str[0].str.zfill(7)

    def integrate(self):
        logger.info("Starting final data integration...")

        # 1. Load datasets
        if not self.cities_path.exists():
            logger.error(f"Cities data not found at {self.cities_path}")
            return
        if not self.business_path.exists():
            logger.error(f"Business data not found at {self.business_path}")
            return

        logger.info("Loading cities data...")
        cities_df = pd.read_csv(self.cities_path)

        logger.info("Loading business status data...")
        business_df = pd.read_csv(self.business_path)

        # 2. Standardize IDs
        logger.info("Standardizing IBGE codes for merging...")
        cities_df["cod_ibge"] = self._standardize_id(cities_df["cod_ibge"])
        business_df["cod_ibge"] = self._standardize_id(business_df["cod_cidade"])

        # Drop the old cod_cidade as requested
        business_df.drop(columns=["cod_cidade"], inplace=True)

        # 3. Merge
        logger.info("Merging datasets...")
        # Since business_df has multiple rows per city, we use it as the base (left)
        # to attach city features to every business record.
        final_df = pd.merge(business_df, cities_df, on="cod_ibge", how="left")

        # 4. Final adjustments
        # Reorder columns: ID, names, description, business stats, then city stats
        fixed_cols = [
            "cod_ibge",
            "municipality_name",
            "state_name",
            "secao_cnae",
            "description",
        ]
        other_cols = [c for c in final_df.columns if c not in fixed_cols]
        final_df = final_df[fixed_cols + other_cols]

        logger.success(f"Integration complete! Final shape: {final_df.shape}")

        # 5. Save
        final_df.to_csv(self.output_path, index=False)
        logger.info(f"Final dataset saved to: {self.output_path}")


if __name__ == "__main__":
    integrator = DataIntegrator()
    integrator.integrate()
