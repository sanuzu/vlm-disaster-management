import streamlit as st
import folium
import pandas as pd
import json
from streamlit_folium import folium_static

def generate_severity_map():
    st.set_page_config(layout="wide")
    st.title("Disaster Severity Heatmap")
    
    try:
        # Load cluster severity data instead of centroids
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
        
        # Add cluster markers using severity data
        for cluster in clusters:
            folium.CircleMarker(
                location=[cluster['latitude'], cluster['longitude']],
                radius=cluster['average_rating']*1.2,
                color=__get_color(cluster['average_rating']),
                fill=True,
                fill_opacity=0.5,
                popup=f"Severity: {cluster['average_rating']}/10\nImages: {cluster['image_count']}"
            ).add_to(m)
        
        # Add heatmap layer
        heat_data = [[a['location']['latitude'], a['location']['longitude'], a['rating']] 
                    for a in assessments if a.get('cluster') != -1]
        folium.plugins.HeatMap(heat_data, radius=40).add_to(m)
        
        folium_static(m, width=1200, height=800)

        
    except FileNotFoundError:
        st.error("Required data files not found. Process images first in the main dashboard.")

def __get_color(rating):
    """Convert severity rating to color gradient (red = high severity)"""
    return f"hsl({(10 - rating) * 10}, 100%, 50%)"  # Adjusted hue scaling


if __name__ == "__main__":
    generate_severity_map()
