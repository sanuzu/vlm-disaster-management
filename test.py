import json
import random

# Load and modify data
with open('damage_assessments.json', 'r+') as f:
    data = json.load(f)
    for entry in data:
        entry['rating'] = random.randint(1, 10)
    f.seek(0)  # Reset file position
    json.dump(data, f, indent=2)
    f.truncate()  # Remove remaining content if new data is shorter
