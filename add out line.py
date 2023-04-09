bl_info = {
    "name": "Outline Material Addon",
    "author": "copy cat :3",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Adds a solidify modifier and an outline material to the active object.",
    "category": "Object"
}

import bpy

class OBJECT_PT_add_outline_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Add Outline"
    bl_idname = "OBJECT_PT_add_outline_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Add Outline"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Add Outline to Object:")

        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("object.outline_material_addon", text="Add Outline")

class OutlineMaterialAddOn(bpy.types.Operator):
    """Adds a solidify modifier and an outline material to the active object."""
    bl_idname = "object.outline_material_addon"
    bl_label = "Outline Material Addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active object (the last selected object)
        obj = bpy.context.object

        # Create a new material and assign it to the object
        material = bpy.data.materials.new(name="Material")
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

        # Create a new material named "Outline"
        outline_material = bpy.data.materials.new(name="Outline")

        # Assign the new material to the object's second material slot
        if len(obj.data.materials) > 1:
            obj.data.materials[1] = outline_material
        else:
            obj.data.materials.append(outline_material)
        bpy.context.object.active_material_index = 1
        bpy.context.object.active_material.diffuse_color = (0, 0, 0, 1)
        bpy.context.object.active_material.use_backface_culling = True
        solidify_modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
        solidify_modifier.thickness = 0.1
        solidify_modifier.use_flip_normals = True
        bpy.context.object.modifiers["Solidify"].material_offset = 1
        bpy.context.object.modifiers["Solidify"].use_rim = False

        return {'FINISHED'}


def register():
    bpy.utils.register_class(OBJECT_PT_add_outline_panel)
    bpy.utils.register_class(OutlineMaterialAddOn)


def unregister():
    bpy.utils.unregister_class(OBJECT_PT_add_outline_panel)
    bpy.utils.unregister_class(OutlineMaterialAddOn)


if __name__ == "__main__":
    register()
