"""
Mirrors and enhances jb_traders_can_model.glb to match the reference image:
- Spout and yellow cylindrical screw cap on the LEFT (translation X = -0.52)
- Ergonomic molded handle with finger grips on the RIGHT (X > 0)
- Front recessed label reservoir on the LEFT / CENTER (X in [-0.98, 0.32])
- Proper outward triangle winding and inverted normal vectors
- Updated golden-yellow HDPE plastic PBR materials matching Image 1
- Dual UV mapping for Left (Front) and Right (Back) labels
"""

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IN_GLB = ROOT / "assets" / "jb_traders_can_model.glb"

with open(IN_GLB, "rb") as f:
    magic, version, length = struct.unpack("<4sII", f.read(12))
    chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
    gltf_json = json.loads(f.read(chunk_len).decode("utf-8"))
    
    bin_len, bin_type = struct.unpack("<I4s", f.read(8))
    bin_data = bytearray(f.read(bin_len))

print(f"[+] Loaded GLB: JSON len={chunk_len}, BIN len={bin_len}")

# 1. Update Nodes: mirror translation for Can_Cap and Can_Spout
for node in gltf_json["nodes"]:
    if "translation" in node:
        t = node["translation"]
        node["translation"] = [-t[0], t[1], t[2]]
        print(f"  Node {node.get('name')}: translation mirrored to {node['translation']}")

# 2. Update Materials: golden-yellow HDPE plastic
# Material 0: Cap
gltf_json["materials"][0]["pbrMetallicRoughness"]["baseColorFactor"] = [0.96, 0.72, 0.08, 1.0]
gltf_json["materials"][0]["pbrMetallicRoughness"]["roughnessFactor"] = 0.26
gltf_json["materials"][0]["pbrMetallicRoughness"]["metallicFactor"] = 0.02

# Material 1: Spout
gltf_json["materials"][1]["pbrMetallicRoughness"]["baseColorFactor"] = [0.96, 0.72, 0.08, 1.0]
gltf_json["materials"][1]["pbrMetallicRoughness"]["roughnessFactor"] = 0.28
gltf_json["materials"][1]["pbrMetallicRoughness"]["metallicFactor"] = 0.0

# Material 2: Can Body
gltf_json["materials"][2]["pbrMetallicRoughness"]["roughnessFactor"] = 0.28
gltf_json["materials"][2]["pbrMetallicRoughness"]["metallicFactor"] = 0.0

# Helper to mirror a mesh's positions, normals, and invert index winding
def mirror_mesh_primitive(prim_idx, mesh_name):
    prim = gltf_json["meshes"][prim_idx]["primitives"][0]
    
    # 1. Mirror POSITION (X -> -X)
    pos_acc = gltf_json["accessors"][prim["attributes"]["POSITION"]]
    pos_bv = gltf_json["bufferViews"][pos_acc["bufferView"]]
    pos_off = pos_bv["byteOffset"] + pos_acc.get("byteOffset", 0)
    v_count = pos_acc["count"]
    
    for i in range(v_count):
        idx = pos_off + i * 12
        x, y, z = struct.unpack_from("<3f", bin_data, idx)
        struct.pack_into("<3f", bin_data, idx, -x, y, z)
        
    # Update min/max in accessor
    if "min" in pos_acc and "max" in pos_acc:
        old_min_x = pos_acc["min"][0]
        old_max_x = pos_acc["max"][0]
        pos_acc["min"][0] = -old_max_x
        pos_acc["max"][0] = -old_min_x
        
    # 2. Mirror NORMAL (Nx -> -Nx)
    norm_acc = gltf_json["accessors"][prim["attributes"]["NORMAL"]]
    norm_bv = gltf_json["bufferViews"][norm_acc["bufferView"]]
    norm_off = norm_bv["byteOffset"] + norm_acc.get("byteOffset", 0)
    for i in range(v_count):
        idx = norm_off + i * 12
        nx, ny, nz = struct.unpack_from("<3f", bin_data, idx)
        struct.pack_into("<3f", bin_data, idx, -nx, ny, nz)
        
    # 3. Invert triangle index winding (i0, i1, i2) -> (i0, i2, i1) to preserve outward normal direction
    ind_acc = gltf_json["accessors"][prim["indices"]]
    ind_bv = gltf_json["bufferViews"][ind_acc["bufferView"]]
    ind_off = ind_bv["byteOffset"] + ind_acc.get("byteOffset", 0)
    i_count = ind_acc["count"]
    comp_type = ind_acc["componentType"]
    
    if comp_type == 5123: # UNSIGNED_SHORT
        for t in range(0, i_count, 3):
            b_idx = ind_off + t * 2
            i0, i1, i2 = struct.unpack_from("<3H", bin_data, b_idx)
            struct.pack_into("<3H", bin_data, b_idx, i0, i2, i1)
    elif comp_type == 5125: # UNSIGNED_INT
        for t in range(0, i_count, 3):
            b_idx = ind_off + t * 4
            i0, i1, i2 = struct.unpack_from("<3I", bin_data, b_idx)
            struct.pack_into("<3I", bin_data, b_idx, i0, i2, i1)
            
    print(f"[+] Primitive {mesh_name}: mirrored {v_count} vertices and inverted {i_count // 3} triangles")

# Mirror mesh 0 (Cap), mesh 1 (Spout), mesh 2 (Can Body)
mirror_mesh_primitive(0, "Can_Cap")
mirror_mesh_primitive(1, "Can_Spout")
mirror_mesh_primitive(2, "JB_Traders_Can_Body")

# 4. Now update UV mapping for JB_Traders_Can_Body (Mesh 2)
prim_body = gltf_json["meshes"][2]["primitives"][0]
pos_acc = gltf_json["accessors"][prim_body["attributes"]["POSITION"]]
pos_bv = gltf_json["bufferViews"][pos_acc["bufferView"]]
pos_off = pos_bv["byteOffset"] + pos_acc.get("byteOffset", 0)
v_count = pos_acc["count"]

tc_acc = gltf_json["accessors"][prim_body["attributes"]["TEXCOORD_0"]]
tc_bv = gltf_json["bufferViews"][tc_acc["bufferView"]]
tc_off = tc_bv["byteOffset"] + tc_acc.get("byteOffset", 0)

# With mirrored X, reservoir is at X in [-0.98, 0.32], Y in [0.15, 2.65]
x_min, x_max = -0.98, 0.32
y_min, y_max = 0.15, 2.65

front_mapped = 0
back_mapped = 0

for i in range(v_count):
    p_idx = pos_off + i * 12
    x, y, z = struct.unpack_from("<3f", bin_data, p_idx)
    t_idx = tc_off + i * 8
    
    is_front = (z > 0.30) and (x >= x_min - 0.05) and (x <= x_max + 0.05)
    is_back = (z < -0.30) and (x >= x_min - 0.05) and (x <= x_max + 0.05)
    
    if is_front:
        u_raw = (x - x_min) / (x_max - x_min)
        u_norm = max(0.0, min(1.0, u_raw))
        v_raw = (y - y_min) / (y_max - y_min)
        v_norm = max(0.0, min(1.0, v_raw))
        
        # Left half: [0.03, 0.47] for U, [0.08, 0.92] for V
        u_final = 0.03 + u_norm * (0.47 - 0.03)
        v_final = 0.08 + v_norm * (0.92 - 0.08)
        struct.pack_into("<2f", bin_data, t_idx, u_final, v_final)
        front_mapped += 1
    elif is_back:
        # For back label: when viewing from behind, +X is viewer's left, -X is viewer's right
        u_raw = 1.0 - ((x - x_min) / (x_max - x_min))
        u_norm = max(0.0, min(1.0, u_raw))
        v_raw = (y - y_min) / (y_max - y_min)
        v_norm = max(0.0, min(1.0, v_raw))
        
        # Right half: [0.53, 0.97] for U, [0.08, 0.92] for V
        u_final = 0.53 + u_norm * (0.97 - 0.53)
        v_final = 0.08 + v_norm * (0.92 - 0.08)
        struct.pack_into("<2f", bin_data, t_idx, u_final, v_final)
        back_mapped += 1
    else:
        # Pure yellow margin coordinate (neutral area)
        struct.pack_into("<2f", bin_data, t_idx, 0.25, 0.005)

print(f"[+] UV mapping completed: {front_mapped} front reservoir vertices, {back_mapped} back reservoir vertices")

# 5. Assemble and save the updated GLB
json_bytes = json.dumps(gltf_json, separators=(',', ':')).encode("utf-8")
pad_len = (4 - (len(json_bytes) % 4)) % 4
json_bytes += b' ' * pad_len
new_json_chunk_len = len(json_bytes)

# Binary chunk padding
bin_pad = (4 - (len(bin_data) % 4)) % 4
bin_data.extend(b'\x00' * bin_pad)
new_bin_chunk_len = len(bin_data)

total_length = 12 + 8 + new_json_chunk_len + 8 + new_bin_chunk_len

header = struct.pack("<4sII", b"glTF", 2, total_length)
json_chunk_header = struct.pack("<I4s", new_json_chunk_len, b"JSON")
bin_chunk_header = struct.pack("<I4s", new_bin_chunk_len, b"BIN\x00")

final_glb = header + json_chunk_header + json_bytes + bin_chunk_header + bytes(bin_data)

# Save to assets and source/assets
OUT_PATHS = [
    ROOT / "assets" / "jb_traders_can_model.glb",
    ROOT / "source" / "assets" / "jb_traders_can_model.glb"
]

for p in OUT_PATHS:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(final_glb)
    print(f"[+] Saved updated GLB to {p} ({len(final_glb)} bytes)")

print("=== CAN MODEL GENERATION COMPLETED SUCCESSFULLY ===")
