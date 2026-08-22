import app

catalog = app.get_catalog()
print(f"Total categories returned by API: {len(catalog['categories'])}")
print(f"Total products returned by API: {len(catalog['products'])}")

print("\nCategory Image Mappings:")
for cat in sorted(catalog['categories']):
    img = app.get_image_url(cat)
    print(f" - '{cat}' -> {img}")
