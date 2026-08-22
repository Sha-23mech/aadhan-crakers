import os
import openpyxl
from app import get_image_url, STATIC_IMG_DIR

wb = openpyxl.load_workbook("Firecrackers_Catalog_and_Orders.xlsx", read_only=True)
ws = wb["Product Catalog"]
cats = set()
for row in ws.iter_rows(min_row=2, values_only=True):
    if row and row[3]:
        cats.add(str(row[3]).strip())
wb.close()

print("Checking category image mappings:")
for c in sorted(cats):
    img_url = get_image_url(c)
    filename = os.path.basename(img_url)
    img_path = os.path.join(STATIC_IMG_DIR, filename)
    exists = os.path.exists(img_path)
    print(f"Category: '{c}' -> Image URL: '{img_url}' | Exists: {exists}")

