import numpy as np
import pandas as pd

def generate_geo_data(n_points=500, seed=42):
    """Generate synthetic location data with sales, competitors, population."""
    np.random.seed(seed)
    
    # Bounding box for a fictional city (Springfield)
    lat_center, lon_center = 40.75, -73.98
    lat = np.random.normal(lat_center, 0.03, n_points)
    lon = np.random.normal(lon_center, 0.04, n_points)
    
    # Business metrics
    sales = np.random.exponential(2000, n_points) + 500  # range 500–10000
    competitor_count = np.random.poisson(2, n_points)    # 0–5 typical
    population = np.random.gamma(2, 10000, n_points) + 2000  # 2000–40000
    
    # Store ID
    store_id = [f"STORE_{i:04d}" for i in range(n_points)]
    
    df = pd.DataFrame({
        'store_id': store_id,
        'latitude': lat,
        'longitude': lon,
        'sales': np.round(sales, 2),
        'competitor_count': competitor_count,
        'population': np.round(population, 0).astype(int)
    })
    
    # Ensure realistic boundaries (clip if needed)
    df['latitude'] = df['latitude'].clip(lat_center-0.1, lat_center+0.1)
    df['longitude'] = df['longitude'].clip(lon_center-0.15, lon_center+0.15)
    
    return df

if __name__ == "__main__":
    df = generate_geo_data()
    df.to_csv("data/sample_geo_data.csv", index=False)
    print("Saved data/sample_geo_data.csv")