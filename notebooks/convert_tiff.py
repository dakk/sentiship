import rasterio
import numpy as np

DIR = './sattest/'
# Open the band files using rasterio
b02 = rasterio.open(DIR + 'S2B_MSIL2A_20230428T100559_N0509_R022_T32SNJ_20230428T133214.SAFE/GRANULE/L2A_T32SNJ_A032080_20230428T101606/IMG_DATA/R10m/T32SNJ_20230428T100559_B02_10m.jp2')
b03 = rasterio.open(DIR + 'S2B_MSIL2A_20230428T100559_N0509_R022_T32SNJ_20230428T133214.SAFE/GRANULE/L2A_T32SNJ_A032080_20230428T101606/IMG_DATA/R10m/T32SNJ_20230428T100559_B03_10m.jp2')
b04 = rasterio.open(DIR + 'S2B_MSIL2A_20230428T100559_N0509_R022_T32SNJ_20230428T133214.SAFE/GRANULE/L2A_T32SNJ_A032080_20230428T101606/IMG_DATA/R10m/T32SNJ_20230428T100559_B04_10m.jp2')

# Read the data into numpy arrays
b02_data = b02.read(1).astype(np.uint16)
b03_data = b03.read(1).astype(np.uint16)
b04_data = b04.read(1).astype(np.uint16)

# Create a new rasterio dataset with the desired output format
with rasterio.open('output.tif', 'w', driver='GTiff', 
                   width=b02.width, height=b02.height,
                   count=3, dtype=b02_data.dtype, 
                   crs=b02.crs, transform=b02.transform) as dst:
    # Write the data to the new dataset
    dst.write(b02_data, 1)
    dst.write(b03_data, 2)
    dst.write(b04_data, 3)
