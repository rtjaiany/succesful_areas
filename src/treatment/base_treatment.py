"""
Base Data Treatment Utilities

This script provides common functions for cleaning and standardizing
geospatial and economic data from different sources.
"""

import pandas as pd
import geopandas as gpd
from pathlib import Path
from loguru import logger


class DataTreater:
    """
    Base class for data treatment operations.
    """

    def __init__(
        self, raw_data_dir: str = "data/raw", processed_data_dir: str = "data/processed"
    ):
        self.raw_dir = Path(raw_data_dir)
        self.processed_dir = Path(processed_data_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def standardize_municipality_id(
        self, df: pd.DataFrame, id_column: str
    ) -> pd.DataFrame:
        """
        Ensures municipality IDs are 7-digit strings (IBGE standard).
        """
        logger.info(f"Standardizing municipality ID column: {id_column}")
        df = df.copy()
        df[id_column] = df[id_column].astype(str).str.zfill(7)
        return df

    def save_processed(self, df: pd.DataFrame, filename: str):
        """
        Saves a processed dataframe to the processed directory.
        """
        output_path = self.processed_dir / filename
        if isinstance(df, gpd.GeoDataFrame):
            df.to_file(output_path, driver="GPKG")
            logger.success(f"Saved processed GeoPackage to: {output_path}")
        else:
            df.to_csv(output_path, index=False)
            logger.success(f"Saved processed CSV to: {output_path}")


def main():
    logger.info("Data treatment module initialized.")
    # This script can be expanded with specific treatment functions as data is added.


if __name__ == "__main__":
    main()
