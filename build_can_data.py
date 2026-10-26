"""
Builds assets/can_data.js with embedded Base64 Data URIs for:
- 3D J B Traders 5L Can model (GLB)
- Product labels (2wheeler, 3wheeler, 4wheeler, jcb, tractor, industrial)
This allows index.html to load the authentic 3D can over file:/// protocol without CORS restriction!
"""

import base64
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = SCRIPT_DIR / "assets"
OUT_JS = ASSETS_DIR / "can_data.js"

glb_path = ASSETS_DIR / "jb_traders_can_model.glb"
glb_bytes = glb_path.read_bytes()
glb_b64 = base64.b64encode(glb_bytes).decode("ascii")
glb_data_uri = f"data:model/gltf-binary;base64,{glb_b64}"

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
    "// Auto-generated 3D Asset Bundle for J B TRADERS (GANDHI OIL)",
    "// Guarantees 100% offline & file:/// protocol execution with zero CORS errors",
    f"window.JB_CAN_MODEL_B64 = '{glb_data_uri}';",
    "window.JB_PRODUCT_TEXTURES = {"
]

for k, uri in textures.items():
    js_lines.append(f"  '{k}': '{uri}',")

js_lines.append("};")
js_lines.append("console.log('[+] J B TRADERS 3D Assets bundle loaded successfully.');")

OUT_JS.write_text("\n".join(js_lines), encoding="utf-8")
print(f"[+] Successfully generated: {OUT_JS} ({OUT_JS.stat().st_size // 1024} KB)")
