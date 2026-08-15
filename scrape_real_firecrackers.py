import os
import urllib.request
import urllib.parse
import json
import re
from PIL import Image

output_dir = r"c:\Users\shaai\OneDrive\Desktop\fireworks\static\images"
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

CURATED_REAL_IMAGES = {
    "7 Cm Sparklers": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "10 Cm Sparklers": "https://images.pexels.com/photos/2599244/pexels-photo-2599244.jpeg?auto=compress&cs=tinysrgb&w=600",
    "15 Cm Sparklers": "https://images.pexels.com/photos/1105666/pexels-photo-1105666.jpeg?auto=compress&cs=tinysrgb&w=600",
    "30 Cm Sparklers": "https://images.pexels.com/photos/949587/pexels-photo-949587.jpeg?auto=compress&cs=tinysrgb&w=600",
    "50 Cm Sparklers": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Single Crackers": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Chakkar": "https://images.pexels.com/photos/2599244/pexels-photo-2599244.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Flower Pots": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Novelty": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Rockets": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Bombs": "https://images.pexels.com/photos/1105666/pexels-photo-1105666.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Festival Crackers": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Fancy Chotta": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "3 Pcs Mini Something Special": "https://images.pexels.com/photos/2599244/pexels-photo-2599244.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Magic Fancy Fountain Special": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Color Fountains Tree Mix": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "1 1/2\" Pipe": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "2\" Pipe": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "3\" Pipe": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "3 1/2\" Pipe": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "4\" Pipe": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Crackling Showers": "https://images.pexels.com/photos/1387174/pexels-photo-1387174.jpeg?auto=compress&cs=tinysrgb&w=600",
    "Repeating Shots": "https://images.pexels.com/photos/1190298/pexels-photo-1190298.jpeg?auto=compress&cs=tinysrgb&w=600"
}

def download_and_crop(img_url, output_file):
    req = urllib.request.Request(img_url, headers=headers)
    with urllib.request.urlopen(req, timeout=12) as response:
        with open(output_file, 'wb') as f:
            f.write(response.read())
    
    with Image.open(output_file) as img:
        img = img.convert('RGB')
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        right = (w + min_dim) / 2
        bottom = (h + min_dim) / 2
        img_cropped = img.crop((left, top, right, bottom))
        img_resized = img_cropped.resize((400, 400), Image.Resampling.LANCZOS)
        img_resized.save(output_file, 'PNG')

def main():
    for cat, url in CURATED_REAL_IMAGES.items():
        safe_filename = cat.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
        out_path = os.path.join(output_dir, safe_filename)
        print(f"Downloading real firecracker photo for {cat}...", flush=True)
        try:
            download_and_crop(url, out_path)
            print(f"Saved: {safe_filename}", flush=True)
        except Exception as e:
            print(f"Error downloading for {cat}: {e}", flush=True)

    print("All 23 real firecracker web photos downloaded & updated successfully!", flush=True)

if __name__ == "__main__":
    main()
