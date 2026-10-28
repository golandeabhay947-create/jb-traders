"""Publish the homepage GLB and generate the embedded product-label texture bundle."""

import base64
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR / "assets"
OUT_JS = ASSETS_DIR / "can_data.js"
SOURCE_ASSETS_DIR = SCRIPT_DIR / "source" / "assets"
SOURCE_OUT_JS = SOURCE_ASSETS_DIR / "can_data.js"
MODEL_SOURCE = SOURCE_ASSETS_DIR / "jb_traders_can_model_new.glb"
MODEL_PUBLIC = ASSETS_DIR / "jb_traders_can_model_new.glb"

if not MODEL_SOURCE.is_file():
    raise FileNotFoundError(f"New 3D model not found: {MODEL_SOURCE}")

shutil.copyfile(MODEL_SOURCE, MODEL_PUBLIC)

product_keys = ["2wheeler", "3wheeler", "4wheeler", "jcb", "tractor", "industrial"]
textures = {}

for k in product_keys:
    p_path = ASSETS_DIR / f"label_{k}.png"
    if p_path.exists():
        p_bytes = p_path.read_bytes()
        p_b64 = base64.b64encode(p_bytes).decode("ascii")
        textures[k] = f"data:image/png;base64,{p_b64}"
    else:
        print(f"Warning: {p_path} not found")

js_lines = [
    "// Auto-generated product texture bundle for J B TRADERS (GANDHI OIL)",
    "window.JB_PRODUCT_TEXTURES = {"
]

for k, uri in textures.items():
    js_lines.append(f"  '{k}': '{uri}',")

js_lines.append("};")
js_lines.append("console.log('[+] J B TRADERS 3D Assets bundle loaded successfully.');")

OUT_JS.write_text("\n".join(js_lines), encoding="utf-8")
SOURCE_OUT_JS.write_text("\n".join(js_lines), encoding="utf-8")
print(f"[+] Published 3D model: {MODEL_PUBLIC} ({MODEL_PUBLIC.stat().st_size // 1024} KB)")
print(f"[+] Successfully generated: {OUT_JS} ({OUT_JS.stat().st_size // 1024} KB)")
