import pandas as pd
from sklearn.cluster import DBSCAN
from pyproj import Proj, transform
import numpy as np

def convert_to_web_mercator(lat, lon):
    """Convert WGS84 coordinates to Web Mercator (EPSG:3857)"""
    wgs84 = Proj(init='epsg:4326')
    mercator = Proj(init='epsg:3857')
    return transform(wgs84, mercator, lon, lat)

def find_clusters(geo_data, min_samples=4, max_distance_ft=600):
    """
    Cluster geo-tagged points using DBSCAN
    :param geo_data: DataFrame with 'latitude' and 'longitude' columns
    :param min_samples: Minimum points to form a cluster
    :param max_distance_ft: Maximum distance between cluster points (feet)
    """
    # Convert coordinates to meters (1 ft = 0.3048 meters)
    max_distance_m = max_distance_ft * 0.3048
    
    # Convert geographic coordinates to projected system
    coords = geo_data.apply(
        lambda row: convert_to_web_mercator(row['latitude'], row['longitude']), 
        axis=1
    ).tolist()
    
    # Perform DBSCAN clustering
    db = DBSCAN(
        eps=max_distance_m,
        min_samples=min_samples,
        metric='euclidean'
    ).fit(coords)
    
    # Extract cluster labels and filter noise
    geo_data['cluster'] = db.labels_
    clusters = geo_data[geo_data['cluster'] != -1]
    
    # Calculate cluster centroids
    centroids = clusters.groupby('cluster').agg({
        'latitude': 'mean',
        'longitude': 'mean',
        'cluster': 'count'
    }).rename(columns={'cluster': 'count'})
    
    return centroids.reset_index()

# Example usage
if __name__ == "__main__":
    # Load sample data (replace with your image metadata)
    data = pd.read_csv('geo_images.csv')  # Columns: image_path, latitude, longitude
    
    # Find clusters with minimum 4 points within 600ft
    clusters = find_clusters(data)
    
    # Save results
    clusters.to_csv('cluster_centroids.csv', index=False)
    print(f"Found {len(clusters)} clusters:\n{clusters}")
