import ee

ee.Initialize(project="velvety-gearbox-451304-s0")

lon_min, lat_min, lon_max, lat_max = 72.5833, 18.7833, 73.2000, 19.6000
city_bbox = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

# Copernicus DEM GLO-30 -- 30m global elevation, matches your Landsat resolution
dem = ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").mosaic().select("DEM")

# Slope is a required SOLWEIG input, easy to derive from the DEM directly in GEE
slope = ee.Terrain.slope(dem)

for img, name in [(dem, "DEM"), (slope, "slope")]:
    task = ee.batch.Export.image.toDrive(
        image=img,
        description=f"mumbai_{name}",
        folder="urban_heat_project/raw_DEM",
        region=city_bbox,
        scale=30,
        crs="EPSG:4326"
    )
    task.start()

print("DEM + slope exports started — check Google Drive in a few minutes")