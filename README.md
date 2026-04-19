# Biodiversity — CCE mooring data notebook

## What this repo contains

| Item | Purpose |
|------|---------|
| **`cce_mooring_timeseries.ipynb`** | Main notebook: download CCE1/CCE2 mooring data (OceanSITES THREDDS), merge temperature / nitrate / oxygen, export CSVs, optional dashboard summaries. |
| **`requirements.txt`** | Python dependencies (`xarray`, `pandas`, `requests`, etc.). |

Run the notebook top to bottom after creating a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook cce_mooring_timeseries.ipynb
```

## Outputs (created next to the notebook)

| File pattern | Description |
|--------------|-------------|
| `cce_mooring_timeseries.csv` | Merged mooring time series |
| `cce_thredds_file_catalog.csv` | Full THREDDS file list |
| `cce_deployment_file_index.csv` | Per-deployment instrument files |
| `dashboard_cce_*.csv` | Monthly/annual means, trends, warming spikes (after Section 6) |

## Data source

Data are **not** from the CalCOFI website API directly; they come from **NDBC OceanSITES** NetCDF via OPeNDAP, as linked from the [CCE moorings page](https://mooring.ucsd.edu/cce/). See the notebook header for links and usage policy.
