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

# a kép arányát a terület arányához igazítjuk, hogy ne maradjon üres sáv
extent = [-17.3, 36.3, 30.1, 46.0]
aspect = (extent[1] - extent[0]) / (extent[3] - extent[2])  # ~3.37
fig = plt.figure(figsize=(16, 16 / aspect))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(extent, crs=ccrs.PlateCarree())

mesh = da.plot.pcolormesh(
    ax=ax,
    x=lon,
    y=lat,
    transform=ccrs.PlateCarree(),
    cmap="RdYlBu_r",
    vmin=18,
    vmax=28,
    add_colorbar=True,
    cbar_kwargs={
        "label": "°C",
        "shrink": 0.35,   # rövid skála
        "aspect": 50,     # vékony skála
        "pad": 0.01,      # közel a térképhez
    },
)

ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=2)
ax.coastlines(resolution="50m", linewidth=0.5, zorder=3)

# koordináták / tengelyfeliratok eltávolítása
ax.set_title("")
ax.set_xlabel("")
ax.set_ylabel("")

# a térkép töltse ki a képet, minimális margóval
fig.subplots_adjust(left=0, right=0.99, top=0.99, bottom=0)

# dpi: a ~4.2 km-es rács kb. 1300 cella széles; 16" * 220 dpi ≈ 3500 px,
# azaz ~2.7× túlmintázás — éles cellaélek, de nincs fölösleges fájlméret
fig.savefig(out_path, dpi=220, bbox_inches="tight", pad_inches=0.02)
print(f"Kész: {out_path}")
