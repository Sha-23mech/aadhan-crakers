import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")
SRC_PATH = r"C:\Users\shaai\OneDrive\Desktop\fireworks\assets\images\10 CM SPARKLER.png"
OUT_PATH = os.path.join(STATIC_IMG_DIR, "10_cm_sparklers.png")

with Image.open(SRC_PATH) as img:
    img = img.convert('RGBA')
    w, h = img.size
    
    # Create an editing layer to put '10 CM' over the top text area
    draw = ImageDraw.Draw(img)
    
    # Cover the top right '7 CM' pink text box area
    # In 2322x1824 image, top right header text area is around x=1000..1800, y=300..700
    # Let's cover with yellow gradient patch matching background
    yellow_fill = (255, 215, 0, 255)
    pink_fill = (235, 30, 90, 255)
    white_fill = (255, 255, 255, 255)
    dark_fill = (20, 20, 20, 255)

    # Cover '7 CM' region
    draw.rectangle([1150, 280, 1650, 500], fill=(254, 212, 10, 255))
    
    # Try loading bold font
    try:
        font_lg = ImageFont.truetype("arialbd.ttf", 160)
        font_sm = ImageFont.truetype("arialbd.ttf", 80)
    except:
        font_lg = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    # Draw '10 CM' in bold pink text with white border
    text = "10 CM"
    # Shadow/Border
    for dx, dy in [(-4,-4), (4,-4), (-4,4), (4,4), (-6,0), (6,0), (0,-6), (0,6)]:
        draw.text((1180 + dx, 300 + dy), text, font=font_lg, fill=white_fill)
    draw.text((1180, 300), text, font=font_lg, fill=pink_fill)
    
    # Resize to 400x400 for static images
    max_dim = max(w, h)
    bg = Image.new('RGBA', (max_dim, max_dim), (10, 14, 28, 255))
    offset = ((max_dim - w) // 2, (max_dim - h) // 2)
    bg.paste(img, offset, img)
    
    bg_rgb = Image.new('RGB', (max_dim, max_dim), (10, 14, 28))
    bg_rgb.paste(bg, (0, 0), bg)
    img_resized = bg_rgb.resize((400, 400), Image.Resampling.LANCZOS)
    img_resized.save(OUT_PATH, 'PNG')

print("Fixed 10_cm_sparklers.png with clear '10 CM' artwork!")
