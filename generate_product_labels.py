"""
Script to generate ultra-crisp 2048x2048 texture labels for each J B TRADERS product line.
Used dynamically on the 3D can model in the website's 3D showroom:
- 2 Wheeler (1L compact)
- 3 Wheeler (3L medium)
- 4 Wheeler (3.5L synthetic)
- JCB & Earth Moving (5L heavy duty)
- Tractor Oil (5L agricultural)
- Industrial (5L factory grade)
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR / "assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

W, H = 2048, 2048

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

products = [
    {
        "id": "2wheeler",
        "filename": "label_2wheeler.png",
        "badge_bg": (140, 24, 24, 255),      # Sport Racing Crimson
        "spec_text": "4T 20W-40",
        "spec_sub": "HIGH-RPM 2 WHEELER ENGINE OIL",
        "spec_desc": "Bikes & Scooters · Smooth Pickup · Cooler Running",
        "badges": [("SMOOTH CLUTCH", "JASO MA2 Standard"), ("HEAT SHIELD", "High Temp Protection"), ("EASY PICKUP", "Low Drag Friction")],
        "volume": "1 L",
        "volume_sub": "NET PACK (BIKE)"
    },
    {
        "id": "3wheeler",
        "filename": "label_3wheeler.png",
        "badge_bg": (18, 64, 48, 255),       # Commercial Emerald
        "spec_text": "20W-40 CNG",
        "spec_sub": "3 WHEELER LONG-DRAIN AUTO OIL",
        "spec_desc": "Auto Rickshaws · CNG & Diesel · All-Day Duty",
        "badges": [("LONG DRAIN", "Extended Fleet Life"), ("CLEAN VALVE", "Low Ash Deposit"), ("FUEL SAVER", "High Efficiency")],
        "volume": "3 L",
        "volume_sub": "NET PACK (AUTO)"
    },
    {
        "id": "4wheeler",
        "filename": "label_4wheeler.png",
        "badge_bg": (16, 42, 88, 255),       # High-Tech Synthetic Blue
        "spec_text": "5W-30 SN",
        "spec_sub": "FULLY SYNTHETIC CAR & SUV OIL",
        "spec_desc": "Petrol & Diesel Engines · Maximum Fuel Economy",
        "badges": [("INSTANT START", "Zero Friction Cranking"), ("TURBO BOOST", "API SN Formulation"), ("QUIET CABIN", "Vibration Damper")],
        "volume": "3.5 L",
        "volume_sub": "NET PACK (CAR)"
    },
    {
        "id": "jcb",
        "filename": "label_jcb.png",
        "badge_bg": (22, 24, 30, 255),       # Heavy Duty Industrial Charcoal
        "spec_text": "15W-40 CI-4",
        "spec_sub": "HEAVY DUTY JCB & EARTH MOVING",
        "spec_desc": "Loaders · Excavators · Heavy Duty Commercial Trucks",
        "badges": [("HEAVY LOAD", "Anti-Wear Shock Film"), ("SOOT CONTROL", "EGR & Turbo Protection"), ("HYDRAULIC SAFE", "Anti-Cavitation")],
        "volume": "5 L",
        "volume_sub": "NET PACK (FLEET)"
    },
    {
        "id": "tractor",
        "filename": "label_tractor.png",
        "badge_bg": (26, 68, 32, 255),       # Agri Forest Green
        "spec_text": "STOU 15W-40",
        "spec_sub": "MULTI-PURPOSE TRACTOR & HYDRAULIC",
        "spec_desc": "Engine · Wet Brakes · Transmission & Hydraulics",
        "badges": [("ALL-IN-ONE", "Engine + UTTO Unified"), ("WET BRAKE", "Chatter-Free Braking"), ("DUST PROOF", "Heavy Agri Sealed")],
        "volume": "5 L",
        "volume_sub": "NET PACK (TRACTOR)"
    },
    {
        "id": "industrial",
        "filename": "label_industrial.png",
        "badge_bg": (34, 38, 48, 255),       # Factory Graphite
        "spec_text": "HYD 68 / GEAR",
        "spec_sub": "FACTORY INDUSTRIAL HYDRAULIC & GEAR",
        "spec_desc": "Compressors · Turbines · Heavy Gearboxes & Pumps",
        "badges": [("ANTI-FOAM", "Rapid Air Release"), ("ANTI-RUST", "Zinc Thermal Film"), ("5000+ HOURS", "Industrial Endurance")],
        "volume": "5 L",
        "volume_sub": "NET PACK (FACTORY)"
    }
]

pad_x = 180
top_y = 120
bot_y = 1920
corner_radius = 80
cx = W // 2
cy = top_y + 280
emblem_r = 135

for p in products:
    # Yellow HDPE background
    img = Image.new("RGBA", (W, H), (245, 184, 20, 255))
    draw = ImageDraw.Draw(img)

    for y in range(H):
        factor = 1.0 - 0.12 * math.sin(y / H * math.pi)
        r = int(245 * factor)
        g = int(184 * factor)
        b = int(20 * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

    # Badge Shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([pad_x - 12, top_y - 8, W - pad_x + 12, bot_y + 16], radius=corner_radius + 8, fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # Main Shield Body
    badge_rect = [pad_x, top_y, W - pad_x, bot_y]
    draw.rounded_rectangle(badge_rect, radius=corner_radius, fill=p["badge_bg"], outline=(229, 169, 60, 255), width=10)
    draw.rounded_rectangle([pad_x + 20, top_y + 20, W - pad_x - 20, bot_y - 20], radius=corner_radius - 16, outline=(245, 200, 105, 180), width=4)

    # Top Header
    partner_text = "MOTOCOAT  ·  FINOLUBE  ·  HPCL"
    bbox = draw.textbbox((0, 0), partner_text, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, top_y + 48), partner_text, font=font_small, fill=(229, 169, 60, 255))
    div_y = top_y + 105
    draw.line([(pad_x + 80, div_y), (W - pad_x - 80, div_y)], fill=(120, 130, 150, 160), width=2)

    # JB Monogram
    draw.ellipse([cx - emblem_r - 12, cy - emblem_r - 12, cx + emblem_r + 12, cy + emblem_r + 12], fill=(229, 169, 60, 100))
    draw.ellipse([cx - emblem_r, cy - emblem_r, cx + emblem_r, cy + emblem_r], fill=(245, 195, 68, 255), outline=(255, 235, 170, 255), width=8)
    draw.ellipse([cx - emblem_r + 14, cy - emblem_r + 14, cx + emblem_r - 14, cy + emblem_r - 14], fill=(229, 169, 60, 255), outline=(180, 120, 25, 255), width=4)
    jb_text = "JB"
    bbox = draw.textbbox((0, 0), jb_text, font=font_jb_badge)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 16), jb_text, font=font_jb_badge, fill=(18, 20, 24, 255))

    # Brand Title
    brand_y = cy + emblem_r + 35
    brand_text = "J B TRADERS"
    bbox = draw.textbbox((0, 0), brand_text, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2 + 3, brand_y + 3), brand_text, font=font_title, fill=(0, 0, 0, 200))
    draw.text(((W - tw) // 2, brand_y), brand_text, font=font_title, fill=(255, 255, 255, 255))

    sub_y = brand_y + 120
    sub_text = "G A N D H I   O I L"
    bbox = draw.textbbox((0, 0), sub_text, font=font_subtitle)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, sub_y), sub_text, font=font_subtitle, fill=(229, 169, 60, 255))

    # Ribbon
    ribbon_y = sub_y + 105
    ribbon_h = 100
    ribbon_rect = [pad_x + 60, ribbon_y, W - pad_x - 60, ribbon_y + ribbon_h]
    draw.rounded_rectangle(ribbon_rect, radius=24, fill=(229, 169, 60, 255), outline=(255, 220, 120, 255), width=4)
    tagline = "LIQUID GOLD FOR EVERY ENGINE."
    bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((W - tw) // 2, ribbon_y + (ribbon_h - th) // 2 - 8), tagline, font=font_tagline, fill=(18, 20, 24, 255))

    # Product Spec Text
    spec_y = ribbon_y + ribbon_h + 50
    spec_text = p["spec_text"]
    bbox = draw.textbbox((0, 0), spec_text, font=font_spec)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2 + 4, spec_y + 4), spec_text, font=font_spec, fill=(0, 0, 0, 180))
    draw.text(((W - tw) // 2, spec_y), spec_text, font=font_spec, fill=(255, 204, 51, 255))

    spec_sub_y = spec_y + 145
    spec_sub = p["spec_sub"]
    bbox = draw.textbbox((0, 0), spec_sub, font=font_body)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, spec_sub_y), spec_sub, font=font_body, fill=(235, 240, 250, 255))

    spec_sub2_y = spec_sub_y + 60
    spec_sub2 = p["spec_desc"]
    bbox = draw.textbbox((0, 0), spec_sub2, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, spec_sub2_y), spec_sub2, font=font_small, fill=(180, 190, 210, 255))

    # 3 Badges
    badge_row_y = spec_sub2_y + 80
    badge_w = 460
    badge_h = 105
    start_bx = pad_x + 90
    gap_bx = ((W - pad_x * 2 - 180) - (badge_w * 3)) // 2

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

    # Footer
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
    draw.line([(pad_x + 60, reg_y), (W - pad_x - 60, reg_y)], fill=(80, 90, 110, 255), width=2)
    draw.text((pad_x + 120, reg_y + 24), "ISO 9001 / API CERTIFIED FORMULATION · RECYCLE HDPE (2)", font=font_small, fill=(150, 160, 180, 255))

    # Save label directly in natural orientation (unrotated, unmirrored)
    # Three.js Texture flipY = false will render this 100% upright and unmirrored on the 3D can
    out_file = ASSETS_DIR / p["filename"]
    img.save(str(out_file), "PNG", quality=100)
    print(f"[+] Generated normal upright & unmirrored product label: {out_file.name}")

print("[*] All product labels successfully created.")
