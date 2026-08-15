import os
import urllib.request
import urllib.parse
import re
import ssl
from PIL import Image

output_dir = r"c:\Users\shaai\OneDrive\Desktop\fireworks\static\images"
os.makedirs(output_dir, exist_ok=True)

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://stdfireworks.in/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

def fetch_page(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}", flush=True)
        return ""

print("Fetching stdfireworks.in main index page...", flush=True)
index_html = fetch_page("https://stdfireworks.in/index.php")
gallery_images = re.findall(r'gallery/[a-zA-Z0-9_\-\.\s%]+\.(?:png|jpg|jpeg|PNG|JPG|JPEG)', index_html)

gallery_list = []
for g in gallery_images:
    full_u = urllib.parse.urljoin(BASE_URL, g)
    if full_u not in gallery_list:
        gallery_list.append(full_u)

# Fetch product pages
cids = [3, 6, 12, 13, 14, 15, 18, 20, 21, 22, 23, 24, 30, 31, 32, 36, 41, 42, 43, 44]
for cid in cids:
    p_url = f"https://stdfireworks.in/productn.php?id={cid}"
    html = fetch_page(p_url)
    imgs = re.findall(r'gallery/[a-zA-Z0-9_\-\.\s%]+\.(?:png|jpg|jpeg|PNG|JPG|JPEG)', html)
    if imgs:
        for img in imgs:
            full_u = urllib.parse.urljoin(BASE_URL, img)
            if full_u not in gallery_list:
                gallery_list.append(full_u)

print(f"Total unique product photos extracted from stdfireworks.in: {len(gallery_list)}", flush=True)

OUR_CATEGORIES = [
    "7 Cm Sparklers",
    "10 Cm Sparklers",
    "15 Cm Sparklers",
    "30 Cm Sparklers",
    "50 Cm Sparklers",
    "Single Crackers",
    "Chakkar",
    "Flower Pots",
    "Novelty",
    "Rockets",
    "Bombs",
    "Festival Crackers",
    "Fancy Chotta",
    "3 Pcs Mini Something Special",
    "Magic Fancy Fountain Special",
    "Color Fountains Tree Mix",
    "1 1/2\" Pipe",
    "2\" Pipe",
    "3\" Pipe",
    "3 1/2\" Pipe",
    "4\" Pipe",
    "Crackling Showers",
    "Repeating Shots"
]

def download_and_process(img_url, output_file):
    clean_url = urllib.parse.quote(img_url, safe=':/')
    req = urllib.request.Request(clean_url, headers=headers)
    with urllib.request.urlopen(req, context=ssl_ctx, timeout=12) as response:
        with open(output_file, 'wb') as f:
            f.write(response.read())
    
    with Image.open(output_file) as img:
        img = img.convert('RGBA')
        w, h = img.size
        max_dim = max(w, h)
        bg = Image.new('RGBA', (max_dim, max_dim), (10, 14, 28, 255))
        offset = ((max_dim - w) // 2, (max_dim - h) // 2)
        bg.paste(img, offset, img if img.mode == 'RGBA' else None)
        
        bg_rgb = Image.new('RGB', (max_dim, max_dim), (10, 14, 28))
        bg_rgb.paste(bg, (0, 0), bg)
        img_resized = bg_rgb.resize((400, 400), Image.Resampling.LANCZOS)
        img_resized.save(output_file, 'PNG')

if gallery_list:
    for idx, my_cat in enumerate(OUR_CATEGORIES):
        safe_filename = my_cat.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
        out_path = os.path.join(output_dir, safe_filename)
        img_url = gallery_list[idx % len(gallery_list)]
        print(f"Downloading stdfireworks.in photo for '{my_cat}' ({img_url})...", flush=True)
        try:
            download_and_process(img_url, out_path)
            print(f"Successfully updated {safe_filename} from stdfireworks.in!", flush=True)
        except Exception as e:
            print(f"Failed {my_cat}: {e}", flush=True)
else:
    print("No images extracted directly.", flush=True)

print("\nAll 23 category product images updated directly from stdfireworks.in!", flush=True)
