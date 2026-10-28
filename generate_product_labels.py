"""
Generates ultra-crisp 4096x2048 dual texture labels (Front + Back) for J B TRADERS product line.
- Left 2048x2048: Front Label (identical layout to original)
- Right 2048x2048: Back Label (matching Image 4 packaging with directions, safety diamond, barcode, and Gandhi Oil branding)
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

W, H = 4096, 2048
pad_x = 180
top_y = 120
bot_y = 1920
corner_radius = 80

def get_font(name, size, bold=True):
    paths = [
        f"C:/Windows/Fonts/{name}.ttf",
        f"C:/Windows/Fonts/{name}bd.ttf" if bold else f"C:/Windows/Fonts/{name}.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_title = get_font("arialbd", 104)
font_subtitle = get_font("arialbd", 60)
font_tagline = get_font("arialbd", 54)
font_spec = get_font("impact", 136)
font_body = get_font("arialbd", 46)
font_small = get_font("arialbd", 34)
font_jb_badge = get_font("arialbd", 175)

font_back_title = get_font("arialbd", 68)
font_back_sub = get_font("arialbd", 40)
font_back_section = get_font("arialbd", 32)
font_back_body = get_font("arialbd", 28)
font_back_small = get_font("arialbd", 24)
font_back_micro = get_font("arial", 22, bold=False)
font_back_jb = get_font("arialbd", 90)
font_back_vol = get_font("impact", 68)

products = [
    {
        "id": "2wheeler",
        "filename": "label_2wheeler.png",
        "badge_bg": (140, 24, 24, 255),
        "spec_text": "4T 20W-40",
        "spec_sub": "HIGH-RPM 2 WHEELER ENGINE OIL",
        "spec_desc": "Bikes & Scooters · Smooth Pickup · Cooler Running",
        "badges": [("SMOOTH CLUTCH", "JASO MA2 Standard"), ("HEAT SHIELD", "High Temp Protection"), ("EASY PICKUP", "Low Drag Friction")],
        "volume": "1 L",
        "volume_sub": "NET PACK (BIKE)",
        "back_desc": "High-performance 4-stroke motorcycle engine oil formulated with active shear-stable polymers and specialized wet-clutch friction enhancers. Engineered to prevent clutch slip, reduce engine heat in stop-and-go city traffic, and protect transmission gear sets against pitting.",
        "back_specs": [("SAE VISCOSITY", "20W-40 / 10W-30"), ("STANDARDS", "JASO MA2 · API SL"), ("BASE OIL", "Group II+ Semi-Synthetic"), ("RECOMMENDED DRAIN", "2,500 – 3,500 KM")]
    },
    {
        "id": "3wheeler",
        "filename": "label_3wheeler.png",
        "badge_bg": (18, 64, 48, 255),
        "spec_text": "20W-40 CNG",
        "spec_sub": "3 WHEELER LONG-DRAIN AUTO OIL",
        "spec_desc": "Auto Rickshaws · CNG & Diesel · All-Day Duty",
        "badges": [("LONG DRAIN", "Extended Fleet Life"), ("CLEAN VALVE", "Low Ash Deposit"), ("FUEL SAVER", "High Efficiency")],
        "volume": "3 L",
        "volume_sub": "NET PACK (AUTO)",
        "back_desc": "Commercial-grade lubricant engineered for passenger auto rickshaws and cargo loaders operating on CNG, LPG, and diesel fuels. Features low-ash detergency to eliminate spark-plug fouling, maintain cylinder compression, and resist thermal breakdown across long continuous shifts.",
        "back_specs": [("SAE VISCOSITY", "20W-40 / 15W-40"), ("STANDARDS", "API SF/CD Low-Ash"), ("BASE OIL", "Hydrocracked Base Stock"), ("RECOMMENDED DRAIN", "3,500 – 4,500 KM")]
    },
    {
        "id": "4wheeler",
        "filename": "label_4wheeler.png",
        "badge_bg": (16, 42, 88, 255),
        "spec_text": "5W-30 SN",
        "spec_sub": "FULLY SYNTHETIC CAR & SUV OIL",
        "spec_desc": "Petrol & Diesel Engines · Maximum Fuel Economy",
        "badges": [("INSTANT START", "Zero Friction Cranking"), ("TURBO BOOST", "API SN Formulation"), ("QUIET CABIN", "Vibration Damper")],
        "volume": "3.5 L",
        "volume_sub": "NET PACK (CAR)",
        "back_desc": "100% full synthetic passenger car engine oil engineered for modern multi-valve, turbocharged petrol, diesel, and hybrid engines. Provides ultra-fast cold start oil circulation, zero sludge formation, and exceptional thermal resistance under aggressive highway driving conditions.",
        "back_specs": [("SAE VISCOSITY", "5W-30 Full Synthetic"), ("STANDARDS", "API SN Plus / CF · ACEA A3/B4"), ("BASE OIL", "100% Synthetic Group III+"), ("RECOMMENDED DRAIN", "10,000 KM / 1 Year")]
    },
    {
        "id": "jcb",
        "filename": "label_jcb.png",
        "badge_bg": (22, 24, 30, 255),
        "spec_text": "15W-40 CI-4",
        "spec_sub": "HEAVY DUTY JCB & EARTH MOVING",
        "spec_desc": "Loaders · Excavators · Heavy Duty Commercial Trucks",
        "badges": [("HEAVY LOAD", "Anti-Wear Shock Film"), ("SOOT CONTROL", "EGR & Turbo Protection"), ("HYDRAULIC SAFE", "Anti-Cavitation")],
        "volume": "5 L",
        "volume_sub": "NET PACK (FLEET)",
        "back_desc": "Heavy-duty commercial fleet lubricant engineered for earthmoving excavators, backhoe loaders, tippers, and mining equipment. High TBN reserve (10.5+) neutralizes corrosive combustion acids, while advanced dispersants encapsulate sub-micron soot particles to eliminate valve-train wear under heavy dust.",
        "back_specs": [("SAE VISCOSITY", "15W-40 CI-4 / CH-4"), ("STANDARDS", "API CI-4 / SL · MB 228.3"), ("TBN RESERVE", "10.5 mg KOH/g Min"), ("SERVICE INTERVAL", "500 Operating Hours")]
    },
    {
        "id": "tractor",
        "filename": "label_tractor.png",
        "badge_bg": (26, 68, 32, 255),
        "spec_text": "STOU 15W-40",
        "spec_sub": "MULTI-PURPOSE TRACTOR & HYDRAULIC",
        "spec_desc": "Engine · Wet Brakes · Transmission & Hydraulics",
        "badges": [("ALL-IN-ONE", "Engine + UTTO Unified"), ("WET BRAKE", "Chatter-Free Braking"), ("DUST PROOF", "Heavy Agri Sealed")],
        "volume": "5 L",
        "volume_sub": "NET PACK (TRACTOR)",
        "back_desc": "Universal Tractor Transmission Oil (UTTO & STOU) for modern farm tractors and agricultural machinery. Delivers unified lubrication across diesel engine, hydraulic lift cylinders, transmissions, and oil-immersed wet brake packs with complete elimination of brake chatter and squawk.",
        "back_specs": [("SAE VISCOSITY", "15W-40 UTTO / STOU"), ("STANDARDS", "John Deere J20C · Ford M2C"), ("APPLICATION", "Engine + Hydraulic + Wet Brake"), ("SERVICE INTERVAL", "600 Operating Hours")]
    },
    {
        "id": "industrial",
        "filename": "label_industrial.png",
        "badge_bg": (34, 38, 48, 255),
        "spec_text": "HYD 68 / GEAR",
        "spec_sub": "FACTORY INDUSTRIAL HYDRAULIC & GEAR",
        "spec_desc": "Compressors · Turbines · Heavy Gearboxes & Pumps",
        "badges": [("ANTI-FOAM", "Rapid Air Release"), ("ANTI-RUST", "Zinc Thermal Film"), ("5000+ HOURS", "Industrial Endurance")],
        "volume": "5 L",
        "volume_sub": "NET PACK (FACTORY)",
        "back_desc": "Factory-grade anti-wear hydraulic oil (ISO VG 68) and extreme-pressure industrial gear fluid. Formulated with thermally stable zinc-dithiophosphate chemistry and rapid air-release antifoam agents to protect high-pressure vane, piston, and gear pumps operating continuously at 210+ bar.",
        "back_specs": [("ISO VISCOSITY", "VG 68 · DIN 51524 Part 2 HLP"), ("GEAR RATING", "ISO EP 90 / 140 Additives"), ("DROP POINT", "195°C+ High Temperature"), ("SERVICE LIFE", "5,000+ Operating Hours")]
    }
]

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for w in words:
        test_line = " ".join(current_line + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(w)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

for p in products:
    # 4096 x 2048 RGBA canvas
    img = Image.new("RGBA", (W, H), (245, 184, 20, 255))
    draw = ImageDraw.Draw(img)

    # HDPE subtle gradient across all 4096 columns
    for y in range(H):
        factor = 1.0 - 0.12 * math.sin(y / H * math.pi)
        r = int(245 * factor)
        g = int(184 * factor)
        b = int(20 * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # =========================================================================
    # LEFT HALF (0 to 2048): FRONT LABEL
    # =========================================================================
    cx_front = 1024
    cy_front = top_y + 280
    emblem_r = 135

    # Front Shadow
    shadow_front = Image.new("RGBA", (2048, H), (0, 0, 0, 0))
    s_draw_f = ImageDraw.Draw(shadow_front)
    s_draw_f.rounded_rectangle([pad_x - 12, top_y - 8, 2048 - pad_x + 12, bot_y + 16], radius=corner_radius + 8, fill=(0, 0, 0, 110))
    shadow_front = shadow_front.filter(ImageFilter.GaussianBlur(24))
    img.alpha_composite(shadow_front, (0, 0))
    draw = ImageDraw.Draw(img)

    # Front Main Badge
    front_badge = [pad_x, top_y, 2048 - pad_x, bot_y]
    draw.rounded_rectangle(front_badge, radius=corner_radius, fill=p["badge_bg"], outline=(229, 169, 60, 255), width=10)
    draw.rounded_rectangle([pad_x + 20, top_y + 20, 2048 - pad_x - 20, bot_y - 20], radius=corner_radius - 16, outline=(245, 200, 105, 180), width=4)

    # Front Top Header
    partner_text = "MOTOCOAT  ·  FINOLUBE  ·  HPCL"
    bbox = draw.textbbox((0, 0), partner_text, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, top_y + 48), partner_text, font=font_small, fill=(229, 169, 60, 255))
    div_y = top_y + 105
    draw.line([(pad_x + 80, div_y), (2048 - pad_x - 80, div_y)], fill=(120, 130, 150, 160), width=2)

    # Front JB Monogram
    draw.ellipse([cx_front - emblem_r - 12, cy_front - emblem_r - 12, cx_front + emblem_r + 12, cy_front + emblem_r + 12], fill=(229, 169, 60, 100))
    draw.ellipse([cx_front - emblem_r, cy_front - emblem_r, cx_front + emblem_r, cy_front + emblem_r], fill=(245, 195, 68, 255), outline=(255, 235, 170, 255), width=8)
    draw.ellipse([cx_front - emblem_r + 14, cy_front - emblem_r + 14, cx_front + emblem_r - 14, cy_front + emblem_r - 14], fill=(229, 169, 60, 255), outline=(180, 120, 25, 255), width=4)
    jb_text = "JB"
    bbox = draw.textbbox((0, 0), jb_text, font=font_jb_badge)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx_front - tw // 2, cy_front - th // 2 - 16), jb_text, font=font_jb_badge, fill=(18, 20, 24, 255))

    # Front Brand Title
    brand_y = cy_front + emblem_r + 35
    brand_text = "J B TRADERS"
    bbox = draw.textbbox((0, 0), brand_text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2 + 3, brand_y + 3), brand_text, font=font_title, fill=(0, 0, 0, 200))
    draw.text(((2048 - tw) // 2, brand_y), brand_text, font=font_title, fill=(255, 255, 255, 255))

    sub_y = brand_y + 120
    sub_text = "G A N D H I   O I L"
    bbox = draw.textbbox((0, 0), sub_text, font=font_subtitle)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, sub_y), sub_text, font=font_subtitle, fill=(229, 169, 60, 255))

    # Front Ribbon
    ribbon_y = sub_y + 105
    ribbon_h = 100
    ribbon_rect = [pad_x + 60, ribbon_y, 2048 - pad_x - 60, ribbon_y + ribbon_h]
    draw.rounded_rectangle(ribbon_rect, radius=24, fill=(229, 169, 60, 255), outline=(255, 220, 120, 255), width=4)
    tagline = "LIQUID GOLD FOR EVERY ENGINE."
    bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((2048 - tw) // 2, ribbon_y + (ribbon_h - th) // 2 - 8), tagline, font=font_tagline, fill=(18, 20, 24, 255))

    # Front Spec
    spec_y = ribbon_y + ribbon_h + 50
    spec_text = p["spec_text"]
    bbox = draw.textbbox((0, 0), spec_text, font=font_spec)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2 + 4, spec_y + 4), spec_text, font=font_spec, fill=(0, 0, 0, 180))
    draw.text(((2048 - tw) // 2, spec_y), spec_text, font=font_spec, fill=(255, 204, 51, 255))

    spec_sub_y = spec_y + 145
    spec_sub = p["spec_sub"]
    bbox = draw.textbbox((0, 0), spec_sub, font=font_body)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, spec_sub_y), spec_sub, font=font_body, fill=(235, 240, 250, 255))

    spec_sub2_y = spec_sub_y + 60
    spec_sub2 = p["spec_desc"]
    bbox = draw.textbbox((0, 0), spec_sub2, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((2048 - tw) // 2, spec_sub2_y), spec_sub2, font=font_small, fill=(180, 190, 210, 255))

    # Front 3 Badges
    badge_row_y = spec_sub2_y + 80
    badge_w = 460
    badge_h = 105
    start_bx = pad_x + 90
    gap_bx = ((2048 - pad_x * 2 - 180) - (badge_w * 3)) // 2

    for i, (b_title, b_sub) in enumerate(p["badges"]):
        bx = start_bx + i * (badge_w + gap_bx)
        draw.rounded_rectangle([bx, badge_row_y, bx + badge_w, badge_row_y + badge_h], radius=16, fill=(20, 22, 28, 200), outline=(80, 90, 110, 255), width=2)
        bbox = draw.textbbox((0, 0), b_title, font=font_small)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (badge_w - tw) // 2, badge_row_y + 16), b_title, font=font_small, fill=(245, 200, 105, 255))
        font_micro = get_font("arial", 26, bold=False)
        bbox = draw.textbbox((0, 0), b_sub, font=font_micro)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (badge_w - tw) // 2, badge_row_y + 60), b_sub, font=font_micro, fill=(190, 200, 215, 255))

    # Front Footer Box
    footer_y = badge_row_y + badge_h + 65
    vol_box = [pad_x + 90, footer_y, pad_x + 480, footer_y + 175]
    draw.rounded_rectangle(vol_box, radius=20, fill=(229, 169, 60, 255), outline=(255, 235, 170, 255), width=4)
    font_vol = get_font("impact", 90)
    vol_text = p["volume"]
    bbox = draw.textbbox((0, 0), vol_text, font=font_vol)
    tw = bbox[2] - bbox[0]
    draw.text((vol_box[0] + (vol_box[2] - vol_box[0] - tw) // 2, footer_y + 18), vol_text, font=font_vol, fill=(18, 20, 24, 255))
    font_net = get_font("arialbd", 28)
    net_text = p["volume_sub"]
    bbox = draw.textbbox((0, 0), net_text, font=font_net)
    tw = bbox[2] - bbox[0]
    draw.text((vol_box[0] + (vol_box[2] - vol_box[0] - tw) // 2, footer_y + 118), net_text, font=font_net, fill=(18, 20, 24, 255))

    right_x = pad_x + 520
    draw.text((right_x, footer_y + 15), "AUTHORISED LUBRICANT DEALER", font=font_small, fill=(229, 169, 60, 255))
    draw.text((right_x, footer_y + 60), "Helpline: +91 96043 13912", font=font_body, fill=(255, 255, 255, 255))
    draw.text((right_x, footer_y + 120), "Genuine Quality Assured  ·  lubricant-oil-hub.lovable.app", font=font_small, fill=(170, 185, 205, 255))

    reg_y = bot_y - 95
    draw.line([(pad_x + 60, reg_y), (2048 - pad_x - 60, reg_y)], fill=(80, 90, 110, 255), width=2)
    draw.text((pad_x + 120, reg_y + 24), "ISO 9001 / API CERTIFIED FORMULATION · RECYCLE HDPE (2)", font=font_small, fill=(150, 160, 180, 255))

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
    s_draw_b.rounded_rectangle([pad_x - 12, top_y - 8, 2048 - pad_x + 12, bot_y + 16], radius=corner_radius + 8, fill=(0, 0, 0, 110))
    shadow_back = shadow_back.filter(ImageFilter.GaussianBlur(24))
    img.alpha_composite(shadow_back, (2048, 0))
    draw = ImageDraw.Draw(img)

    # Back Main Badge Box
    draw.rounded_rectangle([bx0, top_y, bx1, bot_y], radius=corner_radius, fill=(18, 21, 28, 255), outline=(229, 169, 60, 255), width=10)
    draw.rounded_rectangle([bx0 + 20, top_y + 20, bx1 - 20, bot_y - 20], radius=corner_radius - 16, outline=(245, 200, 105, 180), width=4)

    # Back Top Sub-header
    back_top_str = "AUTHENTIC REFINERY BLENDED LUBRICANT  ·  100% FACTORY SEALED"
    bbox = draw.textbbox((0, 0), back_top_str, font=font_back_small)
    tw = bbox[2] - bbox[0]
    draw.text((cx_back - tw // 2, top_y + 40), back_top_str, font=font_back_small, fill=(229, 169, 60, 255))
    draw.line([(bx0 + 60, top_y + 88), (bx1 - 60, top_y + 88)], fill=(120, 130, 150, 160), width=2)

    # Back JB Monogram + Header Info
    jb_back_cx = bx0 + 130
    jb_back_cy = top_y + 180
    jb_back_r = 72
    draw.ellipse([jb_back_cx - jb_back_r, jb_back_cy - jb_back_r, jb_back_cx + jb_back_r, jb_back_cy + jb_back_r], fill=(245, 195, 68, 255), outline=(255, 235, 170, 255), width=5)
    draw.ellipse([jb_back_cx - jb_back_r + 8, jb_back_cy - jb_back_r + 8, jb_back_cx + jb_back_r - 8, jb_back_cy + jb_back_r - 8], fill=(229, 169, 60, 255), outline=(180, 120, 25, 255), width=3)
    bbox = draw.textbbox((0, 0), "JB", font=font_back_jb)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((jb_back_cx - tw // 2, jb_back_cy - th // 2 - 8), "JB", font=font_back_jb, fill=(18, 20, 24, 255))

    header_text_x = bx0 + 240
    draw.text((header_text_x, top_y + 115), "J B TRADERS", font=font_back_title, fill=(255, 255, 255, 255))
    draw.text((header_text_x, top_y + 195), "GANDHI OIL HUB · THE LUBE EXPERT", font=font_back_sub, fill=(229, 169, 60, 255))

    # Product Back Title Ribbon
    prib_y = top_y + 275
    prib_h = 75
    draw.rounded_rectangle([bx0 + 60, prib_y, bx1 - 60, prib_y + prib_h], radius=16, fill=(32, 38, 50, 255), outline=(229, 169, 60, 200), width=2)
    prib_text = f"{p['spec_text']}  —  {p['spec_sub']}"
    bbox = draw.textbbox((0, 0), prib_text, font=font_back_section)
    tw = bbox[2] - bbox[0]
    draw.text((cx_back - tw // 2, prib_y + 20), prib_text, font=font_back_section, fill=(255, 218, 120, 255))

    # Section 1: Product Formulation & Engineering Box
    sec1_y = prib_y + prib_h + 25
    sec1_w = bx1 - bx0 - 120
    draw.rounded_rectangle([bx0 + 60, sec1_y, bx1 - 60, sec1_y + 225], radius=16, fill=(24, 28, 38, 200), outline=(80, 95, 120, 200), width=2)
    draw.text((bx0 + 90, sec1_y + 18), "PRODUCT FORMULATION & MOLECULAR ENGINEERING", font=font_back_section, fill=(229, 169, 60, 255))
    lines_desc = wrap_text(p["back_desc"], font_back_body, sec1_w - 60, draw)
    dy = sec1_y + 65
    for l in lines_desc:
        draw.text((bx0 + 90, dy), l, font=font_back_body, fill=(225, 235, 248, 255))
        dy += 38

    # Section 2: Technical Specifications 4-Grid
    sec2_y = sec1_y + 245
    grid_w = (sec1_w - 20) // 2
    grid_h = 75
    for idx, (sk, sv) in enumerate(p["back_specs"]):
        gx = bx0 + 60 + (idx % 2) * (grid_w + 20)
        gy = sec2_y + (idx // 2) * (grid_h + 12)
        draw.rounded_rectangle([gx, gy, gx + grid_w, gy + grid_h], radius=12, fill=(28, 34, 46, 220), outline=(100, 115, 145, 180), width=2)
        draw.text((gx + 20, gy + 12), sk, font=font_back_micro, fill=(180, 195, 215, 255))
        draw.text((gx + 20, gy + 38), sv, font=font_back_body, fill=(255, 225, 130, 255))

    # Section 3: Directions for Application (4 numbered steps)
    sec3_y = sec2_y + 195
    draw.rounded_rectangle([bx0 + 60, sec3_y, bx1 - 60, sec3_y + 270], radius=16, fill=(24, 28, 38, 200), outline=(80, 95, 120, 200), width=2)
    draw.text((bx0 + 90, sec3_y + 18), "DIRECTIONS FOR USE & WORKSHOP MAINTENANCE", font=font_back_section, fill=(229, 169, 60, 255))

    steps = [
        "1. Drain contaminated oil completely while engine is warm for maximum particulate evacuation.",
        "2. Replace engine oil filter with genuine OEM-certified unit prior to refilling lubricant.",
        "3. Refill fresh oil to recommended sump capacity as specified in manufacturer service manual.",
        "4. Check dipstick level; avoid overfilling. Inspect for leaks after 5 minutes of idle running."
    ]
    s_y = sec3_y + 65
    for s in steps:
        draw.text((bx0 + 90, s_y), s, font=font_back_body, fill=(215, 225, 240, 255))
        s_y += 46

    # Section 4: Cautionary / Environmental Notice (Inspired by Image 4 Hazard Diamond!)
    sec4_y = sec3_y + 295
    sec4_h = 245
    draw.rounded_rectangle([bx0 + 60, sec4_y, bx1 - 60, sec4_y + sec4_h], radius=16, fill=(30, 22, 22, 230), outline=(210, 50, 50, 255), width=3)

    # Red Hazard Diamond
    dia_cx = bx0 + 155
    dia_cy = sec4_y + sec4_h // 2
    dia_r = 75
    pts = [(dia_cx, dia_cy - dia_r), (dia_cx + dia_r, dia_cy), (dia_cx, dia_cy + dia_r), (dia_cx - dia_r, dia_cy)]
    draw.polygon(pts, fill=(255, 255, 255, 255), outline=(210, 35, 35, 255), width=7)
    font_excl = get_font("impact", 90)
    bbox = draw.textbbox((0, 0), "!", font=font_excl)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((dia_cx - tw // 2, dia_cy - th // 2 - 8), "!", font=font_excl, fill=(20, 20, 20, 255))

    # Caution Text block
    c_text_x = bx0 + 265
    draw.text((c_text_x, sec4_y + 18), "CAUTIONARY & ENVIRONMENTAL PROTECTION NOTICE", font=font_back_section, fill=(255, 110, 110, 255))
    caution_str = "Avoid prolonged or repeated skin contact with used engine oil. Thoroughly wash exposed areas with soap and water after handling. Keep out of reach of children. PROTECT THE ENVIRONMENT: Do not pollute drains, watercourses, soil, or municipal trash. Return drained lubricant to authorised recycling collection depots."
    c_lines = wrap_text(caution_str, font_back_body, bx1 - c_text_x - 90, draw)
    cy_text = sec4_y + 65
    for cl in c_lines:
        draw.text((c_text_x, cy_text), cl, font=font_back_body, fill=(240, 225, 225, 255))
        cy_text += 40

    # Section 5: Bottom Barcode, Recyclable HDPE, Factory Authenticity & Volume
    sec5_y = sec4_y + sec4_h + 30
    b_code_w = 420
    b_code_h = 175
    draw.rectangle([bx0 + 60, sec5_y, bx0 + 60 + b_code_w, sec5_y + b_code_h], fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)

    import random
    rng = random.Random(hash(p["id"]) & 0xffff)
    cur_x = bx0 + 80
    end_x = bx0 + 60 + b_code_w - 20
    while cur_x < end_x:
        bw = rng.choice([3, 5, 8, 12])
        if cur_x + bw > end_x: break
        draw.rectangle([cur_x, sec5_y + 12, cur_x + bw, sec5_y + b_code_h - 35], fill=(15, 15, 15, 255))
        gap = rng.choice([3, 5, 7, 10])
        cur_x += bw + gap
    draw.text((bx0 + 95, sec5_y + b_code_h - 28), "8  906043  139120", font=font_back_small, fill=(20, 20, 20, 255))

    # Middle Center Info: Distributor & Tamper Proof Stamp
    mid_info_x = bx0 + 60 + b_code_w + 35
    draw.text((mid_info_x, sec5_y + 10), "AUTHORISED MASTER DISTRIBUTOR", font=font_back_section, fill=(229, 169, 60, 255))
    draw.text((mid_info_x, sec5_y + 50), "J B TRADERS (Gandhi Oil Hub)", font=font_back_body, fill=(255, 255, 255, 255))
    draw.text((mid_info_x, sec5_y + 88), "Depot: Sinhagad Road, Pune · Helpline: +91 96043 13912", font=font_back_body, fill=(200, 215, 235, 255))
    draw.text((mid_info_x, sec5_y + 128), "100% Factory Tamper-Proof Induction Foil Sealed", font=font_back_small, fill=(245, 200, 105, 255))

    # Right Volume Box
    vol_box_w = 340
    vol_box_x = bx1 - 60 - vol_box_w
    draw.rounded_rectangle([vol_box_x, sec5_y, bx1 - 60, sec5_y + b_code_h], radius=18, fill=(229, 169, 60, 255), outline=(255, 235, 170, 255), width=3)
    v_str = p["volume"]
    bbox = draw.textbbox((0, 0), v_str, font=font_back_vol)
    tw = bbox[2] - bbox[0]
    draw.text((vol_box_x + (vol_box_w - tw) // 2, sec5_y + 20), v_str, font=font_back_vol, fill=(18, 20, 24, 255))
    vsub_str = p["volume_sub"]
    bbox = draw.textbbox((0, 0), vsub_str, font=font_back_small)
    tw = bbox[2] - bbox[0]
    draw.text((vol_box_x + (vol_box_w - tw) // 2, sec5_y + 115), vsub_str, font=font_back_small, fill=(18, 20, 24, 255))

    # Bottom Registration Bar
    reg_y = bot_y - 65
    draw.line([(bx0 + 60, reg_y), (bx1 - 60, reg_y)], fill=(80, 95, 120, 255), width=2)
    reg_str = "RECYCLABLE HDPE (2)  ·  BATCH NO: JBT-2026-V8  ·  NET WEIGHT VERIFIED  ·  MANUFACTURED IN MAHARASHTRA"
    bbox = draw.textbbox((0, 0), reg_str, font=font_back_micro)
    tw = bbox[2] - bbox[0]
    draw.text((cx_back - tw // 2, reg_y + 18), reg_str, font=font_back_micro, fill=(150, 165, 185, 255))

    # Save to assets/ and source/assets/
    out_file = ASSETS_DIR / p["filename"]
    img.save(str(out_file), "PNG", quality=100)

    # Mirror to source/assets/
    source_asset_file = SCRIPT_DIR / "source" / "assets" / p["filename"]
    if source_asset_file.parent.exists():
        img.save(str(source_asset_file), "PNG", quality=100)

    print(f"[+] Successfully generated 4096x2048 dual label: {out_file.name}")

print("[*] All 6 product dual labels successfully created!")
