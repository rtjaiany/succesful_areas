"""
Memory-Optimized Google Earth Engine Satellite Embedding Extraction

This script extracts 64-dimensional satellite embeddings for all Brazilian municipalities
using Google Earth Engine with optimized memory usage through streaming and chunked processing.

Key optimizations:
- Streaming CSV writes (no full DataFrame in memory)
- Chunked batch processing with garbage collection
- Generator-based iteration
- Incremental file writes
- Memory-efficient data structures

Author: iGuide Project Team
Date: 2026-01-28
"""

import ee
import os
import sys
import yaml
import csv
import gc
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from typing import Iterator, Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.gee_auth import authenticate_gee
from src.utils.logger_config import setup_logger


class MemoryEfficientEmbeddingExtractor:
    """
    Memory-optimized satellite embedding extractor using streaming and chunked processing.

    This class minimizes memory usage by:
    1. Writing results incrementally to CSV (no large DataFrame in memory)
    2. Processing municipalities in small batches with garbage collection
    3. Using generators instead of lists where possible
    4. Clearing processed data immediately after writing
    """

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
        logger.info("Initializing Memory-Efficient Satellite Embedding Extractor")

        # Authenticate GEE
        self.project_id = os.getenv("GEE_PROJECT_ID")
        authenticate_gee(self.project_id)

        # GEE parameters
        self.scale = self.config["gee"]["scale"]
        self.max_pixels = int(self.config["gee"]["max_pixels"])

        # Processing parameters
        self.batch_size = self.config["processing"]["batch_size"]
        self.chunk_size = 10  # Write to disk every N records

        # Output setup
        self.output_path = self._setup_output_path()
        self.csv_file = None
        self.csv_writer = None
        self.records_written = 0

    def _setup_output_path(self) -> Path:
        """Set up output file path."""
        output_dir = project_root / "data" / "processed"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return output_dir / f"municipality_embeddings_{timestamp}.csv"

    def load_municipality_boundaries(self) -> ee.FeatureCollection:
        """
        Load Brazilian municipality boundaries from GEE.

        Returns:
            ee.FeatureCollection: Municipality boundaries
        """
        logger.info("Loading Brazilian municipality boundaries")

        try:
            # Using FAO GAUL dataset (has Brazil admin boundaries)
            municipalities = ee.FeatureCollection("FAO/GAUL/2015/level2").filter(
                ee.Filter.eq("ADM0_NAME", "Brazil")
            )

            logger.info("Loaded municipality boundaries")
            return municipalities

        except Exception as e:
            logger.error(f"Error loading municipality boundaries: {e}")
            logger.info(
                "You may need to upload IBGE municipality boundaries as a GEE asset"
            )
            raise

    def get_satellite_embedding(
        self, geometry: ee.Geometry, municipality_name: str
    ) -> Optional[Dict]:
        """
        Compute mean satellite embedding for a given geometry.

        Args:
            geometry: ee.Geometry of the municipality
            municipality_name: Name of the municipality for logging

        Returns:
            dict: Dictionary with embedding values, or None if error
        """
        try:
            # Load Google Satellite Embedding dataset
            # Note: Adjust asset path based on actual GEE asset
            embedding_image = ee.Image("GOOGLE/Research/open-buildings-embeddings/v1")

            # Compute mean embedding over the municipality
            mean_embedding = embedding_image.reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=geometry,
                scale=self.scale,
                maxPixels=self.max_pixels,
                bestEffort=True,  # Allows GEE to reduce scale if needed
            )

            # Get the computed values (this is the memory-intensive operation)
            embedding_dict = mean_embedding.getInfo()

            logger.debug(f"Extracted embedding for {municipality_name}")
            return embedding_dict

        except Exception as e:
            logger.error(f"Error extracting embedding for {municipality_name}: {e}")
            return None

    def _initialize_csv_writer(self, first_record: Dict):
        """
        Initialize CSV writer with headers from first record.

        Args:
            first_record: First data record to determine columns
        """
        self.csv_file = open(self.output_path, "w", newline="", encoding="utf-8")

        # Define column order
        fieldnames = [
            "municipality_id",
            "municipality_name",
            "state_name",
            "state_code",
        ]

        # Add embedding columns in order
        embedding_cols = sorted(
            [k for k in first_record.keys() if k.startswith("embedding_")]
        )
        fieldnames.extend(embedding_cols)

        # Add metadata columns
        fieldnames.extend(["extraction_date", "data_source"])

        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.csv_writer.writeheader()

        logger.info(f"Initialized CSV writer with {len(fieldnames)} columns")

    def _write_record(self, record: Dict):
        """
        Write a single record to CSV.

        Args:
            record: Data record to write
        """
        if self.csv_writer is None:
            self._initialize_csv_writer(record)

        self.csv_writer.writerow(record)
        self.records_written += 1

        # Flush to disk periodically
        if self.records_written % self.chunk_size == 0:
            self.csv_file.flush()
            logger.debug(f"Flushed {self.records_written} records to disk")

    def _close_csv_writer(self):
        """Close CSV file."""
        if self.csv_file:
            self.csv_file.close()
            logger.info(
                f"Closed CSV file. Total records written: {self.records_written}"
            )

    def process_municipality_batch(
        self, municipality_list: ee.List, start_idx: int, end_idx: int
    ) -> int:
        """
        Process a batch of municipalities and write results incrementally.

        Args:
            municipality_list: EE list of municipalities
            start_idx: Start index of batch
            end_idx: End index of batch

        Returns:
            int: Number of successfully processed municipalities
        """
        batch_num = start_idx // self.batch_size + 1
        logger.info(
            f"Processing batch {batch_num}: municipalities {start_idx} to {end_idx}"
        )

        successful = 0

        for j in range(start_idx, end_idx):
            try:
                # Get municipality feature
                municipality = ee.Feature(municipality_list.get(j))
                properties = municipality.getInfo()["properties"]
                geometry = municipality.geometry()

                # Extract identifiers
                municipality_name = properties.get("ADM2_NAME", f"Unknown_{j}")
                state_name = properties.get("ADM1_NAME", "Unknown")
                state_code = properties.get("ADM1_CODE", "")
                municipality_id = properties.get("ADM2_CODE", str(j))

                logger.info(f"Processing [{j+1}]: {municipality_name}, {state_name}")

                # Get embedding
                embedding = self.get_satellite_embedding(geometry, municipality_name)

                if embedding:
                    # Prepare record
                    record = {
                        "municipality_id": municipality_id,
                        "municipality_name": municipality_name,
                        "state_name": state_name,
                        "state_code": state_code,
                        "extraction_date": datetime.now().isoformat(),
                        "data_source": "Google Satellite Embedding V1",
                    }

                    # Add embedding dimensions
                    record.update(embedding)

                    # Write immediately to CSV (memory-efficient!)
                    self._write_record(record)
                    successful += 1

                    # Clear the embedding dict to free memory
                    del embedding
                    del record

                # Clear properties to free memory
                del properties

            except Exception as e:
                logger.error(f"Error processing municipality {j}: {e}")
                continue

        # Force garbage collection after each batch
        gc.collect()
        logger.info(
            f"Batch {batch_num} complete. Processed {successful} municipalities. Memory cleared."
        )

        return successful

    def extract_all_embeddings_streaming(self) -> Path:
        """
        Extract embeddings for all municipalities using streaming approach.

        This method writes results incrementally to CSV, avoiding memory issues
        with large datasets.

        Returns:
            Path: Path to output CSV file
        """
        logger.info("Starting memory-efficient streaming extraction")

        try:
            # Load municipalities
            municipalities = self.load_municipality_boundaries()

            # Get municipality list
            municipality_list = municipalities.toList(municipalities.size())
            num_municipalities = municipality_list.size().getInfo()

            logger.info(f"Total municipalities to process: {num_municipalities}")
            logger.info(f"Batch size: {self.batch_size}")
            logger.info(f"Output file: {self.output_path}")

            total_successful = 0

            # Process in batches
            for i in range(0, num_municipalities, self.batch_size):
                batch_end = min(i + self.batch_size, num_municipalities)

                successful = self.process_municipality_batch(
                    municipality_list, i, batch_end
                )
                total_successful += successful

                # Log progress
                progress = (batch_end / num_municipalities) * 100
                logger.info(
                    f"Progress: {progress:.1f}% ({batch_end}/{num_municipalities})"
                )

            # Close CSV file
            self._close_csv_writer()

            logger.success(
                f"Extraction complete! Successfully processed {total_successful}/{num_municipalities} municipalities"
            )
            logger.info(f"Output saved to: {self.output_path}")

            return self.output_path

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            self._close_csv_writer()
            raise

    def export_to_drive_efficient(self) -> ee.batch.Task:
        """
        Export data to Google Drive using GEE's server-side processing.

        This is more memory-efficient than loading data into Python first.

        Returns:
            ee.batch.Task: Export task
        """
        logger.info("Initiating server-side export to Google Drive")

        try:
            # Load municipalities
            municipalities = self.load_municipality_boundaries()

            # Load embedding image
            embedding_image = ee.Image("GOOGLE/Research/open-buildings-embeddings/v1")

            # Function to compute embeddings for each municipality
            def compute_embedding(feature):
                geometry = feature.geometry()

                # Compute mean embedding
                mean_embedding = embedding_image.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=geometry,
                    scale=self.scale,
                    maxPixels=self.max_pixels,
                    bestEffort=True,
                )

                # Add embeddings to feature properties
                return feature.set(mean_embedding).set(
                    {
                        "extraction_date": datetime.now().isoformat(),
                        "data_source": "Google Satellite Embedding V1",
                    }
                )

            # Map over all municipalities (server-side)
            municipalities_with_embeddings = municipalities.map(compute_embedding)

            # Export task
            folder_id = os.getenv("GDRIVE_FOLDER_ID")
            filename = os.getenv(
                "GDRIVE_OUTPUT_FILENAME", "brazilian_municipalities_embeddings"
            )

            task = ee.batch.Export.table.toDrive(
                collection=municipalities_with_embeddings,
                description="Export_Municipality_Embeddings_Efficient",
                folder=folder_id,
                fileNamePrefix=filename,
                fileFormat="CSV",
            )

            task.start()
            logger.info(f"Server-side export task started. Task ID: {task.id}")
            logger.info(
                "This approach processes data on GEE servers, saving local memory"
            )
            logger.info("Check Google Earth Engine Tasks tab for progress")

            return task

        except Exception as e:
            logger.error(f"Export to Drive failed: {e}")
            raise


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Memory-efficient satellite embedding extraction"
    )
    parser.add_argument(
        "--mode",
        choices=["streaming", "server-side", "both"],
        default="streaming",
        help="Extraction mode: streaming (local), server-side (GEE), or both",
    )

    args = parser.parse_args()

    try:
        extractor = MemoryEfficientEmbeddingExtractor()

        if args.mode in ["streaming", "both"]:
            logger.info("=== Starting Streaming Extraction (Memory-Efficient) ===")
            output_path = extractor.extract_all_embeddings_streaming()
            logger.success(f"Streaming extraction complete: {output_path}")

        if args.mode in ["server-side", "both"]:
            logger.info("=== Starting Server-Side Export to Google Drive ===")
            task = extractor.export_to_drive_efficient()
            logger.success("Server-side export initiated")

        logger.success("All extraction tasks completed successfully!")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise


if __name__ == "__main__":
    main()
