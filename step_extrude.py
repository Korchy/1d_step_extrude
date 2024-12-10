# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#    https://github.com/Korchy/1d_step_extrude

import bpy
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class

bl_info = {
    "name": "Step Extrude",
    "description": "Continuous extrude simulation with press only mouse left clicks",
    "author": "Nikita Akimov, Paul Kotelevets",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool panel > 1D > Step Extrude",
    "doc_url": "https://github.com/Korchy/1d_step_extrude",
    "tracker_url": "https://github.com/Korchy/1d_step_extrude",
    "category": "All"
}


# MAIN CLASS

class StepExtrude:

    @staticmethod
    def ui(layout, context):
        # ui panel
        # Step Extrude
        layout.operator(
            operator='stepextrude.step_extrude',
            icon='FRAME_NEXT'
        )


# OPERATORS

class StepExtrude_OT_step_extrude(Operator):
    bl_idname = 'stepextrude.step_extrude'
    bl_label = 'Step Extrude'
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.started = False

    def modal(self, context, event):
        # Working modal
        # check if starting was success
        if not self.started:
            return {'CANCELLED'}
        # LEFT MOUSE - RELEASE
        #   only here we can check if extrude operator stop executing,
        #   and we heed to run it again for the next step
        if event.type == 'LEFTMOUSE':
            if event.value == 'RELEASE':
                bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN')
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            # exit
            # remove last selected vertices, because they stayed on the last "extrude" operator call
            # bpy.ops.mesh.delete(type='VERT')
            # finish executing modal mode of this operator
            return {'FINISHED'}
        # PASS_THROUGH to stay modal mode active
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        # exec invoke - to start modal mode
        # add handler for modal mode
        context.window_manager.modal_handler_add(self)
        # start "extrude" for the first time (in modal mode)
        extrude_starts_with = bpy.ops.mesh.extrude_region_move('INVOKE_REGION_WIN')
        # need flag, Blender brokes if try to exit with cancel here
        self.started = extrude_starts_with == {'RUNNING_MODAL'}
        # switch to modal mode
        return {'RUNNING_MODAL'}


# PANELS

class StepExtrude_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Step Extrude'
    bl_category = '1D'

    def draw(self, context):
        StepExtrude.ui(
            layout=self.layout,
            context=context
        )


# KEYMAPS

class StepExtrudeKeyMap:

    _keymaps = []

    @classmethod
    def register(cls, context):
        # add new key map
        if context.window_manager.keyconfigs.addon:
            keymap = context.window_manager.keyconfigs.addon.keymaps.new(name='Window')
            # add keys
            keymap_item = keymap.keymap_items.new(
                idname='stepextrude.step_extrude',
                type='E',
                value='PRESS',
                ctrl=True,
                shift=True
            )
            cls._keymaps.append((keymap, keymap_item))

    @classmethod
    def unregister(cls):
        for keymap, keymap_item in cls._keymaps:
            keymap.keymap_items.remove(keymap_item)
        cls._keymaps.clear()


# REGISTER

def register(ui=True):
    register_class(StepExtrude_OT_step_extrude)
    StepExtrudeKeyMap.register(context=bpy.context)
    if ui:
        register_class(StepExtrude_PT_panel)


def unregister(ui=True):
    if ui:
        unregister_class(StepExtrude_PT_panel)
    StepExtrudeKeyMap.unregister()
    unregister_class(StepExtrude_OT_step_extrude)


if __name__ == "__main__":
    register()
