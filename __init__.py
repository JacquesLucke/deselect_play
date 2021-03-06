import bpy

bl_info = {
    "name": "Deselect - Play",
    "description": "Deselect all objects and play animation.",
    "author": "Jacques Lucke",
    "version": (0, 0, 3),
    "blender": (2, 78, 5),
    "location": "Timeline",
    "warning": "",
    "wiki_url": "",
    "category": "Animation" }


class DeselectPlayButtonInHeader(bpy.types.Header):
    bl_idname = "deselect_play_header"
    bl_space_type = "TIMELINE"

    def draw(self, context):
        layout = self.layout
        icon = "PAUSE" if is_animation_playing(context) else "PLAY"
        layout.operator("screen.deselect_and_play", "", icon = icon)

class DeselectAndPlay(bpy.types.Operator):
    bl_idname = "screen.deselect_and_play"
    bl_label = "Deselect and Play"
    bl_description = "Deselect/select objects and play/pause."
    bl_options = {"REGISTER"}
    object_names = []
    last_mode = "OBJECT"
    last_active_object_name = None

    def execute(self, context):
        objects = context.scene.objects
        if is_animation_playing(context):
            if is_no_object_selected(objects):
                select_objects(self.object_names, context)
                if try_make_object_active(objects, self.last_active_object_name):
                    bpy.ops.object.mode_set(mode = self.last_mode)
        else:
            type(self).last_mode = context.object.mode if context.object else "OBJECT"
            type(self).last_active_object_name = getattr(context.object, "name", None)
            if objects.active is not None: bpy.ops.object.mode_set(mode = "OBJECT")

            type(self).object_names = get_selected_object_names(objects)
            bpy.ops.object.select_all(action = "DESELECT")
            objects.active = None

        bpy.ops.screen.animation_play()
        return {"FINISHED"}

def is_animation_playing(context):
    return context.screen.is_animation_playing

def get_selected_object_names(objects):
    return [object.name for object in objects if object.select]

def select_objects(names, context):
    for name in names:
        if name in context.scene.objects:
            context.scene.objects[name].select = True

def is_no_object_selected(objects):
    return not any(object.select for object in objects)

def try_make_object_active(objects, name):
    try:
        objects.active = objects[name]
        return True
    except:
        return False

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)
