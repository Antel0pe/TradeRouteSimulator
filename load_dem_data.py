import numpy as np
import matplotlib.pyplot as plt

def analyze_elevation_data():
    # Load the elevation data
    print("Loading elevation data...")
    elevation = np.load('elevation_data.npy')
    
    # Basic statistics
    print(f"Array shape: {elevation.shape}")
    print(f"Data type: {elevation.dtype}")
    print(f"Min elevation: {elevation.min()} meters")
    print(f"Max elevation: {elevation.max()} meters")
    print(f"Mean elevation: {elevation.mean():.1f} meters")
    print(f"Standard deviation: {elevation.std():.1f} meters")
    
    # Remove no-data values for more accurate statistics
    valid_elevation = elevation[elevation != -32768]
    if len(valid_elevation) > 0:
        print(f"\nValid data points: {len(valid_elevation)}")
        print(f"Min valid elevation: {valid_elevation.min()} meters")
        print(f"Max valid elevation: {valid_elevation.max()} meters")
        print(f"Mean valid elevation: {valid_elevation.mean():.1f} meters")
    
    # Create a histogram of elevation values
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.hist(valid_elevation, bins=50, alpha=0.7, color='brown')
    plt.xlabel('Elevation (meters)')
    plt.ylabel('Frequency')
    plt.title('Elevation Distribution')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.imshow(elevation, cmap='terrain', aspect='equal')
    plt.colorbar(label='Elevation (meters)')
    plt.title('Elevation Map')
    
    plt.tight_layout()
    plt.savefig('elevation_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return elevation

if __name__ == "__main__":
    elevation_data = analyze_elevation_data()
    print(f"\nElevation data loaded successfully!")
    print(f"You can now work with the 'elevation_data' array: {elevation_data.shape}") 