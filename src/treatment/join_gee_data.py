"""
Join Cities/Business data with GEE Embeddings.

This script merges the integrated business/cities table with the
satellite embeddings using municipality and state names.
"""

import pandas as pd
import unicodedata
from pathlib import Path
from loguru import logger


class GEEIntegrator:
    def __init__(
        self,
        integrated_path: str = "data/processed/cities_business_integrated.csv",
        embeddings_path: str = "data/processed/municipality_embeddings_20260202_183247.csv",
        output_path: str = "data/processed/city_business_gee.csv",
    ):
        self.integrated_path = Path(integrated_path)
        self.embeddings_path = Path(embeddings_path)
        self.output_path = Path(output_path)

    def _clean_text(self, text):
        """Normalizes text for robust matching (removes accents, title case)."""
        if pd.isna(text) or not isinstance(text, str):
            return text

        # Remove accents
        text = "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )

        # Strip and clean artifacts
        text = text.strip().title()

        return text

    def integrate(self):
        logger.info("Starting GEE data integration...")

        if not self.integrated_path.exists():
            logger.error(f"Integrated file not found: {self.integrated_path}")
            return
        if not self.embeddings_path.exists():
            logger.error(f"Embeddings file not found: {self.embeddings_path}")
            return

        # 1. Load data
        logger.info("Loading datasets...")
        df_base = pd.read_csv(self.integrated_path)
        df_gee = pd.read_csv(self.embeddings_path)

        # 2. Add temporary normalized columns for matching
        logger.info("Normalizing names for matching...")

        # Base data often comes with clean names already, but let's be sure
        df_base["match_name"] = df_base["municipality_name"].apply(self._clean_text)
        df_base["match_state"] = df_base["state_name"].apply(self._clean_text)

        df_gee["match_name"] = df_gee["municipality_name"].apply(self._clean_text)
        df_gee["match_state"] = df_gee["state_name"].apply(self._clean_text)

        # 3. Merge
        logger.info("Merging on municipality and state name...")

        # We drop the duplicate name/state columns from gee before merging
        gee_cols_to_drop = [
            "municipality_name",
            "state_name",
            "municipality_id",
            "state_code",
        ]
        df_gee_unique = df_gee.drop(columns=gee_cols_to_drop)

        final_df = pd.merge(
            df_base, df_gee_unique, on=["match_name", "match_state"], how="left"
        )

        # 4. Cleanup
        logger.info("Cleaning up matching helpers...")
        final_df.drop(columns=["match_name", "match_state"], inplace=True)

        # 5. Save
        logger.success(f"Integration complete! Final shape: {final_df.shape}")
        final_df.to_csv(self.output_path, index=False)
        logger.info(f"Final file saved to: {self.output_path}")


if __name__ == "__main__":
    integrator = GEEIntegrator()
    integrator.integrate()
