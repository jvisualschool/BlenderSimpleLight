import json
import os
import subprocess
import sys
import tempfile
import time
import bpy

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY_JSON_DIR = os.path.join(ROOT_DIR, "py-json")
PREVIEW_DIR = os.path.join(ROOT_DIR, "Preview")
IMAGES_DIR = os.path.join(PREVIEW_DIR, "images")
ICONS_DIR = os.path.join(PY_JSON_DIR, "simple_light", "icons")
BLEND_DIR = os.path.join(ROOT_DIR, "blend")

for d in (IMAGES_DIR, ICONS_DIR, BLEND_DIR):
    os.makedirs(d, exist_ok=True)

sys.path.insert(0, PY_JSON_DIR)
import simple_light
from simple_light import builder

simple_light.register()
bpy.ops.simple_light.create_demo(preset='05_hard')
scene = bpy.context.scene

# Ensure 128 samples, CPU, AgX, 1200x1200
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGB'
scene.render.image_settings.color_depth = '8'
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0.0
scene.view_settings.gamma = 1.0

data = builder.load_presets_data()
render_records = []

t_start = time.time()
for p in data["presets"]:
    pid = p["id"]
    t0 = time.time()
    scene.simple_light.selected_preset = pid
    bpy.ops.simple_light.apply_preset(replace_existing=True)
    scene.frame_set(1)

    png_path = os.path.join(IMAGES_DIR, f"{pid}.png")
    webp_path = os.path.join(IMAGES_DIR, f"{pid}.webp")
    icon_path = os.path.join(ICONS_DIR, f"{pid}.png")

    scene.render.filepath = png_path
    bpy.ops.render.render(write_still=True)

    # Convert to WebP and 256x256 PNG thumbnail from the exact same 1200x1200 PNG master
    subprocess.run(["/opt/homebrew/bin/cwebp", "-q", "90", png_path, "-o", webp_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["/usr/bin/sips", "-z", "256", "256", png_path, "--out", icon_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    elapsed = round(time.time() - t0, 2)
    print(f"[Render 1200x1200] {pid} done in {elapsed}s")
    render_records.append({
        "id": pid,
        "render_png": f"images/{pid}.png",
        "render_webp": f"images/{pid}.webp",
        "icon_png": f"icons/{pid}.png",
        "samples": 128,
        "resolution": [1200, 1200],
        "elapsed_sec": elapsed,
    })

# Render 18_candlelight 1..48 loop video (600x600, 48 samples for smooth loop)
print("Rendering 18_candlelight 1..48 animation frames...")
scene.simple_light.selected_preset = "18_candlelight"
bpy.ops.simple_light.apply_preset(replace_existing=True)
frames_dir = os.path.join(tempfile.gettempdir(), "simple_light_candle_frames")
os.makedirs(frames_dir, exist_ok=True)
scene.render.resolution_x = 600
scene.render.resolution_y = 600
scene.cycles.samples = 48

for f in range(1, 49):
    scene.frame_set(f)
    scene.render.filepath = os.path.join(frames_dir, f"frame_{f:03d}.png")
    bpy.ops.render.render(write_still=True)

mp4_path = os.path.join(IMAGES_DIR, "18_candlelight.mp4")
subprocess.run([
    "/usr/local/bin/ffmpeg", "-y", "-framerate", "24",
    "-i", os.path.join(frames_dir, "frame_%03d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
    mp4_path
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Saved 18_candlelight.mp4")

# Restore 1200x1200, 128 samples, and set to 05_hard for saved editable blend file
scene.render.resolution_x = 1200
scene.render.resolution_y = 1200
scene.cycles.samples = 128
scene.frame_set(1)
scene.simple_light.selected_preset = "05_hard"
bpy.ops.simple_light.apply_preset(replace_existing=True)

blend_path = os.path.join(BLEND_DIR, "suzanne_simple_light.blend")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print("Saved editable Suzanne scene:", blend_path)

meta_path = os.path.join(PY_JSON_DIR, "render_metadata.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({
        "blender_version": bpy.app.version_string,
        "engine": "CYCLES",
        "device": "CPU",
        "samples": 128,
        "denoising": True,
        "view_transform": "AgX",
        "look": "None",
        "exposure": 0.0,
        "gamma": 1.0,
        "preset_schema_version": 1,
        "candle_seed": 18,
        "total_elapsed_sec": round(time.time() - t_start, 2),
        "records": render_records,
    }, f, ensure_ascii=False, indent=2)

simple_light.unregister()
