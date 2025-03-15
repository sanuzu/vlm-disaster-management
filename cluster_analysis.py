import pandas as pd
import json  # Added import
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
    Returns: Original DataFrame with cluster labels (-1 for noise)
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
    
    # Assign cluster labels to original data
    geo_data = geo_data.copy()
    geo_data['cluster'] = db.labels_
    
    return geo_data  # Contains all points with cluster IDs (-1 for noise)

def get_cluster_centroids(geo_data):
    """Calculate cluster centroids from clustered data"""
    non_noise = geo_data[geo_data['cluster'] != -1]
    centroids = non_noise.groupby('cluster').agg({
        'latitude': 'mean',
        'longitude': 'mean'
    }).reset_index()
    centroids['count'] = non_noise['cluster'].value_counts().values
    return centroids

# Modified example usage
if __name__ == "__main__":
    # Load data from damage_assessments.json
    with open('damage_assessments.json') as f:
        assessments = json.load(f)
    
    # Create DataFrame from JSON data
    geo_data = pd.DataFrame([{
        'image_path': item['image_name'],
        'latitude': item['location']['latitude'],
        'longitude': item['location']['longitude']
    } for item in assessments])
    
    # Find clusters with minimum 4 points within 600ft
    clusters = find_clusters(geo_data)
    
    # Save results
    clusters.to_csv('cluster_centroids.csv', index=False)
    print(f"Found {len(clusters)} clusters:\n{clusters}")
    print("\nCluster columns:", clusters.columns.tolist())
