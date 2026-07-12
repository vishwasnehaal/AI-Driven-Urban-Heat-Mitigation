import ee
import datetime

ee.Initialize(project="velvety-gearbox-451304-s0")

lon_min, lat_min, lon_max, lat_max = 72.5833, 18.7833, 73.2000, 19.6000
city_bbox = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

def generate_quarters(start_year=2023, end_date=None):
    if end_date is None:
        end_date = datetime.date.today()
    quarters = []
    year = start_year
    while True:
        for i, q_start_month in enumerate([1, 4, 7, 10], start=1):
            q_start = datetime.date(year, q_start_month, 1)
            if q_start > end_date:
                return quarters
            q_end_month = q_start_month + 2
            q_end = (datetime.date(year, 12, 31) if q_end_month == 12
                      else datetime.date(year, q_end_month + 1, 1) - datetime.timedelta(days=1))
            q_end = min(q_end, end_date)
            quarters.append({"start": q_start.isoformat(), "end": q_end.isoformat(), "label": f"{year}_Q{i}"})
        year += 1

quarters = generate_quarters(start_year=2023)

for q in quarters:
    s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
          .filterBounds(city_bbox).filterDate(q["start"], q["end"])
          .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)))
    n = s2.size().getInfo()
    print(f"{q['label']}: {n} S2 images for compositing")

    if n == 0:
        print("  -> no usable images, skipping")
        continue

    # B11 (SWIR) is included here so NDBI can be computed later in Week 2
    composite = s2.median().select(["B2", "B3", "B4", "B8", "B11"]).clip(city_bbox)

    task = ee.batch.Export.image.toDrive(
        image=composite,
        description=f"mumbai_S2_{q['label']}",
        folder="urban_heat_project/raw_LULC/sentinel2",
        region=city_bbox,
        scale=10,
        crs="EPSG:4326"
    )
    task.start()
    print(f"  -> export started: mumbai_S2_{q['label']}")

print("\nAll S2 exports started. Check https://code.earthengine.google.com/tasks")