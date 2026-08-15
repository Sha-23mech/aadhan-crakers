import os
import math
from PIL import Image, ImageDraw, ImageFont

output_dir = r"c:\Users\shaai\OneDrive\Desktop\fireworks\static\images"
os.makedirs(output_dir, exist_ok=True)

# Category styling configuration
CATEGORY_CONFIGS = {
    "7 Cm Sparklers": {"color1": (255, 60, 0), "color2": (255, 180, 0), "sub": "10 BOX PACK | ELECTRIC SPARKLERS"},
    "10 Cm Sparklers": {"color1": (0, 180, 216), "color2": (114, 9, 183), "sub": "10 BOX PACK | BRIGHT GREEN SPARKLERS"},
    "15 Cm Sparklers": {"color1": (56, 176, 0), "color2": (157, 2, 8), "sub": "10 BOX PACK | PREMIUM RED & GREEN"},
    "30 Cm Sparklers": {"color1": (255, 159, 28), "color2": (231, 29, 54), "sub": "10 BOX PACK | LONG DURATION SPARKLERS"},
    "50 Cm Sparklers": {"color1": (123, 44, 191), "color2": (247, 37, 133), "sub": "10 PIPE PACK | GIANT SPARKLERS"},
    "Single Crackers": {"color1": (208, 0, 0), "color2": (255, 186, 8), "sub": "4 INCH LAKSHMI & KURUVI PACKETS"},
    "Chakkar": {"color1": (247, 127, 0), "color2": (0, 48, 73), "sub": "GROUND CHAKKAR DELUXE & SPECIAL"},
    "Flower Pots": {"color1": (224, 170, 255), "color2": (157, 78, 221), "sub": "FLOWER POTS & COLOR KOTI DELUXE"},
    "Novelty": {"color1": (72, 202, 228), "color2": (3, 4, 94), "sub": "NOVELTY T-STAR FIREWORKS PACK"},
    "Rockets": {"color1": (255, 77, 109), "color2": (89, 13, 34), "sub": "COLOR & TWO SOUND HIGH FLYING ROCKETS"},
    "Bombs": {"color1": (56, 102, 65), "color2": (188, 71, 73), "sub": "HYDROGEN & CLASSIC SOUND BOMBS"},
    "Festival Crackers": {"color1": (217, 4, 41), "color2": (141, 153, 174), "sub": "RED BIJILI & CHORSA GARLAND CRACKERS"},
    "Fancy Chotta": {"color1": (255, 183, 3), "color2": (33, 158, 188), "sub": "7 SHOT & PENTA SKY FANCY BOX"},
    "3 Pcs Mini Something Special": {"color1": (181, 23, 158), "color2": (72, 12, 168), "sub": "MINI SPECIAL COMBO PACK"},
    "Magic Fancy Fountain Special": {"color1": (67, 97, 238), "color2": (76, 201, 240), "sub": "ASHRAFI KOTI & SIREN WHISTLING"},
    "Color Fountains Tree Mix": {"color1": (43, 147, 72), "color2": (247, 127, 0), "sub": "CHERRY & KOKO TREE COLOR FOUNTAINS"},
    "1 1/2\" Pipe": {"color1": (208, 0, 0), "color2": (255, 186, 8), "sub": "1.5 INCH SINGLE PIPE AERIAL SHOT"},
    "2\" Pipe": {"color1": (114, 9, 183), "color2": (247, 37, 133), "sub": "2 INCH SKY SURF & RANGOLI PIPE"},
    "3\" Pipe": {"color1": (0, 119, 182), "color2": (144, 224, 239), "sub": "3 INCH AMERICAN STYLE & FANCY TOUCH"},
    "3 1/2\" Pipe": {"color1": (247, 127, 0), "color2": (214, 40, 40), "sub": "3.5 INCH DIGITAL MIXER & ROYAL PALM"},
    "4\" Pipe": {"color1": (157, 2, 8), "color2": (3, 7, 30), "sub": "4 INCH REAL STEEL & SKY FORCE PIPE"},
    "Crackling Showers": {"color1": (255, 159, 28), "color2": (157, 2, 8), "sub": "DUCATI & FAZER CRACKLING SHOWERS"},
    "Repeating Shots": {"color1": (114, 9, 183), "color2": (72, 149, 239), "sub": "12 SHOT TO 240 MULTI SHOT CAKE BOX"}
}

def create_carton_box_image(cat_name, filename):
    cfg = CATEGORY_CONFIGS.get(cat_name, {
        "color1": (255, 183, 3),
        "color2": (255, 46, 99),
        "sub": "PREMIUM FIREWORKS PACKAGING"
    })
    
    W, H = 400, 400
    img = Image.new("RGBA", (W, H), (10, 14, 28, 255))
    draw = ImageDraw.Draw(img)

    # 3D Carton Box coordinates
    front_pts = [(70, 130), (270, 130), (270, 330), (70, 330)]
    top_pts = [(70, 130), (140, 70), (340, 70), (270, 130)]
    right_pts = [(270, 130), (340, 70), (340, 270), (270, 330)]

    c1 = cfg["color1"]
    c2 = cfg["color2"]

    top_color = (min(255, c1[0]+40), min(255, c1[1]+40), min(255, c1[2]+40))
    draw.polygon(top_pts, fill=top_color, outline=(255, 255, 255, 180))

    right_color = (max(0, c2[0]-40), max(0, c2[1]-40), max(0, c2[2]-40))
    draw.polygon(right_pts, fill=right_color, outline=(255, 255, 255, 180))

    draw.polygon(front_pts, fill=c1, outline=(255, 255, 255, 220))

    draw.rectangle([76, 136, 264, 324], outline=(255, 215, 0), width=3)
    draw.rectangle([80, 140, 260, 320], fill=(15, 20, 35))

    draw.rectangle([80, 140, 260, 180], fill=c2)

    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 13)
        font_title = ImageFont.truetype("arialbd.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 10)
    except:
        font_brand = font_title = font_sub = ImageFont.load_default()

    draw.text((170, 150), "AADHAN FIRE WORKS", fill=(255, 255, 255), font=font_brand, anchor="mm")
    draw.text((170, 166), "PREMIUM QUALITY CRACKERS", fill=(255, 215, 0), font=font_sub, anchor="mm")

    title_text = cat_name.upper()
    if len(title_text) > 18:
        parts = title_text.split(" ", 1)
        draw.text((170, 210), parts[0], fill=(255, 255, 255), font=font_title, anchor="mm")
        if len(parts) > 1:
            draw.text((170, 235), parts[1], fill=(255, 183, 3), font=font_title, anchor="mm")
    else:
        draw.text((170, 220), title_text, fill=(255, 255, 255), font=font_title, anchor="mm")

    draw.text((170, 270), cfg["sub"], fill=(200, 210, 230), font=font_sub, anchor="mm")

    draw.rectangle([88, 290, 252, 310], fill=(0, 180, 216))
    draw.text((170, 300), "ENGLISH PACKAGING ONLY", fill=(10, 14, 28), font=font_sub, anchor="mm")

    draw.text((205, 100), "PREMIUM RETAIL CARTON", fill=(255, 255, 255), font=font_sub, anchor="mm")

    img.save(os.path.join(output_dir, filename), "PNG")

def generate_all():
    for cat in CATEGORY_CONFIGS:
        safe_name = cat.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
        create_carton_box_image(cat, safe_name)
    print("All AADHAN FIRE WORKS 3D Carton Box images generated successfully!")

if __name__ == "__main__":
    generate_all()
