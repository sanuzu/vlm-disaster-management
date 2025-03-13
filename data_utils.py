from datasets import load_dataset
import os
from datasets import load_dataset
from PIL import Image
import os
def download_images():


    # Configure streaming
    dataset = load_dataset(
        "MITLL/LADI-v2-dataset",
        streaming=True,
        trust_remote_code=True
    )

    # Damage labels to check (v2a configuration)
    DAMAGE_LABELS = {
        'buildings_affected_or_greater',
        'buildings_minor_or_greater',
        'debris_any',
        'flooding_structures',
        'roads_damage',
        'trees_damage'
    }

    # Output setup
    os.makedirs("damaged_images", exist_ok=True)
    target_count = 400
    downloaded = 0

    # Stream through dataset efficiently
    for split in ['train', 'validation', 'test']:
        for example in iter(dataset[split]):
            if any(example.get(label, False) for label in DAMAGE_LABELS):
                img = example['image'].convert('RGB')
                img.save(f"damaged_images/{downloaded}.jpg")
                downloaded += 1
                
                if downloaded >= target_count:
                    break
        if downloaded >= target_count:
            break

    print(f"Successfully saved {downloaded} damaged images")

