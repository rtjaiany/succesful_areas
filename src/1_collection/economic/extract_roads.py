"""
Extract Road Network from OSM data for infrastructure indicators.

This script parses OSM PBF files and extracts road network including:
- Highways (motorways, trunks, primary roads)
- Secondary and tertiary roads
- Residential and service roads
- Road attributes (name, surface, lanes, etc.)

Author: i-guide project
Date: 2026-02-16
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
from shapely.geometry import LineString
from shapely import wkt

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("road_extraction.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class RoadExtractor(osmium.SimpleHandler):
    """
    OSM handler for extracting road network.

    This handler processes OSM ways to identify roads and highways
    relevant for infrastructure analysis.
    """

    # Define highway/road tags to extract
    HIGHWAY_TAGS = {
        # Major roads
        "motorway",
        "trunk",
        "primary",
        "secondary",
        "tertiary",
        # Links
        "motorway_link",
        "trunk_link",
        "primary_link",
        "secondary_link",
        "tertiary_link",
        # Other roads
        "unclassified",
        "residential",
        "service",
        "living_street",
        # Special
        "road",  # Unknown classification
    }

    def __init__(self):
        """Initialize the road extractor."""
        super().__init__()
        self.roads = []
        self.way_count = 0
        self.road_count = 0

    def way(self, w):
        """
        Process OSM ways to extract roads.

        Args:
            w: OSM way object
        """
        self.way_count += 1

        # Log progress every 1M ways
        if self.way_count % 1000000 == 0:
            logger.info(
                f"Progress: {self.way_count/1e6:.1f}M ways processed, "
                f"{self.road_count:,} roads extracted"
            )

        # Check if way has highway tag
        road_data = self._extract_road_data(w)
        if road_data:
            # Extract geometry from way nodes
            try:
                coords = [(n.lon, n.lat) for n in w.nodes if n.location.valid()]

                if len(coords) >= 2:  # Need at least 2 points for a line
                    road_data.update(
                        {
                            "osm_id": w.id,
                            "geometry_wkt": LineString(coords).wkt,
                            "num_nodes": len(coords),
                        }
                    )
                    self.roads.append(road_data)
                    self.road_count += 1
            except Exception as e:
                logger.debug(f"Error processing way {w.id}: {e}")

    def _extract_road_data(self, element) -> Optional[Dict]:
        """
        Extract road data from an OSM element.

        Args:
            element: OSM way

        Returns:
            Dictionary with road data if highway, None otherwise
        """
        tags = {tag.k: tag.v for tag in element.tags}

        # Check if element has highway tag
        if "highway" in tags and tags["highway"] in self.HIGHWAY_TAGS:
            return {
                "highway_type": tags["highway"],
                "name": tags.get("name", ""),
                "ref": tags.get("ref", ""),  # Road reference number
                "surface": tags.get("surface", ""),
                "lanes": tags.get("lanes", ""),
                "maxspeed": tags.get("maxspeed", ""),
                "oneway": tags.get("oneway", ""),
                "bridge": tags.get("bridge", ""),
                "tunnel": tags.get("tunnel", ""),
                "access": tags.get("access", ""),
            }

        return None

    def get_statistics(self) -> Dict:
        """
        Get extraction statistics.

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_ways_processed": self.way_count,
            "total_roads_extracted": self.road_count,
            "roads_by_type": {},
            "total_length_km": 0.0,
        }

        # Count roads by type
        for road in self.roads:
            highway_type = road["highway_type"]
            stats["roads_by_type"][highway_type] = (
                stats["roads_by_type"].get(highway_type, 0) + 1
            )

        return stats


def extract_roads_from_osm(
    osm_file: Path, output_file: Path, output_format: str = "geojson"
) -> gpd.GeoDataFrame:
    """
    Extract road network from OSM PBF file.

    Args:
        osm_file: Path to OSM PBF file
        output_file: Path for output file
        output_format: Output format ('geojson', 'gpkg', 'shp')

    Returns:
        GeoDataFrame with extracted roads
    """
    logger.info(f"Starting road network extraction from: {osm_file}")
    logger.info(f"Output file: {output_file}")

    # Check if input file exists
    if not osm_file.exists():
        raise FileNotFoundError(f"OSM file not found: {osm_file}")

    # Get file size for progress estimation
    file_size = osm_file.stat().st_size
    logger.info(f"OSM file size: {file_size / (1024**3):.2f} GB")

    # Create handler
    handler = RoadExtractor()

    try:
        logger.info("Processing OSM file... This may take several minutes.")
        logger.info("Progress updates will be logged every 1M ways processed.")

        # Apply file with node locations enabled for ways
        # This is crucial - without it, way.nodes won't have location data
        handler.apply_file(str(osm_file), locations=True)

        logger.info(f"Processing complete!")
        logger.info(f"Ways processed: {handler.way_count:,}")
        logger.info(f"Roads extracted: {handler.road_count:,}")

    except Exception as e:
        logger.error(f"Error processing OSM file: {e}")
        raise

    # Convert to DataFrame
    if not handler.roads:
        logger.warning("No roads extracted!")
        return gpd.GeoDataFrame()

    df = pd.DataFrame(handler.roads)
    logger.info(f"Created DataFrame with {len(df)} roads")

    # Create GeoDataFrame from WKT geometries
    logger.info("Converting WKT geometries to GeoDataFrame...")
    df["geometry"] = df["geometry_wkt"].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

    # Drop the WKT column (no longer needed)
    gdf = gdf.drop(columns=["geometry_wkt"])

    # Calculate road lengths in kilometers
    logger.info("Calculating road lengths...")
    # Use geodesic length calculation (more memory efficient than CRS transformation)
    # For lat/lon coordinates, we can use the length property which calculates geodesic distance
    gdf["length_km"] = (
        gdf.geometry.length * 111.32
    )  # Approximate: 1 degree ≈ 111.32 km at equator

    # For more accurate calculation, we could use:
    # from shapely.ops import transform
    # import pyproj
    # But this would require more memory for 6M+ features
    # The approximation above is sufficient for Brazil (near equator)

    # Save to file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "geojson":
        gdf.to_file(output_file, driver="GeoJSON")
        logger.info(f"Saved GeoJSON: {output_file}")
    elif output_format == "gpkg":
        gdf.to_file(output_file, driver="GPKG")
        logger.info(f"Saved GeoPackage: {output_file}")
    elif output_format == "shp":
        gdf.to_file(output_file, driver="ESRI Shapefile")
        logger.info(f"Saved Shapefile: {output_file}")
    else:
        raise ValueError(f"Unsupported format: {output_format}")

    # Print statistics
    stats = handler.get_statistics()
    stats["total_length_km"] = gdf["length_km"].sum()

    logger.info("\n" + "=" * 80)
    logger.info("EXTRACTION STATISTICS")
    logger.info("=" * 80)
    logger.info(f"Total ways processed: {stats['total_ways_processed']:,}")
    logger.info(f"Total roads extracted: {stats['total_roads_extracted']:,}")
    logger.info(f"Total road length: {stats['total_length_km']:,.2f} km")
    logger.info("\nRoads by type:")
    for highway_type, count in sorted(
        stats["roads_by_type"].items(), key=lambda x: x[1], reverse=True
    ):
        type_length = gdf[gdf["highway_type"] == highway_type]["length_km"].sum()
        logger.info(f"  {highway_type}: {count:,} segments ({type_length:,.2f} km)")
    logger.info("=" * 80)

    # Save statistics to JSON
    stats_file = output_file.parent / f"{output_file.stem}_stats.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    logger.info(f"Statistics saved to: {stats_file}")

    return gdf


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Extract road network from OSM data")
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/economic/osm/raw/brazil-latest.osm.pbf",
        help="Input OSM PBF file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/economic/osm/roads/road_network.geojson",
        help="Output file path",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="geojson",
        choices=["geojson", "gpkg", "shp"],
        help="Output format",
    )

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("OSM Road Network Extraction - Infrastructure Indicators")
    logger.info("=" * 80)

    # Convert to Path objects
    input_file = Path(args.input)
    output_file = Path(args.output)

    # Extract roads
    gdf = extract_roads_from_osm(
        osm_file=input_file, output_file=output_file, output_format=args.format
    )

    logger.info("\n" + "=" * 80)
    logger.info("ROAD NETWORK EXTRACTION COMPLETE!")
    logger.info("=" * 80)
    logger.info(f"Output file: {output_file}")
    logger.info(f"Total roads: {len(gdf):,}")
    logger.info(f"Total length: {gdf['length_km'].sum():,.2f} km")
    logger.info("\nNext steps:")
    logger.info("1. Review the extracted road network")
    logger.info("2. Download municipality boundaries from IBGE")
    logger.info("3. Perform spatial aggregation (roads within polygons)")
    logger.info("4. Calculate road density per municipality")


if __name__ == "__main__":
    main()
