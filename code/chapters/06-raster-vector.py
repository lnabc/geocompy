# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Raster-vector interactions {#raster-vector}
#
# ## Prerequisites

import pandas as pd
import matplotlib.pyplot as plt
pd.set_option("display.max_rows", 4)
pd.set_option("display.max_columns", 6)
pd.options.display.max_rows = 10
pd.options.display.max_columns = 6
pd.options.display.max_colwidth = 35
plt.rcParams["figure.figsize"] = (5, 5)

# Let's import the required packages:

import numpy as np
import geopandas as gpd
import rasterio
import rasterio.mask
from rasterio.plot import show

# and load the sample data:

src_srtm = rasterio.open("data/srtm.tif")
zion = gpd.read_file("data/zion.gpkg")

# ## Introduction
#
# ## Raster cropping
#
# Many geographic data projects involve integrating data from many different sources, such as remote sensing images (rasters) and administrative boundaries (vectors). Often the extent of input raster datasets is larger than the area of interest. In this case raster **cropping** and **masking** are useful for unifying the spatial extent of input data. Both operations reduce object memory use and associated computational resources for subsequent analysis steps, and may be a necessary preprocessing step before creating attractive maps involving raster data.
#
# We will use two objects to illustrate raster cropping:
#
# * The `srtm.tif` raster representing elevation (meters above sea level) in south-western Utah
# * The `zion.gpkg` vector layer representing the Zion National Park
#
# Both target and cropping objects must have the same projection. The following reprojects the vector layer `zion` into the CRS of the raster `src_srtm`:

zion = zion.to_crs(src_srtm.crs)

# To mask the image, i.e., convert all pixels which do not intersect with the `zion` polygon to "No Data", we use the `rasterio.mask.mask` function as follows:

out_image, out_transform = rasterio.mask.mask(src_srtm, zion.geometry, crop=False, nodata=9999)

# Note that we need to specify the "No Data" value.
#
# The result is the `out_image` array with the masked values: 

out_image

# and the new `out_transform`:

out_transform

# Note that masking (without cropping!) does not modify the raster spatial configuration. Therefore, the new transform is identical to the original:

src_srtm.transform

# To write the cropped raster to file, we need to modify the "No Data" setting in the metadata:

out_meta = src_srtm.meta
out_meta.update(nodata=9999)
out_meta

# Then we can write the cropped raster to file:

new_dataset = rasterio.open("output/srtm_masked.tif", "w", **out_meta)
new_dataset.write(out_image)
new_dataset.close()

# and re-import it:

src_srtm_masked = rasterio.open("output/srtm_masked.tif")
show(src_srtm_masked)

# Cropping means to reduce the raster extent to the extent of the vector layer. To crop *and* mask, we just need to set `crop=False` in `rasterio.mask.mask` (see above). Crop...
#
# Plot...

fig, axes = plt.subplots(ncols=3, figsize=(9,5))
show(src_srtm, ax=axes[0])
show(src_srtm, ax=axes[1])
show(src_srtm_masked, ax=axes[2])
axes[0].set_title("Original")
axes[1].set_title("Crop")
axes[2].set_title("Mask");

# ## Raster extraction
#
# ## Rasterization
#
# ## Spatial vectorization

src = rasterio.open("data/grain.tif")

# ## Exercises
