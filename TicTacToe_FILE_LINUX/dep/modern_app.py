import ctypes
from kivymd.app import MDApp
from screeninfo import get_monitors
from kivy.core.window import Window

# ---------------------------------------------------------------------- #
#                                                                        #
#                            Modern App Class                            #
#                                                                        #
# ---------------------------------------------------------------------- #
# +----------------------------------------------------------------------+ 
# | Description:                                                         |
# |      MDN_App aka(Modern App) is a modernized app with many different |
# |  tools and features. The app will store the screeenmanager, declare  |
# |  device breakpoints, and store the screens that are in the app       |
# |                                                                      |
# | Local Variables:                                                     |
# |     mdn_app_name:                                                    |
# |         type: 'str'                                                  |
# |         description: The name of the app                             |
# |                                                                      |
# |     mdn_screenmanager:                                               |
# |         type: <kivy_screenmanager>                                   |
# |         description: This is a reference of the screenmanager        |
# |                                                                      |
# |     mdn_window_resizable:                                            |
# |         type: 'bool'                                                 |
# |         description: Determines if the window can be resized or not  |
# |                                                                      |
# |     mdn_min_window_size:                                             |
# |         type: 'tuple'                                                |
# |         description: The min size of the window can be resized to    |
# |                                                                      |
# |     mdn_max_window_size:                                             |
# |         type: 'tuple'                                                |
# |         description: The max size of the window can be resized to    |
# |                                                                      |
# |     mdn_device_breakpoints:                                          |
# |         type: 'dictionary'                                           |
# |         description: The sizes for each breakpoint (desktop, tablet  |  
# |                      mobile) (eg. tablet: [800, 1200])               |
# |                                                                      |
# |     mdn_window_size:                                                 |
# |         type: 'tuple'                                                |
# |         description: The default size of the window                  |
# |                                                                      |
# |     mdn_window_pos:                                                  |
# |         type: 'tuple'                                                |
# |         description: The default pos of the window                   |
# |                                                                      |
# |     mdn_app_icon:                                                    |
# |         type: 'str'                                                  |
# |         description: Path to find the icon for the app               |
# |                                                                      |
# |     mdn_allow_screensaver:                                           |
# |         type: 'bool'                                                 |
# |         description: Determines if desktop screensaver should run    |
# |                      if app is running                               |
# |                                                                      |
# |     mdn_default_font_size:                                           |
# |         type: 'int'                                                  |
# |         description: Determines the default font size for the entire |
# |                      app, so it doesn't have to be specified all the |
# |                      time.                                           |
# |                                                                      |
# +----------------------------------------------------------------------+

class MDN_App(MDApp):
    """
    Description:
        MDN_App aka(Modern App) is a modernized app with many different tools and features. The app will store the screeenmanager, declare device breakpoints, and store the screens that are in the app\n
    Local Variables:
        mdn_app_name, 
        mdn_screenmanager, 
        mdn_window_resizable, 
        mdn_min_window_size,
        mdn_max_window_size, 
        mdn_device_breakpoints, 
        mdn_window_size, 
        mdn_window_pos, 
        mdn_app_icon, 
        mdn_allow_screensaver,
        mdn_default_font_size
    """
    # init function
    def __init__(self, **kwargs):
        super().__init__()
        # Set 'mdn_app_name' variable
        self.mdn_app_name = "My App"

        # Set 'mdn_screenmanager' variable
        self.mdn_screenmanager = None

        # Set 'mdn_window_resizable' variable
        self.mdn_window_resizable = True

        # Set 'mdn_min_window_size' variable
        self.mdn_min_window_size = (250, 300)

        # Set 'mdn_max_window_size' variable
        self.mdn_max_window_size = (1500, 1500)

        # Set 'mdn_device_breakpoints' variable
        self.mdn_device_breakpoints = {"desktop": [3000], "tablet": [1000, 2999], "mobile": [0, 999]}

        # Set 'mdn_window_size' variable
        self.mdn_window_size = (1000, 800)

        # Set 'mdn_window_size' variable
        self.mdn_window_size = "center"

        # Set 'mdn_app_icon' variable
        self.mdn_app_icon = "py_includes/default_icon.png"

        # Set 'mdn_allow_screensaver' variable
        self.mdn_allow_screensaver = True

        # Set 'mdn_default_font_size' variable
        self.mdn_default_font_size = {
            "desktop": 30,
            "tablet": 25,
            "mobile": 20,
        }

        # Bind function and call functions to the resizing of the window
        Window.bind(size = self._mdn_resize_window)
        self._mdn_update_app_params(kwargs)
        self._mdn_position_window()

    # _mdn_update_app_params method
    def _mdn_update_app_params(self, kwargs):
        """
            Mdn_Update_App_Params is a private method. The purpose of the method is to update the parameters of this class. This method will SHOULD be called once during the running of the app!!!!
        """

        # Assign args["mdn_app_name"] to the self.mdn_app_name
        if "mdn_app_name" in kwargs: self.mdn_app_name = kwargs["mdn_app_name"]

        # Assign kwargs["mdn_screenmanager"] to the self.mdn_screenmanager
        if "mdn_screenmanager" in kwargs: self.mdn_screenmanager = kwargs["mdn_screenmanager"]

        # Assign kwargs["mdn_window_resizable"] to the self.mdn_window_resizable
        if "mdn_window_resizable" in kwargs: self.mdn_window_resizable = kwargs["mdn_window_resizable"]

        # Assign kwargs["mdn_min_window_size"] to the self.mdn_min_window_size
        if "mdn_min_window_size" in kwargs: self.mdn_min_window_size = kwargs["mdn_min_window_size"]

        # Assign kwargs["mdn_max_window_size"] to the self.mdn_max_window_size
        if "mdn_max_window_size" in kwargs: self.mdn_max_window_size = kwargs["mdn_max_window_size"]

        # Assign kwargs["mdn_device_breakpoints"] to the self.mdn_device_breakpoints
        if "mdn_device_breakpoints" in kwargs: self.mdn_device_breakpoints = kwargs["mdn_device_breakpoints"]

        # Assign kwargs["mdn_window_size"] to the self.mdn_window_size
        if "mdn_window_size" in kwargs: self.mdn_window_size = kwargs["mdn_window_size"]

        # Assign kwargs["mdn_window_pos"] to the self.mdn_window_pos
        if "mdn_window_pos" in kwargs: self.mdn_window_pos = kwargs["mdn_window_pos"]

        # Assign kwargs["mdn_app_icon"] to the self.mdn_app_icon
        if "mdn_app_icon" in kwargs: self.mdn_app_icon = kwargs["mdn_app_icon"]

        # Assign kwargs["mdn_allow_screensaver"] to the "self.mdn_allow_screensaver"
        if "mdn_allow_screensaver" in kwargs: self.mdn_allow_screensaver = kwargs["mdn_allow_screensaver"]

        # Assign kwargs["mdn_default_font_size"] to the "self.mdn_default_font_size"
        if "mdn_default_font_size" in kwargs: self.mdn_default_font_size = kwargs["mdn_default_font_size"]

        # Call the update method
        self._mdn_update_app()

    # _mdn_update_app method
    def _mdn_update_app(self):
        """
           Mdn_Update_App is a private method. The purpose of this method is to update the app and the graphic parameters.
        """
        # Set the actual window size
        Window.size = self.mdn_window_size

        # Set the minimum window width
        Window.minimum_width = self.mdn_min_window_size[0]

        # Set the minimum window height
        Window.minimum_height = self.mdn_min_window_size[1]

        # Set the app icon
        self.icon = self.mdn_app_icon

        # Set the screensaver option. If False, the screensaver will be prevented to operate
        self.allow_screensaver = self.mdn_allow_screensaver

    # _mdn_resize_window method
    def _mdn_resize_window(self, *args):
        """
           Mdn_Resize_Window is a private method. The purpose of this method is to update the size of the window. This will prevent the size of the window to get smaller than the 'mdn_min_window_size' variable. This will also work on the when the window is resized to get larger.
        """
        # If 'mdn_window_resizeable' is False, then exit this function
        if not self.mdn_window_resizable: 
            Window.size = self.mdn_window_size
            return

        # If window size is greater than the 'mdn_max_window_size', then shrink it to the max size and exit this function
        if Window.size[0]/2 >= self.mdn_max_window_size[0] and Window.size[1]/2 >= self.mdn_max_window_size[1]:
            Window.size = self.mdn_max_window_size
            return

        # If window size is greater than the 'mdn_max_window_size[0]' var, then reset its width
        if Window.size[0]/2 >= self.mdn_max_window_size[0]:
            Window.size = (self.mdn_max_window_size[0], Window.size[1]/2)
            return

        # If window size is greater than the 'mdn_max_window_size[0]' var, then reset its width
        if Window.size[1]/2 >= self.mdn_max_window_size[1]:
            Window.size = (Window.size[0]/2, self.mdn_max_window_size[1])
            return

    # mdn_position_window method
    def _mdn_position_window(self):
        """
           Mdn_Position Window is a private method. The purpose of this method is to position the app window on the screen. A position can be specified or one can use the default values: 
           Top: top_left, top_center, top_right,
           Center: center_left, center, center_right
           Bottom: bottom_left, bottom_center, bottom_right
        """ 
        # This is the ref variable of the 'self.mdn_window_pos'. This will hold the default position of the window when ran
        pos_ref = self.mdn_window_pos

        # If the pos_ref var is a tuple, then take this path
        if type(pos_ref) == tuple:
            Window.top = pos_ref[0]
            Window.left = pos_ref[1]

        # If the pos_ref var is a string, then take this path
        if type(pos_ref) == str:
            pos_ref = pos_ref.split("_")
            if len(pos_ref) == 2:
                if pos_ref[0] == "top": Window.top = 0 
                if pos_ref[0] == "center": Window.top = (get_monitors()[0].height - self.mdn_window_size[1]) / 2
                if pos_ref[0] == "bottom": Window.top = (get_monitors()[0].height - self.mdn_window_size[1])
                if pos_ref[1] == "left":  Window.left = 0
                if pos_ref[1] == "center": Window.left = (get_monitors()[0].width - self.mdn_window_size[0]) / 2
                if pos_ref[1] == "right": Window.left = (get_monitors()[0].width - self.mdn_window_size[0])
            elif len(pos_ref) == 1 and pos_ref[0] == "center" :
                Window.top = (get_monitors()[0].height - self.mdn_window_size[1]) / 2
                Window.left = (get_monitors()[0].width - self.mdn_window_size[0]) / 2
            else:
                print("Incorrect position was specified!!")