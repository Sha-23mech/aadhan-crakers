import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

DIRECT_ASSET_MAPPING = {
    "7 Cm Sparklers": "7 CM SPARKLERS.png",
    "10 Cm Sparklers": "10 CM SPARKLER.png",
    "15 Cm Sparklers": "15 CM Sparklers.png",
    "30 Cm Sparklers": "30 cm sparklers.png",
    "50 Cm Sparklers": "50 CM SPARLERS.png",
    "Single Crackers": "SINGLE CRACKERS.png",
    "Chakkar": "CHAKKARA.png",
    "Flower Pots": "FLOWER POTS.png",
    "Novelty": "T-STAR.png",
    "Rockets": "rockets.jpg",
    "Bombs": "BOMBS.png",
    "Festival Crackers": "FESTIVAL CRACKERS.png",
    "Fancy Chotta": "FANCY CHOTTA.png",
    "3 Pcs Mini Something Special": "SOMETHING SPECIAL.png",
    "Magic Fancy Fountain Special": "MAGIC FOUNTAN  SPECIAL.png",
    "Color Fountains Tree Mix": "COLOR FOUNDATION.png",
    "1 1/2\" Pipe": "1 12 PIPE.png",
    "2\" Pipe": "2 PIPE.png",
    "3\" Pipe": "3 PIPE.png",
    "3 1/2\" Pipe": "3 12 PIPE.png",
    "4\" Pipe": "4 pipe.png",
    "Crackling Showers": "crackling showers.png",
    "Repeating Shots": "REPEATING SHOTS.png"
}

def process_direct_asset(src_filename, out_filename):
    src_path = os.path.join(ASSETS_DIR, src_filename)
    out_path = os.path.join(STATIC_IMG_DIR, out_filename)
    
    if not os.path.exists(src_path):
        print(f"Warning: asset file missing: {src_path}")
        return
        
    with Image.open(src_path) as img:
        img = img.convert('RGBA')
        w, h = img.size
        max_dim = max(w, h)
        
        bg = Image.new('RGBA', (max_dim, max_dim), (10, 14, 28, 255))
        offset = ((max_dim - w) // 2, (max_dim - h) // 2)
        bg.paste(img, offset, img)
        
        bg_rgb = Image.new('RGB', (max_dim, max_dim), (10, 14, 28))
        bg_rgb.paste(bg, (0, 0), bg)
        img_resized = bg_rgb.resize((400, 400), Image.Resampling.LANCZOS)
        img_resized.save(out_path, 'PNG')
        print(f"Processed direct asset '{src_filename}' -> static/images/{out_filename}")

for cat_name, asset_filename in DIRECT_ASSET_MAPPING.items():
    safe_filename = cat_name.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
    process_direct_asset(asset_filename, safe_filename)

print("All 23 category images converted directly from assets/images!")
