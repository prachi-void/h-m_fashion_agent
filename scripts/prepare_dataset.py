import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

# Set up paths
BASE_DIR = r"C:\Users\admin\.gemini\antigravity-ide\scratch\hm_fashion_agent"
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Initializing dataset in {BASE_DIR}...")

# 1. Define sample articles dataset matching H&M exact schema
articles_data = [
    # Style 1: Tailored Oversized Blazer (Tailored Minimalist)
    {
        "article_id": "0108775015", "product_code": "0108775", "prod_name": "Strap Tailored Blazer",
        "product_type_no": 264, "product_type_name": "Blazer", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 9, "colour_group_name": "Black",
        "perceived_colour_value_name": "Dark", "perceived_colour_master_name": "Black",
        "department_no": 1610, "department_name": "Blazers & Jackets",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1003, "garment_group_name": "Dresses Outerwear",
        "detail_desc": "Oversized single-breasted blazer with structured shoulders, peak lapels, and double welt pockets."
    },
    {
        "article_id": "0108775044", "product_code": "0108775", "prod_name": "Strap Tailored Blazer Beige",
        "product_type_no": 264, "product_type_name": "Blazer", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 12, "colour_group_name": "Beige",
        "perceived_colour_value_name": "Light", "perceived_colour_master_name": "Beige",
        "department_no": 1610, "department_name": "Blazers & Jackets",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1003, "garment_group_name": "Dresses Outerwear",
        "detail_desc": "Relaxed beige wool-blend blazer with clean minimalist lines and horn buttons."
    },
    # Style 2: Chunky Ribbed Knit Crew (Cozy Streetwear Knit)
    {
        "article_id": "0215882001", "product_code": "0215882", "prod_name": "Chunky Rib Sweater",
        "product_type_no": 252, "product_type_name": "Sweater", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010010, "graphical_appearance_name": "Melange",
        "colour_group_code": 7, "colour_group_name": "Grey",
        "perceived_colour_value_name": "Medium", "perceived_colour_master_name": "Grey",
        "department_no": 1642, "department_name": "Knitwear",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1005, "garment_group_name": "Knitwear",
        "detail_desc": "Heavyweight chunky rib sweater in soft wool blend with dropped shoulders and boxy silhouette."
    },
    {
        "article_id": "0215882008", "product_code": "0215882", "prod_name": "Chunky Rib Sweater Ecru",
        "product_type_no": 252, "product_type_name": "Sweater", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 11, "colour_group_name": "Off White",
        "perceived_colour_value_name": "Dusty Light", "perceived_colour_master_name": "White",
        "department_no": 1642, "department_name": "Knitwear",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1005, "garment_group_name": "Knitwear",
        "detail_desc": "Ecru ribbed crewneck jumper featuring oversized sleeves and high tactile finish."
    },
    # Style 3: Wide Pleated Pleat Trouser (Relaxed Tailored Bottoms)
    {
        "article_id": "0349910002", "product_code": "0349910", "prod_name": "High Waist Tailored Trouser",
        "product_type_no": 272, "product_type_name": "Trousers", "product_group_name": "Garment Lower body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 9, "colour_group_name": "Black",
        "perceived_colour_value_name": "Dark", "perceived_colour_master_name": "Black",
        "department_no": 1618, "department_name": "Trousers",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1009, "garment_group_name": "Trousers",
        "detail_desc": "High-waisted wide leg pants with front pleats, slant side pockets, and relaxed fluid drape."
    },
    {
        "article_id": "0349910005", "product_code": "0349910", "prod_name": "High Waist Tailored Trouser Olive",
        "product_type_no": 272, "product_type_name": "Trousers", "product_group_name": "Garment Lower body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 19, "colour_group_name": "Green",
        "perceived_colour_value_name": "Medium Dark", "perceived_colour_master_name": "Green",
        "department_no": 1618, "department_name": "Trousers",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1009, "garment_group_name": "Trousers",
        "detail_desc": "Olive wide-leg trousers with front pressed creases and concealed hook zipper closure."
    },
    # Style 4: Floral Satin Midi Slip Dress (Boho Romance)
    {
        "article_id": "0458120003", "product_code": "0458120", "prod_name": "Floral Satin Midi Dress",
        "product_type_no": 265, "product_type_name": "Dress", "product_group_name": "Garment Full body",
        "graphical_appearance_no": 1010001, "graphical_appearance_name": "Floral",
        "colour_group_code": 42, "colour_group_name": "Red",
        "perceived_colour_value_name": "Bright", "perceived_colour_master_name": "Red",
        "department_no": 1640, "department_name": "Dresses",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1010, "garment_group_name": "Dresses",
        "detail_desc": "Flowing satin midi dress with delicate botanical floral print, cowl neck, and adjustable spaghetti straps."
    },
    # Style 5: Cropped Utility Puffer Jacket (Technical Outerwear)
    {
        "article_id": "0512490001", "product_code": "0512490", "prod_name": "Cropped Puffer Jacket",
        "product_type_no": 262, "product_type_name": "Jacket", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 9, "colour_group_name": "Black",
        "perceived_colour_value_name": "Dark", "perceived_colour_master_name": "Black",
        "department_no": 1610, "department_name": "Blazers & Jackets",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1003, "garment_group_name": "Dresses Outerwear",
        "detail_desc": "Water-repellent cropped puffer jacket with high funnel collar and adjustable toggle hem."
    },
    # Style 6: Seamless Ribbed Crop Top (Athleisure Basics)
    {
        "article_id": "0601990004", "product_code": "0601990", "prod_name": "Seamless Crop Top",
        "product_type_no": 253, "product_type_name": "Top", "product_group_name": "Garment Upper body",
        "graphical_appearance_no": 1010016, "graphical_appearance_name": "Solid",
        "colour_group_code": 10, "colour_group_name": "White",
        "perceived_colour_value_name": "Light", "perceived_colour_master_name": "White",
        "department_no": 1626, "department_name": "Jersey Basic",
        "index_code": "A", "index_name": "Ladieswear", "index_group_code": 1, "index_group_name": "Ladieswear",
        "section_no": 15, "section_name": "Womens Everyday",
        "garment_group_no": 1002, "garment_group_name": "Jersey Basic",
        "detail_desc": "Fitted seamless crop top in ribbed stretch jersey with crew neckline."
    }
]

df_articles = pd.DataFrame(articles_data)
df_articles.to_csv(os.path.join(DATA_DIR, "articles.csv"), index=False)
print(f"Articles saved ({len(df_articles)} records)")

# 2. Generate Realistic Transactions Data (2024-01-01 to 2025-12-31, 104 weeks)
np.random.seed(42)
records = []
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
total_days = (end_date - start_date).days

# Base demand trends per article family
# Style 1 (Tailored Blazer): Strong year-round, accelerating dramatically in Autumn/Winter
# Style 2 (Chunky Knit): High Winter/Autumn peak, low Summer
# Style 3 (Wide Trousers): High growth trend year-round, top performer overall
# Style 4 (Floral Dress): High Summer peak, low Winter
# Style 5 (Cropped Puffer): Winter peak only
# Style 6 (Basic Crop Top): Steady low price baseline

article_weights = {
    "0108775015": {"base": 80, "growth": 0.015, "spring": 1.1, "summer": 0.8, "autumn": 1.6, "winter": 1.4, "price": 49.99},
    "0108775044": {"base": 65, "growth": 0.012, "spring": 1.2, "summer": 0.9, "autumn": 1.5, "winter": 1.3, "price": 49.99},
    "0215882001": {"base": 90, "growth": 0.008, "spring": 0.7, "summer": 0.2, "autumn": 1.7, "winter": 2.2, "price": 34.99},
    "0215882008": {"base": 70, "growth": 0.010, "spring": 0.8, "summer": 0.3, "autumn": 1.6, "winter": 2.0, "price": 34.99},
    "0349910002": {"base": 110, "growth": 0.022, "spring": 1.4, "summer": 1.3, "autumn": 1.8, "winter": 1.5, "price": 39.99},
    "0349910005": {"base": 95, "growth": 0.020, "spring": 1.3, "summer": 1.2, "autumn": 1.7, "winter": 1.4, "price": 39.99},
    "0458120003": {"base": 60, "growth": -0.002, "spring": 1.6, "summer": 2.4, "autumn": 0.7, "winter": 0.3, "price": 29.99},
    "0512490001": {"base": 50, "growth": 0.001, "spring": 0.4, "summer": 0.1, "autumn": 1.3, "winter": 2.5, "price": 59.99},
    "0601990004": {"base": 75, "growth": 0.003, "spring": 1.1, "summer": 1.5, "autumn": 0.8, "winter": 0.6, "price": 14.99},
}

for day_idx in range(0, total_days, 3): # Sample every 3 days
    current_date = start_date + timedelta(days=day_idx)
    date_str = current_date.strftime("%Y-%m-%d")
    month = current_date.month
    
    # Define Season
    if month in [3, 4, 5]: season = "spring"
    elif month in [6, 7, 8]: season = "summer"
    elif month in [9, 10, 11]: season = "autumn"
    else: season = "winter"

    week_num = day_idx // 7
    
    for art_id, params in article_weights.items():
        seasonal_mult = params[season]
        trend_mult = 1.0 + (params["growth"] * week_num)
        noise = np.random.normal(1.0, 0.15)
        
        # Calculate sales count for this day
        n_sales = int(max(0, round(params["base"] * seasonal_mult * trend_mult * noise / 10)))
        
        for i in range(n_sales):
            cust_id = f"cust_{np.random.randint(1000, 9999)}"
            channel = np.random.choice([1, 2], p=[0.3, 0.7]) # 1: store, 2: online
            records.append({
                "t_dat": date_str,
                "customer_id": cust_id,
                "article_id": art_id,
                "price": params["price"],
                "sales_channel_id": channel
            })

df_tx = pd.DataFrame(records)
df_tx.to_csv(os.path.join(DATA_DIR, "transactions_train.csv"), index=False)
print(f"Transactions saved ({len(df_tx)} records)")

# 3. Create Catalogue Reference Images
for _, row in df_articles.iterrows():
    art_id = row["article_id"]
    img_path = os.path.join(IMAGES_DIR, f"{art_id}.jpg")
    img = Image.new("RGB", (400, 500), color=(245, 243, 240))
    draw = ImageDraw.Draw(img)
    
    # Draw simple visual card representation
    draw.rectangle([20, 20, 380, 480], outline=(200, 200, 200), width=2)
    draw.rectangle([40, 40, 360, 320], fill=(220, 215, 210))
    
    # Text label
    draw.text((50, 340), f"H&M ARTICLE: {art_id}", fill=(30, 30, 30))
    draw.text((50, 370), f"{row['prod_name']}", fill=(50, 50, 50))
    draw.text((50, 400), f"Group: {row['garment_group_name']}", fill=(80, 80, 80))
    draw.text((50, 430), f"Color: {row['colour_group_name']}", fill=(80, 80, 80))
    
    img.save(img_path)

print(f"Generated {len(df_articles)} catalogue reference images in {IMAGES_DIR}")
