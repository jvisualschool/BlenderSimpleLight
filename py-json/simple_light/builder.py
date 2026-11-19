import json
import math
import os
import random
import uuid
import bpy
from mathutils import Matrix, Vector, Euler

REFERENCE_CENTER = Vector((0.0, 0.0, 1.2))
REFERENCE_D0 = 1.640625


def hex_to_linear_rgb(value):
    value = value.lstrip('#')
    channels = [int(value[index:index + 2], 16) / 255.0
                for index in (0, 2, 4)]
    result = []
    for channel in channels:
        if channel <= 0.04045:
            result.append(channel / 12.92)
        else:
            result.append(((channel + 0.055) / 1.055) ** 2.4)
    return tuple(result)


_PRESETS_DATA_CACHE = None


def load_presets_data():
    global _PRESETS_DATA_CACHE
    if _PRESETS_DATA_CACHE is None:
        json_path = os.path.join(os.path.dirname(__file__), "presets.json")
        with open(json_path, "r", encoding="utf-8") as f:
            _PRESETS_DATA_CACHE = json.load(f)
    return _PRESETS_DATA_CACHE


def get_preset_by_id(preset_id):
    data = load_presets_data()
    for p in data.get("presets", []):
        if p["id"] == preset_id:
            return p
    return data["presets"][0]


def aim_at(obj, target):
    direction = Vector(target) - obj.location
    if direction.length < 1e-6:
        direction = Vector((0.0, 0.0, -1.0))
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def compute_bounds(context, target_mode, target_obj, target_col, fallback_size=1.64):
    depsgraph = context.evaluated_depsgraph_get()
    objs = []
    if target_mode == 'COLLECTION' and target_col is not None:
        objs = [o for o in target_col.all_objects if o.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}]
    elif target_obj is not None:
        objs = [target_obj]

    if not objs:
        return None, 0.0

    min_v = Vector((1e9, 1e9, 1e9))
    max_v = Vector((-1e9, -1e9, -1e9))
    found = False
    for o in objs:
        eval_o = o.evaluated_get(depsgraph)
        if not hasattr(eval_o, "bound_box") or eval_o.bound_box is None:
            continue
        for corner in eval_o.bound_box:
            w = eval_o.matrix_world @ Vector(corner)
            min_v.x = min(min_v.x, w.x)
            min_v.y = min(min_v.y, w.y)
            min_v.z = min(min_v.z, w.z)
            max_v.x = max(max_v.x, w.x)
            max_v.y = max(max_v.y, w.y)
            max_v.z = max(max_v.z, w.z)
            found = True

    if not found:
        return objs[0].location.copy(), 0.0

    center = (min_v + max_v) * 0.5
    dx = max_v.x - min_v.x
    dy = max_v.y - min_v.y
    width = max(dx, dy)
    return center, width


def compute_basis(context, center, direction_mode, rotate_deg=0.0):
    forward = Vector((0.0, 1.0, 0.0))  # Default camera looks toward +Y (subject front is -Y)
    if direction_mode == 'CAMERA' and context.scene.camera is not None:
        cam_loc = context.scene.camera.matrix_world.translation
        vec = center - cam_loc
        vec_xy = Vector((vec.x, vec.y, 0.0))
        if vec_xy.length > 1e-4:
            forward = vec_xy.normalized()
    elif direction_mode == 'VIEW':
        for area in context.screen.areas if context.screen else []:
            if area.type == 'VIEW_3D':
                r3d = area.spaces.active.region_3d
                view_inv = r3d.view_matrix.inverted()
                view_dir = -(view_inv.col[2].xyz)
                vec_xy = Vector((view_dir.x, view_dir.y, 0.0))
                if vec_xy.length > 1e-4:
                    forward = vec_xy.normalized()
                break

    base_yaw = math.atan2(-forward.x, forward.y)
    total_yaw = base_yaw + math.radians(rotate_deg)
    rot_mat = Matrix.Rotation(total_yaw, 3, 'Z')
    return rot_mat


def map_point(rel_pt, center, k, flip_x, rot_mat):
    p = Vector(rel_pt) - REFERENCE_CENTER
    if flip_x:
        p.x = -p.x
    p = p * k
    p = rot_mat @ p
    return center + p


def map_ground_point(rel_pt, center, k, flip_x, rot_mat):
    # Maps relative to reference ground z=0 -> center.z - 1.2 * k
    return map_point(rel_pt, center, k, flip_x, rot_mat)


def tag_owned(datablock, rig_id, role=""):
    if datablock is None:
        return
    datablock["simple_light_owned"] = True
    datablock["simple_light_rig_id"] = str(rig_id)
    if role:
        datablock["simple_light_role"] = role


def remove_rig_by_id(scene, rig_id):
    if not rig_id:
        return
    rig_id = str(rig_id)

    for obj in list(bpy.data.objects):
        if obj.get("simple_light_owned") and obj.get("simple_light_rig_id") == rig_id:
            data = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            if data and data.users == 0:
                if isinstance(data, bpy.types.Light):
                    bpy.data.lights.remove(data)
                elif isinstance(data, bpy.types.Mesh):
                    bpy.data.meshes.remove(data)
                elif isinstance(data, bpy.types.Camera):
                    bpy.data.cameras.remove(data)

    for mat in list(bpy.data.materials):
        if mat.get("simple_light_owned") and mat.get("simple_light_rig_id") == rig_id:
            if mat.users == 0:
                bpy.data.materials.remove(mat)

    for col in list(bpy.data.collections):
        if col.get("simple_light_owned") and col.get("simple_light_rig_id") == rig_id:
            bpy.data.collections.remove(col)


def set_comparison_isolation(scene, isolate, rig_id):
    if isolate:
        snapshot = {
            "world_name": scene.world.name if scene.world else "",
            "world_strength": None,
            "lights": {}
        }
        if scene.world and scene.world.node_tree and "Background" in scene.world.node_tree.nodes:
            snapshot["world_strength"] = float(
                scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value
            )
            scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0

        for obj in scene.objects:
            if obj.type == 'LIGHT' and obj.get("simple_light_rig_id") != rig_id:
                snapshot["lights"][obj.name] = {
                    "hide_viewport": bool(obj.hide_viewport),
                    "hide_render": bool(obj.hide_render),
                }
                obj.hide_viewport = True
                obj.hide_render = True

        if not scene.get("simple_light_compare_snapshot"):
            scene["simple_light_compare_snapshot"] = json.dumps(snapshot)
    else:
        raw = scene.get("simple_light_compare_snapshot")
        if raw:
            try:
                snapshot = json.loads(raw)
                w_name = snapshot.get("world_name", "")
                if w_name and w_name in bpy.data.worlds:
                    scene.world = bpy.data.worlds[w_name]
                    if snapshot.get("world_strength") is not None and scene.world.node_tree:
                        bg = scene.world.node_tree.nodes.get("Background")
                        if bg:
                            bg.inputs["Strength"].default_value = float(snapshot["world_strength"])
                for l_name, states in snapshot.get("lights", {}).items():
                    if l_name in bpy.data.objects:
                        o = bpy.data.objects[l_name]
                        o.hide_viewport = bool(states.get("hide_viewport", False))
                        o.hide_render = bool(states.get("hide_render", False))
            except Exception:
                pass
            del scene["simple_light_compare_snapshot"]


def create_matte_material(name, linear_rgb, roughness, rig_id):
    mat = bpy.data.materials.new(name)
    tag_owned(mat, rig_id)
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if isinstance(linear_rgb, (int, float)):
            c = (linear_rgb, linear_rgb, linear_rgb, 1.0)
        else:
            c = (linear_rgb[0], linear_rgb[1], linear_rgb[2], 1.0)
        bsdf.inputs["Base Color"].default_value = c
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def create_emission_material(name, linear_rgb, strength, rig_id):
    mat = bpy.data.materials.new(name)
    tag_owned(mat, rig_id)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    em = nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (linear_rgb[0], linear_rgb[1], linear_rgb[2], 1.0)
    em.inputs["Strength"].default_value = strength
    links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat, em


def create_volume_material(name, density, anisotropy, rig_id):
    mat = bpy.data.materials.new(name)
    tag_owned(mat, rig_id)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    vol = nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Color"].default_value = (0.85, 0.92, 1.0, 1.0)
    vol.inputs["Density"].default_value = density
    vol.inputs["Anisotropy"].default_value = anisotropy
    links.new(vol.outputs["Volume"], out.inputs["Volume"])
    return mat


def add_box_mesh(name, size_xyz, col, mat, rig_id):
    bm_mesh = bpy.data.meshes.new(name)
    tag_owned(bm_mesh, rig_id)
    sx, sy, sz = size_xyz[0] * 0.5, size_xyz[1] * 0.5, size_xyz[2] * 0.5
    verts = [
        (-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
        (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz),
    ]
    faces = [
        (0, 3, 2, 1), (4, 5, 6, 7),
        (0, 1, 5, 4), (1, 2, 6, 5),
        (2, 3, 7, 6), (3, 0, 4, 7),
    ]
    bm_mesh.from_pydata(verts, [], faces)
    bm_mesh.update()
    obj = bpy.data.objects.new(name, bm_mesh)
    tag_owned(obj, rig_id, "Prop")
    if mat:
        obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def add_cylinder_mesh(name, radius_bottom, radius_top, height, segments, open_ends, col, mat, rig_id):
    mesh = bpy.data.meshes.new(name)
    tag_owned(mesh, rig_id)
    verts = []
    faces = []
    hz = height * 0.5
    for i in range(segments):
        ang = 2.0 * math.pi * i / segments
        verts.append((radius_bottom * math.cos(ang), radius_bottom * math.sin(ang), -hz))
    for i in range(segments):
        ang = 2.0 * math.pi * i / segments
        verts.append((radius_top * math.cos(ang), radius_top * math.sin(ang), hz))
    for i in range(segments):
        ni = (i + 1) % segments
        faces.append((i, ni, segments + ni, segments + i))
    if not open_ends:
        faces.append(tuple(reversed(range(segments))))
        faces.append(tuple(range(segments, 2 * segments)))
    mesh.from_pydata(verts, [], faces)
    for p in mesh.polygons:
        p.use_smooth = True
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    tag_owned(obj, rig_id, "Prop")
    if mat:
        obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def add_sphere_mesh(name, radius, scale_z, col, mat, rig_id):
    mesh = bpy.data.meshes.new(name)
    tag_owned(mesh, rig_id)
    rings = 12
    segs = 16
    verts = [(0.0, 0.0, -radius * scale_z)]
    for r in range(1, rings):
        phi = math.pi * r / rings - math.pi * 0.5
        z = radius * math.sin(phi) * scale_z
        rc = radius * math.cos(phi)
        for s in range(segs):
            theta = 2.0 * math.pi * s / segs
            verts.append((rc * math.cos(theta), rc * math.sin(theta), z))
    verts.append((0.0, 0.0, radius * scale_z))
    faces = []
    for s in range(segs):
        ns = (s + 1) % segs
        faces.append((0, 1 + ns, 1 + s))
    for r in range(rings - 2):
        base = 1 + r * segs
        for s in range(segs):
            ns = (s + 1) % segs
            faces.append((base + s, base + ns, base + segs + ns, base + segs + s))
    top_idx = len(verts) - 1
    base = 1 + (rings - 2) * segs
    for s in range(segs):
        ns = (s + 1) % segs
        faces.append((base + s, base + ns, top_idx))
    mesh.from_pydata(verts, [], faces)
    for p in mesh.polygons:
        p.use_smooth = True
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    tag_owned(obj, rig_id, "Prop")
    if mat:
        obj.data.materials.append(mat)
    col.objects.link(obj)
    return obj


def apply_candle_keyframes(scene, light_obj, emission_node, base_energy, base_emission, amp=0.08, seed=18):
    rng = random.Random(seed)
    scene.render.fps = 24
    scene.frame_start = 1
    scene.frame_end = 48

    frames = list(range(1, 49, 4))
    multipliers = [rng.uniform(1.0 - amp, 1.0 + amp) for _ in frames]
    frames.append(49)
    multipliers.append(multipliers[0])

    for f, m in zip(frames, multipliers):
        light_obj.data.energy = base_energy * m
        light_obj.data.keyframe_insert(data_path="energy", frame=f)
        if emission_node is not None:
            emission_node.inputs["Strength"].default_value = base_emission * m
            emission_node.inputs["Strength"].keyframe_insert(data_path="default_value", frame=f)

    # Set linear interpolation and cyclic modifier on animation data if available
    for id_block in (light_obj.data, emission_node.id_data if emission_node else None):
        if id_block and id_block.animation_data and id_block.animation_data.action:
            act = id_block.animation_data.action
            fcurves = getattr(act, "fcurves", [])
            for fc in fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'LINEAR'
                if not any(mod.type == 'CYCLES' for mod in fc.modifiers):
                    fc.modifiers.new(type='CYCLES')

    scene.frame_set(1)


def build_preset_rig(
    context,
    preset,
    center,
    k,
    direction_mode='CAMERA',
    energy_mult=1.0,
    size_mult=1.0,
    flip_x=False,
    rotate_deg=0.0,
    use_key=True,
    use_fill=True,
    use_back=True,
    spot_cone_deg=0.0,
    spot_blend_val=-1.0,
    blind_gap=0.16,
    blind_angle_deg=20.0,
    volume_density=0.025,
    candle_flicker_amp=0.08,
    create_backdrop=False,
    rig_id=None,
):
    scene = context.scene
    if not rig_id:
        rig_id = str(uuid.uuid4())
    else:
        remove_rig_by_id(scene, rig_id)

    col_name = f"SL_{preset['number']}_{preset['name_en']}"
    col = bpy.data.collections.new(col_name)
    tag_owned(col, rig_id, "Collection")
    scene.collection.children.link(col)

    rot_mat = compute_basis(context, center, direction_mode, rotate_deg)
    created_lights = []

    # Optional backdrop for demo/comparison scene or when requested
    if create_backdrop and not preset.get("backdrop_remove", False):
        bg_linear = preset.get("backdrop_color_linear", 0.08)
        bg_y = preset.get("backdrop_offset_y", 1.5)
        bg_mat = create_matte_material(f"SL_Backdrop_Mat_{preset['number']}", bg_linear, 1.0, rig_id)
        bg_obj = add_box_mesh(
            f"SL_Backdrop_{preset['number']}",
            (6.0 * k, 0.04 * k, 4.0 * k),
            col,
            bg_mat,
            rig_id,
        )
        bg_obj.location = map_point((0.0, bg_y, 2.0), center, k, flip_x, rot_mat)
        bg_obj.rotation_euler = rot_mat.to_euler()

    # Create Lights
    for l_spec in preset.get("lights", []):
        role = l_spec["role"]
        if role == "Key" and not use_key:
            continue
        if role in ("Fill", "RoomFill") and not use_fill:
            continue
        if role in ("Back", "Rim", "RimLeft", "RimShadow", "BackSpot") and not use_back:
            continue

        l_type = l_spec["type"]
        l_name = f"SL_{preset['number']}_{role}"
        l_data = bpy.data.lights.new(l_name, l_type)
        tag_owned(l_data, rig_id, role)
        l_data.color = hex_to_linear_rgb(l_spec.get("color_srgb", "#FFFFFF"))

        if l_type == 'SUN':
            l_data.energy = float(l_spec["energy"]) * energy_mult
            l_data.angle = math.radians(float(l_spec.get("angle_deg", 1.0)) * size_mult)
            elev = math.radians(float(l_spec.get("elevation_deg", 8.0)))
            azim = math.radians(float(l_spec.get("azimuth_deg", 140.0)))
            if flip_x:
                azim = -azim
            # Azimuth: 0 deg = front (-Y), 90 deg = right (+X), 140 deg = back-right
            dir_from_subject = Vector((
                math.cos(elev) * math.sin(azim),
                -math.cos(elev) * math.cos(azim),
                math.sin(elev),
            ))
            dir_from_subject = rot_mat @ dir_from_subject
            l_obj = bpy.data.objects.new(l_name, l_data)
            tag_owned(l_obj, rig_id, role)
            col.objects.link(l_obj)
            l_obj.location = center + dir_from_subject * (4.0 * k)
            aim_at(l_obj, center)
            created_lights.append(l_obj)
            continue

        # Finite light energy scales by k^2
        base_energy = float(l_spec["energy"]) * (k ** 2) * energy_mult
        l_data.energy = base_energy

        if l_type == 'AREA':
            shape = l_spec.get("shape", "SQUARE")
            l_data.shape = shape
            l_data.size = max(0.005, float(l_spec.get("size", 1.0)) * k * size_mult)
            if shape == 'RECTANGLE':
                l_data.size_y = max(0.005, float(l_spec.get("size_y", 1.0)) * k * size_mult)
        elif l_type == 'POINT':
            l_data.shadow_soft_size = max(0.002, float(l_spec.get("radius", 0.05)) * k * size_mult)
        elif l_type == 'SPOT':
            l_data.shadow_soft_size = max(0.002, float(l_spec.get("radius", 0.05)) * k * size_mult)
            cone = spot_cone_deg if spot_cone_deg > 0.0 else float(l_spec.get("spot_size_deg", 35.0))
            blend = spot_blend_val if spot_blend_val >= 0.0 else float(l_spec.get("spot_blend", 0.15))
            l_data.spot_size = math.radians(cone)
            l_data.spot_blend = blend

        l_obj = bpy.data.objects.new(l_name, l_data)
        tag_owned(l_obj, rig_id, role)
        col.objects.link(l_obj)
        l_obj.location = map_point(l_spec["position"], center, k, flip_x, rot_mat)

        if "target" in l_spec:
            tgt = map_point(l_spec["target"], center, k, flip_x, rot_mat)
            aim_at(l_obj, tgt)
        created_lights.append(l_obj)

    # Create Props
    for p_spec in preset.get("props", []):
        p_type = p_spec["type"]

        if p_type == "BLINDS" and created_lights:
            key_light = created_lights[0]
            tgt_world = map_point(preset["target"], center, k, flip_x, rot_mat)
            mid_pos = (key_light.location + tgt_world) * 0.5
            to_light = (key_light.location - tgt_world).normalized()
            frame_rot = to_light.to_track_quat('Z', 'Y').to_matrix().to_3x3()
            roll_angle = math.radians(-blind_angle_deg if flip_x else blind_angle_deg)
            roll_mat = Matrix.Rotation(roll_angle, 3, 'Z')
            final_mat = frame_rot @ roll_mat

            root = bpy.data.objects.new("SL_14_Blinds_Root", None)
            tag_owned(root, rig_id, "PropRoot")
            col.objects.link(root)
            root.location = mid_pos
            root.rotation_euler = final_mat.to_euler()

            black_mat = create_matte_material("SL_14_Black_Mat", 0.01, 0.9, rig_id)
            slat_count = int(p_spec.get("slat_count", 14))
            slat_len = float(p_spec.get("slat_length", 4.0)) * k
            slat_h = float(p_spec.get("slat_height", 0.10)) * k
            slat_t = float(p_spec.get("slat_thickness", 0.02)) * k
            gap = float(blind_gap if blind_gap > 0 else p_spec.get("slat_gap", 0.16)) * k

            for i in range(slat_count):
                offset_y = (i - (slat_count - 1) * 0.5) * gap
                slat = add_box_mesh(f"SL_14_Slat_{i:02d}", (slat_len, slat_h, slat_t), col, black_mat, rig_id)
                slat.parent = root
                slat.location = (0.0, offset_y, 0.0)

        elif p_type == "VOLUME_GOBO" and created_lights:
            dens = (volume_density if volume_density > 0 else float(p_spec.get("density", 0.025))) / max(k, 0.1)
            aniso = float(p_spec.get("anisotropy", 0.3))
            vol_mat = create_volume_material("SL_15_Volume_Mat", dens, aniso, rig_id)
            b_size = [s * k for s in p_spec.get("box_size", [6.0, 6.0, 4.0])]
            vol_box = add_box_mesh("SL_15_Volume_Box", b_size, col, vol_mat, rig_id)
            vol_box.location = map_point(p_spec.get("box_center", [0.0, 0.0, 2.0]), center, k, flip_x, rot_mat)
            vol_box.rotation_euler = rot_mat.to_euler()
            vol_box.display_type = 'WIRE'

            spot_light = created_lights[0]
            tgt_world = map_point(preset["target"], center, k, flip_x, rot_mat)
            mid_pos = spot_light.location.lerp(tgt_world, 0.35)
            to_light = (spot_light.location - tgt_world).normalized()
            frame_rot = to_light.to_track_quat('Z', 'Y').to_matrix().to_3x3()
            roll_mat = Matrix.Rotation(math.radians(30.0 if not flip_x else -30.0), 3, 'Z')
            gobo_rot = (frame_rot @ roll_mat).to_euler()

            gobo_root = bpy.data.objects.new("SL_15_Gobo_Root", None)
            tag_owned(gobo_root, rig_id, "PropRoot")
            col.objects.link(gobo_root)
            gobo_root.location = mid_pos
            gobo_root.rotation_euler = gobo_rot

            black_mat = create_matte_material("SL_15_Gobo_Mat", 0.01, 0.9, rig_id)
            bar_w = float(p_spec.get("bar_width", 0.12)) * k
            bar_gap = float(p_spec.get("bar_gap", 0.28)) * k
            bar_cnt = int(p_spec.get("bar_count", 5))
            for i in range(bar_cnt):
                ox = (i - (bar_cnt - 1) * 0.5) * bar_gap
                bar = add_box_mesh(f"SL_15_Gobo_Bar_{i+1}", (bar_w, 2.5 * k, 0.02 * k), col, black_mat, rig_id)
                bar.parent = gobo_root
                bar.location = (ox, 0.0, 0.0)
                bar.visible_camera = False

        elif p_type == "RIM_FLOOR_BLOCKER":
            blk_mat = create_matte_material("SL_12_Blocker_Mat", 0.002, 1.0, rig_id)
            blk = add_box_mesh("SL_12_Floor_Blocker", (12.0 * k, 12.0 * k, 0.02 * k), col, blk_mat, rig_id)
            blk.location = map_point((0.0, 0.0, 0.35), center, k, flip_x, rot_mat)
            blk.rotation_euler = rot_mat.to_euler()
            blk.visible_camera = False

        elif p_type == "WINDOW_WALL":
            wall_x = float(p_spec.get("wall_x", -1.8))
            open_w = float(p_spec.get("open_width", 1.5))
            open_h = float(p_spec.get("open_height", 2.0))
            cz = float(p_spec.get("center_z", 1.5))
            thick = float(p_spec.get("frame_thickness", 0.08))
            wall_mat = create_matte_material("SL_16_Window_Mat", 0.03, 0.9, rig_id)

            root = bpy.data.objects.new("SL_16_Window_Root", None)
            tag_owned(root, rig_id, "PropRoot")
            col.objects.link(root)
            root.location = map_point((wall_x, 0.0, cz), center, k, flip_x, rot_mat)
            root.rotation_euler = rot_mat.to_euler()

            # 4 surrounding opaque wall pieces + Mullion crossbars in YZ plane
            pieces = [
                ("Top", (thick * k, 6.0 * k, 2.0 * k), (0.0, 0.0, (open_h * 0.5 + 1.0) * k)),
                ("Bottom", (thick * k, 6.0 * k, 2.0 * k), (0.0, 0.0, -(open_h * 0.5 + 1.0) * k)),
                ("Front", (thick * k, 2.25 * k, open_h * k), (0.0, -(open_w * 0.5 + 1.125) * k, 0.0)),
                ("Back", (thick * k, 2.25 * k, open_h * k), (0.0, (open_w * 0.5 + 1.125) * k, 0.0)),
                ("Mullion_H", (thick * k, open_w * k, 0.09 * k), (0.0, 0.0, 0.0)),
                ("Mullion_V", (thick * k, 0.09 * k, open_h * k), (0.0, 0.0, 0.0)),
            ]
            for p_name, sz, loc in pieces:
                part = add_box_mesh(f"SL_16_Wall_{p_name}", sz, col, wall_mat, rig_id)
                part.parent = root
                part.location = loc

        elif p_type == "PRACTICAL_LAMP" and created_lights:
            bulb_light = created_lights[0]
            root = bpy.data.objects.new("SL_17_Lamp_Root", None)
            tag_owned(root, rig_id, "PropRoot")
            col.objects.link(root)
            root.location = bulb_light.location.copy()
            root.rotation_euler = rot_mat.to_euler()
            bulb_light.parent = root
            bulb_light.location = (0.0, 0.0, 0.0)

            lin_col = hex_to_linear_rgb(p_spec.get("color_srgb", "#FFD0A0"))
            em_mat, _ = create_emission_material(
                "SL_17_Bulb_Mat", lin_col, float(p_spec.get("emission_strength", 8.0)) * energy_mult, rig_id
            )
            bulb_r = float(p_spec.get("bulb_radius", 0.045)) * k
            bulb_mesh = add_sphere_mesh("SL_17_Bulb_Mesh", bulb_r, 1.0, col, em_mat, rig_id)
            bulb_mesh.parent = root
            bulb_mesh.location = (0.0, 0.0, 0.0)

            shade_mat = create_matte_material("SL_17_Shade_Mat", (0.28, 0.20, 0.12), 0.35, rig_id)
            sr = float(p_spec.get("shade_radius", 0.16)) * k
            sh = float(p_spec.get("shade_height", 0.18)) * k
            shade = add_cylinder_mesh("SL_17_Shade", sr, sr * 0.50, sh, 24, True, col, shade_mat, rig_id)
            shade.parent = root
            shade.location = (-0.06 * k if not flip_x else 0.06 * k, 0.0, 0.09 * k)
            shade.rotation_euler = (0.0, math.radians(-32.0 if flip_x else 32.0), 0.0)

            stand_mat = create_matte_material("SL_17_Stand_Mat", (0.35, 0.28, 0.18), 0.3, rig_id)
            stem_h = 1.6 * k
            stem = add_cylinder_mesh("SL_17_Stand_Stem", 0.018 * k, 0.018 * k, stem_h, 12, False, col, stand_mat, rig_id)
            stem.parent = root
            stem.location = (-(0.16 * k) if not flip_x else (0.16 * k), 0.0, -stem_h * 0.5 + 0.08 * k)
            base_disc = add_cylinder_mesh("SL_17_Stand_Base", 0.14 * k, 0.14 * k, 0.03 * k, 20, False, col, stand_mat, rig_id)
            base_disc.parent = root
            base_disc.location = (-(0.16 * k) if not flip_x else (0.16 * k), 0.0, -stem_h + 0.09 * k)

        elif p_type == "CANDLE" and created_lights:
            candle_light = created_lights[0]
            root = bpy.data.objects.new("SL_18_Candle_Root", None)
            tag_owned(root, rig_id, "PropRoot")
            col.objects.link(root)
            root.location = candle_light.location.copy()
            root.rotation_euler = rot_mat.to_euler()
            candle_light.parent = root
            candle_light.location = (0.0, 0.0, 0.0)

            lin_col = hex_to_linear_rgb(p_spec.get("color_srgb", "#FFAA55"))
            base_em = float(p_spec.get("emission_strength", 5.0)) * energy_mult
            flame_mat, em_node = create_emission_material("SL_18_Flame_Mat", lin_col, base_em, rig_id)
            fh = float(p_spec.get("flame_height", 0.06)) * k
            flame = add_sphere_mesh("SL_18_Flame", fh * 0.28, 1.8, col, flame_mat, rig_id)
            flame.parent = root
            flame.location = (0.0, 0.0, 0.0)

            wax_mat = create_matte_material("SL_18_Wax_Mat", (0.75, 0.70, 0.60), 0.4, rig_id)
            cr = float(p_spec.get("candle_radius", 0.035)) * k
            ch = float(p_spec.get("candle_height", 0.30)) * k
            wax = add_cylinder_mesh("SL_18_Candle_Body", cr, cr, ch, 20, False, col, wax_mat, rig_id)
            wax.parent = root
            wax.location = (0.0, 0.0, -(ch * 0.5 + fh * 0.5))

            base_energy = float(preset["lights"][0]["energy"]) * (k ** 2) * energy_mult
            apply_candle_keyframes(
                scene,
                candle_light,
                em_node,
                base_energy,
                base_em,
                amp=candle_flicker_amp,
                seed=int(p_spec.get("seed", 18)),
            )

    scene["simple_light_active_rig_id"] = str(rig_id)
    scene["simple_light_active_preset_id"] = preset["id"]
    return rig_id
