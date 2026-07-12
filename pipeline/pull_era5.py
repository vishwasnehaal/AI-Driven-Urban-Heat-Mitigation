import ee
import csv
import datetime

ee.Initialize(project="velvety-gearbox-451304-s0")

lon_min, lat_min, lon_max, lat_max = 72.5833, 18.7833, 73.2000, 19.6000
city_bbox = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

# Requires pull_lst.py to have run first
with open("data/processed/lst_scene_dates.csv") as f:
    scene_dates = list(csv.DictReader(f))

met_bands_list = [
    "temperature_2m",
    "dewpoint_temperature_2m",
    "u_component_of_wind_10m",
    "v_component_of_wind_10m",
    "surface_solar_radiation_downwards_hourly"
]

for row in scene_dates:
    quarter = row["quarter"]
    scene_dt = datetime.datetime.fromisoformat(row["scene_date_utc"])
    hour_start = scene_dt.replace(minute=0, second=0, microsecond=0)
    hour_end = hour_start + datetime.timedelta(hours=1)

    era5 = (ee.ImageCollection("ECMWF/ERA5_LAND/HOURLY")
            .filterBounds(city_bbox)
            .filterDate(hour_start.isoformat(), hour_end.isoformat())
            .first())

    met_bands = era5.select(met_bands_list)

    task = ee.batch.Export.image.toDrive(
        image=met_bands,
        description=f"mumbai_ERA5_met_{quarter}",
        folder="urban_heat_project/raw_ERA5",
        region=city_bbox,
        scale=1000,  # ERA5-Land's native resolution is ~9km; this is interpolation, not real precision gain
        crs="EPSG:4326"
    )
    task.start()
    print(f"{quarter}: ERA5 export started, matched to scene time {row['scene_date_utc']}")

print("\nAll ERA5 exports started, matched to each quarter's actual Landsat acquisition time")