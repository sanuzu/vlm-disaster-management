import streamlit as st
import os
import json
import pandas as pd
import numpy as np
from PIL import Image
import subprocess
import webbrowser
from cluster_severity import calculate_cluster_severity
from geocoder import get_location_name

# Folder picker components
try:
    from tkinter import Tk
    from tkinter.filedialog import askdirectory
except ImportError:
    Tk = None

# Configuration
DEFAULT_IMAGE_FOLDER = "damaged_images"
CLUSTER_FILE = "cluster_centroids.csv"
ASSESSMENT_FILE = "damage_assessments.json"

def select_image_folder():
    """Open folder selection dialog"""
    try:
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = askdirectory(title="Select Images Folder")
        root.destroy()
        return folder or DEFAULT_IMAGE_FOLDER
    except Exception as e:
        st.error(f"Folder selection failed: {str(e)}")
        return DEFAULT_IMAGE_FOLDER

def main():
    st.set_page_config(layout="wide")
    st.title("Disaster Management Analytics Dashboard")
    
    # Initialize session state
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'selected_cluster' not in st.session_state:
        st.session_state.selected_cluster = None
    if 'image_folder' not in st.session_state:
        st.session_state.image_folder = DEFAULT_IMAGE_FOLDER

    # Sidebar controls
    with st.sidebar:
        st.header("Configuration")
        
        # Factors management button
        if st.button("⚙️ Manage Assessment Factors"):
            try:
                subprocess.Popen(["streamlit", "run", "factors.py", "--server.port=8503"])
                webbrowser.open_new_tab("http://localhost:8503")
            except Exception as e:
                st.error(f"Factors management failed: {str(e)}")

        # Folder selection
        if st.button("📁 Select Image Folder"):
            selected_folder = select_image_folder()
            if os.path.isdir(selected_folder):
                st.session_state.image_folder = selected_folder
                with open('config.json', 'w') as f:
                    json.dump({'image_folder': st.session_state.image_folder}, f)
                st.rerun()
        
        st.write(f"**Selected Folder:**\n`{st.session_state.image_folder}`")
        
        # Processing control
        if st.button("🚀 Process Images"):
            with st.spinner("Analyzing disaster data..."):
                try:
                    from damage_assessor import main as process_images
                    from cluster_analysis import find_clusters
                    
                    #process_images(image_folder=st.session_state.image_folder)

                    with open(ASSESSMENT_FILE) as f:
                        assessments = json.load(f)

                    geo_data = pd.DataFrame([{
                        'latitude': a['location']['latitude'],
                        'longitude': a['location']['longitude']
                    } for a in assessments])

                    clustered_data = find_clusters(geo_data)
                    
                    with open(ASSESSMENT_FILE, 'r+') as f:
                        assessments = json.load(f)
                        if len(assessments) != len(clustered_data):
                            raise ValueError("Data mismatch between assessments and clusters")
                            
                        for a, cluster_id in zip(assessments, clustered_data['cluster']):
                            a['cluster'] = int(cluster_id)
                        
                        f.seek(0)
                        json.dump(assessments, f, indent=2)
                        f.truncate()

                    non_noise = clustered_data[clustered_data['cluster'] != -1]
                    centroids = non_noise.groupby('cluster').agg({
                        'latitude': 'mean',
                        'longitude': 'mean'
                    }).reset_index()
                    
                    counts = non_noise['cluster'].value_counts()
                    centroids = centroids.merge(
                        counts.rename('count').reset_index(),
                        on='cluster'
                    )
                    centroids.to_csv(CLUSTER_FILE, index=False)
                    
                    severity_scores = calculate_cluster_severity(
                        CLUSTER_FILE,
                        ASSESSMENT_FILE
                    )
                    with open('cluster_severity.json', 'w') as f:
                        json.dump(severity_scores, f, indent=2)
                    
                    st.session_state.processed = True
                    st.success("Processing completed!")
                    
                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")

        if st.button("🗺️ Generate Severity Map"):
            try:
                subprocess.Popen(["streamlit", "run", "map_generator.py", "--server.port=8502"])
                webbrowser.open_new_tab("http://localhost:8502")
            except Exception as e:
                st.error(f"Map generation failed: {str(e)}")

    # Main display area
    if st.session_state.processed:
        clusters = pd.read_csv(CLUSTER_FILE)
        with open(ASSESSMENT_FILE) as f:
            assessments = json.load(f)
        
        st.header("Cluster Analysis")
        cols = st.columns(4)
        for idx, cluster in clusters.iterrows():
            location_name = get_location_name(cluster['latitude'], cluster['longitude'])
            with cols[idx % 4]:
                if st.button(
                    f"Cluster {cluster['cluster']}\n"
                    f"Images: {cluster['count']}\n"
                    f"Location: {location_name}",
                    key=f"cluster_{cluster['cluster']}"
                ):
                    st.session_state.selected_cluster = cluster['cluster']

        if st.session_state.selected_cluster is not None:
            st.subheader(f"Images in Cluster {st.session_state.selected_cluster}")
            cluster_images = [a for a in assessments if a.get('cluster') == st.session_state.selected_cluster]
            
            if not cluster_images:
                st.warning("No images found in this cluster")
            else:
                cols = st.columns(4)
                for idx, img_data in enumerate(cluster_images):
                    with cols[idx % 4]:
                        img_path = os.path.join(st.session_state.image_folder, img_data['image_name'])
                        try:
                            st.image(
                                Image.open(img_path),
                                caption=f"Severity: {img_data['rating']}",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Failed to load {img_data['image_name']}: {str(e)}")
    else:
        st.info("Please select an image folder and process images using the sidebar controls")

if __name__ == "__main__":
    main()
