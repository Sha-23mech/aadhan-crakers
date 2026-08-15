# 🚀 Deployment Guide - AADHAN FIRE WORKS

This project is fully prepared for 1-click cloud deployment on platforms like **Render.com**, **Railway**, **PythonAnywhere**, or any Linux VPS server.

---

## 🌟 Deploying on Render.com (100% Free)

1. **Upload your project to GitHub**:
   - Create a repository named `aadhan-fireworks` on GitHub.
   - Push all files from `c:\Users\shaai\OneDrive\Desktop\fireworks` to your repository:
     ```bash
     git init
     git add .
     git commit -m "Initial commit for AADHAN FIRE WORKS"
     git remote add origin https://github.com/YOUR_USERNAME/aadhan-fireworks.git
     git push -u origin main
     ```

2. **Deploy on Render**:
   - Go to [https://dashboard.render.com](https://dashboard.render.com).
   - Click **New +** -> **Web Service**.
   - Connect your `aadhan-fireworks` GitHub repository.
   - Fill in the details:
     - **Name**: `aadhan-fireworks`
     - **Runtime**: `Python`
     - **Build Command**: `pip install -r requirements.txt && python generate_excel.py`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Click **Create Web Service**.

3. **Your Website is Live!**:
   - Render will build your site and give you a free live URL: `https://aadhan-fireworks.onrender.com`.
   - Your client can access this link from any mobile phone or computer!

---

## 📊 How your client gets the Excel Sheet

- At the top right of the live website, there is a **"Download Excel Workbook"** button.
- Whenever your client clicks this button, it downloads the latest `Firecrackers_Catalog_and_Orders.xlsx` file with all current product catalog details and all recorded orders directly to their computer!
