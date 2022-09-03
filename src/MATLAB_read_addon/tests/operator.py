class YourOperator(bpy.types.Operator):
    bl_idname = "youroperatorname"
    bl_label = "Your Operator"

    _updating = False
    _calcs_done = False
    _timer = None

    def do_calcs(self):
        # would be good if you can break up your calcs
        # so when looping over a list, you could do batches
        # of 10 or so by slicing through it.
        # do your calcs here and when finally done
       _calcs_done = True

    def modal(self, context, event):
        if event.type == 'TIMER' and not self._updating:
            self._updating = True
            self.do_calcs()
            self._updating = False
        if _calcs_done:
            self.cancel(context)

        return {'PASS_THROUGH'}

    def execute(self, context):
        context.window_manager.modal_handler_add(self)
        self._updating = False
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self._timer = None
        return {'CANCELLED'}