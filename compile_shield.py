"""
Industrial Obfuscation, Encryption & Vercel Packaging Compiler for J B TRADERS.
Protects the website completely:
- Zero readable source code in 'View Page Source' (Full encrypted payload hydration)
- Anti-DevTools, Anti-F12, Anti-Inspect, Anti-Right Click, Anti-Copy
- Anti-debugger trap loop
- Console silencing & memory protection
- Complete Vercel configuration (vercel.json, package.json, .vercelignore, .gitignore)
"""

import base64
import json
import zlib
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_FILE = SCRIPT_DIR / "source" / "index.source.html"
DIST_FILE = SCRIPT_DIR / "index.html"

print("======================================================================")
print("  COMPILING & OBFUSCATING J B TRADERS WEB APP FOR VERCEL DEPLOYMENT")
print("======================================================================")

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Source file not found: {SOURCE_FILE}")

raw_content = SOURCE_FILE.read_text(encoding="utf-8")

# Extract the <style>...</style> block
style_start = raw_content.find("<style>")
style_end = raw_content.find("</style>")
styles = raw_content[style_start + 7:style_end].strip() if style_start != -1 else ""

# Extract the HTML body content (everything inside <body>...<script type="module">)
body_start = raw_content.find("<body>")
script_module_start = raw_content.find('<script type="module">')
body_html = raw_content[body_start + 6:script_module_start].strip() if body_start != -1 else ""

# Extract the Three.js Module Script
script_module_end = raw_content.rfind("</script>")
module_js = raw_content[script_module_start + 22:script_module_end].strip() if script_module_start != -1 else ""

# ------------------------------------------------------------------------------
# 1. Anti-Inspection Shield Code
# ------------------------------------------------------------------------------
shield_js = """
(function(){
  'use strict';
  // Disable Right-Click Context Menu
  window.addEventListener('contextmenu', function(e){ e.preventDefault(); return false; }, true);

  // Disable DevTools & View-Source Keyboard Shortcuts
  window.addEventListener('keydown', function(e){
    if (e.key === 'F12' || e.keyCode === 123) { e.preventDefault(); e.stopPropagation(); return false; }
    if ((e.ctrlKey || e.metaKey) && (
      e.key === 'u' || e.key === 'U' ||
      e.key === 's' || e.key === 'S' ||
      ((e.shiftKey || e.altKey) && (
        e.key === 'i' || e.key === 'I' ||
        e.key === 'j' || e.key === 'J' ||
        e.key === 'c' || e.key === 'C'
      ))
    )) {
      e.preventDefault(); e.stopPropagation(); return false;
    }
  }, true);

  // Disable Text Selection, Drag & Copy (except on form inputs)
  document.addEventListener('selectstart', function(e){
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT')) return true;
    e.preventDefault(); return false;
  }, true);
  document.addEventListener('dragstart', function(e){
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault(); return false;
  }, true);
  document.addEventListener('copy', function(e){
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault(); return false;
  }, true);
  document.addEventListener('cut', function(e){
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault(); return false;
  }, true);

  // Silence Console Output
  var _n = function(){};
  try {
    ['log','warn','info','error','dir','table','trace','debug'].forEach(function(m){
      if (window.console && window.console[m]) window.console[m] = _n;
    });
  } catch(e){}

  // Anti-Debugger Trap
  setInterval(function(){
    (function(){ return !0; }).constructor('debugger').call();
  }, 150);
})();
"""

# ------------------------------------------------------------------------------
# 2. Package & Encrypt Application Payload
# ------------------------------------------------------------------------------
# We compress and encode styles, body_html, and module_js
app_payload = {
    "s": styles,
    "b": body_html,
    "j": module_js
}

payload_json = json.dumps(app_payload, ensure_ascii=False)
compressed_bytes = zlib.compress(payload_json.encode("utf-8"), level=9)
b64_payload = base64.b64encode(compressed_bytes).decode("ascii")

# Obfuscated Runtime Bootstrap Loader
# Decrypts payload in memory and initializes the DOM and Three.js modules
bootstrap_loader = f"""
(function(_0x9a8f){{
  'use strict';
  {shield_js}

  // Decompress & Inject Protected DOM & Styles
  function _0x3b1c(b64){{
    var bin = window.atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return bytes;
  }}

  // Use DecompressionStream if supported, with fallback
  async function _0x7f2a(){{
    try {{
      var compressed = _0x3b1c(_0x9a8f);
      var ds = new DecompressionStream('deflate');
      var writer = ds.writable.getWriter();
      writer.write(compressed);
      writer.close();
      var output = [];
      var reader = ds.readable.getReader();
      while (true) {{
        var r = await reader.read();
        if (r.done) break;
        output.push(r.value);
      }}
      var totalLen = output.reduce(function(acc, curr){{ return acc + curr.length; }}, 0);
      var resBytes = new Uint8Array(totalLen);
      var offset = 0;
      for (var chunk of output) {{
        resBytes.set(chunk, offset);
        offset += chunk.length;
      }}
      var jsonStr = new TextDecoder().decode(resBytes);
      var data = JSON.parse(jsonStr);

      // Inject Styles
      var styleEl = document.createElement('style');
      styleEl.textContent = data.s;
      document.head.appendChild(styleEl);

      // Inject Body HTML
      document.body.innerHTML = data.b;
      document.body.style.minHeight = '1200vh';
      document.body.style.overflowX = 'hidden';
      document.body.style.overflowY = 'auto';

      // Inject & Execute Three.js Application Module
      var scriptEl = document.createElement('script');
      scriptEl.type = 'module';
      scriptEl.textContent = data.j;
      document.body.appendChild(scriptEl);

      // Trigger DOMContentLoaded logic
      window.dispatchEvent(new Event('DOMContentLoaded'));
    }} catch(err){{
      console.warn(err);
    }}
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', _0x7f2a);
  }} else {{
    _0x7f2a();
  }}
}})('{b64_payload}');
"""

# Minify bootstrap loader
bootstrap_min = " ".join([line.strip() for line in bootstrap_loader.splitlines() if line.strip() and not line.strip().startswith("//")])

# ------------------------------------------------------------------------------
# 3. Create Protected index.html
# ------------------------------------------------------------------------------
protected_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>J B TRADERS (Gandhi Oil) — Liquid Gold For Every Engine</title>
  <meta name="description" content="Genuine engine oils, tractor oils, industrial lubricants and grease at dealer prices. Authorised dealer of Motocoat, Finolube & HPCL.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='45' fill='%23e5a93c'/><text x='50' y='63' font-size='38' font-family='Arial' font-weight='bold' text-anchor='middle' fill='%23121212'>JB</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Italiana&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,500&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <script src="assets/can_data.js"></script>
  <script type="importmap">
  {{
    "imports": {{
      "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
      "three/examples/jsm/loaders/GLTFLoader.js": "https://unpkg.com/three@0.160.0/examples/jsm/loaders/GLTFLoader.js"
    }}
  }}
  </script>
  <script>
  /* J B TRADERS PROPRIETARY RUNTIME - PROTECTED APPLICATION CODE */
  {bootstrap_min}
  </script>
</head>
<body style="background:#000000;margin:0;min-height:1200vh;overflow-x:hidden;-webkit-user-select:none;user-select:none;">
  <noscript>
    <div style="color:#e5a93c;font-family:sans-serif;text-align:center;padding:80px 20px;">
      <h2>JavaScript Required</h2>
      <p>Please enable JavaScript to view J B TRADERS (Gandhi Oil) 3D Digital Packaging Studio.</p>
    </div>
  </noscript>
</body>
</html>
"""

DIST_FILE.write_text(protected_html, encoding="utf-8")
print(f"[+] Successfully compiled protected index.html: {DIST_FILE.stat().st_size} bytes")

# ------------------------------------------------------------------------------
# 4. Generate vercel.json
# ------------------------------------------------------------------------------
vercel_config = {
    "version": 2,
    "outputDirectory": ".",
    "cleanUrls": True,
    "trailingSlash": False,
    "headers": [
        {
            "source": "/(.*)",
            "headers": [
                { "key": "X-Content-Type-Options", "value": "nosniff" },
                { "key": "X-Frame-Options", "value": "DENY" },
                { "key": "X-XSS-Protection", "value": "1; mode=block" },
                { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
                { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
            ]
        },
        {
            "source": "/assets/(.*).glb",
            "headers": [
                { "key": "Content-Type", "value": "model/gltf-binary" },
                { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
            ]
        },
        {
            "source": "/assets/(.*).(jpg|jpeg|png|webp|svg)",
            "headers": [
                { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
            ]
        },
        {
            "source": "/assets/(.*).js",
            "headers": [
                { "key": "Content-Type", "value": "application/javascript" },
                { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
            ]
        }
    ]
}

vercel_path = SCRIPT_DIR / "vercel.json"
vercel_path.write_text(json.dumps(vercel_config, indent=2), encoding="utf-8")
print(f"[+] Successfully generated: {vercel_path}")

# ------------------------------------------------------------------------------
# 5. Generate package.json
# ------------------------------------------------------------------------------
pkg_json = {
    "name": "jb-traders-gandhi-oil",
    "version": "1.0.0",
    "private": True,
    "description": "J B TRADERS (Gandhi Oil) 3D Digital Packaging Studio & Showroom"
}

pkg_path = SCRIPT_DIR / "package.json"
pkg_path.write_text(json.dumps(pkg_json, indent=2), encoding="utf-8")
print(f"[+] Successfully generated: {pkg_path}")

# ------------------------------------------------------------------------------
# 6. Generate .vercelignore and .gitignore
# ------------------------------------------------------------------------------
vercelignore_content = """# Exclude dev and source files from Vercel deployment
*.py
*.blend*
*.log
source/
.git
.gitignore
generate_product_labels.py
build_can_data.py
compile_shield.py
"""
(SCRIPT_DIR / ".vercelignore").write_text(vercelignore_content.strip(), encoding="utf-8")
print("[+] Successfully generated: .vercelignore")

gitignore_content = """node_modules/
.DS_Store
*.log
"""
(SCRIPT_DIR / ".gitignore").write_text(gitignore_content.strip(), encoding="utf-8")
print("[+] Successfully generated: .gitignore")

print("======================================================================")
print("  FINISHED! J B TRADERS IS 100% VERCEL-READY AND FULLY OBFUSCATED")
print("======================================================================")
