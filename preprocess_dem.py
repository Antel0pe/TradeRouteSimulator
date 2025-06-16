import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt

def preprocess_dem(input_file, output_file):
    # Open the HGT file
    dataset = gdal.Open(input_file)
    if dataset is None:
        raise Exception(f"Could not open {input_file}")
    
    # Get the geotransform
    geotransform = dataset.GetGeoTransform()
    
    # Read the data
    band = dataset.GetRasterBand(1)
    elevation = band.ReadAsArray()
    
    # Create output GeoTIFF
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(
        output_file,
        dataset.RasterXSize,
        dataset.RasterYSize,
        1,
        gdal.GDT_Float32
    )
    
    # Set the geotransform and projection
    out_dataset.SetGeoTransform(geotransform)
    out_dataset.SetProjection(dataset.GetProjection())
    
    # Write the data
    out_band = out_dataset.GetRasterBand(1)
    out_band.WriteArray(elevation)
    out_band.SetNoDataValue(-32768)  # SRTM no-data value
    
    # Clean up
    dataset = None
    out_dataset = None
    
    # Create a simple visualization
    plt.figure(figsize=(10, 10))
    plt.imshow(elevation, cmap='terrain')
    plt.colorbar(label='Elevation (meters)')
    plt.title('DEM Visualization')
    plt.savefig('dem_visualization.png')
    plt.close()

if __name__ == "__main__":
    input_file = "N39E035.SRTMGL1.hgt/N39E035.SRTMGL1.hgt"
    output_file = "processed_dem.tif"
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found!")
    else:
        print("Processing DEM file...")
        preprocess_dem(input_file, output_file)
        print(f"Processing complete! Output saved as {output_file}")
        print("Visualization saved as dem_visualization.png") 