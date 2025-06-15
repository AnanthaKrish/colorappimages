import os
import json
import base64
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

# 4. Convert images to base64 and store in JSON array
def convert_to_base64_json(image_list, output_file='images_base64.json'):
    base64_images = []
    
    for img_path in image_list:
        try:
            with open(img_path, 'rb') as img_file:
                # Read the binary data
                img_data = img_file.read()
                # Convert to base64
                base64_data = base64.b64encode(img_data).decode('utf-8')
                
                # Get file extension
                _, ext = os.path.splitext(img_path)
                mime_type = {
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.png': 'image/png',
                    '.webp': 'image/webp',
                    '.bmp': 'image/bmp',
                    '.gif': 'image/gif'
                }.get(ext.lower(), 'application/octet-stream')
                
                # Create data URI
                data_uri = f"{base64_data}"
                
                # Add to array with metadata
                base64_images.append({
                    'filename': os.path.basename(img_path),
                    'path': img_path,
                    'data_uri': data_uri
                })
                
            print(f"Converted {img_path} to base64")
        except Exception as e:
            print(f"Error converting {img_path}: {e}")
    
    # Write to JSON file
    with open(output_file, 'w') as f:
        json.dump(base64_images, f, indent=2)
    
    print(f"Created {output_file} with {len(base64_images)} base64 encoded images.")
    return base64_images

if __name__ == "__main__":
    ARTS_FOLDER = 'arts'  # Change this if your arts folder is elsewhere
    images = find_images(ARTS_FOLDER)
    if not images:
        print("No images found under 'arts' folder.")
    else:
        # write_batches(images, batch_size=200, prefix='art_links')
        # Uncomment the line below to convert images to base64
        convert_to_base64_json(images, 'images_base64.json')