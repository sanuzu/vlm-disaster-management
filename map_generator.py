import streamlit as st
import folium
import pandas as pd
import json
import base64
import os
from streamlit_folium import folium_static
from PIL import Image
from io import BytesIO

def generate_severity_map():
    st.set_page_config(layout="wide")
    st.title("Disaster Severity Heatmap")
    
    try:
        # Load configuration and data
        with open("config.json") as f:
            config = json.load(f)
            
        with open("cluster_severity.json") as f:
            clusters = json.load(f)
            
        with open("damage_assessments.json") as f:
            assessments = json.load(f)

        # Create base map
        m = folium.Map(
            location=[clusters[0]['latitude'], clusters[0]['longitude']],
            zoom_start=12,
            tiles='CartoDB positron'
        )
        
        # Add cluster markers with images
        for cluster in clusters:
            # Find images in this cluster
            cluster_images = [a for a in assessments 
                            if a.get('cluster') == cluster['cluster_id']]
            
            # Create popup content
            popup_content = f"<b>Severity:</b> {cluster['average_rating']}/10<br>"
            popup_content += f"<b>Images:</b> {len(cluster_images)}<br>"
            popup_content += "<div style='max-height: 200px; overflow-y: auto;'>"
            
            # Add first 3 images as thumbnails
            for img_data in cluster_images[:3]:
                img_path = os.path.join(config['image_folder'], img_data['image_name'])
                try:
                    # Resize and encode image
                    img = Image.open(img_path)
                    img.thumbnail((150, 150))
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    popup_content += (
                        f"<img src='data:image/jpeg;base64,{encoded}' "
                        "style='width: 150px; margin: 2px;'/>"
                    )
                except Exception as e:
                    popup_content += f"<p>Error loading image: {img_data['image_name']}</p>"
            
            popup_content += "</div>"
            
            # Create marker with popup
            folium.CircleMarker(
                location=[cluster['latitude'], cluster['longitude']],
                radius=cluster['average_rating'] * 1.5,
                color=__get_color(cluster['average_rating']),
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_content, max_width=300)
            ).add_to(m)
        
        # Add heatmap layer
        heat_data = [[a['location']['latitude'], a['location']['longitude'], a['rating']] 
                    for a in assessments if a.get('cluster') != -1]
        folium.plugins.HeatMap(heat_data, radius=40).add_to(m)
        
        folium_static(m, width=1200, height=800)

    except FileNotFoundError:
        st.error("Required data files not found. Process images first in the main dashboard.")

def __get_color(rating):
    """Convert severity rating to color gradient"""
    return f"hsl({(10 - rating) * 10}, 100%, 50%)"

if __name__ == "__main__":
    generate_severity_map()
