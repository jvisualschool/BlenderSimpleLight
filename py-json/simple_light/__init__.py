import bpy
from mathutils import Vector


def aim_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


class SIMPLELIGHT_OT_demo(bpy.types.Operator):
    bl_idname = "simple_light.create_demo"
    bl_label = "Create Light Demo"
    bl_description = "Create a new Suzanne scene for a hard or soft light comparison"
    bl_options = {'REGISTER', 'UNDO'}

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=(('HARD', "05 Hard Light", "Small area light"),
               ('SOFT', "06 Soft Light", "Large area light")),
        default='HARD',
    )

    def execute(self, context):
        scene = bpy.data.scenes.new("Simple Light " + self.preset)
        context.window.scene = scene
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 64
        scene.cycles.use_denoising = True
        scene.render.resolution_x = 1200
        scene.render.resolution_y = 1200
        scene.render.resolution_percentage = 100
        scene.render.image_settings.file_format = 'PNG'
        scene.view_settings.view_transform = 'AgX'
        scene.view_settings.exposure = 0.0
        scene.view_settings.gamma = 1.0
        world = bpy.data.worlds.new("SL World")
        world.use_nodes = True
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
        material.use_nodes = True
        shader = material.node_tree.nodes['Principled BSDF']
        shader.inputs['Base Color'].default_value = (0.4, 0.4, 0.4, 1.0)
        shader.inputs['Roughness'].default_value = 0.6
        subject.data.materials.append(material)
        bpy.ops.mesh.primitive_plane_add(size=200.0)
        context.object.name = "SL Ground"
        context.object.data.materials.append(material)

        camera_data = bpy.data.cameras.new("SL Camera")
        camera_data.lens = 70.0
        camera_data.sensor_width = 36.0
        camera = bpy.data.objects.new("SL Camera", camera_data)
        scene.collection.objects.link(camera)
        camera.location = (0.0, -5.0, 1.7)
        aim_at(camera, (0.0, 0.0, 1.2))
        scene.camera = camera

        light_data = bpy.data.lights.new("SL Key", 'AREA')
        light_data.shape = 'SQUARE'
        light_data.size = 0.08 if self.preset == 'HARD' else 2.0
        light_data.energy = 500.0
        light = bpy.data.objects.new("SL Key", light_data)
        scene.collection.objects.link(light)
        light.location = (-2.0, -3.0, 3.5)
        aim_at(light, (0.0, 0.0, 1.2))
        self.report({'INFO'}, "Demo created. Render with F12")
        return {'FINISHED'}


class SIMPLELIGHT_PT_panel(bpy.types.Panel):
    bl_label = "Simple Light"
    bl_idname = "SIMPLELIGHT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Simple Light"

    def draw(self, context):
        for preset, label in (('HARD', "05 Hard Light"), ('SOFT', "06 Soft Light")):
            operator = self.layout.operator("simple_light.create_demo", text=label)
            operator.preset = preset


CLASSES = (SIMPLELIGHT_OT_demo, SIMPLELIGHT_PT_panel)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
