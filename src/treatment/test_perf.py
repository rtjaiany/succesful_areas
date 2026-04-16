import pyogrio
from pathlib import Path
import time
import geopandas as gpd

roads_path = Path("data/raw/osm/roads/road_network.geojson")
muni_path = Path("data/raw/shapefiles/BR_Municipios_2022/BR_Municipios_2022.shp")

start = time.time()
info = pyogrio.read_info(roads_path)
print(f"Info read in {time.time() - start:.2f}s")
print(info)

start = time.time()
chunk = pyogrio.read_dataframe(roads_path, max_features=10000)
print(f"10k roads read in {time.time() - start:.2f}s")

start = time.time()
muni = gpd.read_file(muni_path, rows=100)  # just some munis
muni = muni.to_crs("EPSG:5880")
chunk = chunk.to_crs("EPSG:5880")
intersection = gpd.overlay(chunk, muni, how="intersection")
print(f"Overlay for 10k roads and 100 munis took {time.time() - start:.2f}s")
