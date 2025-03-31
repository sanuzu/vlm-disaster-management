import json
import os
import piexif
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
import torch

# Initialize Florence-2 with proper configuration
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/florence-2-base",
    trust_remote_code=True,
    revision="refs/pr/6",  # Required for VQA capability
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

processor = AutoProcessor.from_pretrained(
    "microsoft/florence-2-base",
    trust_remote_code=True,
    revision="refs/pr/6"
)

def extract_geotag(image_path):
    """Extract GPS coordinates with error handling"""
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get('exif', b''))
        
        gps = exif_dict.get('GPS', {})
        if not gps:
            return {'latitude': 0.0, 'longitude': 0.0}

        def convert_coord(coord, ref):
            degrees = coord[0][0] / coord[0][1]
            minutes = coord[1][0] / coord[1][1]
            seconds = coord[2][0] / coord[2][1]
            return degrees + (minutes / 60) + (seconds / 3600)

        lat = convert_coord(gps[2], gps[1])
        lat_ref = gps[1].decode('utf-8')
        if lat_ref in ['S', 'W']:
            lat = -lat

        lon = convert_coord(gps[4], gps[3])
        lon_ref = gps[3].decode('utf-8')
        if lon_ref in ['S', 'W']:
            lon = -lon

        return {'latitude': lat, 'longitude': lon}
    except Exception as e:
        print(f"Geotag error in {image_path}: {str(e)}")
        return {'latitude': 0.0, 'longitude': 0.0}

def get_damage_rating(image_path, factors):
    """Get damage rating using Florence-2 with robust parsing"""
    
    image = Image.open(image_path)
    factors_text = "\n".join(f"- {factor}" for factor in factors)
    
    prompt = (
        "<VQA>Question: What's the disaster severity from 1-10 considering:\n"
        f"{factors_text}\n"
        "Consider structural damage, human impact, and environmental effects.\n"
        "Answer with only the number between 1 and 10. Answer:"
    )

    inputs = processor(
        text=prompt,
        images=image,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=10,
        temperature=0.1  # For more deterministic outputs
    )

    answer = processor.decode(outputs[0], skip_special_tokens=True)
    numbers = [int(s) for s in answer.split() if s.isdigit()]
    rating = min(10, max(1, numbers[0])) 
    return rating
        
    

def main():
    # Load assessment factors
    with open('factors.txt') as f:
        factors = [line.strip() for line in f if line.strip()]

    # Process images
    results = []
    for img_name in os.listdir('damaged_images'):
        if img_name.lower().split('.')[-1] not in ['jpg', 'jpeg', 'png']:
            continue
            
        img_path = os.path.join('damaged_images', img_name)
        location = extract_geotag(img_path)
        
        rating = get_damage_rating(img_path, factors)
        
        results.append({
            'image_name': img_name,
            'location': location,
            'rating': rating,
            'factors': factors
        })

    # Save results
    with open('damage_assessments.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Processed {len(results)} images. Results saved.")

if __name__ == "__main__":
    main()
