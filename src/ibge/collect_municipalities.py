"""
IBGE Municipality Boundaries Collection

This script downloads officially maintained municipality boundary shapefiles
from the IBGE (Brazilian Institute of Geography and Statistics) Geosciences portal.

Reference: https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/
"""

import os
import zipfile
import requests
import argparse
from pathlib import Path
from tqdm import tqdm
from loguru import logger


class IBGEBoundaryCollector:
    """
    Collector for IBGE municipality boundary shapefiles.
    """

    BASE_URL = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais"

    def __init__(self, output_dir: str = "data/raw/ibge"):
        """
        Initialize the collector.

        Args:
            output_dir: Directory to save the downloaded and extracted files.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized IBGE collector. Output directory: {self.output_dir}")

    def download_boundaries(self, year: int = 2022) -> Path:
        """
        Download municipality boundaries for a specific year.

        Args:
            year: The year of the territorial mesh.

        Returns:
            Path to the downloaded zip file.
        """
        # Construct the URL based on IBGE's standard directory structure
        # Example for 2022: .../municipio_2022/Brasil/BR/BR_Municipios_2022.zip
        url = f"{self.BASE_URL}/municipio_{year}/Brasil/BR/BR_Municipios_{year}.zip"

        zip_filename = f"BR_Municipios_{year}.zip"
        zip_path = self.output_dir / zip_filename

        logger.info(f"Downloading IBGE municipality boundaries for {year}...")
        logger.info(f"URL: {url}")

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024  # 1 Kibibyte

            with open(zip_path, "wb") as f:
                with tqdm(
                    total=total_size, unit="iB", unit_scale=True, desc=zip_filename
                ) as pbar:
                    for data in response.iter_content(block_size):
                        f.write(data)
                        pbar.update(len(data))

            logger.success(f"Download complete: {zip_path}")
            return zip_path

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download IBGE boundaries: {e}")
            if response.status_code == 404:
                logger.error(
                    f"Year {year} might not be available at this specific URL pattern."
                )
            raise

    def extract_boundaries(self, zip_path: Path):
        """
        Extract the downloaded zip file.

        Args:
            zip_path: Path to the zip file.
        """
        extract_dir = self.output_dir / zip_path.stem
        extract_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Extracting shapefiles to: {extract_dir}")

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            logger.success(
                f"Extraction complete. Shapefiles available in {extract_dir}"
            )

            # Optional: Remove the zip file after extraction
            # logger.info("Cleaning up zip file...")
            # zip_path.unlink()

        except zipfile.BadZipFile as e:
            logger.error(f"Failed to extract zip file: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Collect IBGE municipality boundary shapefiles"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=2022,
        help="Year of the boundaries (e.g., 2022, 2023)",
    )
    parser.add_argument(
        "--output-dir", type=str, default="data/raw/ibge", help="Output directory"
    )

    args = parser.parse_args()

    try:
        collector = IBGEBoundaryCollector(output_dir=args.output_dir)
        zip_path = collector.download_boundaries(year=args.year)
        collector.extract_boundaries(zip_path)

        logger.info("\n" + "=" * 50)
        logger.info("IBGE BOUNDARIES COLLECTION COMPLETE!")
        logger.info("=" * 50)
        logger.info(
            f"Shapefiles are located in: {args.output_dir}/BR_Municipios_{args.year}"
        )
        logger.info("\nNext steps:")
        logger.info("1. Load these shapefiles using GeoPandas")
        logger.info("2. Use them for spatial analysis with satellite or OSM data")

    except Exception as e:
        logger.error(f"Script failed: {e}")


if __name__ == "__main__":
    main()
