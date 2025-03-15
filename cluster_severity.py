import json
import pandas as pd
from pyproj import Proj, transform
import numpy as np

def calculate_cluster_severity(cluster_centroids_file, damage_assessments_file):
    """
    Calculate average severity rating per cluster center
    Returns: List of dicts with cluster info and average rating
    """
    # Load data
    clusters = pd.read_csv(cluster_centroids_file)
    with open(damage_assessments_file) as f:
        assessments = json.load(f)

    # Convert cluster centers to Web Mercator
    wgs84 = Proj(init='epsg:4326')
    mercator = Proj(init='epsg:3857')
    
    cluster_points = []
    for _, row in clusters.iterrows():
        x, y = transform(wgs84, mercator, row['longitude'], row['latitude'])
        cluster_points.append({
            'x': x,
            'y': y,
            'cluster_id': row['cluster'],
            'original_lat': row['latitude'],
            'original_lon': row['longitude']
        })

    # Convert assessment points to Web Mercator
    assessment_points = []
    for assessment in assessments:
        x, y = transform(wgs84, mercator, 
                       assessment['location']['longitude'],
                       assessment['location']['latitude'])
        assessment_points.append({
            'x': x,
            'y': y,
            'rating': assessment['rating']
        })

    # Calculate nearest cluster for each assessment
    cluster_ratings = {c['cluster_id']: [] for c in cluster_points}
    
    for assessment in assessment_points:
        min_dist = float('inf')
        nearest_cluster = None
        
        for cluster in cluster_points:
            dist = np.sqrt(
                (assessment['x'] - cluster['x'])**2 +
                (assessment['y'] - cluster['y'])**2
            )
            
            if dist < min_dist:
                min_dist = dist
                nearest_cluster = cluster['cluster_id']
        
        if nearest_cluster is not None:
            cluster_ratings[nearest_cluster].append(assessment['rating'])

    # Calculate averages and prepare results
    results = []
    for cluster in cluster_points:
        ratings = cluster_ratings[cluster['cluster_id']]
        avg_rating = np.mean(ratings) if ratings else 0
        
        results.append({
            'cluster_id': cluster['cluster_id'],
            'latitude': cluster['original_lat'],
            'longitude': cluster['original_lon'],
            'average_rating': round(avg_rating, 2),
            'image_count': len(ratings)
        })

    return results

# Example usage
if __name__ == "__main__":
    severity_scores = calculate_cluster_severity(
        cluster_centroids_file='cluster_centroids.csv',
        damage_assessments_file='damage_assessments.json'
    )
    
    # Save results
    with open('cluster_severity.json', 'w') as f:
        json.dump(severity_scores, f, indent=2)
    
    print(f"Calculated severity for {len(severity_scores)} clusters")
