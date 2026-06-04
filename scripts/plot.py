#!/usr/bin/env python3
"""A letöltött NetCDF-ből térkép-PNG-t rajzol a Földközi-tenger felszíni
hőmérsékletéről (thetao). Használat: python scripts/plot.py 2026-06-04
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")  # nincs kijelző a CI-ben
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import xarray as xr

date = sys.argv[1]
nc_path = f"data/med_sst_{date}.nc"
out_dir = "maps"
out_path = f"{out_dir}/med_sst_{date}.png"
os.makedirs(out_dir, exist_ok=True)

ds = xr.open_dataset(nc_path)
da = ds["thetao"].squeeze()  # az 1 méretű idő/mélység dimenziók eldobása

# a koordináták neve a Copernicus-terméknél longitude/latitude
lon = "longitude" if "longitude" in da.coords else "lon"
lat = "latitude" if "latitude" in da.coords else "lat"

fig = plt.figure(figsize=(12, 5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-17.3, 36.3, 30.1, 46.0], crs=ccrs.PlateCarree())

mesh = da.plot.pcolormesh(
    ax=ax,
    x=lon,
    y=lat,
    transform=ccrs.PlateCarree(),
    cmap="RdYlBu_r",
    add_colorbar=True,
    cbar_kwargs={"label": "Tengervíz-hőmérséklet (°C)", "shrink": 0.8},
)

ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=2)
ax.coastlines(resolution="50m", linewidth=0.5, zorder=3)
gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.5)
gl.top_labels = False
gl.right_labels = False

ax.set_title(f"Földközi-tenger – felszíni hőmérséklet ({date})")

fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Kész: {out_path}")
