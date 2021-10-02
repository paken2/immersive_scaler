import bpy

from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, CollectionProperty
from bpy.types import Scene

def make_annotations(cls):
    bl_props = {k: v for k, v in cls.__dict__.items() if isinstance(v, tuple)}
    if bl_props:
        if '__annotations__' not in cls.__dict__:
            setattr(cls, '__annotations__', {})
        annotations = cls.__dict__['__annotations__']
        for k, v in bl_props.items():
            annotations[k] = v
            delattr(cls, k)
    return cls

def set_properties():

    Scene.target_height = FloatProperty(
        name = "Target Height",
        description = "Desired height of the highest vertex in the model. If Scale to Eyes is set, Desired Eye Height",
        default = 1.61,
        step = 0.01,
        precision = 3,
        soft_min = 0,
        soft_max = 3,
        subtype = 'DISTANCE'
    )

    Scene.arm_to_legs = FloatProperty(
        name = "Leg/Arm Scaling",
        description = "What percentage of the needed rescaling should be done to the legs. Remaining scaling is done on the arms",
        default = 55,
        step = 1,
        precision = 3,
        soft_min = 0,
        soft_max = 100,
        subtype = 'PERCENTAGE'
    )

    Scene.arm_thickness = FloatProperty(
        name = "Arm Thickness",
        description = "How much arm thickness should be kept or added when scaling",
        default = 50,
        step = 1,
        precision = 3,
        soft_min = 0,
        soft_max = 100,
        subtype = 'PERCENTAGE'
    )

    Scene.leg_thickness = FloatProperty(
        name = "Leg Thickness",
        description = "How much leg thickness should be kept or added when scaling",
        default = 50,
        step = 1,
        precision = 3,
        soft_min = 0,
        soft_max = 100,
        subtype = 'PERCENTAGE'
    )

    Scene.extra_leg_length = FloatProperty(
        name = "Extra Leg Length",
        description = "How far beneath the real floor should the model's legs go - how far below the real floor should the vrchat floor be. This is calculated before scaling so the",
        default = 0,
        step = 0.01,
        precision = 3,
        soft_min = -1,
        soft_max = 1,
        subtype = 'DISTANCE'
    )

    Scene.thigh_percentage = FloatProperty(
        name = "Upper Leg Percent",
        description = "Percentage of the distance from the hips to the heel that should be taken up by the upper leg",
        default = 53,
        step = 1,
        precision = 3,
        soft_min = 10,
        soft_max = 90,
        subtype = 'PERCENTAGE'
    )

    Scene.scale_hand = BoolProperty(
        name = "Scale hand",
        description = "Toggle for scaling the hand with the arm",
        default = False
        )

    Scene.scale_foot = BoolProperty(
        name = "Scale foot",
        description = "Toggle for scaling the foot with the leg",
        default = False
        )

    Scene.center_model = BoolProperty(
        name = "Center Model",
        description = "Toggle for centering the model on x,y = 0,0",
        default = False
        )

    Scene.debug_no_scale = BoolProperty(
        name = "Skip Height Scaling",
        description = "Toggle for the final scaling phase",
        default = False
        )

    Scene.debug_no_floor = BoolProperty(
        name = "Skip move to floor",
        description = "Toggle for the scaling phase",
        default = False
        )

    Scene.debug_no_adjust = BoolProperty(
        name = "Skip Main Rescale",
        description = "Toggle for the first adjustment phase",
        default = False
        )

    Scene.scale_eyes = BoolProperty(
        name = "Scale to Eyes",
        description = "Target height targets eyes instead of the highest vertex",
        default = False
        )

    # Finger spreading
    Scene.spare_thumb = BoolProperty(
        name = "Ignore thumb",
        description = "Toggle if the thumb should be adjusted in addition to the body",
        default = True
        )

    Scene.spread_factor = FloatProperty(
        name = "Spread Factor",
        description = "Value showing how much fingers should be rotated. 1 is default, and will cause the finger bone to point directly away from the head of the wrist bone.",
        default = 1,
        step = .1,
        precision = 2,
        soft_min = 0,
        soft_max = 2,
        subtype = 'FACTOR'
    )

    # UI options
    bpy.types.Scene.imscale_show_customize = bpy.props.BoolProperty(name='Show customize panel', default=False)
    bpy.types.Scene.imscale_show_sf_custom = bpy.props.BoolProperty(name='Show customize panel', default=False)
    bpy.types.Scene.imscale_show_debug = bpy.props.BoolProperty(name='Show debug panel', default=False)


class ImmersiveScalerMenu(bpy.types.Panel):
    bl_label = 'Immersive Scaler Menu'
    bl_idname = "VIEW3D_PT_imscale"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "IMScale"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        col=box.column(align=True)
        col.label(text="Avatar Rescale")

        # Armature Rescale
        split = col.row(align=True)
        row = split.row(align=True)
        row.prop(bpy.context.scene, 'target_height', expand=True)
        row = split.row(align=True)
        row.alignment = 'RIGHT'
        row.operator("armature.get_avatar_height", text="", icon="EMPTY_SINGLE_ARROW")

        row = col.row(align=True)
        row.prop(bpy.context.scene, 'arm_to_legs', expand=True)

        # row = col.row(align=True)
        # row.prop(bpy.context.scene, 'scale_hand', expand=True)
        # row = col.row(align=True)
        # row.prop(bpy.context.scene, 'scale_foot', expand=True)


        # Customization options
        row = col.row(align=False)
        if scn.imscale_show_customize:
            row.prop(scn, "imscale_show_customize", icon="DOWNARROW_HLT", text="", emboss=False)
        else:
            row.prop(scn, "imscale_show_customize", icon="RIGHTARROW", text="", emboss=False)
        row.label(text="Customization")

        if scn.imscale_show_customize:
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'arm_thickness', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'leg_thickness', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'thigh_percentage', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'extra_leg_length', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'scale_eyes', expand=True)


        # Debug/section toggle options
        row = col.row(align=False)
        if scn.imscale_show_debug:
            row.prop(scn, "imscale_show_debug", icon="DOWNARROW_HLT", text="", emboss=False)
        else:
            row.prop(scn, "imscale_show_debug", icon="RIGHTARROW", text="", emboss=False)
        row.label(text="Core functionality toggle")

        if scn.imscale_show_debug:
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'debug_no_adjust', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'debug_no_floor', expand=True)
            row = col.row(align=True)
            row.prop(bpy.context.scene, 'debug_no_scale', expand=True)

        row = col.row(align=True)
        row.label(text="-------------")

        row = col.row(align=True)
        row.prop(bpy.context.scene, 'center_model', expand=True)

        row = col.row(align=True)
        row.scale_y=1.1
        op = row.operator("armature.rescale", text="Rescale Armature")

        # Spread Fingers
        box = layout.box()
        col=box.column(align=True)
        col.label(text="Finger Spreading")

        row = col.row(align=False)
        if scn.imscale_show_sf_custom:
            row.prop(scn, "imscale_show_sf_custom", icon="DOWNARROW_HLT", text="", emboss=False)
        else:
            row.prop(scn, "imscale_show_sf_custom", icon="RIGHTARROW", text="", emboss=False)
        row.label(text="Customization")

        if scn.imscale_show_sf_custom:
            row = col.row(align=True)
            row.prop(context.scene, 'spare_thumb')
            row = col.row(align=False)
            row.prop(context.scene, 'spread_factor')

        row = col.row(align=True)
        row.label(text="-------------")
        row.scale_y=1.1
        row = col.row(align=False)
        row.operator("armature.spreadfingers", text="Spread Fingers")

        # Shrink Hip
        box = layout.box()
        col=box.column(align=True)
        col.label(text="Hip fix (beta)")
        row.scale_y=1.1
        row = col.row(align=True)
        row.operator("armature.shrink_hips", text="Shrink Hip bone")

        return None




def ui_register():
    set_properties()
    make_annotations(ImmersiveScalerMenu)
    bpy.utils.register_class(ImmersiveScalerMenu)

def ui_unregister():
    bpy.utils.unregister_class(ImmersiveScalerMenu)

if __name__ == "__main__":
    register()
