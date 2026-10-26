"""
Test script to reproduce the exact side profile view from the user's screenshot
and test smooth organic fillets/bevels on the can sides.
"""

import bpy
import bmesh
import math
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RENDER_SIDE_PATH = SCRIPT_DIR / "side_profile_test.png"

bpy.ops.wm.read_factory_settings(use_empty=True)

# Load existing jb_traders_can_studio.blend to see current side profile
blend_path = Path("d:/QuickBite - Sinhagad/jarvislabs/can-3d/jb_traders_can_studio.blend")
if blend_path.exists():
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))

# Set camera to the exact side view shown in user's screenshot (looking at handle and side)
cam = bpy.data.objects.get("Camera")
if not cam:
    bpy.ops.object.camera_add()
    cam = bpy.context.active_object
    bpy.context.scene.camera = cam

cam.location = (-6.5, 0.4, 1.7)
cam.rotation_euler = (math.radians(90), 0, math.radians(-85))
cam.data.lens = 55

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 720
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = str(RENDER_SIDE_PATH)

bpy.ops.render.render(write_still=True)
print(f"[+] Rendered side profile test: {RENDER_SIDE_PATH}")
