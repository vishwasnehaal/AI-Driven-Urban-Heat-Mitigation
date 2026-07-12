# pipeline/
Data pull scripts for LST, LULC, DEM, and met data. Pulls a full quarterly time series (2023–present) for Mumbai + surrounding region.

## Run order
1. `pull_lst.py` — Landsat LST, one per quarter. Also writes `data/processed/lst_scene_dates.csv`.
2. `pull_era5.py` — needs the CSV from step 1, so run this after.
3. `pull_s2.py` — Sentinel-2 LULC. Independent, run whenever.
4. `pull_dem.py` — DEM + slope. One-time only, no need to re-run per quarter.

Exports go straight to Google Drive (`urban_heat_project/...`), not your local disk — download from there into `data/raw/` after running.

## Before running
- Activate venv: `venv\Scripts\activate`
- Every script needs your GEE project ID filled in: `ee.Initialize(project="will type soon")`
- Bounding box (same across all scripts): `72.5833, 18.7833, 73.2000, 19.6000`

## Heads up
- `pull_lst.py` masks clouds + mosaics per quarter — don't swap this for a simple `.first()`, it'll leave gaps if your AOI spans more than one Landsat tile.
- Some quarters may return 0 usable scenes (monsoon cloud cover) — that's expected, script just skips and prints a note.