import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

def preprocess_dem(input_file, output_file):
    # Open the HGT file
    with rasterio.open(input_file) as src:
        # Read the elevation data
        elevation = src.read(1)
        
        # Get the geotransform information
        transform = src.transform
        
        # Create output GeoTIFF
        with rasterio.open(
            output_file,
            'w',
            driver='GTiff',
            height=elevation.shape[0],
            width=elevation.shape[1],
            count=1,
            dtype=elevation.dtype,
            crs='EPSG:4326',  # WGS84
            transform=transform,
            nodata=-32768
        ) as dst:
            # Write the elevation data
            dst.write(elevation, 1)
    
    # Save as NumPy array for direct loading
    np.save('elevation_data.npy', elevation)
    
    # Create visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(elevation, cmap='terrain')
    plt.colorbar(label='Elevation (meters)')
    plt.title('DEM Visualization')
    plt.savefig('dem_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    input_file = "N39E035.SRTMGL1.hgt/N39E035.hgt"
    output_file = "processed_dem.tif"
    
    if os.path.exists(input_file):
        print(f"Processing DEM file: {input_file}")
        preprocess_dem(input_file, output_file)
        print(f"Processed DEM saved as: {output_file}")
        print("NumPy array saved as: elevation_data.npy")
        print("Visualization saved as: dem_visualization.png")
    else:
        print(f"Error: Input file {input_file} not found!") 