"""
Google Earth Engine Satellite Embedding Extraction

This script extracts 64-dimensional satellite embeddings for all Brazilian municipalities
using Google Earth Engine's Satellite Embedding V1 dataset.

Author: iGuide Project Team
Date: 2026-01-28
"""

import ee
import os
import sys
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.gee_auth import authenticate_gee
from src.utils.logger_config import setup_logger


class SatelliteEmbeddingExtractor:
    """Extract satellite embeddings for Brazilian municipalities using GEE."""

    def __init__(self, config_path: str = None):
        """
        Initialize the extractor.

        Args:
            config_path: Path to configuration file
        """
        # Load environment variables
        load_dotenv()

        # Load configuration
        if config_path is None:
            config_path = project_root / "config" / "gee_config.yaml"

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Setup logging
        setup_logger()
        logger.info("Initializing Satellite Embedding Extractor")

        # Authenticate GEE
        self.project_id = os.getenv("GEE_PROJECT_ID")
        authenticate_gee(self.project_id)

        # GEE parameters
        self.scale = self.config["gee"]["scale"]
        self.max_pixels = int(self.config["gee"]["max_pixels"])

    def load_municipality_boundaries(self):
        """
        Load Brazilian municipality boundaries from GEE.

        Returns:
            ee.FeatureCollection: Municipality boundaries
        """
        logger.info("Loading Brazilian municipality boundaries")

        # Using IBGE municipality boundaries
        # Note: You may need to upload your own asset or use a different source
        # This is a placeholder - adjust based on available GEE assets

        try:
            # Option 1: Use FAO GAUL dataset (has Brazil admin boundaries)
            municipalities = ee.FeatureCollection("FAO/GAUL/2015/level2").filter(
                ee.Filter.eq("ADM0_NAME", "Brazil")
            )

            logger.info(f"Loaded municipality boundaries")
            return municipalities

        except Exception as e:
            logger.error(f"Error loading municipality boundaries: {e}")
            logger.info(
                "You may need to upload IBGE municipality boundaries as a GEE asset"
            )
            raise

    def get_satellite_embedding(self, geometry, municipality_name):
        """
        Compute mean satellite embedding for a given geometry.

        Args:
            geometry: ee.Geometry of the municipality
            municipality_name: Name of the municipality for logging

        Returns:
            dict: Dictionary with embedding values
        """
        try:
            # Load Google Satellite Embedding dataset
            # Note: This is a placeholder - adjust based on actual GEE asset name
            # The actual asset path may be different
            embedding_image = ee.Image("GOOGLE/Research/open-buildings-embeddings/v1")

            # Compute mean embedding over the municipality
            mean_embedding = embedding_image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=self.scale,
                maxPixels=self.max_pixels,
            )

            # Get the computed values
            embedding_dict = mean_embedding.getInfo()

            logger.debug(f"Extracted embedding for {municipality_name}")
            return embedding_dict

        except Exception as e:
            logger.error(f"Error extracting embedding for {municipality_name}: {e}")
            return None

    def extract_all_embeddings(self):
        """
        Extract embeddings for all Brazilian municipalities.

        Returns:
            pd.DataFrame: DataFrame with municipality data and embeddings
        """
        logger.info("Starting extraction of all municipality embeddings")

        # Load municipalities
        municipalities = self.load_municipality_boundaries()

        # Get municipality list
        municipality_list = municipalities.toList(municipalities.size())
        num_municipalities = municipality_list.size().getInfo()

        logger.info(f"Processing {num_municipalities} municipalities")

        results = []
        batch_size = self.config["processing"]["batch_size"]

        for i in range(0, num_municipalities, batch_size):
            batch_end = min(i + batch_size, num_municipalities)
            logger.info(
                f"Processing batch {i//batch_size + 1}: municipalities {i} to {batch_end}"
            )

            for j in range(i, batch_end):
                try:
                    # Get municipality feature
                    municipality = ee.Feature(municipality_list.get(j))
                    properties = municipality.getInfo()["properties"]
                    geometry = municipality.geometry()

                    # Extract identifiers
                    municipality_name = properties.get("ADM2_NAME", f"Unknown_{j}")
                    state_name = properties.get("ADM1_NAME", "Unknown")
                    municipality_id = properties.get("ADM2_CODE", str(j))

                    logger.info(f"Processing: {municipality_name}, {state_name}")

                    # Get embedding
                    embedding = self.get_satellite_embedding(
                        geometry, municipality_name
                    )

                    if embedding:
                        # Prepare result
                        result = {
                            "municipality_id": municipality_id,
                            "municipality_name": municipality_name,
                            "state_name": state_name,
                            "extraction_date": datetime.now().isoformat(),
                        }

                        # Add embedding dimensions
                        for key, value in embedding.items():
                            result[key] = value

                        results.append(result)

                except Exception as e:
                    logger.error(f"Error processing municipality {j}: {e}")
                    continue

        # Convert to DataFrame
        df = pd.DataFrame(results)
        logger.info(f"Extraction complete. Processed {len(df)} municipalities")

        return df

    def export_to_csv(self, df: pd.DataFrame, output_path: str = None):
        """
        Export DataFrame to CSV.

        Args:
            df: DataFrame to export
            output_path: Path to save CSV file
        """
        if output_path is None:
            output_dir = project_root / "data" / "processed"
            output_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"municipality_embeddings_{timestamp}.csv"

        df.to_csv(output_path, index=False)
        logger.info(f"Exported data to {output_path}")

        return output_path

    def export_to_drive(self, df: pd.DataFrame):
        """
        Export DataFrame to Google Drive using GEE.

        Args:
            df: DataFrame to export
        """
        logger.info("Exporting to Google Drive")

        # Convert DataFrame to GEE FeatureCollection
        features = []
        for _, row in df.iterrows():
            properties = row.to_dict()
            feature = ee.Feature(None, properties)
            features.append(feature)

        feature_collection = ee.FeatureCollection(features)

        # Export task
        folder_id = os.getenv("GDRIVE_FOLDER_ID")
        filename = os.getenv(
            "GDRIVE_OUTPUT_FILENAME", "brazilian_municipalities_embeddings"
        )

        task = ee.batch.Export.table.toDrive(
            collection=feature_collection,
            description="Export_Municipality_Embeddings",
            folder=folder_id,
            fileNamePrefix=filename,
            fileFormat="CSV",
        )

        task.start()
        logger.info(f"Export task started. Task ID: {task.id}")
        logger.info("Check Google Earth Engine Tasks tab for progress")

        return task


def main():
    """Main execution function."""
    try:
        # Initialize extractor
        extractor = SatelliteEmbeddingExtractor()

        # Extract embeddings
        df = extractor.extract_all_embeddings()

        # Export locally
        local_path = extractor.export_to_csv(df)
        logger.info(f"Local export complete: {local_path}")

        # Export to Google Drive
        task = extractor.export_to_drive(df)
        logger.info("Google Drive export initiated")

        logger.success("Extraction process completed successfully!")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


if __name__ == "__main__":
    main()
