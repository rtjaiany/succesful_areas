import geopandas as gpd
from pathlib import Path

path = Path(
    r"c:\Users\jaian\OneDrive\Documentos\01 - In Progress\06 - SWE\geolocate\data\raw\shapefiles\BR_Municipios_2022\BR_Municipios_2022.shp"
)
gdf = gpd.read_file(path, rows=5)
print(gdf.columns)
print(gdf.head())
