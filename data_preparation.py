import os
import random
from PIL import Image
import piexif
from geopy.geocoders import Nominatim

def get_image_paths(folder_path="damaged_images"):
    """Get list of image paths from specified folder"""
    valid_extensions = ('.jpg', '.jpeg', '.png')
    return [os.path.join(folder_path, f) 
            for f in os.listdir(folder_path)
            if f.lower().endswith(valid_extensions)]

def generate_geotags(centers, num_images, max_offset=0.01):
    """Generate Chicago coordinates within 1km of flood centers"""
    return [
        (
            center[0] + random.uniform(-max_offset, max_offset),
            center[1] + random.uniform(-max_offset, max_offset)
        )
        for center in random.choices(centers, k=num_images)
    ]

def validate_chicago_location(lat, lon):
    """Optional: Ensure coordinates are within Chicago"""
    geolocator = Nominatim(user_agent="disaster_mapper")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    return "Chicago" in location.address

def add_geotag(image_path, lat, lon):
    """Add GPS metadata to image with validation"""
    # Convert coordinates to EXIF format
    def deg_to_dms(decimal_deg):
        deg = int(decimal_deg)
        min = int((decimal_deg - deg) * 60)
        sec = (decimal_deg - deg - min/60) * 3600
        return [(deg, 1), (min, 1), (int(sec*100), 100)]
    
    # Create EXIF GPS data
    exif_dict = {
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: "N",
            piexif.GPSIFD.GPSLatitude: deg_to_dms(abs(lat)),
            piexif.GPSIFD.GPSLongitudeRef: "W",
            piexif.GPSIFD.GPSLongitude: deg_to_dms(abs(lon)),
        }
    }
    
    # Insert metadata into image
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

# Chicago flood centers (same as previous)
DISASTER_CENTERS = [
    (41.7750, -87.6417),  # Englewood
    (41.7460, -87.6135),  # Chatham
    (41.8186, -87.6989),  # Brighton Park
    (41.9686, -87.7236),  # Albany Park
    (41.8600, -87.7000),  # Douglas Park
    (41.8050, -87.6720),  # Back of the Yards
    (41.9547, -87.6817),  # North Center
    (41.9231, -87.7091)   # Logan Square
]

# Get existing images
image_files = get_image_paths()

# Generate locations
geotags = generate_geotags(DISASTER_CENTERS, len(image_files))

# Add geotags with validation
for img_path, (lat, lon) in zip(image_files, geotags):
    try:
        
        add_geotag(img_path, lat, lon)
        print(f"Geotagged {os.path.basename(img_path)} to ({lat:.4f}, {lon:.4f})")

    except Exception as e:
        print(f"Error processing {img_path}: {str(e)}")
