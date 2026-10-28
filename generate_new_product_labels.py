"""
Generates ultra-high-definition 4096x2048 dual labels (Front + Back) for J B TRADERS.
Front label precisely matches the uploaded reference image:
- Obsidian black curved container label with metallic gold borders
- Top gold crescent & droplet emblem
- Bold white 'J B TRADERS' with gold '— GANDHI OIL —'
- Subtitle: 'POWERING YOUR ENGINE FOR A SMOOTHER TOMORROW'
- Gold ribbon with category name ('PREMIUM', etc.) and bold white 'ENGINE OIL'
- 3 feature badges with gold icons on the left
- Authentic chrome piston with dynamic swirling liquid gold oil splashes on the right
- Bottom dark-gold bar with viscosity (e.g. SAE 15W-40) and pack size callout (e.g. 5L)
- Footer: 'TRUST | QUALITY | PERFORMANCE'
- Backside label with full industrial layout: directions, specs matrix, GHS diamond, barcode, and trade helpline.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
SOURCE_ASSETS_DIR = ROOT / "source" / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
SOURCE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

W, H = 4096, 2048
pad_x = 180
top_y = 120
bot_y = 1920
corner_radius = 90

def get_font(name, size, bold=True):
    paths = [
        f"C:/Windows/Fonts/{name}bd.ttf" if bold else f"C:/Windows/Fonts/{name}.ttf",
        f"C:/Windows/Fonts/{name}.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

# Typography
font_brand = get_font("arialbd", 112)
font_gandhi = get_font("arialbd", 64)
font_tagline = get_font("arialbd", 40)
font_ribbon = get_font("arialbd", 54)
font_headline = get_font("arialbd", 118)
font_subhead = get_font("arialbd", 46)
font_feature_title = get_font("arialbd", 40)
font_feature_sub = get_font("arial", 30, bold=False)
font_visc = get_font("arialbd", 96)
font_visc_sub = get_font("arialbd", 38)
font_vol_num = get_font("impact", 130)
font_trust = get_font("arialbd", 40)

# Backside typography
font_back_title = get_font("arialbd", 68)
font_back_sub = get_font("arialbd", 40)
font_back_section = get_font("arialbd", 34)
font_back_body = get_font("arialbd", 28)
font_back_small = get_font("arialbd", 24)
font_back_micro = get_font("arial", 22, bold=False)
font_back_jb = get_font("arialbd", 84)

# Load piston and emblem assets if available
piston_img = None
if (ASSETS_DIR / "piston_splash_crop.png").exists():
    raw_piston = Image.open(ASSETS_DIR / "piston_splash_crop.png").convert("RGBA")
    # Upscale smoothly to fit right side of front label
    piston_img = raw_piston.resize((820, 940), Image.Resampling.LANCZOS)

emblem_img = None
if (ASSETS_DIR / "gold_emblem_crop.png").exists():
    raw_emblem = Image.open(ASSETS_DIR / "gold_emblem_crop.png").convert("RGBA")
    emblem_img = raw_emblem.resize((260, 195), Image.Resampling.LANCZOS)

products = [
    {
        "id": "2wheeler",
        "filename": "label_2wheeler.png",
        "ribbon": "4T MOTORCYCLE",
        "headline": "ENGINE OIL",
        "subhead": "HIGH PERFORMANCE 4-STROKE LUBRICANT",
        "features": [
            ("Zero Clutch Slip", "JASO MA2 Wet Clutch Standard"),
            ("Thermal Heat Shield", "Low Drag in High-RPM Traffic"),
            ("Fast Throttle Response", "Anti-Piston Friction Coating")
        ],
        "viscosity": "SAE 20W-40",
        "viscosity_sub": "FOR 4-STROKE MOTORCYCLES & SCOOTERS",
        "volume": "1L",
        "volume_sub": "NET PACK (BIKE)",
        "back_desc": "High-performance 4-stroke motorcycle engine oil formulated with shear-stable polymers and specialized wet-clutch friction enhancers. Engineered to eliminate clutch slip, resist thermal breakdown in urban traffic, and protect transmission gears.",
        "back_specs": [("SAE VISCOSITY", "20W-40 / 10W-30"), ("STANDARDS", "JASO MA2 · API SL"), ("BASE OIL", "Group II+ Semi-Synthetic"), ("RECOMMENDED DRAIN", "2,500 – 3,500 KM")]
    },
    {
        "id": "3wheeler",
        "filename": "label_3wheeler.png",
        "ribbon": "CNG & DIESEL AUTO",
        "headline": "ENGINE OIL",
        "subhead": "COMMERCIAL FLEET HEAVY DUTY OIL",
        "features": [
            ("Extended Fleet Drain", "Severe City Traffic Endurance"),
            ("Low-Ash Spark Clean", "Prevents Plug Fouling in CNG"),
            ("Maximum Fuel Economy", "High Compression Seal")
        ],
        "viscosity": "SAE 20W-40",
        "viscosity_sub": "FOR CNG, LPG & DIESEL AUTOS",
        "volume": "3L",
        "volume_sub": "NET PACK (AUTO)",
        "back_desc": "Commercial-grade lubricant engineered for passenger auto rickshaws and cargo loaders operating on CNG, LPG, and diesel fuels. Low-ash chemistry prevents spark-plug fouling and maintains compression under continuous daily shifts.",
        "back_specs": [("SAE VISCOSITY", "20W-40 / 15W-40"), ("STANDARDS", "API SF/CD Low-Ash"), ("BASE OIL", "Hydrocracked Base Stock"), ("RECOMMENDED DRAIN", "3,500 – 4,500 KM")]
    },
    {
        "id": "4wheeler",
        "filename": "label_4wheeler.png",
        "ribbon": "FULL SYNTHETIC",
        "headline": "CAR ENGINE OIL",
        "subhead": "PREMIUM MULTI-VALVE PASSENGER CAR OIL",
        "features": [
            ("Instant Sub-Zero Start", "Ultra-Fast Oil Pressure Build"),
            ("Turbo & Sludge Shield", "API SN Plus Formulation"),
            ("Smooth Quiet Cruising", "Vibration Damper Molecules")
        ],
        "viscosity": "SAE 5W-30",
        "viscosity_sub": "FOR MODERN PETROL, DIESEL & HYBRID CARS",
        "volume": "3.5L",
        "volume_sub": "NET PACK (CAR)",
        "back_desc": "100% full synthetic passenger car engine oil engineered for modern turbocharged petrol, diesel, and hybrid engines. Provides ultra-fast cold start lubrication, zero sludge formation, and exceptional thermal resistance at sustained highway speeds.",
        "back_specs": [("SAE VISCOSITY", "5W-30 Full Synthetic"), ("STANDARDS", "API SN Plus / CF · ACEA A3/B4"), ("BASE OIL", "100% Synthetic Group III+"), ("RECOMMENDED DRAIN", "10,000 KM / 1 Year")]
    },
    {
        "id": "jcb",
        "filename": "label_jcb.png",
        "ribbon": "PREMIUM",
        "headline": "ENGINE OIL",
        "subhead": "HIGH PERFORMANCE LUBRICANT",
        "features": [
            ("Better Engine Protection", "Heavy Duty Anti-Wear Film"),
            ("Improved Fuel Efficiency", "Reduced Friction Resistance"),
            ("Longer Engine Life", "Soot & Corrosion Inhibitor")
        ],
        "viscosity": "SAE 15W-40",
        "viscosity_sub": "FOR DIESEL & PETROL ENGINES",
        "volume": "5L",
        "volume_sub": "NET PACK (FLEET)",
        "back_desc": "Heavy-duty commercial fleet lubricant engineered for earthmoving excavators, backhoe loaders, tippers, and mining machinery. High TBN reserve (10.5+) neutralizes combustion acids and encapsulates sub-micron soot to protect bearings.",
        "back_specs": [("SAE VISCOSITY", "15W-40 CI-4 / CH-4"), ("STANDARDS", "API CI-4 / SL · MB 228.3"), ("TBN RESERVE", "10.5 mg KOH/g Min"), ("SERVICE INTERVAL", "500 Operating Hours")]
    },
    {
        "id": "tractor",
        "filename": "label_tractor.png",
        "ribbon": "MULTI-PURPOSE UTTO",
        "headline": "TRACTOR OIL",
        "subhead": "UNIVERSAL TRACTOR TRANSMISSION & HYDRAULIC",
        "features": [
            ("Chatter-Free Wet Brakes", "Eliminates Brake Squawk"),
            ("Unified Engine & UTTO", "Transmission, Lift & Gear Safe"),
            ("Heavy Dust & Agri Shield", "Extreme Load Viscosity Stability")
        ],
        "viscosity": "SAE 15W-40",
        "viscosity_sub": "FOR TRACTOR ENGINE, TRANSMISSION & LIFTS",
        "volume": "5L",
        "volume_sub": "NET PACK (TRACTOR)",
        "back_desc": "Universal Tractor Transmission Oil (UTTO & STOU) for modern farm tractors and agricultural machinery. Delivers unified lubrication across diesel engine, hydraulic lift cylinders, transmissions, and oil-immersed wet brake packs.",
        "back_specs": [("SAE VISCOSITY", "15W-40 UTTO / STOU"), ("STANDARDS", "John Deere J20C · Ford M2C"), ("APPLICATION", "Engine + Hydraulic + Wet Brake"), ("SERVICE INTERVAL", "600 Operating Hours")]
    },
    {
        "id": "industrial",
        "filename": "label_industrial.png",
        "ribbon": "HEAVY INDUSTRIAL",
        "headline": "HYDRAULIC OIL",
        "subhead": "ANTI-WEAR HIGH PRESSURE HYDRAULIC FLUID",
        "features": [
            ("Anti-Wear EP Film", "Sustains 210 Bar Continuous Pressure"),
            ("Cavitation & Foam Control", "Rapid Air Release Chemistry"),
            ("Thermal Oxidation Shield", "Zero Sludge in Proportional Valves")
        ],
        "viscosity": "ISO VG 68",
        "viscosity_sub": "FOR INDUSTRIAL HYDRAULICS, PRESSES & PUMPS",
        "volume": "26L",
        "volume_sub": "NET PACK (DRUM)",
        "back_desc": "High-VI anti-wear industrial hydraulic fluid engineered for sustained 210-bar industrial hydraulic systems, injection molding machines, CNC machine tools, and enclosed industrial circulating gearboxes.",
        "back_specs": [("ISO VISCOSITY", "ISO VG 68 (Anti-Wear)"), ("STANDARDS", "DIN 51524 Part 2 (HLP)"), ("DIELECTRIC / EP", "Zero Zinc Ash / Low Sludge"), ("RECOMMENDED DRAIN", "4,000 Operating Hours")]
    }
]

def draw_bullet_icon(draw, cx, cy, r=20):
    # Gold circular bullet icon with central dot
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(229, 169, 60, 255), outline=(255, 225, 120, 255), width=3)
    draw.ellipse([cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7], fill=(12, 14, 18, 255))
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(245, 200, 105, 255))

for p in products:
    # Golden-yellow HDPE plastic background across full canvas
    img = Image.new("RGBA", (W, H), (245, 184, 20, 255))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        factor = 1.0 - 0.10 * math.sin(y / H * math.pi)
        r = int(245 * factor)
        g = int(184 * factor)
        b = int(20 * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # =========================================================================
    # LEFT HALF (0 to 2048): FRONT LABEL (EXACT MATCH TO REFERENCE IMAGE!)
    # =========================================================================
    front_box = [pad_x, top_y, 2048 - pad_x, bot_y]

    # Front label shadow
    shadow_front = Image.new("RGBA", (2048, H), (0, 0, 0, 0))
    s_draw_f = ImageDraw.Draw(shadow_front)
    s_draw_f.rounded_rectangle([pad_x - 12, top_y - 8, 2048 - pad_x + 12, bot_y + 16], radius=corner_radius + 8, fill=(0, 0, 0, 120))
    shadow_front = shadow_front.filter(ImageFilter.GaussianBlur(24))
    img.alpha_composite(shadow_front, (0, 0))
    draw = ImageDraw.Draw(img)

    # Front Main Card: Deep obsidian black with outer gold border
    draw.rounded_rectangle(front_box, radius=corner_radius, fill=(7, 7, 9, 255), outline=(229, 169, 60, 255), width=8)
    # Inner gold contour line
    draw.rounded_rectangle([pad_x + 16, top_y + 16, 2048 - pad_x - 16, bot_y - 16], radius=corner_radius - 12, outline=(245, 200, 105, 140), width=3)

    # 1. Top Emblem: Gold oil drop inside crescent
    emblem_y = top_y + 40
    if emblem_img:
        # Paste emblem centered
        ex = (2048 - emblem_img.width) // 2
        img.paste(emblem_img, (ex, emblem_y), emblem_img)
    else:
        # Fallback procedural emblem
        cx = 1024
        draw.ellipse([cx - 70, emblem_y, cx + 70, emblem_y + 140], outline=(229, 169, 60, 255), width=6)
        draw.ellipse([cx - 30, emblem_y + 35, cx + 30, emblem_y + 105], fill=(229, 169, 60, 255))

    # 2. Brand Name: 'J B TRADERS'
    brand_y = emblem_y + 175
    brand_text = "J B TRADERS"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2 + 3, brand_y + 3), brand_text, font=font_brand, fill=(0, 0, 0, 180))
    draw.text(((2048 - tw) // 2, brand_y), brand_text, font=font_brand, fill=(255, 255, 255, 255))

    # 3. Sub-brand: '— GANDHI OIL —'
    gandhi_y = brand_y + 125
    gandhi_text = "—  GANDHI OIL  —"
    bbox = draw.textbbox((0, 0), gandhi_text, font=font_gandhi)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, gandhi_y), gandhi_text, font=font_gandhi, fill=(229, 169, 60, 255))

    # 4. Tagline: 'POWERING YOUR ENGINE FOR A SMOOTHER TOMORROW'
    tagline_y = gandhi_y + 80
    tagline_text = "POWERING YOUR ENGINE FOR A SMOOTHER TOMORROW"
    bbox = draw.textbbox((0, 0), tagline_text, font=font_tagline)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, tagline_y), tagline_text, font=font_tagline, fill=(220, 230, 245, 240))

    # Thin divider line
    div_y1 = tagline_y + 65
    draw.line([(pad_x + 60, div_y1), (2048 - pad_x - 60, div_y1)], fill=(120, 100, 40, 180), width=2)

    # 5. Metallic Gold Ribbon: e.g. 'PREMIUM'
    ribbon_y = div_y1 + 25
    ribbon_w = 540
    ribbon_h = 75
    rx0 = pad_x + 80
    draw.rounded_rectangle([rx0, ribbon_y, rx0 + ribbon_w, ribbon_y + ribbon_h], radius=16, fill=(229, 169, 60, 255), outline=(255, 225, 120, 255), width=3)
    rib_text = p["ribbon"]
    bbox = draw.textbbox((0, 0), rib_text, font=font_ribbon)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((rx0 + (ribbon_w - tw) // 2, ribbon_y + (ribbon_h - th) // 2 - 4), rib_text, font=font_ribbon, fill=(7, 7, 9, 255))

    # 6. Headline: 'ENGINE OIL'
    headline_y = ribbon_y + ribbon_h + 20
    head_text = p["headline"]
    draw.text((pad_x + 80, headline_y), head_text, font=font_headline, fill=(255, 255, 255, 255))

    # 7. Subhead: 'HIGH PERFORMANCE LUBRICANT'
    subhead_y = headline_y + 130
    subhead_text = p["subhead"]
    draw.text((pad_x + 85, subhead_y), subhead_text, font=font_subhead, fill=(229, 169, 60, 255))

    # 8. Middle Right: Composite the Chrome Piston & Liquid Gold Splash Graphic
    if piston_img:
        px = 2048 - pad_x - piston_img.width + 40
        py = subhead_y - 80
        img.paste(piston_img, (px, py), piston_img)

    # 9. Middle Left: 3 Feature Badges
    feat_start_y = subhead_y + 100
    feat_spacing = 135
    for i, (f_title, f_sub) in enumerate(p["features"]):
        fy = feat_start_y + i * feat_spacing
        draw_bullet_icon(draw, pad_x + 115, fy + 24, r=18)
        draw.text((pad_x + 160, fy), f_title, font=font_feature_title, fill=(255, 255, 255, 255))
        draw.text((pad_x + 160, fy + 46), f_sub, font=font_feature_sub, fill=(190, 200, 215, 240))

    # 10. Bottom Bar Section
    bot_bar_y = bot_y - 340
    bot_bar_h = 240
    bar_rect = [pad_x + 30, bot_bar_y, 2048 - pad_x - 30, bot_bar_y + bot_bar_h]
    draw.rounded_rectangle(bar_rect, radius=24, fill=(16, 18, 22, 255), outline=(229, 169, 60, 200), width=3)

    # Left: Viscosity Grade (e.g. SAE 15W-40)
    draw.text((pad_x + 70, bot_bar_y + 24), p["viscosity"], font=font_visc, fill=(245, 200, 105, 255))
    draw.text((pad_x + 75, bot_bar_y + 140), p["viscosity_sub"], font=font_visc_sub, fill=(220, 230, 245, 240))

    # Right: Volume Pill (e.g. 5L)
    vol_w = 260
    vol_h = 190
    vx0 = 2048 - pad_x - 30 - vol_w - 20
    vy0 = bot_bar_y + 25
    draw.rounded_rectangle([vx0, vy0, vx0 + vol_w, vy0 + vol_h], radius=20, fill=(229, 169, 60, 255), outline=(255, 235, 150, 255), width=4)
    v_text = p["volume"]
    bbox = draw.textbbox((0, 0), v_text, font=font_vol_num)
    vw, vh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((vx0 + (vol_w - vw) // 2, vy0 + (vol_h - vh) // 2 - 12), v_text, font=font_vol_num, fill=(7, 7, 9, 255))

    # 11. Footer: 'TRUST   |   QUALITY   |   PERFORMANCE'
    trust_y = bot_y - 75
    trust_text = "TRUST   |   QUALITY   |   PERFORMANCE"
    bbox = draw.textbbox((0, 0), trust_text, font=font_trust)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, trust_y), trust_text, font=font_trust, fill=(229, 169, 60, 255))

    # =========================================================================
    # RIGHT HALF (2048 to 4096): BACKSIDE LABEL
    # =========================================================================
    ox = 2048
    bx0 = ox + pad_x
    bx1 = W - pad_x
    cx_back = (bx0 + bx1) // 2

    # Back Shadow
    shadow_back = Image.new("RGBA", (2048, H), (0, 0, 0, 0))
    s_draw_b = ImageDraw.Draw(shadow_back)
    s_draw_b.rounded_rectangle([pad_x - 12, top_y - 8, 2048 - pad_x + 12, bot_y + 16], radius=corner_radius + 8, fill=(0, 0, 0, 120))
    shadow_back = shadow_back.filter(ImageFilter.GaussianBlur(24))
    img.alpha_composite(shadow_back, (2048, 0))
    draw = ImageDraw.Draw(img)

    # Back Main Card
    back_badge = [bx0, top_y, bx1, bot_y]
    draw.rounded_rectangle(back_badge, radius=corner_radius, fill=(10, 12, 16, 255), outline=(229, 169, 60, 255), width=8)
    draw.rounded_rectangle([bx0 + 16, top_y + 16, bx1 - 16, bot_y - 16], radius=corner_radius - 12, outline=(245, 200, 105, 140), width=3)

    # Back Header
    b_head_y = top_y + 40
    bh_title = "J B TRADERS  ·  TECHNICAL SPECIFICATION"
    bbox = draw.textbbox((0, 0), bh_title, font=font_back_title)
    tw = bbox[2] - bbox[0]
    draw.text(((bx0 + bx1 - tw) // 2, b_head_y), bh_title, font=font_back_title, fill=(255, 255, 255, 255))

    bh_sub = f"GANDHI OIL HUB  ·  {p['viscosity']}  ·  {p['volume']} NET COMMERCIAL PACK"
    bbox = draw.textbbox((0, 0), bh_sub, font=font_back_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((bx0 + bx1 - tw) // 2, b_head_y + 75), bh_sub, font=font_back_sub, fill=(229, 169, 60, 255))

    div_by = b_head_y + 130
    draw.line([(bx0 + 60, div_by), (bx1 - 60, div_by)], fill=(120, 100, 40, 180), width=2)

    # Section 1: Directions for Use & Engine Flushing
    s1_y = div_by + 25
    draw.text((bx0 + 60, s1_y), "DIRECTIONS FOR USE & LUBRICATION MATRIX", font=font_back_section, fill=(245, 200, 105, 255))
    desc_lines = [
        p["back_desc"],
        "• FLUSHING: Always drain previous oil completely while the engine is at normal operating temperature.",
        "• FILTER: Replace oil filter element simultaneously to ensure zero particle contamination.",
        "• TOP-UP: Fill to the upper dipstick notch. Do not overfill. Run engine at idle for 2 minutes to inspect seals."
    ]
    cur_y = s1_y + 48
    for line in desc_lines:
        words = line.split()
        cur_l = []
        for w in words:
            test_l = " ".join(cur_l + [w])
            bbox = draw.textbbox((0, 0), test_l, font=font_back_body)
            if bbox[2] - bbox[0] <= (bx1 - bx0 - 120):
                cur_l.append(w)
            else:
                draw.text((bx0 + 60, cur_y), " ".join(cur_l), font=font_back_body, fill=(220, 230, 245, 255))
                cur_y += 38
                cur_l = [w]
        if cur_l:
            draw.text((bx0 + 60, cur_y), " ".join(cur_l), font=font_back_body, fill=(220, 230, 245, 255))
            cur_y += 44

    # Section 2: Technical Viscometrics & Benchmark Table
    s2_y = cur_y + 15
    draw.line([(bx0 + 60, s2_y), (bx1 - 60, s2_y)], fill=(80, 90, 110, 200), width=2)
    s2_y += 20
    draw.text((bx0 + 60, s2_y), "TECHNICAL BENCHMARKS & TEST STANDARDS", font=font_back_section, fill=(245, 200, 105, 255))
    table_y = s2_y + 45
    t_box_w = (bx1 - bx0 - 120 - 45) // 4
    for idx, (k, v) in enumerate(p["back_specs"]):
        tx = bx0 + 60 + idx * (t_box_w + 15)
        draw.rounded_rectangle([tx, table_y, tx + t_box_w, table_y + 105], radius=14, fill=(18, 22, 28, 255), outline=(100, 115, 135, 200), width=2)
        draw.text((tx + 14, table_y + 14), k, font=font_back_small, fill=(229, 169, 60, 255))
        draw.text((tx + 14, table_y + 55), v, font=font_back_body, fill=(255, 255, 255, 255))

    # Section 3: GHS Hazard Diamond & Safety Guidelines
    s3_y = table_y + 130
    draw.line([(bx0 + 60, s3_y), (bx1 - 60, s3_y)], fill=(80, 90, 110, 200), width=2)
    s3_y += 20
    draw.text((bx0 + 60, s3_y), "SAFETY & HANDLING PRECAUTIONS", font=font_back_section, fill=(245, 200, 105, 255))

    # Draw NFPA / GHS Hazard Diamond
    dia_cx = bx0 + 130
    dia_cy = s3_y + 110
    d_size = 46
    draw.polygon([(dia_cx, dia_cy - d_size*2), (dia_cx + d_size*2, dia_cy), (dia_cx, dia_cy + d_size*2), (dia_cx - d_size*2, dia_cy)], fill=(20, 20, 20, 255), outline=(220, 220, 220, 255))
    # 4 Quadrants
    draw.polygon([(dia_cx, dia_cy - d_size*2), (dia_cx + d_size, dia_cy - d_size), (dia_cx, dia_cy), (dia_cx - d_size, dia_cy - d_size)], fill=(200, 40, 40, 255))
    draw.polygon([(dia_cx - d_size*2, dia_cy), (dia_cx - d_size, dia_cy - d_size), (dia_cx, dia_cy), (dia_cx - d_size, dia_cy + d_size)], fill=(30, 80, 180, 255))
    draw.polygon([(dia_cx, dia_cy), (dia_cx + d_size, dia_cy - d_size), (dia_cx + d_size*2, dia_cy), (dia_cx + d_size, dia_cy + d_size)], fill=(220, 180, 20, 255))
    draw.polygon([(dia_cx - d_size, dia_cy + d_size), (dia_cx, dia_cy), (dia_cx + d_size, dia_cy + d_size), (dia_cx, dia_cy + d_size*2)], fill=(240, 240, 240, 255))

    # Ratings
    draw.text((dia_cx - 9, dia_cy - d_size - 18), "1", font=font_back_title, fill=(255, 255, 255, 255))
    draw.text((dia_cx - d_size - 14, dia_cy - 18), "1", font=font_back_title, fill=(255, 255, 255, 255))
    draw.text((dia_cx + d_size - 6, dia_cy - 18), "0", font=font_back_title, fill=(20, 20, 20, 255))

    safety_x = dia_cx + d_size * 2 + 50
    draw.text((safety_x, s3_y + 40), "• Prolonged skin contact with used engine oil should be avoided. Wash thoroughly with soap.", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((safety_x, s3_y + 75), "• Protect the environment. Return used oil to an authorized recycling collection centre.", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((safety_x, s3_y + 110), "• Do not discharge into drains, soil, or watercourses. Keep container tightly sealed.", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((safety_x, s3_y + 145), "• Store in dry conditions between 5°C and 45°C. Keep out of reach of children.", font=font_back_small, fill=(220, 230, 245, 255))

    # Section 4: Barcode, Batch, Net Quantity & Trade Helpline
    s4_y = s3_y + 195
    draw.line([(bx0 + 60, s4_y), (bx1 - 60, s4_y)], fill=(80, 90, 110, 200), width=2)
    s4_y += 20

    # Barcode
    bar_x0 = bx0 + 60
    bar_y0 = s4_y + 15
    bar_w = 420
    bar_h = 135
    draw.rectangle([bar_x0, bar_y0, bar_x0 + bar_w, bar_y0 + bar_h], fill=(255, 255, 255, 255))
    # Procedural barcode bars
    seed_str = f"89060431391{i}"
    bx = bar_x0 + 20
    for ch in seed_str * 3:
        w_bar = (int(ch) % 3) + 2
        draw.rectangle([bx, bar_y0 + 10, bx + w_bar, bar_y0 + bar_h - 32], fill=(0, 0, 0, 255))
        bx += w_bar + 3
    draw.text((bar_x0 + 40, bar_y0 + bar_h - 26), f"8 906043 13912{i}", font=font_back_small, fill=(0, 0, 0, 255))

    # Batch Matrix Box
    batch_x = bar_x0 + bar_w + 35
    draw.text((batch_x, bar_y0), "BATCH NO: JB-2026-X091", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((batch_x, bar_y0 + 32), "MFG DATE: 02/2026", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((batch_x, bar_y0 + 64), "USE BEFORE: 02/2031 (5 YRS)", font=font_back_small, fill=(220, 230, 245, 255))
    draw.text((batch_x, bar_y0 + 96), "MRP (INCL. TAXES): SEE RATE SHEET", font=font_back_small, fill=(245, 200, 105, 255))

    # Distributor & Helpline Box
    dist_x = bx1 - 580
    draw.text((dist_x, bar_y0), "MARKETED & DISTRIBUTED BY:", font=font_back_small, fill=(229, 169, 60, 255))
    draw.text((dist_x, bar_y0 + 32), "J B TRADERS (GANDHI OIL HUB)", font=font_back_section, fill=(255, 255, 255, 255))
    draw.text((dist_x, bar_y0 + 72), "Helpline: +91 96043 13912", font=font_back_body, fill=(245, 200, 105, 255))
    draw.text((dist_x, bar_y0 + 108), "Email: thelubeexpert999@gmail.com", font=font_back_small, fill=(220, 230, 245, 255))

    # Save to assets and source/assets
    out_a = ASSETS_DIR / p["filename"]
    out_s = SOURCE_ASSETS_DIR / p["filename"]
    img.save(out_a, "PNG", optimize=True)
    img.save(out_s, "PNG", optimize=True)
    print(f"[+] Successfully generated: {out_a} ({out_a.stat().st_size // 1024} KB)")

# Also save label_default.png as JCB
out_def_a = ASSETS_DIR / "label_default.png"
out_def_s = SOURCE_ASSETS_DIR / "label_default.png"
jcb_img = Image.open(ASSETS_DIR / "label_jcb.png")
jcb_img.save(out_def_a, "PNG", optimize=True)
jcb_img.save(out_def_s, "PNG", optimize=True)
print("[+] Successfully generated: label_default.png")

print("=== ALL PRODUCT LABELS GENERATED SUCCESSFULLY ===")
