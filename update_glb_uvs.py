"""
Updates UV coordinates in jb_traders_can_model.glb to support dual Front & Back labels.
- Front labeled vertices: U in [0.0, 0.50]
- Back reservoir vertices: U in [0.50, 1.00] (flipped horizontally so text reads correctly)
- All other vertices: U = 0.25, V = 0.005 (neutral HDPE yellow)
"""

import json
import struct
from pathlib import Path

def update_glb(glb_path):
    glb_path = Path(glb_path)
    with open(glb_path, 'rb') as f:
        magic, ver, total_len = struct.unpack('<4sII', f.read(12))
        chunk0_len, chunk0_type = struct.unpack('<I4s', f.read(8))
        gltf = json.loads(f.read(chunk0_len).decode('utf-8'))
        chunk1_len, chunk1_type = struct.unpack('<I4s', f.read(8))
        bin_data = bytearray(f.read(chunk1_len))

    mesh = gltf['meshes'][2]['primitives'][0]
    pos_acc = gltf['accessors'][mesh['attributes']['POSITION']]
    uv_acc = gltf['accessors'][mesh['attributes']['TEXCOORD_0']]
    pos_bv = gltf['bufferViews'][pos_acc['bufferView']]
    uv_bv = gltf['bufferViews'][uv_acc['bufferView']]

    pos_offset = pos_bv.get('byteOffset', 0) + pos_acc.get('byteOffset', 0)
    uv_offset = uv_bv.get('byteOffset', 0) + uv_acc.get('byteOffset', 0)

    count = pos_acc['count']
    positions = [struct.unpack_from('<3f', bin_data, pos_offset + i*12) for i in range(count)]
    uvs = [struct.unpack_from('<2f', bin_data, uv_offset + i*8) for i in range(count)]

    front_labeled = [i for i, (p, uv) in enumerate(zip(positions, uvs)) if uv[0] > 0.05 or uv[1] < 0.95]

    pairs = {}
    for fi in front_labeled:
        fp = positions[fi]
        found = None
        for bi, bp in enumerate(positions):
            if abs(bp[0] - fp[0]) < 0.02 and abs(bp[1] - fp[1]) < 0.02 and abs(bp[2] + fp[2]) < 0.02:
                found = bi
                break
        if found is not None:
            pairs[fi] = found

    print(f"Matched {len(pairs)} / {len(front_labeled)} front/back vertex pairs in {glb_path.name}")

    # Pack new UVs into binary buffer
    for i in range(count):
        if i in pairs:
            # Front vertex
            u_f, v_f = uvs[i]
            u_new = u_f * 0.50
            v_new = v_f
        elif i in pairs.values():
            # Back vertex: find its front counterpart
            fi = [k for k, v in pairs.items() if v == i][0]
            u_f, v_f = uvs[fi]
            # When looking from back, horizontal axis is reversed so text reads left to right:
            u_new = 0.50 + (1.0 - u_f) * 0.50
            v_new = v_f
        else:
            # Neutral yellow HDPE area in top margin
            u_new = 0.25
            v_new = 0.005

        struct.pack_into('<2f', bin_data, uv_offset + i*8, u_new, v_new)

    # Reconstruct GLB
    json_bytes = json.dumps(gltf, separators=(',', ':')).encode('utf-8')
    # Pad JSON to 4-byte alignment with spaces
    while len(json_bytes) % 4 != 0:
        json_bytes += b' '

    # Pad binary data to 4-byte alignment
    while len(bin_data) % 4 != 0:
        bin_data += b'\x00'

    total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_data)

    with open(glb_path, 'wb') as f:
        f.write(struct.pack('<4sII', magic, ver, total_length))
        f.write(struct.pack('<I4s', len(json_bytes), b'JSON'))
        f.write(json_bytes)
        f.write(struct.pack('<I4s', len(bin_data), b'BIN\x00'))
        f.write(bin_data)

    print(f"[+] Successfully updated UV mapping in {glb_path} ({total_length} bytes)")

update_glb("assets/jb_traders_can_model.glb")
if Path("source/assets/jb_traders_can_model.glb").exists():
    update_glb("source/assets/jb_traders_can_model.glb")
