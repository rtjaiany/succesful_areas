"""
Calculate road-based infrastructure predictors for Brazilian municipalities.

Features:
1. Road Density (km/km2): Calculated using projected lengths.
2. Intersection Density: Nodes with degree >= 3 (true spatial topology).
3. Highway Proximity: Presence/count of motorway and trunk segments.

Optimized for 8GB RAM and speed:
- Pass 1: Uses endpoint-first topology scan to avoid RAM overflow.
- Pass 2: Map-reduce style processing in chunks of 200k.
- Progressive saving and persistence/resume support.
"""

import os
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
import time
from tqdm import tqdm

import pandas as pd
import geopandas as gpd
import fiona
import pyogrio
from shapely.geometry import Point, LineString, shape
import numpy as np
from collections import Counter

# Setting for better performance with 8GB RAM
import gc

gc.collect()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("road_metrics_optimized.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Constants
BRAZIL_METRIC_CRS = "EPSG:5880"  # SIRGAS 2000 / Brazil Polyconic (meters)
HIGHWAY_TYPES_FOR_METRIC = {"motorway", "trunk"}
MAJOR_ROAD_TYPES = {
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "motorway_link",
    "trunk_link",
    "primary_link",
    "secondary_link",
    "tertiary_link",
}
ALL_ROAD_TYPES = MAJOR_ROAD_TYPES | {
    "unclassified",
    "residential",
    "service",
    "living_street",
    "road",
}


def find_intersections_streaming(geojson_path: Path, cache_path: Path) -> pd.DataFrame:
    """
    Pass 1: Memory-efficient topology scan.
    Step 1: Stores only road endpoints in Counter (fixed memory footprint).
    Step 2: Scans interior nodes and increments if they match an endpoint.
    """
    if cache_path.exists():
        logger.info(f"Loading cached intersections from {cache_path}...")
        return pd.read_csv(cache_path)

    logger.info(f"Pass 1/2: Starting Endpoint-First Scan on {geojson_path.name}")
    counts = Counter()

    with fiona.open(geojson_path) as src:
        # Phase 1: Endpoints (Low RAM, max ~12.8M entries for 6.4M roads)
        for feat in tqdm(src, desc="P1 Phase 1 (Ends)", unit="roads"):
            geom = feat.get("geometry")
            if not geom or geom["type"] != "LineString":
                continue
            if feat["properties"].get("highway_type") not in ALL_ROAD_TYPES:
                continue
            coords = geom["coordinates"]
            if len(coords) < 2:
                continue

            counts[tuple(coords[0])] += 1
            counts[tuple(coords[-1])] += 1

    # Phase 2: Interior check (Only adds to memory if it's already a junction candidate)
    with fiona.open(geojson_path) as src:
        for feat in tqdm(src, desc="P1 Phase 2 (Interior)", unit="roads"):
            geom = feat.get("geometry")
            if not geom or geom["type"] != "LineString":
                continue
            if feat["properties"].get("highway_type") not in ALL_ROAD_TYPES:
                continue
            coords = geom["coordinates"]
            if len(coords) < 3:
                continue

            # Check if any interior node hits an existing endpoint
            for c in coords[1:-1]:
                c_tuple = tuple(c)
                if c_tuple in counts:
                    counts[c_tuple] += 1

    logger.info("  Filtering nodes with degree >= 3...")
    intersections = [c for c, deg in counts.items() if deg >= 3]

    # Force Garbage Collection
    del counts
    gc.collect()

    df = pd.DataFrame(intersections, columns=["lon", "lat"])
    df.to_csv(cache_path, index=False)
    logger.info(f"  Found {len(df):,} intersections. Saved to {cache_path}")
    return df


def calculate_metrics_optimized(
    munis_gdf: gpd.GeoDataFrame,
    roads_path: Path,
    intersections_df: pd.DataFrame,
    output_path: Path,
    chunk_size: int = 200000,
):
    """
    Pass 2: Optimized Road-First processing.
    Reads the GeoJSON once in chunks and joins with municipalities.
    """
    logger.info(f"Pass 2/2: Starting Metric Calculation (Chunk Size: {chunk_size})")

    # 1. Prepare Municipalities Result Table
    munis_metric = munis_gdf.to_crs(BRAZIL_METRIC_CRS).copy()
    munis_metric["area_km2"] = munis_metric.geometry.area / 1e6
    munis_clean = munis_metric[
        ["CD_MUN", "NM_MUN", "SIGLA_UF", "area_km2", "geometry"]
    ].copy()

    results = munis_clean[["CD_MUN", "NM_MUN", "SIGLA_UF", "area_km2"]].set_index(
        "CD_MUN"
    )
    results["total_road_km"] = 0.0
    results["intersection_count"] = 0
    results["highway_count"] = 0

    # 2. Count Intersections (One-time spatial join)
    logger.info("  Mapping intersections to municipalities...")
    int_points = [
        Point(x, y) for x, y in zip(intersections_df.lon, intersections_df.lat)
    ]
    int_gdf = gpd.GeoDataFrame(geometry=int_points, crs="EPSG:4326").to_crs(
        BRAZIL_METRIC_CRS
    )
    del int_points
    gc.collect()

    int_mapped = gpd.sjoin(
        int_gdf,
        munis_clean[["CD_MUN", "geometry"]],
        how="inner",
        predicate="intersects",
    )
    int_counts = int_mapped.groupby("CD_MUN").size()
    results["intersection_count"] = int_counts
    del int_gdf, int_mapped
    gc.collect()

    # 3. Process Roads in Chunks
    logger.info(f"  Streaming roads from {roads_path.name}...")
    roads_handled = 0
    resume_path = output_path.with_suffix(".resume.txt")
    start_at_road = 0

    # Load Resume State
    if output_path.with_suffix(".partial.csv").exists() and resume_path.exists():
        try:
            with open(resume_path, "r") as f:
                start_at_road = int(f.read().strip())
            logger.info(f"  Resuming from road index {start_at_road:,}...")
            partial_df = pd.read_csv(output_path.with_suffix(".partial.csv")).set_index(
                "CD_MUN"
            )
            for col in ["total_road_km", "highway_count"]:
                results[col] = partial_df[col]
            del partial_df
        except Exception as e:
            logger.warning(f"  Resume failed, starting fresh: {e}")
            start_at_road = 0

    with fiona.open(roads_path) as src:
        num_features = len(src)
        chunk = []
        with tqdm(total=num_features, desc="Pass 2: Metrics", unit="roads") as pbar:
            if start_at_road > 0:
                pbar.update(start_at_road)
                roads_handled = start_at_road

            for i, feat in enumerate(src):
                if i < start_at_road:
                    continue

                roads_handled += 1
                pbar.update(1)

                highway = feat["properties"].get("highway_type")
                geom = feat.get("geometry")

                if geom and geom["type"] == "LineString" and highway in ALL_ROAD_TYPES:
                    chunk.append({"highway_type": highway, "geometry": shape(geom)})

                if len(chunk) >= chunk_size:
                    pbar.set_postfix({"chunk": roads_handled // chunk_size})
                    process_road_chunk(chunk, munis_clean, results)
                    chunk = []
                    gc.collect()
                    results.to_csv(output_path.with_suffix(".partial.csv"))
                    with open(resume_path, "w") as f:
                        f.write(str(roads_handled))

            if chunk:
                process_road_chunk(chunk, munis_clean, results)

    # 4. Finalize
    logger.info("  Finalizing metrics...")
    results = results.fillna(0)
    results["road_density_km_km2"] = results["total_road_km"] / results["area_km2"]
    results["intersection_density"] = (
        results["intersection_count"] / results["area_km2"]
    )
    results["has_highway"] = (results["highway_count"] > 0).astype(int)

    results.to_csv(output_path)
    if output_path.with_suffix(".partial.csv").exists():
        os.remove(output_path.with_suffix(".partial.csv"))
    if resume_path.exists():
        os.remove(resume_path)

    logger.info(f"DONE! Results saved to {output_path}")


def process_road_chunk(
    chunk_list: List[Dict], munis_gdf: gpd.GeoDataFrame, results_df: pd.DataFrame
):
    chunk_gdf = gpd.GeoDataFrame(chunk_list, crs="EPSG:4326").to_crs(BRAZIL_METRIC_CRS)
    roads_mapped = gpd.overlay(
        chunk_gdf, munis_gdf[["CD_MUN", "geometry"]], how="intersection"
    )
    roads_mapped["length_km"] = roads_mapped.geometry.length / 1000.0

    stats = roads_mapped.groupby("CD_MUN").agg(
        total_road_km=("length_km", "sum"),
        highway_count=(
            "highway_type",
            lambda x: x.isin(HIGHWAY_TYPES_FOR_METRIC).sum(),
        ),
    )
    for cd_mun, row in stats.iterrows():
        if cd_mun in results_df.index:
            results_df.loc[cd_mun, "total_road_km"] += row["total_road_km"]
            results_df.loc[cd_mun, "highway_count"] += row["highway_count"]


def main():
    parser = argparse.ArgumentParser(description="Memory-safe road metrics for Brazil")
    parser.add_argument(
        "--muni",
        type=str,
        default="data/raw/shapefiles/BR_Municipios_2022/BR_Municipios_2022.shp",
        help="Muni shapefile",
    )
    parser.add_argument(
        "--roads",
        type=str,
        default="data/raw/osm/roads/road_network.geojson",
        help="Road GeoJSON",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/road_predictors_muni.csv",
        help="Output path",
    )
    parser.add_argument(
        "--chunk-size", type=int, default=200000, help="Roads per chunk"
    )
    parser.add_argument("--state", type=str, help="State filter")

    args = parser.parse_args()

    logger.info(f"Loading municipalities...")
    all_munis = gpd.read_file(args.muni)
    if args.state:
        all_munis = all_munis[all_munis["SIGLA_UF"] == args.state].copy()

    cache_path = Path("data/processed/intersections_cache.csv")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    intersections_df = find_intersections_streaming(Path(args.roads), cache_path)

    calculate_metrics_optimized(
        all_munis,
        Path(args.roads),
        intersections_df,
        Path(args.output),
        chunk_size=args.chunk_size,
    )


if __name__ == "__main__":
    main()
