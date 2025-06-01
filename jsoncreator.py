import os
import json
from glob import glob

# 1. Find all image files under 'arts' folder
def find_images(arts_folder):
    exts = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.bmp', '*.gif']
    image_paths = []
    for ext in exts:
        image_paths.extend(glob(os.path.join(arts_folder, '**', ext), recursive=True))
    # Normalize paths to relative to repo root
    image_paths = [os.path.relpath(path) for path in image_paths]
    return sorted(image_paths)

# 2. Split list into batches
def batchify(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i+batch_size]

# 3. Write each batch to a JSON file
def write_batches(image_list, batch_size=20, prefix='batch_'):
    for idx, batch in enumerate(batchify(image_list, batch_size), 1):
        fname = f"{prefix}{idx}.json"
        with open(fname, 'w') as f:
            json.dump(batch, f, indent=2)
        print(f"Created {fname} with {len(batch)} images.")

if __name__ == "__main__":
    ARTS_FOLDER = 'arts'  # Change this if your arts folder is elsewhere
    images = find_images(ARTS_FOLDER)
    if not images:
        print("No images found under 'arts' folder.")
    else:
        write_batches(images, batch_size=20)