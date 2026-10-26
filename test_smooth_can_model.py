"""
Test script for 100% smooth finishing on the 3D can:
- Rounded organic side walls with 135-deg corner loops
- Ergonomic finger recess on reservoir inner wall (dy=0.32)
- Arched saddle at top and bottom of handle hole
- Oval handle profile
- Studio lighting & rendering user perspective
"""

import bpy
import bmesh
import math
from pathlib import Path

OUT_DIR = Path("d:/QuickBite - Sinhagad/jbj")
RENDER_USER = OUT_DIR / "smooth_side_user_angle.png"
RENDER_RIGHT = OUT_DIR / "smooth_side_right_angle.png"
RENDER_PERSP = OUT_DIR / "smooth_side_persp_angle.png"

bpy.ops.wm.read_factory_settings(use_empty=True)

# 11 height levels Z
grid_z = [
    0.00,  # L0: Base
    0.15,  # L1: Base chamfer
    0.70,  # L2: Lower body
    1.15,  # L3: Handle root transition
    1.40,  # L4: Hole bottom apex
    1.68,  # L5: Scallop 1
    1.96,  # L6: Scallop 2
    2.24,  # L7: Scallop 3
    2.48,  # L8: Hole top apex / Scallop 4
    2.68,  # L9: Shoulder slope
    2.85,  # L10: Handle crest
]

# 6 Primary X columns
grid_x = [
    [-0.95, -0.60, -0.25, 0.15, 0.55, 0.95],
    [-1.00, -0.62, -0.25, 0.15, 0.58, 0.98],
    [-1.02, -0.62, -0.25, 0.15, 0.60, 1.00],
    [-1.08, -0.75, -0.58, -0.25, 0.55, 0.98],
    [-1.14, -0.86, -0.68, -0.32, 0.52, 0.96],
    [-1.20, -0.96, -0.78, -0.35, 0.48, 0.95],
    [-1.18, -0.95, -0.80, -0.35, 0.46, 0.94],
    [-1.12, -0.90, -0.76, -0.34, 0.44, 0.90],
    [-0.98, -0.78, -0.52, -0.32, 0.44, 0.82],
    [-0.78, -0.52, -0.22, 0.08, 0.46, 0.72],
    [-0.72, -0.46, -0.16, 0.12, 0.52, 0.68],
]

def get_depth_y(row, col):
    if row <= 2:
        if col == 0 or col == 5:
            return 0.52
        elif col == 1 or col == 4:
            return 0.64
        else:
            return 0.68
    elif row == 3:
        if col <= 2:
            return 0.26 if col == 2 else 0.36
        else:
            return 0.45 if col == 3 else (0.54 if col == 5 else 0.66)
    elif 4 <= row <= 8:
        if col <= 2:
            return 0.16 if (col == 0 or col == 2) else 0.22
        else:
            # Ergonomic finger scoop recess at col 3 (facing hole)
            if col == 3:
                return 0.30
            elif col == 4:
                return 0.64
            else:
                return 0.50
    else: # row 9, 10
        if col <= 2:
            return 0.18
        else:
            if col == 3:
                return 0.35
            elif col == 4:
                return 0.52
            else:
                return 0.44

mesh_data = bpy.data.meshes.new("Smooth_Can_Mesh")
bm = bmesh.new()

num_rows = len(grid_z)
num_cols = 6

front_verts = {}
back_verts = {}

for r in range(num_rows):
    z = grid_z[r]
    for c in range(num_cols):
        x = grid_x[r][c]
        dy = get_depth_y(r, c)
        front_verts[(r, c)] = bm.verts.new((x, -dy, z))
        back_verts[(r, c)] = bm.verts.new((x, dy, z))

# 1. Front and Back Faces
for r in range(num_rows - 1):
    for c in range(num_cols - 1):
        if (4 <= r <= 7) and c == 2:
            continue
        v00_f = front_verts[(r, c)]
        v01_f = front_verts[(r, c + 1)]
        v11_f = front_verts[(r + 1, c + 1)]
        v10_f = front_verts[(r + 1, c)]

        v00_b = back_verts[(r, c)]
        v01_b = back_verts[(r, c + 1)]
        v11_b = back_verts[(r + 1, c + 1)]
        v10_b = back_verts[(r + 1, c)]

        bm.faces.new((v00_f, v01_f, v11_f, v10_f))
        bm.faces.new((v10_b, v11_b, v01_b, v00_b))

# 2. Bottom and Top Perimeter Walls
for c in range(num_cols - 1):
    bm.faces.new((front_verts[(0, c)], back_verts[(0, c)], back_verts[(0, c + 1)], front_verts[(0, c + 1)]))
for c in range(num_cols - 1):
    bm.faces.new((front_verts[(10, c)], front_verts[(10, c + 1)], back_verts[(10, c + 1)], back_verts[(10, c)]))

# 3. Outer Left Wall (Handle Spine) - 2 segments in depth for rounded oval spine
spine_left_verts = {}
for r in range(num_rows):
    x = grid_x[r][0] - 0.08  # slight outward bulge
    z = grid_z[r]
    spine_left_verts[r] = bm.verts.new((x, 0.0, z))

for r in range(num_rows - 1):
    # Front-to-Spine quad
    bm.faces.new((front_verts[(r, 0)], front_verts[(r + 1, 0)], spine_left_verts[r + 1], spine_left_verts[r]))
    # Spine-to-Back quad
    bm.faces.new((spine_left_verts[r], spine_left_verts[r + 1], back_verts[(r + 1, 0)], back_verts[(r, 0)]))

# 4. Outer Right Wall (Reservoir Wall) - 2 segments in depth for rounded side wall
spine_right_verts = {}
for r in range(num_rows):
    x = grid_x[r][5] + 0.06  # slight outward convex curve
    z = grid_z[r]
    spine_right_verts[r] = bm.verts.new((x, 0.0, z))

for r in range(num_rows - 1):
    # Front-to-Spine quad
    bm.faces.new((front_verts[(r, 5)], spine_right_verts[r], spine_right_verts[r + 1], front_verts[(r + 1, 5)]))
    # Spine-to-Back quad
    bm.faces.new((spine_right_verts[r], back_verts[(r, 5)], back_verts[(r + 1, 5)], spine_right_verts[r + 1]))

# 4 Corner caps for spine endpoints (keeps mesh 100% closed & manifold)
bm.faces.new((front_verts[(0, 0)], spine_left_verts[0], back_verts[(0, 0)]))
bm.faces.new((front_verts[(0, 5)], back_verts[(0, 5)], spine_right_verts[0]))
bm.faces.new((front_verts[(10, 0)], back_verts[(10, 0)], spine_left_verts[10]))
bm.faces.new((front_verts[(10, 5)], spine_right_verts[10], back_verts[(10, 5)]))

# 5. Inner Handle Hole Walls - Smooth organic contoured tunnel
# Inner handle wall (facing hole at col 2)
spine_inner_handle = {}
for r in range(4, 9):
    x = grid_x[r][2] + 0.06
    z = grid_z[r]
    # Saddle arch at apexes:
    if r == 4:
        z += 0.06  # curve upward at bottom apex
    elif r == 8:
        z -= 0.06  # curve downward at top apex
    spine_inner_handle[r] = bm.verts.new((x, 0.0, z))

for r in range(4, 8):
    bm.faces.new((front_verts[(r, 2)], front_verts[(r + 1, 2)], spine_inner_handle[r + 1], spine_inner_handle[r]))
    bm.faces.new((spine_inner_handle[r], spine_inner_handle[r + 1], back_verts[(r + 1, 2)], back_verts[(r, 2)]))

# Inner reservoir wall (facing hole at col 3) - Concave finger clearance curve
spine_inner_res = {}
for r in range(4, 9):
    # Organic concave sweep
    x_offset = -0.02 if (r == 5 or r == 6 or r == 7) else -0.06
    x = grid_x[r][3] + x_offset
    z = grid_z[r]
    if r == 4:
        z -= 0.06  # U-shape dip at bottom
    elif r == 8:
        z += 0.06  # arch up at top
    spine_inner_res[r] = bm.verts.new((x, 0.0, z))

for r in range(4, 8):
    bm.faces.new((front_verts[(r, 3)], spine_inner_res[r], spine_inner_res[r + 1], front_verts[(r + 1, 3)]))
    bm.faces.new((spine_inner_res[r], back_verts[(r, 3)], back_verts[(r + 1, 3)], spine_inner_res[r + 1]))

# Hole bottom floor (row 4): arched U-saddle transition dipping down smoothly
bm.faces.new((front_verts[(4, 2)], front_verts[(4, 3)], spine_inner_res[4], spine_inner_handle[4]))
bm.faces.new((spine_inner_handle[4], spine_inner_res[4], back_verts[(4, 3)], back_verts[(4, 2)]))

# Hole top ceiling (row 8): arched ceiling transition arching up smoothly
bm.faces.new((front_verts[(8, 2)], spine_inner_handle[8], spine_inner_res[8], front_verts[(8, 3)]))
bm.faces.new((spine_inner_handle[8], back_verts[(8, 2)], back_verts[(8, 3)], spine_inner_res[8]))

# UV unwrap
uv_layer = bm.loops.layers.uv.verify()
x_min, x_max = -0.32, 0.98
z_min, z_max = 0.15, 2.65

for face in bm.faces:
    is_front = all(v.co.y < -0.10 for v in face.verts)
    in_reservoir = any(v.co.x > -0.35 for v in face.verts)
    for loop in face.loops:
        v = loop.vert
        if is_front and in_reservoir:
            u = (v.co.x - x_min) / (x_max - x_min)
            v_coord = (v.co.z - z_min) / (z_max - z_min)
            u = max(0.005, min(0.995, u))
            v_coord = max(0.005, min(0.995, v_coord))
            loop[uv_layer].uv = (u, v_coord)
        else:
            loop[uv_layer].uv = (0.02, 0.02)

bm.to_mesh(mesh_data)
bm.free()

obj = bpy.data.objects.new("Smooth_Can_Body", mesh_data)
bpy.context.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj

# Apply Subsurf
sub = obj.modifiers.new("Subsurf", "SUBSURF")
sub.levels = 2
sub.render_levels = 2

for p in obj.data.polygons:
    p.use_smooth = True

# Spout
bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=0.20, depth=0.32, location=(0.52, 0, 2.92))
spout = bpy.context.active_object
spout.name = "Spout"
for p in spout.data.polygons:
    p.use_smooth = True

# Cap
bpy.ops.mesh.primitive_cylinder_add(vertices=72, radius=0.235, depth=0.26, location=(0.52, 0, 3.12))
cap = bpy.context.active_object
cap.name = "Cap"
for p in cap.data.polygons:
    p.use_smooth = True

# Materials
mat_body = bpy.data.materials.new("Can_Body_Mat")
mat_body.use_nodes = True
bsdf = mat_body.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = (0.96, 0.72, 0.08, 1.0)
bsdf.inputs["Roughness"].default_value = 0.28
obj.data.materials.append(mat_body)
spout.data.materials.append(mat_body)

mat_cap = bpy.data.materials.new("Cap_Mat")
mat_cap.use_nodes = True
bsdf_cap = mat_cap.node_tree.nodes.get("Principled BSDF")
bsdf_cap.inputs["Base Color"].default_value = (0.88, 0.55, 0.02, 1.0)
bsdf_cap.inputs["Roughness"].default_value = 0.24
cap.data.materials.append(mat_cap)

# Lights
bpy.ops.object.light_add(type='AREA', location=(3.8, -5.0, 4.2))
bpy.context.active_object.data.energy = 580
bpy.ops.object.light_add(type='AREA', location=(-4.0, -3.8, 3.4))
bpy.context.active_object.data.energy = 260
bpy.ops.object.light_add(type='SPOT', location=(-4.8, 3.8, 4.0))
bpy.context.active_object.data.energy = 850

# Camera
bpy.ops.object.camera_add(location=(-6.5, 0.4, 1.7), rotation=(math.radians(90), 0, math.radians(-85)))
cam = bpy.context.active_object
cam.data.lens = 55
bpy.context.scene.camera = cam

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 720
bpy.context.scene.render.resolution_y = 1080

# 1. User screenshot side view
bpy.context.scene.render.filepath = str(RENDER_USER)
bpy.ops.render.render(write_still=True)
print(f"[+] Rendered: {RENDER_USER}")

# 2. Right reservoir side view
cam.location = (6.5, 0.0, 1.7)
cam.rotation_euler = (math.radians(90), 0, math.radians(90))
bpy.context.scene.render.filepath = str(RENDER_RIGHT)
bpy.ops.render.render(write_still=True)
print(f"[+] Rendered: {RENDER_RIGHT}")

# 3. Perspective view
cam.location = (-4.5, -4.5, 3.0)
cam.rotation_euler = (math.radians(65), 0, math.radians(-45))
bpy.context.scene.render.filepath = str(RENDER_PERSP)
bpy.ops.render.render(write_still=True)
print(f"[+] Rendered: {RENDER_PERSP}")

print("=== ALL RENDERS COMPLETED SUCCESSFULLY ===")
