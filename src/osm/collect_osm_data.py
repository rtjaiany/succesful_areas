"""
OpenStreetMap (OSM) Data Collection for Brazil

This script downloads OSM data for Brazil and prepares it for economic indicator extraction.
Focus: Commercial density and infrastructure metrics per municipality.

Data Collection
- Download OSM data for Brazil
- Extract relevant features (POIs, roads, amenities)
- Save raw data for later aggregation

Authors: Jaiany Rocha, Devika Jain and Vinicius Brei
Date: 2026-02-15
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

import requests
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
from shapely.geometry import Point, LineString, Polygon

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("osm_collection.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class OSMDataCollector:
    """
    Collector for OpenStreetMap data focused on economic indicators.

    This class handles downloading and initial processing of OSM data for Brazil,
    extracting features relevant to economic analysis:
    - Commercial POIs (banks, shops, amenities)
    - Infrastructure (roads, highways)
    """

    # OSM feature categories for economic indicators
    COMMERCIAL_TAGS = {
        "amenity": ["bank", "atm", "bureau_de_change", "marketplace"],
        "shop": [
            "supermarket",
            "convenience",
            "department_store",
            "mall",
            "clothes",
            "shoes",
            "electronics",
            "furniture",
            "bakery",
            "butcher",
            "car",
            "pharmacy",
            "books",
            "jewelry",
        ],
        "office": ["company", "government", "insurance", "financial"],
    }

    INFRASTRUCTURE_TAGS = {
        "highway": [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "service",
            "motorway_link",
            "trunk_link",
            "primary_link",
            "secondary_link",
            "tertiary_link",
        ]
    }

    def __init__(self, output_dir: str = "data/raw/osm"):
        """
        Initialize the OSM data collector.

        Args:
            output_dir: Directory to save downloaded OSM data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for different data types
        self.poi_dir = self.output_dir / "pois"
        self.roads_dir = self.output_dir / "roads"
        self.raw_dir = self.output_dir / "raw"

        for dir_path in [self.poi_dir, self.roads_dir, self.raw_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized OSM collector. Output directory: {self.output_dir}")

    def download_brazil_osm(self, source: str = "geofabrik") -> Path:
        """
        Download OSM data for Brazil from Geofabrik or other sources.

        Args:
            source: Data source ('geofabrik' or 'overpass')

        Returns:
            Path to downloaded file
        """
        logger.info(f"Starting Brazil OSM download from {source}...")

        if source == "geofabrik":
            return self._download_from_geofabrik()
        elif source == "overpass":
            return self._download_from_overpass()
        else:
            raise ValueError(f"Unknown source: {source}")

    def _download_from_geofabrik(self) -> Path:
        """
        Download Brazil OSM data from Geofabrik.

        Geofabrik provides regularly updated OSM extracts for countries/regions.
        Brazil extract: https://download.geofabrik.de/south-america/brazil-latest.osm.pbf

        Returns:
            Path to downloaded PBF file
        """
        url = "https://download.geofabrik.de/south-america/brazil-latest.osm.pbf"
        output_file = self.raw_dir / "brazil-latest.osm.pbf"

        # Check if file already exists
        if output_file.exists():
            logger.info(f"File already exists: {output_file}")
            user_input = input("File exists. Re-download? (y/n): ").lower()
            if user_input != "y":
                logger.info("Using existing file.")
                return output_file

        logger.info(f"Downloading from: {url}")
        logger.info(f"Output file: {output_file}")
        logger.info(
            "Note: This file is large (~1-2 GB). Download may take several minutes."
        )

        try:
            # Stream download with progress bar
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            block_size = 8192  # 8 KB chunks

            with open(output_file, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc="Downloading Brazil OSM",
            ) as pbar:
                for chunk in response.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

            logger.info(f"Download complete: {output_file}")
            logger.info(f"File size: {output_file.stat().st_size / (1024**3):.2f} GB")
            return output_file

        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise

    def _download_from_overpass(self) -> Path:
        """
        Download Brazil OSM data using Overpass API.

        Note: Overpass API is better for smaller queries. For entire Brazil,
        Geofabrik is recommended.

        Returns:
            Path to downloaded file
        """
        logger.warning("Overpass API download for entire Brazil is not recommended.")
        logger.warning("The query would be too large. Use Geofabrik instead.")
        logger.info("Falling back to Geofabrik download...")
        return self._download_from_geofabrik()

    def extract_pois(
        self, osm_file: Path, region: Optional[str] = None
    ) -> gpd.GeoDataFrame:
        """
        Extract Points of Interest (POIs) from OSM data.

        Extracts commercial POIs like banks, shops, and amenities that are
        relevant for economic indicator calculation.

        Args:
            osm_file: Path to OSM PBF file
            region: Optional region filter (state code)

        Returns:
            GeoDataFrame with POI data
        """
        logger.info("Extracting POIs from OSM data...")

        # Check for required libraries
        try:
            import osmium
        except ImportError:
            logger.error("osmium library not found. Install with: pip install osmium")
            logger.info("Run: pip install osmium")
            raise

        # Import and use the POI extractor
        try:
            from extract_pois import extract_pois_from_osm

            output_file = self.poi_dir / "commercial_pois.geojson"
            gdf = extract_pois_from_osm(
                osm_file=osm_file, output_file=output_file, output_format="geojson"
            )

            return gdf

        except Exception as e:
            logger.error(f"POI extraction failed: {e}")
            logger.info("You can also run POI extraction separately:")
            logger.info("  python src/osm/extract_pois.py")
            raise

    def extract_roads(
        self, osm_file: Path, region: Optional[str] = None
    ) -> gpd.GeoDataFrame:
        """
        Extract road network from OSM data.

        Extracts highway/road features for infrastructure density calculation.

        Args:
            osm_file: Path to OSM PBF file
            region: Optional region filter (state code)

        Returns:
            GeoDataFrame with road network data
        """
        logger.info("Extracting road network from OSM data...")

        # Check for required libraries
        try:
            import osmium
        except ImportError:
            logger.error("osmium library not found. Install with: pip install osmium")
            logger.info("Run: pip install osmium")
            raise

        # Import and use the road extractor
        try:
            from extract_roads import extract_roads_from_osm

            output_file = self.roads_dir / "road_network.geojson"
            gdf = extract_roads_from_osm(
                osm_file=osm_file, output_file=output_file, output_format="geojson"
            )

            return gdf

        except Exception as e:
            logger.error(f"Road extraction failed: {e}")
            logger.info("You can also run road extraction separately:")
            logger.info("  python src/osm/extract_roads.py")
            raise

    def save_data(self, gdf: gpd.GeoDataFrame, name: str, format: str = "geojson"):
        """
        Save GeoDataFrame to file.

        Args:
            gdf: GeoDataFrame to save
            name: Base name for output file
            format: Output format ('geojson', 'gpkg', 'shp')
        """
        if gdf.empty:
            logger.warning(f"Cannot save empty GeoDataFrame: {name}")
            return

        if format == "geojson":
            output_file = self.output_dir / f"{name}.geojson"
            gdf.to_file(output_file, driver="GeoJSON")
        elif format == "gpkg":
            output_file = self.output_dir / f"{name}.gpkg"
            gdf.to_file(output_file, driver="GPKG")
        elif format == "shp":
            output_file = self.output_dir / f"{name}.shp"
            gdf.to_file(output_file, driver="ESRI Shapefile")
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Saved {len(gdf)} features to {output_file}")

    def get_collection_stats(self) -> Dict:
        """
        Get statistics about collected data.

        Returns:
            Dictionary with collection statistics
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "output_dir": str(self.output_dir),
            "files": [],
        }

        # List all files in output directory
        for file_path in self.output_dir.rglob("*"):
            if file_path.is_file():
                stats["files"].append(
                    {
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.output_dir)),
                        "size_mb": file_path.stat().st_size / (1024**2),
                    }
                )

        return stats


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Collect OpenStreetMap data for Brazil economic indicators"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="geofabrik",
        choices=["geofabrik", "overpass"],
        help="Data source for OSM download",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/osm",
        help="Output directory for OSM data",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download data, skip extraction",
    )
    parser.add_argument(
        "--skip-download", action="store_true", help="Skip download if file exists"
    )

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("OSM Data Collection for Brazil - Phase 3.1")
    logger.info("=" * 80)

    # Initialize collector
    collector = OSMDataCollector(output_dir=args.output_dir)

    # Download OSM data
    if not args.skip_download:
        osm_file = collector.download_brazil_osm(source=args.source)
        logger.info(f"OSM data downloaded: {osm_file}")
    else:
        osm_file = collector.raw_dir / "brazil-latest.osm.pbf"
        if not osm_file.exists():
            logger.error(f"OSM file not found: {osm_file}")
            logger.error("Run without --skip-download to download the file first.")
            return

    if args.download_only:
        logger.info("Download complete. Exiting (--download-only flag set).")
        return

    # Extract features
    logger.info("\n" + "=" * 80)
    logger.info("Feature Extraction")
    logger.info("=" * 80)

    # Check if osmium is installed
    try:
        import osmium

        logger.info("osmium is installed. Proceeding with feature extraction...")

        try:
            # Extract POIs
            logger.info("\nExtracting commercial POIs...")
            poi_gdf = collector.extract_pois(osm_file)
            logger.info(f"✓ POI extraction complete: {len(poi_gdf):,} POIs extracted")

        except Exception as e:
            logger.error(f"POI extraction failed: {e}")
            logger.info("\nYou can run POI extraction separately:")
            logger.info("  python src/osm/extract_pois.py")

        try:
            # Extract roads
            logger.info("\nExtracting road network...")
            road_gdf = collector.extract_roads(osm_file)
            logger.info(
                f"✓ Road extraction complete: {len(road_gdf):,} road segments extracted"
            )
            logger.info(f"  Total road length: {road_gdf['length_km'].sum():,.2f} km")

        except Exception as e:
            logger.error(f"Road extraction failed: {e}")
            logger.info("\nYou can run road extraction separately:")
            logger.info("  python src/osm/extract_roads.py")

    except ImportError:
        logger.warning("osmium not installed. Skipping feature extraction.")
        logger.info("\nTo extract features:")
        logger.info("1. Install osmium: pip install osmium")
        logger.info("2. Run POI extraction:")
        logger.info("   python src/osm/extract_pois.py")
        logger.info(
            "3. Or re-run this script: python collect_osm_data.py --skip-download"
        )

    # Get collection statistics
    stats = collector.get_collection_stats()
    logger.info("\n" + "=" * 80)
    logger.info("Collection Statistics")
    logger.info("=" * 80)
    logger.info(f"Timestamp: {stats['timestamp']}")
    logger.info(f"Output directory: {stats['output_dir']}")
    logger.info(f"Files collected: {len(stats['files'])}")
    for file_info in stats["files"]:
        logger.info(f"  - {file_info['path']}: {file_info['size_mb']:.2f} MB")

    logger.info("\n" + "=" * 80)
    logger.info("Collection Complete!")
    logger.info("=" * 80)
    logger.info("Next steps:")
    logger.info("1. Install osmium for feature extraction")
    logger.info("2. Implement POI and road extraction")
    logger.info("3. Proceed to Phase 3.2: Aggregation")


if __name__ == "__main__":
    main()
