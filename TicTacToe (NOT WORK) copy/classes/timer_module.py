from kivy.graphics import Color, Line
from dep.modern_gridlayout import MDN_GridLayout


# ===== Timer_Module Class ===== #
class Timer_Module(MDN_GridLayout):

    # init method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_angle = 0
        self.stop_angle = 360

    # _mdn_update_label_graphic_outline method
    def _mdn_update_gridlayout_graphic_outline(self):
        """
            Mdn_Update_Label_Outline is a private function. The purpose of this function is to update the graphic/ui outline of the label\n
        """
        # Get device size
        mdn_device_size = self._mdn_get_device_size()

        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size
        mdn_outline_ref = self.mdn_outline[mdn_device_size]

        # Create the outline
        self.canvas.after.clear()
        if mdn_outline_ref[0][3] == 0 or mdn_outline_ref[1] == 0: return
        with self.canvas.after:
            Color(*self._mdn_get_rgba(mdn_outline_ref[0]))
            Line(circle = (self.center_x, self.center_y, min(self.width, self.height) / 2, self.current_angle, self.stop_angle), width = mdn_outline_ref[1])


