import os
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import generate_excel

app = FastAPI(title="AADHAN FIRE WORKS - Order Management & Product Catalog")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRIMARY_EXCEL_PATH = os.path.join(BASE_DIR, "Firecrackers_Catalog_and_Orders.xlsx")
UPDATED_EXCEL_PATH = os.path.join(BASE_DIR, "Firecrackers_Catalog_and_Orders_Updated.xlsx")
STATIC_IMG_DIR = os.path.join(BASE_DIR, "static", "images")

def get_active_excel_path():
    if os.path.exists(UPDATED_EXCEL_PATH):
        return UPDATED_EXCEL_PATH
    return PRIMARY_EXCEL_PATH

# Ensure Excel file exists on startup
if not os.path.exists(PRIMARY_EXCEL_PATH) and not os.path.exists(UPDATED_EXCEL_PATH):
    generate_excel.extract_and_generate()

class OrderItem(BaseModel):
    category: str
    cracker_name: str
    unit_price: float
    quantity: int

class OrderCreateRequest(BaseModel):
    buyer_name: str
    contact_number: str
    category: Optional[str] = None
    cracker_name: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    items: Optional[List[OrderItem]] = None

def get_image_url(category_name):
    safe_name = category_name.lower().replace(' ', '_').replace('"', '').replace('/', '_') + ".png"
    img_path = os.path.join(STATIC_IMG_DIR, safe_name)
    if os.path.exists(img_path):
        return f"/static/images/{safe_name}"
    return "/static/images/7_cm_sparklers.png"

@app.get("/api/catalog")
def get_catalog():
    excel_path = get_active_excel_path()
    if not os.path.exists(excel_path):
        generate_excel.extract_and_generate()
        excel_path = get_active_excel_path()
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    if "Product Catalog" not in wb.sheetnames:
        wb.close()
        raise HTTPException(status_code=500, detail="Product Catalog sheet missing")
    
    ws = wb["Product Catalog"]
    products = []
    categories_set = set()
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[1]:
            continue
        box_photo, item_id, factory, category, name, rate, per, case_content = row[:8]
        cat_clean = str(category).strip()
        categories_set.add(cat_clean)
        products.append({
            "item_id": item_id,
            "factory": factory,
            "category": cat_clean,
            "name": str(name).strip(),
            "price": float(rate or 0.0),
            "per": str(per or "").strip(),
            "case_content": str(case_content or "").strip(),
            "image_url": get_image_url(cat_clean)
        })
    wb.close()
        
    return {
        "categories": sorted(list(categories_set)),
        "products": products
    }

@app.get("/api/orders")
def get_orders():
    excel_path = get_active_excel_path()
    if not os.path.exists(excel_path):
        return {"orders": [], "total_revenue": 0.0, "total_orders": 0}
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    if "Order Details" not in wb.sheetnames:
        wb.close()
        return {"orders": [], "total_revenue": 0.0, "total_orders": 0}
    
    ws = wb["Order Details"]
    orders = []
    total_rev = 0.0
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0]:
            continue
        order_id, date_time, buyer, contact, cat, cracker, u_price, qty, total = row[:9]
        tot_val = float(total or 0.0)
        total_rev += tot_val
        orders.append({
            "order_id": str(order_id),
            "date_time": str(date_time),
            "buyer_name": str(buyer),
            "contact_number": str(contact),
            "category": str(cat),
            "cracker_name": str(cracker),
            "unit_price": float(u_price or 0.0),
            "quantity": int(qty or 1),
            "total_amount": tot_val,
            "image_url": get_image_url(str(cat))
        })
    wb.close()
        
    return {
        "orders": orders[::-1],
        "total_revenue": total_rev,
        "total_orders": len(orders)
    }

@app.post("/api/orders")
def place_order(req: OrderCreateRequest):
    if not req.buyer_name or not req.contact_number:
        raise HTTPException(status_code=400, detail="Buyer Name and Contact Number are required.")
    
    order_items = []
    if req.items and len(req.items) > 0:
        order_items = req.items
    elif req.category and req.cracker_name and req.unit_price is not None and req.quantity is not None:
        order_items.append(OrderItem(
            category=req.category,
            cracker_name=req.cracker_name,
            unit_price=req.unit_price,
            quantity=req.quantity
        ))
    else:
        raise HTTPException(status_code=400, detail="Please select a cracker and enter quantity.")

    excel_path = get_active_excel_path()
    try:
        wb = openpyxl.load_workbook(excel_path)
    except Exception:
        excel_path = PRIMARY_EXCEL_PATH
        wb = openpyxl.load_workbook(excel_path)

    if "Order Details" not in wb.sheetnames:
        ws_orders = wb.create_sheet(title="Order Details")
        order_headers = ["Order ID", "Order Date & Time", "Buyer Name", "Contact Number", "Category", "Cracker Name", "Unit Price (₹)", "Quantity", "Total Amount (₹)"]
        ws_orders.append(order_headers)
    else:
        ws_orders = wb["Order Details"]

    existing_rows = max(0, ws_orders.max_row - 1)
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_orders = []
    grand_total = 0.0
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    for i, item in enumerate(order_items):
        existing_rows += 1
        order_id = f"ORD-{existing_rows:04d}"
        item_total = round(item.unit_price * item.quantity, 2)
        grand_total += item_total
        
        row_data = [
            order_id,
            timestamp_str,
            req.buyer_name.strip(),
            req.contact_number.strip(),
            item.category.strip(),
            item.cracker_name.strip(),
            item.unit_price,
            item.quantity,
            item_total
        ]
        
        ws_orders.append(row_data)
        r_idx = ws_orders.max_row
        
        ws_orders.cell(row=r_idx, column=7).number_format = '₹#,##0.00'
        ws_orders.cell(row=r_idx, column=9).number_format = '₹#,##0.00'
        for c in range(1, 10):
            ws_orders.cell(row=r_idx, column=c).border = thin_border
            
        created_orders.append({
            "order_id": order_id,
            "date_time": timestamp_str,
            "buyer_name": req.buyer_name,
            "contact_number": req.contact_number,
            "category": item.category,
            "cracker_name": item.cracker_name,
            "unit_price": item.unit_price,
            "quantity": item.quantity,
            "total_amount": item_total,
            "image_url": get_image_url(item.category)
        })

    try:
        wb.save(excel_path)
    except PermissionError:
        excel_path = UPDATED_EXCEL_PATH
        wb.save(excel_path)
    wb.close()

    return {
        "success": True,
        "message": f"Successfully placed {len(created_orders)} item order(s)!",
        "orders": created_orders,
        "grand_total": grand_total
    }

@app.get("/api/download-excel")
def download_excel():
    excel_path = get_active_excel_path()
    if not os.path.exists(excel_path):
        generate_excel.extract_and_generate()
        excel_path = get_active_excel_path()
    return FileResponse(
        path=excel_path,
        filename="Firecrackers_Catalog_and_Orders.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static_root")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
