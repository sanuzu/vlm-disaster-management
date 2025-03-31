from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import streamlit as st
import pandas as pd
import time

@st.cache_data(show_spinner=False)
def get_location_name(latitude, longitude):
    """Get human-readable location name from coordinates"""
    geolocator = Nominatim(user_agent="disaster_mgmt_app")
    reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
    
    try:
        location = reverse(f"{latitude}, {longitude}", exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            return _format_address(address)
    except Exception as e:
        pass
    return f"{latitude:.4f}, {longitude:.4f}"  # Fallback to coordinates

def _format_address(address):
    """Priority-based address formatting"""
    components = [
        address.get('neighbourhood'),
        address.get('suburb'),
        address.get('village'),
        address.get('town'),
        address.get('city'),
        address.get('county'),
        address.get('state'),
        address.get('country')
    ]
    return next((item for item in components if item), "Unknown Location")
