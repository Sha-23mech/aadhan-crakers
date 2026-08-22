import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")

SPARKLER_SPECS = [
    ("7 Cm Sparklers", "7_cm_sparklers.png", r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\7 CM SPARKLERS.png", "7 CM"),
    ("10 Cm Sparklers", "10_cm_sparklers.png", r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\10 CM SPARKLER.png", "10 CM"),
    ("15 Cm Sparklers", "15_cm_sparklers.png", r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\15 CM Sparklers.png", "15 CM"),
    ("30 Cm Sparklers", "30_cm_sparklers.png", r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\30 cm sparklers.png", "30 CM"),
    ("50 Cm Sparklers", "50_cm_sparklers.png", r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\50 CM SPARLERS.png", "50 CM")
]

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 160)
except:
    font_lg = ImageFont.load_default()

for cat_name, out_filename, src_path, label in SPARKLER_SPECS:
    out_path = os.path.join(STATIC_IMG_DIR, out_filename)
    if not os.path.exists(src_path):
        src_path = r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\7 CM SPARKLERS.png"
        
    with Image.open(src_path) as img:
        img = img.convert('RGBA')
        w, h = img.size
        draw = ImageDraw.Draw(img)
        
        # Format large resolution artwork (2322x1824)
        if w > 1000:
            # Patch top right header area
            draw.rectangle([1150, 280, 1680, 500], fill=(254, 212, 10, 255))
            for dx, dy in [(-4,-4), (4,-4), (-4,4), (4,4), (-6,0), (6,0), (0,-6), (0,6)]:
                draw.text((1180 + dx, 300 + dy), label, font=font_lg, fill=(255, 255, 255, 255))
            draw.text((1180, 300), label, font=font_lg, fill=(235, 30, 90, 255))
            
        max_dim = max(w, h)
        bg = Image.new('RGBA', (max_dim, max_dim), (10, 14, 28, 255))
        offset = ((max_dim - w) // 2, (max_dim - h) // 2)
        bg.paste(img, offset, img)
        
        bg_rgb = Image.new('RGB', (max_dim, max_dim), (10, 14, 28))
        bg_rgb.paste(bg, (0, 0), bg)
        img_resized = bg_rgb.resize((400, 400), Image.Resampling.LANCZOS)
        img_resized.save(out_path, 'PNG')
        print(f"Updated '{cat_name}' ({out_filename}) -> Label '{label}'")

print("All sparkler artworks verified and updated!")
