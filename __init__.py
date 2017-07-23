import bpy

bl_info = {
    "name": "Deselect - Play",
    "description": "Deselect all objects and play animation.",
    "author": "Jacques Lucke",
    "version": (0, 0, 1),
    "blender": (2, 78, 5),
    "location": "Timeline",
    "warning": "",
    "wiki_url": "",
    "category": "Animation" }

object_names = []

class DeselectPlayButtonInHeader(bpy.types.Header):
    bl_idname = "deselect_play_header"
    bl_space_type = "TIMELINE"

    def draw(self, context):
        layout = self.layout
        icon = "PAUSE" if is_animation_playing(context) else "PLAY"
        layout.operator("dp.deselect_and_play", "", icon = icon)

class DeselectAndPlay(bpy.types.Operator):
    bl_idname = "dp.deselect_and_play"
    bl_label = "Deselect and Play"
    bl_description = "Deselect/select objects and play/pause."
    bl_options = {"REGISTER"}

    def execute(self, context):
        global object_names
        if is_animation_playing(context):
            if is_no_object_selected(context):
                select_objects(object_names, context)
        else:
            object_names = get_selected_object_names(context)
            bpy.ops.object.select_all(action = "DESELECT")

        bpy.ops.screen.animation_play()
        return {"FINISHED"}

def is_animation_playing(context):
    return context.screen.is_animation_playing

def get_selected_object_names(context):
    objects = context.scene.objects
    return [object.name for object in objects if object.select]

def select_objects(names, context):
    for name in names:
        if name in context.scene.objects:
            context.scene.objects[name].select = True

def is_no_object_selected(context):
    objects = context.scene.objects
    return not any(object.select for object in objects)

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
