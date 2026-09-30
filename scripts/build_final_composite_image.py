import os
import glob
from PIL import Image, ImageDraw, ImageFont

ARTIFACT_DIR = r"C:\Users\admin\.gemini\antigravity-ide\brain\cf781c48-b30c-42c2-b855-0f082044e94a"
PROJECT_OUTPUT = r"C:\Users\admin\.gemini\antigravity-ide\scratch\hm_fashion_agent\output"

# Find image files
blazer_files = glob.glob(os.path.join(ARTIFACT_DIR, "*concept_1_asymmetrical_blazer*.jpg"))
trouser_files = glob.glob(os.path.join(ARTIFACT_DIR, "*concept_2_origami_trouser*.jpg"))
knit_files = glob.glob(os.path.join(ARTIFACT_DIR, "*concept_3_funnel_knit*.jpg"))

if not (blazer_files and trouser_files and knit_files):
    raise FileNotFoundError("Could not locate all 3 generated concept images.")

img_blazer = Image.open(blazer_files[0]).resize((600, 600))
img_trouser = Image.open(trouser_files[0]).resize((600, 600))
img_knit = Image.open(knit_files[0]).resize((600, 600))

# Composite Layout Dimensions
# 3 columns layout + top banner header + bottom metadata cards
card_w, card_h = 600, 600
padding = 40
banner_h = 160
footer_h = 240
canvas_w = (card_w * 3) + (padding * 4) # 3*600 + 160 = 1960
canvas_h = banner_h + card_h + footer_h + (padding * 2) # 160 + 600 + 240 + 80 = 1080

composite = Image.new("RGB", (canvas_w, canvas_h), color=(248, 246, 242))
draw = ImageDraw.Draw(composite)

# Draw Top Banner Header
draw.rectangle([0, 0, canvas_w, banner_h], fill=(22, 27, 34))
draw.text((padding, 35), "NEXT-SEASON FASHION CONCEPTS | PREDICTED STYLE WINNERS", fill=(255, 255, 255))
draw.text((padding, 90), "H&M Data-Driven Style Forecasting & Agentic Generative AI Synthesis", fill=(180, 190, 205))

# Paste Images & Draw Card Frames
cards = [
    {
        "title": "CONCEPT 1: ASYMMETRICAL WRAP BLAZER",
        "rank": "WINNER #1 (PGS: 0.94)",
        "dna": "Inspired by: Black/Beige Tailored Blazer (Outerwear)",
        "innovation": "Innovations: Architectural wrap lapel, double-face wool-silk blend, sage green palette.",
        "img": img_blazer,
        "x": padding
    },
    {
        "title": "CONCEPT 2: ORIGAMI PLEATED TROUSER",
        "rank": "WINNER #2 (PGS: 0.91)",
        "dna": "Inspired by: High-Waist Wide-Leg Trouser (Trousers)",
        "innovation": "Innovations: Deep twin origami pleating, extended waist tab, oatmeal linen-viscose drape.",
        "img": img_trouser,
        "x": padding + card_w + padding
    },
    {
        "title": "CONCEPT 3: ARCHITECTURAL RIBBED KNIT",
        "rank": "WINNER #3 (PGS: 0.88)",
        "dna": "Inspired by: Chunky Ribbed Sweater (Knitwear)",
        "innovation": "Innovations: Multi-directional diagonal rib, funnel collar, alpaca-merino yarn.",
        "img": img_knit,
        "x": padding + (card_w * 2) + (padding * 2)
    }
]

y_img = banner_h + padding

for card in cards:
    x = card["x"]
    # Card Background Panel
    draw.rectangle([x - 10, y_img - 10, x + card_w + 10, y_img + card_h + footer_h + 10], fill=(255, 255, 255), outline=(210, 210, 210), width=2)
    
    # Paste image
    composite.paste(card["img"], (x, y_img))
    
    # Text metadata below image
    y_text = y_img + card_h + 20
    draw.rectangle([x, y_text - 5, x + 240, y_text + 25], fill=(235, 240, 248))
    draw.text((x + 10, y_text), card["rank"], fill=(20, 70, 160))
    
    y_text += 35
    draw.text((x, y_text), card["title"], fill=(20, 20, 20))
    
    y_text += 30
    draw.text((x, y_text), card["dna"], fill=(80, 80, 80))
    
    y_text += 25
    draw.text((x, y_text), card["innovation"], fill=(40, 100, 50))

# Save output to artifact dir and project output dir
out_artifact = os.path.join(ARTIFACT_DIR, "final_next_season_concepts.png")
out_project = os.path.join(PROJECT_OUTPUT, "final_next_season_concepts.png")

composite.save(out_artifact)
composite.save(out_project)
print(f"Final composite image successfully created:\n- {out_artifact}\n- {out_project}")
