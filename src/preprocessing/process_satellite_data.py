"""
Satellite Data Preprocessing

Process and prepare satellite embedding data for database ingestion.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from loguru import logger
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.logger_config import setup_logger


class SatelliteDataPreprocessor:
    """Preprocess satellite embedding data."""

    def __init__(self, input_file: str):
        """
        Initialize preprocessor.

        Args:
            input_file: Path to input CSV file
        """
        setup_logger()
        self.input_file = Path(input_file)
        self.df = None

        logger.info(f"Initializing preprocessor for {input_file}")

    def load_data(self):
        """Load CSV data."""
        logger.info("Loading data from CSV")
        self.df = pd.read_csv(self.input_file)
        logger.info(
            f"Loaded {len(self.df)} records with {len(self.df.columns)} columns"
        )
        return self.df

    def validate_data(self):
        """Validate data quality."""
        logger.info("Validating data quality")

        issues = []

        # Check for missing values
        missing = self.df.isnull().sum()
        if missing.any():
            logger.warning(f"Found missing values:\n{missing[missing > 0]}")
            issues.append("missing_values")

        # Check for duplicate municipalities
        duplicates = self.df.duplicated(subset=["municipality_id"], keep=False)
        if duplicates.any():
            logger.warning(f"Found {duplicates.sum()} duplicate municipality records")
            issues.append("duplicates")

        # Validate embedding dimensions
        embedding_cols = [
            col for col in self.df.columns if col.startswith("embedding_")
        ]
        if len(embedding_cols) != 64:
            logger.error(
                f"Expected 64 embedding dimensions, found {len(embedding_cols)}"
            )
            issues.append("invalid_dimensions")

        # Check for invalid values (NaN, Inf)
        for col in embedding_cols:
            if self.df[col].isnull().any():
                logger.warning(f"Column {col} has null values")
            if np.isinf(self.df[col]).any():
                logger.warning(f"Column {col} has infinite values")

        if not issues:
            logger.success("Data validation passed")
        else:
            logger.warning(f"Data validation found issues: {', '.join(issues)}")

        return issues

    def clean_data(self):
        """Clean and standardize data."""
        logger.info("Cleaning data")

        # Remove duplicates (keep first occurrence)
        original_len = len(self.df)
        self.df = self.df.drop_duplicates(subset=["municipality_id"], keep="first")
        if len(self.df) < original_len:
            logger.info(f"Removed {original_len - len(self.df)} duplicate records")

        # Handle missing values in embeddings (fill with 0 or mean)
        embedding_cols = [
            col for col in self.df.columns if col.startswith("embedding_")
        ]
        for col in embedding_cols:
            if self.df[col].isnull().any():
                # Fill with column mean
                mean_val = self.df[col].mean()
                self.df[col].fillna(mean_val, inplace=True)
                logger.info(f"Filled missing values in {col} with mean: {mean_val:.4f}")

        # Replace infinite values with max/min
        for col in embedding_cols:
            if np.isinf(self.df[col]).any():
                max_val = self.df[col][~np.isinf(self.df[col])].max()
                min_val = self.df[col][~np.isinf(self.df[col])].min()
                self.df[col].replace(
                    [np.inf, -np.inf], [max_val, min_val], inplace=True
                )
                logger.info(f"Replaced infinite values in {col}")

        logger.success("Data cleaning complete")
        return self.df

    def add_metadata(self):
        """Add additional metadata columns."""
        logger.info("Adding metadata")

        # Add processing timestamp
        self.df["processed_date"] = datetime.now().isoformat()

        # Add data source
        if "data_source" not in self.df.columns:
            self.df["data_source"] = "Google Satellite Embedding V1"

        logger.info("Metadata added")
        return self.df

    def export_processed_data(self, output_path: str = None):
        """
        Export processed data.

        Args:
            output_path: Path to save processed CSV
        """
        if output_path is None:
            output_dir = project_root / "data" / "processed"
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"processed_embeddings_{timestamp}.csv"

        self.df.to_csv(output_path, index=False)
        logger.info(f"Exported processed data to {output_path}")

        return output_path

    def generate_summary_stats(self):
        """Generate summary statistics."""
        logger.info("Generating summary statistics")

        embedding_cols = [
            col for col in self.df.columns if col.startswith("embedding_")
        ]

        stats = {
            "total_municipalities": len(self.df),
            "unique_states": (
                self.df["state_name"].nunique()
                if "state_name" in self.df.columns
                else 0
            ),
            "embedding_dimensions": len(embedding_cols),
            "embedding_stats": self.df[embedding_cols].describe().to_dict(),
        }

        logger.info(
            f"Summary: {stats['total_municipalities']} municipalities, "
            f"{stats['unique_states']} states, "
            f"{stats['embedding_dimensions']} dimensions"
        )

        return stats

    def process(self):
        """Run full preprocessing pipeline."""
        logger.info("Starting preprocessing pipeline")

        # Load data
        self.load_data()

        # Validate
        self.validate_data()

        # Clean
        self.clean_data()

        # Add metadata
        self.add_metadata()

        # Generate stats
        stats = self.generate_summary_stats()

        # Export
        output_path = self.export_processed_data()

        logger.success("Preprocessing pipeline complete")

        return self.df, stats, output_path


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description="Preprocess satellite embedding data")
    parser.add_argument("input_file", type=str, help="Path to input CSV file")
    parser.add_argument(
        "--output", type=str, help="Path to output CSV file", default=None
    )

    args = parser.parse_args()

    try:
        preprocessor = SatelliteDataPreprocessor(args.input_file)
        df, stats, output_path = preprocessor.process()

        logger.success(f"Processing complete! Output saved to {output_path}")

    except Exception as e:
        logger.error(f"Processing failed: {e}")
        raise


if __name__ == "__main__":
    main()
