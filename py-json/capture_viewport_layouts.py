import json
import os
import subprocess
import sys
import bpy
from mathutils import Vector

ROOT_DIR = "/Users/jinhojung/Desktop/블렌더 조명 애드온"
PY_JSON_DIR = os.path.join(ROOT_DIR, "py-json")
LAYOUTS_DIR = os.path.join(ROOT_DIR, "Preview", "layouts")
os.makedirs(LAYOUTS_DIR, exist_ok=True)

sys.path.insert(0, PY_JSON_DIR)
import simple_light
from simple_light import builder

simple_light.register()
bpy.ops.simple_light.create_demo(preset='05_hard')
scene = bpy.context.scene
scene.render.resolution_x = 1200
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

# Select nothing so ground plane doesn't have an orange selection outline
for o in scene.objects:
    o.select_set(False)
if "SL Ground" in scene.objects:
    scene.objects["SL Ground"].scale = (0.08, 0.08, 1.0)  # 16x16m in viewport so it looks like a studio stage

data = builder.load_presets_data()
layout_records = []

for window in bpy.context.window_manager.windows:
    window.scene = scene
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces.active
            space.show_region_ui = False
            space.show_region_toolbar = False
            space.overlay.show_overlays = True
            space.overlay.show_text = True
            space.overlay.show_extras = True
            space.overlay.show_floor = True
            space.overlay.show_axis_x = True
            space.overlay.show_axis_y = True
            space.overlay.show_cursor = False
            space.overlay.show_relationship_lines = False
            space.shading.type = 'SOLID'
            space.shading.light = 'STUDIO'
            space.shading.color_type = 'MATERIAL'

            r3d = space.region_3d
            r3d.view_perspective = 'PERSP'
            target = Vector((0.0, -0.6, 1.4))
            cam_pos = Vector((5.8, -6.8, 4.8))
            direction = target - cam_pos
            r3d.view_location = target
            r3d.view_distance = direction.length
            r3d.view_rotation = direction.to_track_quat('-Z', 'Y')

            for p in data["presets"]:
                pid = p["id"]
                scene.simple_light.selected_preset = pid
                bpy.ops.simple_light.apply_preset(replace_existing=True)
                scene.frame_set(1)

                for o in scene.objects:
                    o.select_set(False)
                    if o.type in {'LIGHT', 'CAMERA'} or o.name == 'Suzanne':
                        o.show_name = True
                    elif o.name.startswith("SL_14_Blinds_Root") or o.name.startswith("SL_15_Gobo_Root") or o.name.startswith("SL_16_Window_Root") or o.name.startswith("SL_17_Lamp_Root") or o.name.startswith("SL_18_Candle_Root"):
                        o.show_name = True
                    if o.name.startswith("SL_Backdrop") or o.name.startswith("SL_12_Floor_Blocker"):
                        o.display_type = 'WIRE'

                png_path = os.path.join(LAYOUTS_DIR, f"{pid}.png")
                webp_path = os.path.join(LAYOUTS_DIR, f"{pid}.webp")
                scene.render.filepath = png_path

                with bpy.context.temp_override(window=window, area=area, region=area.regions[-1]):
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
                    bpy.ops.render.opengl(write_still=True, view_context=True)

                subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", png_path, "-o", webp_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"[Viewport Capture 1200x900] {pid} saved")
                layout_records.append({
                    "id": pid,
                    "layout_png": f"layouts/{pid}.png",
                    "layout_webp": f"layouts/{pid}.webp",
                    "capture_type": "GUI_VIEWPORT_OPENGL",
                    "resolution": [1200, 900],
                })
            break

meta_path = os.path.join(PY_JSON_DIR, "layout_capture_metadata.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({
        "blender_version": bpy.app.version_string,
        "capture_method": "Blender GUI Window 3D Viewport OpenGL Capture (non-headless)",
        "camera_view_pos": [5.8, -6.8, 4.8],
        "camera_target": [0.0, -0.6, 1.4],
        "records": layout_records,
    }, f, ensure_ascii=False, indent=2)

simple_light.unregister()
bpy.ops.wm.quit_blender()
