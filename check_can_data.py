from pathlib import Path
import base64

js_path = Path("d:/QuickBite - Sinhagad/jbj/assets/can_data.js")
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
    # Check magic header: glTF binary begins with 0x46546C67 ("glTF")
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

html_path = Path("d:/QuickBite - Sinhagad/jbj/index.html")
print("index.html size:", html_path.stat().st_size)

source_path = Path("d:/QuickBite - Sinhagad/jbj/source/index.source.html")
raw = source_path.read_text(encoding="utf-8")
tag = '<script type="module">'
s = raw.find(tag)
print("Tag length:", len(tag))
print("Slice +22:", repr(raw[s+22:s+45]))
print("Slice +len(tag):", repr(raw[s+len(tag):s+len(tag)+25]))
