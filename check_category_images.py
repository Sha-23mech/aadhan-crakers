import os
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")

def get_image_url(category_name):
    safe_name = category_name.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
    img_path = os.path.join(STATIC_IMG_DIR, safe_name)
    exists = os.path.exists(img_path)
    return safe_name, exists, img_path

wb = openpyxl.load_workbook("Firecrackers_Catalog_and_Orders.xlsx", read_only=True)
ws = wb["Product Catalog"]
cats = set()
for row in ws.iter_rows(min_row=2, values_only=True):
    if row and row[3]:
        cats.add(str(row[3]).strip())
wb.close()

print("Checking category image mappings:")
for c in sorted(cats):
    s_name, exists, path = get_image_url(c)
    print(f"Category: '{c}' -> filename: '{s_name}' | Exists: {exists}")
