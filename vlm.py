import json
import os
import piexif
from PIL import Image
from transformers import pipeline

# Initialize Florence-2 through Hugging Face
vlm = pipeline("visual-question-answering", model="microsoft/florence-2-base")

def extract_geotag(image_path):
    """Extract GPS coordinates from image EXIF data"""
    try:
        img = Image.open(image_path)
        exif_data = piexif.load(img.info['exif'])
        gps = exif_data['GPS']
        
        lat = gps[piexif.GPSIFD.GPSLatitude]
        lat_ref = gps[piexif.GPSIFD.GPSLatitudeRef]
        lon = gps[piexif.GPSIFD.GPSLongitude]
        lon_ref = gps[piexif.GPSIFD.GPSLongitudeRef]
        
        # Convert to decimal degrees
        def to_deg(v):
            return float(v[0]) + float(v[1])/60 + float(v[2])/3600
        
        return {
            'latitude': to_deg(lat) * (-1 if lat_ref == b'S' else 1),
            'longitude': to_deg(lon) * (-1 if lon_ref == b'W' else 1)
        }
    except:
        return {'latitude': 0.0, 'longitude': 0.0}

def rate_damage(image_path, factors):
    """Get damage rating using Florence-2 VLM"""
    prompt = (
        "Assess disaster damage severity from 1-10 considering:\n" +
        "\n".join(f"- {f}" for f in factors) +
        "\nRespond ONLY with the numerical rating."
    )
    
    result = vlm(image=image_path, question=prompt)
    try:
        return min(10, max(1, int(result['answer'].strip())))
    except:
        return 5  # Default if parsing fails

# Load assessment factors
with open('factors.txt') as f:
    factors = [line.strip() for line in f]

# Process images
results = []
for img_name in os.listdir('damaged_images'):
    img_path = os.path.join('damaged_images', img_name)
    
    results.append({
        'image_name': img_name,
        'location': extract_geotag(img_path),
        'rating': rate_damage(img_path, factors)
    })

# Save results
with open('damage_assessments.json', 'w') as f:
    json.dump(results, f, indent=2)
