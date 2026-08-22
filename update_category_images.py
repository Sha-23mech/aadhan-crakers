import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

CATEGORY_IMAGE_MAPPING = {
    "7 Cm Sparklers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\7 CM SPARKLERS.png",
    "10 Cm Sparklers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\10 CM SPARKLER.png",
    "15 Cm Sparklers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\15 CM Sparklers.png",
    "30 Cm Sparklers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\30 cm sparklers.png",
    "50 Cm Sparklers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\50 CM SPARLERS.png",
    "Single Crackers": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\SINGLE CRACKERS.png",
    "Chakkar": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\CHAKKARA.png",
    "Flower Pots": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\FLOWER POTS.png",
    "Novelty": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\T-STAR.png",
    "Rockets": r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\rockets.jpg"
}

def process_and_save(src_path, out_name):
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

for cat_name, src_path in CATEGORY_IMAGE_MAPPING.items():
    safe_filename = cat_name.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
    if os.path.exists(src_path):
        print(f"Updating '{cat_name}' image from {src_path}...")
        process_and_save(src_path, safe_filename)
        print(f"Saved -> static/images/{safe_filename}")
    else:
        print(f"Warning: File missing for {cat_name}: {src_path}")

print("Category image processing complete!")
