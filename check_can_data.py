from pathlib import Path
import base64

SCRIPT_DIR = Path(__file__).resolve().parent
js_path = SCRIPT_DIR / "assets" / "can_data.js"
content = js_path.read_text(encoding="utf-8")
print("can_data.js length:", len(content))

prefix = "window.JB_CAN_MODEL_B64 = '"
idx = content.find(prefix)
if idx != -1:
    end_idx = content.find("';", idx)
    uri = content[idx + len(prefix):end_idx]
    print("URI start:", uri[:60])
    b64_part = uri.split(",")[1]
    raw_glb = base64.b64decode(b64_part)
    print("Decoded GLB bytes:", len(raw_glb))
    magic = raw_glb[:4]
    print("Magic header:", magic)
    if magic == b"glTF":
        print("[+] Valid glTF binary header!")
        import struct, json
        chunk_len, chunk_type = struct.unpack('<II', raw_glb[12:20])
        gltf = json.loads(raw_glb[20 : 20 + chunk_len].decode('utf-8'))
        for i, node in enumerate(gltf.get('nodes', [])):
            print(f"Node {i}: {node.get('name')}")
    else:
        print("[-] Invalid magic header:", magic)
else:
    print("[-] window.JB_CAN_MODEL_B64 not found!")

html_path = SCRIPT_DIR / "index.html"
print("index.html size:", html_path.stat().st_size)
