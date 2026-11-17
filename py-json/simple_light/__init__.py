import os
import bpy
import bpy.utils.previews
from . import builder

PREVIEW_COLLECTIONS = {}
PRESET_ITEMS_CACHE = []


def get_preset_enum_items(self, context):
    global PRESET_ITEMS_CACHE
    pcoll = PREVIEW_COLLECTIONS.get("main")
    data = builder.load_presets_data()
    items = []
    for idx, p in enumerate(data.get("presets", [])):
        pid = p["id"]
        label = f"{p['number']} {p['name_ko']}"
        desc = f"{p['name_en']} - {p['observation']}"
        icon_id = 0
        if pcoll is not None and pid in pcoll:
            icon_id = pcoll[pid].icon_id
        items.append((pid, label, desc, icon_id, idx))
    PRESET_ITEMS_CACHE = items
    return PRESET_ITEMS_CACHE


def on_preset_selection_changed(self, context):
    preset = builder.get_preset_by_id(self.selected_preset)
    prev_auto = self.auto_update_active
    self.auto_update_active = False
    try:
        # Load default preset-specific controls when user selects a preset
        for l_spec in preset.get("lights", []):
            if l_spec["type"] == "SPOT":
                self.spot_cone_deg = float(l_spec.get("spot_size_deg", 35.0))
                self.spot_blend = float(l_spec.get("spot_blend", 0.15))
        for p_spec in preset.get("props", []):
            if p_spec["type"] == "BLINDS":
                self.blind_gap = float(p_spec.get("slat_gap", 0.16))
                self.blind_angle_deg = float(p_spec.get("roll_deg", 20.0))
            elif p_spec["type"] == "VOLUME_GOBO":
                self.volume_density = float(p_spec.get("density", 0.025))
            elif p_spec["type"] == "CANDLE":
                self.candle_flicker_amp = 0.08
    finally:
        self.auto_update_active = prev_auto


def on_live_param_changed(self, context):
    scene = context.scene
    rig_id = scene.get("simple_light_active_rig_id", "")
    if rig_id and self.auto_update_active:
        bpy.ops.simple_light.apply_preset('EXEC_DEFAULT', replace_existing=True)


def on_compare_mode_changed(self, context):
    scene = context.scene
    rig_id = scene.get("simple_light_active_rig_id", "")
    builder.set_comparison_isolation(scene, self.comparison_mode, rig_id)


class SimpleLightSettings(bpy.types.PropertyGroup):
    selected_preset: bpy.props.EnumProperty(
        name="프리셋",
        description="수잔 썸네일과 한글 이름을 보고 조명 프리셋을 선택합니다",
        items=get_preset_enum_items,
        update=on_preset_selection_changed,
    )
    target_mode: bpy.props.EnumProperty(
        name="대상 종류",
        items=(
            ('OBJECT', "오브젝트", "선택하거나 지정한 단일 오브젝트를 기준으로 설치"),
            ('COLLECTION', "컬렉션", "지정한 컬렉션 전체 경계를 기준으로 설치"),
        ),
        default='OBJECT',
    )
    target_object: bpy.props.PointerProperty(
        name="피사체 오브젝트",
        type=bpy.types.Object,
        description="조명을 설치할 대상 오브젝트 (비워두면 현재 활성 오브젝트 사용)",
    )
    target_collection: bpy.props.PointerProperty(
        name="피사체 컬렉션",
        type=bpy.types.Collection,
        description="조명을 설치할 대상 컬렉션",
    )
    direction_mode: bpy.props.EnumProperty(
        name="촬영 방향",
        items=(
            ('CAMERA', "활성 카메라", "현재 장면의 활성 카메라가 바라보는 방향을 정면으로 사용"),
            ('VIEW', "현재 뷰", "현재 3D 뷰포트가 바라보는 방향을 정면으로 지정"),
        ),
        default='CAMERA',
        update=on_live_param_changed,
    )
    fallback_size: bpy.props.FloatProperty(
        name="기본 폭 (m)",
        description="피사체 폭이 0일 때 사용할 기준 크기(m)",
        default=1.64,
        min=0.05,
        max=100.0,
    )
    energy_mult: bpy.props.FloatProperty(
        name="밝기 배율",
        description="광원 전체 밝기 배율",
        default=1.0,
        min=0.0,
        max=20.0,
        update=on_live_param_changed,
    )
    size_mult: bpy.props.FloatProperty(
        name="광원 크기 배율",
        description="광원 발광면 크기 및 반지름 배율",
        default=1.0,
        min=0.05,
        max=10.0,
        update=on_live_param_changed,
    )
    flip_x: bpy.props.BoolProperty(
        name="좌우 반전",
        description="카메라 기준 좌우 조명과 소품 위치를 반전합니다",
        default=False,
        update=on_live_param_changed,
    )
    rotate_deg: bpy.props.FloatProperty(
        name="수평 회전 (도)",
        description="피사체 중심을 기준으로 조명 세트를 회전합니다",
        default=0.0,
        min=-180.0,
        max=180.0,
        update=on_live_param_changed,
    )
    create_backdrop: bpy.props.BoolProperty(
        name="배경판 함께 설치",
        description="실루엣, 하이키, 보색 등 배경 연출용 배경판을 함께 설치합니다",
        default=False,
        update=on_live_param_changed,
    )
    comparison_mode: bpy.props.BoolProperty(
        name="비교 모드 (기존 조명 격리)",
        description="기존 조명과 월드 배경광을 잠시 끄고 현재 프리셋만 격리해 비교합니다",
        default=False,
        update=on_compare_mode_changed,
    )
    auto_update_active: bpy.props.BoolProperty(
        name="조절값 실시간 반영",
        description="조절값을 바꿀 때 현재 설치된 조명 세트에 즉시 반영합니다",
        default=True,
    )
    # Preset-specific controls
    use_key: bpy.props.BoolProperty(
        name="Key 켜기",
        default=True,
        update=on_live_param_changed,
    )
    use_fill: bpy.props.BoolProperty(
        name="Fill 켜기",
        default=True,
        update=on_live_param_changed,
    )
    use_back: bpy.props.BoolProperty(
        name="Back / Rim 켜기",
        default=True,
        update=on_live_param_changed,
    )
    spot_cone_deg: bpy.props.FloatProperty(
        name="스포트 원뿔 각도 (도)",
        default=35.0,
        min=5.0,
        max=120.0,
        update=on_live_param_changed,
    )
    spot_blend: bpy.props.FloatProperty(
        name="스포트 가장자리 흐림",
        default=0.15,
        min=0.0,
        max=1.0,
        update=on_live_param_changed,
    )
    blind_gap: bpy.props.FloatProperty(
        name="블라인드 줄 간격 (m)",
        default=0.16,
        min=0.06,
        max=0.50,
        update=on_live_param_changed,
    )
    blind_angle_deg: bpy.props.FloatProperty(
        name="블라인드 회전 각도 (도)",
        default=20.0,
        min=-80.0,
        max=80.0,
        update=on_live_param_changed,
    )
    volume_density: bpy.props.FloatProperty(
        name="볼륨 안개 밀도",
        default=0.025,
        min=0.001,
        max=0.20,
        update=on_live_param_changed,
    )
    candle_flicker_amp: bpy.props.FloatProperty(
        name="촛불 흔들림 폭",
        default=0.08,
        min=0.0,
        max=0.50,
        update=on_live_param_changed,
    )


class SIMPLELIGHT_OT_create_demo(bpy.types.Operator):
    bl_idname = "simple_light.create_demo"
    bl_label = "수잔 비교 장면 만들기"
    bl_description = "새 수잔 비교 장면을 만들고 선택한 조명 프리셋을 설치합니다"
    bl_options = {'REGISTER', 'UNDO'}

    preset: bpy.props.StringProperty(
        name="Preset ID",
        default="05_hard",
    )

    def execute(self, context):
        p_id = self.preset
        if p_id == 'HARD':
            p_id = '05_hard'
        elif p_id == 'SOFT':
            p_id = '06_soft'

        preset_data = builder.get_preset_by_id(p_id)
        scene = bpy.data.scenes.new(f"Simple Light {preset_data['number']} {preset_data['name_en']}")
        if context.window:
            context.window.scene = scene

        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 128
        scene.cycles.use_denoising = True
        scene.render.resolution_x = 1200
        scene.render.resolution_y = 1200
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.look = 'None'
        scene.view_settings.exposure = 0.0
        scene.view_settings.gamma = 1.0

        world = bpy.data.worlds.new("SL World")
        world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.0
        scene.world = world

        bpy.ops.mesh.primitive_monkey_add(location=(0.0, 0.0, 1.2))
        subject = context.object
        subject.name = "Suzanne"
        subject.scale = (0.6, 0.6, 0.6)
        for polygon in subject.data.polygons:
            polygon.use_smooth = True
        modifier = subject.modifiers.new("Subdivision", 'SUBSURF')
        modifier.levels = 2
        modifier.render_levels = 2

        material = bpy.data.materials.new("SL Neutral")
        shader = material.node_tree.nodes['Principled BSDF']
        shader.inputs['Base Color'].default_value = (0.4, 0.4, 0.4, 1.0)
        shader.inputs['Roughness'].default_value = 0.6
        subject.data.materials.append(material)

        bpy.ops.mesh.primitive_plane_add(size=200.0, location=(0.0, 0.0, 0.0))
        ground = context.object
        ground.name = "SL Ground"
        ground.data.materials.append(material)

        camera_data = bpy.data.cameras.new("SL Camera")
        camera_data.lens = 70.0
        camera_data.sensor_width = 36.0
        camera = bpy.data.objects.new("SL Camera", camera_data)
        scene.collection.objects.link(camera)
        camera.location = (0.0, -5.0, 1.7)
        builder.aim_at(camera, (0.0, 0.0, 1.2))
        scene.camera = camera

        settings = scene.simple_light
        settings.auto_update_active = False
        settings.selected_preset = preset_data["id"]
        settings.target_object = subject
        settings.create_backdrop = True
        settings.auto_update_active = True

        builder.build_preset_rig(
            context,
            preset=preset_data,
            center=builder.REFERENCE_CENTER,
            k=1.0,
            direction_mode='CAMERA',
            create_backdrop=True,
        )
        self.report({'INFO'}, f"수잔 데모 장면 생성 완료: {preset_data['number']} {preset_data['name_ko']}")
        return {'FINISHED'}


class SIMPLELIGHT_OT_apply_preset(bpy.types.Operator):
    bl_idname = "simple_light.apply_preset"
    bl_label = "조명 세트 적용 / 교체"
    bl_description = "선택한 피사체 크기와 촬영 방향에 맞춰 조명 세트를 설치하거나 교체합니다"
    bl_options = {'REGISTER', 'UNDO'}

    replace_existing: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        scene = context.scene
        settings = scene.simple_light
        preset = builder.get_preset_by_id(settings.selected_preset)

        target_obj = settings.target_object
        if settings.target_mode == 'OBJECT' and target_obj is None:
            if context.active_object and not context.active_object.get("simple_light_owned"):
                target_obj = context.active_object
                settings.target_object = target_obj

        if settings.target_mode == 'OBJECT' and (target_obj is None or target_obj.name not in scene.objects):
            self.report({'ERROR'}, "조명을 설치할 피사체 오브젝트를 선택하거나 지정해주세요.")
            return {'CANCELLED'}
        if settings.target_mode == 'COLLECTION' and settings.target_collection is None:
            self.report({'ERROR'}, "조명을 설치할 피사체 컬렉션을 지정해주세요.")
            return {'CANCELLED'}

        center, width = builder.compute_bounds(
            context, settings.target_mode, target_obj, settings.target_collection, settings.fallback_size
        )
        if center is None:
            self.report({'ERROR'}, "대상의 경계를 계산할 수 없습니다. 빈 컬렉션이거나 유효한 메쉬가 없습니다.")
            return {'CANCELLED'}

        if width <= 1e-4:
            if settings.fallback_size <= 0.0:
                self.report({'ERROR'}, "대상 폭(D)이 0입니다. 기본 폭(m)을 입력해주세요.")
                return {'CANCELLED'}
            width = settings.fallback_size
            self.report({'WARNING'}, f"대상 폭이 0이어서 입력된 기본 폭 {width:.2f}m를 사용합니다.")

        k = width / builder.REFERENCE_D0
        existing_rig_id = scene.get("simple_light_active_rig_id", "") if self.replace_existing else None

        rig_id = builder.build_preset_rig(
            context,
            preset=preset,
            center=center,
            k=k,
            direction_mode=settings.direction_mode,
            energy_mult=settings.energy_mult,
            size_mult=settings.size_mult,
            flip_x=settings.flip_x,
            rotate_deg=settings.rotate_deg,
            use_key=settings.use_key,
            use_fill=settings.use_fill,
            use_back=settings.use_back,
            spot_cone_deg=settings.spot_cone_deg,
            spot_blend_val=settings.spot_blend,
            blind_gap=settings.blind_gap,
            blind_angle_deg=settings.blind_angle_deg,
            volume_density=settings.volume_density,
            candle_flicker_amp=settings.candle_flicker_amp,
            create_backdrop=settings.create_backdrop,
            rig_id=existing_rig_id,
        )

        if settings.comparison_mode:
            builder.set_comparison_isolation(scene, True, rig_id)

        self.report({'INFO'}, f"{preset['number']} {preset['name_ko']} 적용 완료 (비례 배율 k={k:.2f})")
        return {'FINISHED'}


class SIMPLELIGHT_OT_remove_rig(bpy.types.Operator):
    bl_idname = "simple_light.remove_rig"
    bl_label = "조명 세트 제거"
    bl_description = "방금 설치한 Simple Light 조명 세트와 소품을 장면에서 제거하고 원래 상태로 복구합니다"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        rig_id = scene.get("simple_light_active_rig_id", "")
        if not rig_id:
            self.report({'INFO'}, "제거할 Simple Light 조명 세트가 없습니다.")
            return {'CANCELLED'}

        if scene.simple_light.comparison_mode or scene.get("simple_light_compare_snapshot"):
            scene.simple_light.comparison_mode = False
            builder.set_comparison_isolation(scene, False, rig_id)

        builder.remove_rig_by_id(scene, rig_id)
        if "simple_light_active_rig_id" in scene:
            del scene["simple_light_active_rig_id"]
        if "simple_light_active_preset_id" in scene:
            del scene["simple_light_active_preset_id"]

        self.report({'INFO'}, "Simple Light 조명 세트를 제거했습니다.")
        return {'FINISHED'}


class SIMPLELIGHT_PT_panel(bpy.types.Panel):
    bl_label = "Simple Light 1.0.0"
    bl_idname = "SIMPLELIGHT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Simple Light"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.simple_light
        preset = builder.get_preset_by_id(settings.selected_preset)

        # 1. Preset Thumbnail Selector
        box = layout.box()
        box.label(text="1. 프리셋 선택 (Jinho Jung)", icon='LIGHT')
        box.template_icon_view(settings, "selected_preset", show_labels=True, scale=6.0, scale_popup=5.0)
        box.prop(settings, "selected_preset", text="")

        info_col = box.column(align=True)
        info_col.label(text=f"[{preset['number']}] {preset['name_ko']} ({preset['name_en']}) - {preset['category']}")
        obs_box = box.box()
        obs_box.label(text=preset["observation"], icon='INFO')

        # 2. Target & Direction
        t_box = layout.box()
        t_box.label(text="2. 피사체 및 촬영 방향", icon='OBJECT_DATA')
        t_box.prop(settings, "target_mode", expand=True)
        if settings.target_mode == 'OBJECT':
            t_box.prop(settings, "target_object", text="대상")
            if settings.target_object is None and context.active_object:
                t_box.label(text=f"현재 선택: {context.active_object.name}", icon='RESTRICT_SELECT_OFF')
        else:
            t_box.prop(settings, "target_collection", text="컬렉션")

        row = t_box.row(align=True)
        row.prop(settings, "direction_mode", expand=True)
        t_box.prop(settings, "create_backdrop")
        t_box.prop(settings, "comparison_mode")

        # Warn if external lights or world lighting are active
        rig_id = scene.get("simple_light_active_rig_id", "")
        other_lights = [
            o for o in scene.objects
            if o.type == 'LIGHT' and not o.hide_render and o.get("simple_light_rig_id") != rig_id
        ]
        world_lit = False
        if scene.world and scene.world.node_tree and "Background" in scene.world.node_tree.nodes:
            world_lit = scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value > 0.001
        if (other_lights or world_lit) and not settings.comparison_mode:
            warn = t_box.box()
            warn.label(text=f"기존 조명 {len(other_lights)}개 / 월드 환경광이 함께 비추는 중", icon='ERROR')

        # 3. Apply / Replace / Remove Buttons
        act_box = layout.box()
        row = act_box.row(align=True)
        row.scale_y = 1.4
        op_apply = row.operator("simple_light.apply_preset", text="적용 / 교체", icon='CHECKMARK')
        op_apply.replace_existing = True
        row.operator("simple_light.remove_rig", text="제거", icon='TRASH')

        demo_row = act_box.row(align=True)
        op_demo = demo_row.operator("simple_light.create_demo", text="독립 수잔 비교 장면 열기", icon='MONKEY')
        op_demo.preset = settings.selected_preset

        # 4. Adjustments
        adj_box = layout.box()
        adj_box.label(text="3. 공통 및 프리셋별 조절", icon='PREFERENCES')
        adj_box.prop(settings, "auto_update_active")
        col = adj_box.column(align=True)
        col.prop(settings, "energy_mult")
        col.prop(settings, "size_mult")
        col.prop(settings, "rotate_deg")
        col.prop(settings, "flip_x")

        # Conditional preset-specific controls
        roles = {l["role"] for l in preset.get("lights", [])}
        l_types = {l["type"] for l in preset.get("lights", [])}
        p_types = {p["type"] for p in preset.get("props", [])}

        if len(roles) > 1:
            r_box = adj_box.box()
            r_box.label(text="광원 역할별 켜기:")
            r_row = r_box.row(align=True)
            r_row.prop(settings, "use_key", toggle=True)
            r_row.prop(settings, "use_fill", toggle=True)
            r_row.prop(settings, "use_back", toggle=True)

        if "SPOT" in l_types:
            s_box = adj_box.box()
            s_box.label(text="스포트라이트 조절:")
            s_box.prop(settings, "spot_cone_deg")
            s_box.prop(settings, "spot_blend")

        if "BLINDS" in p_types:
            b_box = adj_box.box()
            b_box.label(text="블라인드 차광판 조절:")
            b_box.prop(settings, "blind_gap")
            b_box.prop(settings, "blind_angle_deg")

        if "VOLUME_GOBO" in p_types:
            v_box = adj_box.box()
            v_box.label(text="볼륨 안개 조절:")
            v_box.prop(settings, "volume_density")

        if "CANDLE" in p_types:
            c_box = adj_box.box()
            c_box.label(text="촛불 애니메이션 (1~48f):")
            c_box.prop(settings, "candle_flicker_amp")


CLASSES = (
    SimpleLightSettings,
    SIMPLELIGHT_OT_create_demo,
    SIMPLELIGHT_OT_apply_preset,
    SIMPLELIGHT_OT_remove_rig,
    SIMPLELIGHT_PT_panel,
)


def load_previews():
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    data = builder.load_presets_data()
    for p in data.get("presets", []):
        pid = p["id"]
        icon_path = os.path.join(icons_dir, f"{pid}.png")
        if os.path.exists(icon_path):
            pcoll.load(pid, icon_path, 'IMAGE')
    PREVIEW_COLLECTIONS["main"] = pcoll


def unload_previews():
    for pcoll in PREVIEW_COLLECTIONS.values():
        bpy.utils.previews.remove(pcoll)
    PREVIEW_COLLECTIONS.clear()


def register():
    load_previews()
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.simple_light = bpy.props.PointerProperty(type=SimpleLightSettings)


def unregister():
    if hasattr(bpy.types.Scene, "simple_light"):
        del bpy.types.Scene.simple_light
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    unload_previews()


if __name__ == "__main__":
    register()
