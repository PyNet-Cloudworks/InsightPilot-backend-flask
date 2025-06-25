from PIL import Image
import imagehash
import os

HASH_DB = {}  # Temporary store – for real app, store in DB or JSON

def calculate_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.phash(img)
    except Exception as e:
        print(f"❌ Error hashing image: {e}")
        return None

def check_similarity(new_image_path, existing_dir="uploads/images", threshold=5):
    new_hash = calculate_hash(new_image_path)
    if new_hash is None:
        return [], None

    similar_images = []
    for fname in os.listdir(existing_dir):
        fpath = os.path.join(existing_dir, fname)
        if os.path.isfile(fpath):
            existing_hash = calculate_hash(fpath)
            if existing_hash and abs(new_hash - existing_hash) <= threshold:
                similar_images.append(fname)

    return similar_images, new_hash
