import streamlit as st
import os
import json
import pandas as pd
import numpy as np
from PIL import Image
# Add to imports
import subprocess
import webbrowser
from cluster_severity import calculate_cluster_severity

# Configuration
DEFAULT_IMAGE_FOLDER = "damaged_images"
CLUSTER_FILE = "cluster_centroids.csv"
ASSESSMENT_FILE = "damage_assessments.json"

def main():
    st.set_page_config(layout="wide")
    st.title("Disaster Management Analytics Dashboard")
    
    # Initialize session state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'selected_cluster' not in st.session_state:
        st.session_state.selected_cluster = None

    # Sidebar controls
    with st.sidebar:
        st.header("Configuration")
        image_folder = st.text_input("Image folder path:", DEFAULT_IMAGE_FOLDER)
        
        if st.button("🚀 Process Images"):
            with st.spinner("Analyzing disaster data..."):
                try:
                    from damage_assessor import main as process_images
                    from cluster_analysis import find_clusters
                    
                    # 1. Run image processing
                    # process_images()

                    # 2. Load assessments and perform clustering
                    with open(ASSESSMENT_FILE) as f:
                        assessments = json.load(f)

                    geo_data = pd.DataFrame([{
                        'latitude': a['location']['latitude'],
                        'longitude': a['location']['longitude']
                    } for a in assessments])

                    # 3. Get clustered data with image-cluster mapping
                    clustered_data = find_clusters(geo_data)
                    
                    # 4. Update assessments with cluster IDs
                    with open(ASSESSMENT_FILE, 'r+') as f:
                        assessments = json.load(f)
                        if len(assessments) != len(clustered_data):
                            raise ValueError("Mismatch between assessments and cluster data")
                            
                        for a, cluster_id in zip(assessments, clustered_data['cluster']):
                            a['cluster'] = int(cluster_id)
                        
                        f.seek(0)
                        json.dump(assessments, f, indent=2)
                        f.truncate()

                    # 5. Calculate and save centroids (excluding noise)
                    non_noise = clustered_data[clustered_data['cluster'] != -1]
                    centroids = non_noise.groupby('cluster').agg({
                        'latitude': 'mean',
                        'longitude': 'mean'
                    }).reset_index()
                    
                    # Get counts from non-noise data
                    counts = non_noise['cluster'].value_counts()
                    centroids = centroids.merge(
                        counts.rename('count').reset_index(),
                        on='cluster'
                    )
                    
                    centroids.to_csv(CLUSTER_FILE, index=False)
                    severity_scores = calculate_cluster_severity(
                        'cluster_centroids.csv',
                        'damage_assessments.json'
                    )
                    with open('cluster_severity.json', 'w') as f:
                        json.dump(severity_scores, f, indent=2)
                    st.session_state.processed = True
                    st.success("Processing completed!")
                    
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")
        
        # Modify the dummy button in sidebar
        if st.button("🗺️ Generate Severity Map"):
            try:
                # Run map generator in background
                subprocess.Popen(["streamlit", "run", "map_generator.py", "--server.port=8502"])
                # Open in new tab
                webbrowser.open_new_tab("http://localhost:8502")
            except Exception as e:
                st.error(f"Map generation failed: {str(e)}")
        

    # Main display area
    if st.session_state.processed:
        # Load data
        clusters = pd.read_csv(CLUSTER_FILE)
        with open(ASSESSMENT_FILE) as f:
            assessments = json.load(f)
        
        # Cluster selection
        st.header("Cluster Analysis")
        cols = st.columns(4)
        for idx, cluster in clusters.iterrows():
            with cols[idx % 4]:
                if st.button(
                    f"Cluster {cluster['cluster']}\n"
                    f"Images: {cluster['count']}\n"
                    f"Location: {cluster['latitude']:.4f}, {cluster['longitude']:.4f}",
                    key=f"cluster_{cluster['cluster']}"
                ):
                    st.session_state.selected_cluster = cluster['cluster']

        # Display images for selected cluster
        if st.session_state.selected_cluster is not None:
            st.subheader(f"Images in Cluster {st.session_state.selected_cluster}")
            cluster_images = [a for a in assessments if a.get('cluster') == st.session_state.selected_cluster]
            
            if not cluster_images:
                st.warning("No images found in this cluster")
            else:
                cols = st.columns(4)
                for idx, img_data in enumerate(cluster_images):
                    with cols[idx % 4]:
                        img_path = os.path.join(image_folder, img_data['image_name'])
                        try:
                            st.image(
                                Image.open(img_path),
                                caption=f"Severity: {img_data['rating']}",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Failed to load {img_data['image_name']}: {str(e)}")

    else:
        st.info("Please process images using the sidebar controls to begin analysis")

if __name__ == "__main__":
    main()
