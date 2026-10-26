import zlib
import base64
import json
from pathlib import Path

html = Path("d:/QuickBite - Sinhagad/jbj/index.html").read_text(encoding="utf-8")
prefix = "})('"
p_start = html.rfind(prefix)
if p_start != -1:
    p_end = html.rfind("');")
    b64_payload = html[p_start + len(prefix) : p_end]
    compressed = base64.b64decode(b64_payload)
    json_str = zlib.decompress(compressed).decode("utf-8")
    data = json.loads(json_str)

    js = data["j"]
    print("JS length:", len(js))
    print("Has selectProduct:", "window.selectProduct" in js)
    print("Has triggerCanSpin:", "window.triggerCanSpin" in js)
    print("Has handleFormSubmit:", "window.handleFormSubmit" in js)
    print("Has init:", "function init()" in js)
    print("Start of JS:", repr(js[:120]))
    print("End of JS:", repr(js[-120:]))
else:
    print("Prefix not found!")
