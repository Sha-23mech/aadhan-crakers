import os
import shutil
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")

os.makedirs(STATIC_IMG_DIR, exist_ok=True)

# List all screenshot files sorted chronologically
screenshot_files = [f for f in os.listdir(ASSETS_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
screenshot_files.sort(key=lambda f: os.path.getmtime(os.path.join(ASSETS_DIR, f)))

print(f"Found {len(screenshot_files)} user screenshot files in assets/images.")

def process_and_save(src_file, out_name):
    src_path = os.path.join(ASSETS_DIR, src_file)
    out_path = os.path.join(STATIC_IMG_DIR, out_name)
    
    with Image.open(src_path) as img:
        img = img.convert('RGBA')
        w, h = img.size
        max_dim = max(w, h)
        
        # Square canvas on dark background
        bg = Image.new('RGBA', (max_dim, max_dim), (10, 14, 28, 255))
        offset = ((max_dim - w) // 2, (max_dim - h) // 2)
        bg.paste(img, offset, img if img.mode == 'RGBA' else None)
        
        bg_rgb = Image.new('RGB', (max_dim, max_dim), (10, 14, 28))
        bg_rgb.paste(bg, (0, 0), bg)
        img_resized = bg_rgb.resize((400, 400), Image.Resampling.LANCZOS)
        img_resized.save(out_path, 'PNG')

# Map our 23 categories to the chronologically ordered screenshots
OUR_CATEGORIES = [
    ("7 Cm Sparklers", 0),
    ("10 Cm Sparklers", 1),
    ("15 Cm Sparklers", 2),
    ("30 Cm Sparklers", 3),
    ("50 Cm Sparklers", 4),
    ("Single Crackers", 5),
    ("Chakkar", 6),
    ("Flower Pots", 7),
    ("Novelty", 8),
    ("Rockets", 9),
    ("Bombs", 10),
    ("Festival Crackers", 11),
    ("Fancy Chotta", 12),
    ("3 Pcs Mini Something Special", 13),
    ("Magic Fancy Fountain Special", 14),
    ("Color Fountains Tree Mix", 15),
    ("1 1/2\" Pipe", 16),
    ("2\" Pipe", 17),
    ("3\" Pipe", 18),
    ("3 1/2\" Pipe", 19),
    ("4\" Pipe", 20),
    ("Crackling Showers", 21),
    ("Repeating Shots", 22)
]

for cat_name, idx in OUR_CATEGORIES:
    safe_filename = cat_name.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
    if idx < len(screenshot_files):
        src_file = screenshot_files[idx]
        print(f"Mapping '{cat_name}' -> {src_file}")
        process_and_save(src_file, safe_filename)
    else:
        print(f"No asset file for {cat_name}, using default.")

print("All category images updated from user assets!")
