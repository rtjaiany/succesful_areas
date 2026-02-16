"""
Extract Points of Interest (POIs) from OSM data for economic indicators.

This script parses OSM PBF files and extracts commercial POIs including:
- Banks and financial institutions
- Shops and retail
- Offices
- Marketplaces and amenities

Authors: Jaiany Rocha, Devika Jain and Vinicius Brei
Date: 2026-02-15
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
import json

import osmium
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("poi_extraction.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class POIExtractor(osmium.SimpleHandler):
    """
    OSM handler for extracting commercial Points of Interest.

    This handler processes OSM nodes and ways to identify commercial
    establishments relevant for economic analysis.
    """

    # Define commercial tags to extract
    COMMERCIAL_TAGS = {
        "amenity": {
            "bank",
            "atm",
            "bureau_de_change",
            "marketplace",
            "restaurant",
            "cafe",
            "fast_food",
            "bar",
            "pub",
            "pharmacy",
            "clinic",
            "hospital",
            "dentist",
            "doctors",
            "fuel",
            "car_wash",
            "car_rental",
            "parking",
        },
        "shop": {
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
            "hardware",
            "mobile_phone",
            "bicycle",
            "sports",
            "toys",
            "gift",
            "florist",
            "beauty",
            "hairdresser",
            "optician",
            "pet",
            "alcohol",
            "beverages",
            "kiosk",
        },
        "office": {
            "company",
            "government",
            "insurance",
            "financial",
            "lawyer",
            "accountant",
            "estate_agent",
            "travel_agent",
            "employment_agency",
            "consulting",
        },
        "tourism": {
            "hotel",
            "motel",
            "hostel",
            "guest_house",
            "attraction",
            "museum",
            "gallery",
        },
    }

    def __init__(self, progress_bar: Optional[tqdm] = None):
        """
        Initialize the POI extractor.

        Args:
            progress_bar: Optional tqdm progress bar for tracking
        """
        super().__init__()
        self.pois = []
        self.node_count = 0
        self.way_count = 0
        self.poi_count = 0
        self.progress_bar = progress_bar

        # Track way nodes for geometry
        self.way_nodes = {}

    def node(self, n):
        """
        Process OSM nodes to extract POIs.

        Args:
            n: OSM node object
        """
        self.node_count += 1

        # Log progress every 1M nodes
        if self.node_count % 1000000 == 0:
            logger.info(
                f"Progress: {self.node_count/1e6:.1f}M nodes processed, "
                f"{self.poi_count:,} POIs extracted"
            )

        # Check if node has commercial tags
        poi_data = self._extract_poi_data(n)
        if poi_data:
            poi_data.update(
                {
                    "osm_id": n.id,
                    "osm_type": "node",
                    "lat": n.location.lat,
                    "lon": n.location.lon,
                }
            )
            self.pois.append(poi_data)
            self.poi_count += 1

    def way(self, w):
        """
        Process OSM ways to extract POIs (e.g., building footprints).

        Args:
            w: OSM way object
        """
        self.way_count += 1

        # Check if way has commercial tags
        poi_data = self._extract_poi_data(w)
        if poi_data:
            # Calculate centroid from way nodes
            try:
                lats = [n.lat for n in w.nodes]
                lons = [n.lon for n in w.nodes]

                if lats and lons:
                    centroid_lat = sum(lats) / len(lats)
                    centroid_lon = sum(lons) / len(lons)

                    poi_data.update(
                        {
                            "osm_id": w.id,
                            "osm_type": "way",
                            "lat": centroid_lat,
                            "lon": centroid_lon,
                        }
                    )
                    self.pois.append(poi_data)
                    self.poi_count += 1
            except Exception as e:
                logger.debug(f"Error processing way {w.id}: {e}")

    def _extract_poi_data(self, element) -> Optional[Dict]:
        """
        Extract POI data from an OSM element.

        Args:
            element: OSM node or way

        Returns:
            Dictionary with POI data if commercial, None otherwise
        """
        tags = {tag.k: tag.v for tag in element.tags}

        # Check each commercial tag category
        for category, values in self.COMMERCIAL_TAGS.items():
            if category in tags and tags[category] in values:
                return {
                    "category": category,
                    "type": tags[category],
                    "name": tags.get("name", ""),
                    "brand": tags.get("brand", ""),
                    "operator": tags.get("operator", ""),
                    "address": tags.get("addr:street", ""),
                    "city": tags.get("addr:city", ""),
                    "postcode": tags.get("addr:postcode", ""),
                    "phone": tags.get("phone", ""),
                    "website": tags.get("website", ""),
                    "opening_hours": tags.get("opening_hours", ""),
                }

        return None

    def get_statistics(self) -> Dict:
        """
        Get extraction statistics.

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_nodes_processed": self.node_count,
            "total_ways_processed": self.way_count,
            "total_pois_extracted": self.poi_count,
            "pois_by_category": {},
        }

        # Count POIs by category
        for poi in self.pois:
            category = poi["category"]
            stats["pois_by_category"][category] = (
                stats["pois_by_category"].get(category, 0) + 1
            )

        return stats


def extract_pois_from_osm(
    osm_file: Path, output_file: Path, output_format: str = "geojson"
) -> gpd.GeoDataFrame:
    """
    Extract POIs from OSM PBF file.

    Args:
        osm_file: Path to OSM PBF file
        output_file: Path for output file
        output_format: Output format ('geojson', 'gpkg', 'csv')

    Returns:
        GeoDataFrame with extracted POIs
    """
    logger.info(f"Starting POI extraction from: {osm_file}")
    logger.info(f"Output file: {output_file}")

    # Check if input file exists
    if not osm_file.exists():
        raise FileNotFoundError(f"OSM file not found: {osm_file}")

    # Get file size for progress estimation
    file_size = osm_file.stat().st_size
    logger.info(f"OSM file size: {file_size / (1024**3):.2f} GB")

    # Create handler (without progress bar to avoid tqdm/osmium compatibility issues)
    handler = POIExtractor(progress_bar=None)

    try:
        logger.info("Processing OSM file... This may take several minutes.")
        logger.info("Progress updates will be logged every 1M nodes processed.")
        handler.apply_file(str(osm_file))

        logger.info(f"Processing complete!")
        logger.info(f"Nodes processed: {handler.node_count:,}")
        logger.info(f"Ways processed: {handler.way_count:,}")
        logger.info(f"POIs extracted: {handler.poi_count:,}")

    except Exception as e:
        logger.error(f"Error processing OSM file: {e}")
        raise

    # Convert to DataFrame
    if not handler.pois:
        logger.warning("No POIs extracted!")
        return gpd.GeoDataFrame()

    df = pd.DataFrame(handler.pois)
    logger.info(f"Created DataFrame with {len(df)} POIs")

    # Create GeoDataFrame
    geometry = [Point(lon, lat) for lat, lon in zip(df["lat"], df["lon"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    # Save to file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "geojson":
        gdf.to_file(output_file, driver="GeoJSON")
        logger.info(f"Saved GeoJSON: {output_file}")
    elif output_format == "gpkg":
        gdf.to_file(output_file, driver="GPKG")
        logger.info(f"Saved GeoPackage: {output_file}")
    elif output_format == "csv":
        # For CSV, save without geometry column
        df_csv = df.copy()
        df_csv.to_csv(output_file, index=False)
        logger.info(f"Saved CSV: {output_file}")
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    # Print statistics
    stats = handler.get_statistics()
    logger.info("\n" + "=" * 80)
    logger.info("EXTRACTION STATISTICS")
    logger.info("=" * 80)
    logger.info(f"Total nodes processed: {stats['total_nodes_processed']:,}")
    logger.info(f"Total ways processed: {stats['total_ways_processed']:,}")
    logger.info(f"Total POIs extracted: {stats['total_pois_extracted']:,}")
    logger.info("\nPOIs by category:")
    for category, count in sorted(stats["pois_by_category"].items()):
        logger.info(f"  {category}: {count:,}")
    logger.info("=" * 80)

    # Save statistics to JSON
    stats_file = output_file.parent / f"{output_file.stem}_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"Statistics saved to: {stats_file}")

    return gdf


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Extract commercial POIs from OSM data"
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/osm/raw/brazil-latest.osm.pbf",
        help="Input OSM PBF file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/osm/pois/commercial_pois.geojson",
        help="Output file path",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="geojson",
        choices=["geojson", "gpkg", "csv"],
        help="Output format",
    )

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("OSM POI Extraction - Commercial Economic Indicators")
    logger.info("=" * 80)

    # Convert to Path objects
    input_file = Path(args.input)
    output_file = Path(args.output)

    # Extract POIs
    gdf = extract_pois_from_osm(
        osm_file=input_file, output_file=output_file, output_format=args.format
    )

    logger.info("\n" + "=" * 80)
    logger.info("POI EXTRACTION COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"Output file: {output_file}")
    logger.info(f"Total POIs: {len(gdf):,}")
    logger.info("\nNext steps:")
    logger.info("1. Review the extracted POIs")
    logger.info("2. Download municipality boundaries from IBGE")
    logger.info("3. Perform spatial aggregation (Point-in-Polygon)")
    logger.info("4. Calculate commercial density per municipality")


if __name__ == "__main__":
    main()
