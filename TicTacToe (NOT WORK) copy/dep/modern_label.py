from functools import partial
import random, string
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.graphics.texture import Texture
from kivymd.utils.fitimage import FitImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line

# ---------------------------------------------------------------------- #
#                                                                        #
#                            Modern Label Class                          #
#                                                                        #
# ---------------------------------------------------------------------- #
# +----------------------------------------------------------------------+ 
# | Description:                                                         |
# |     MDN_Label aka(Modern Label) is a new modernized label class with |
# | many different tools and features. This classs will store the app    |
# | and the ids that belong to the class                                 |
# |                                                                      |
# | Local Variables:                                                     |
# |     mdn_app:                                                         |
# |         type: <kivy_app>                                             |
# |         description: This is a reference of the app                  |
# |                                                                      |
# |     mdn_bg_kv:                                                       |
# |         type: <gridlayout>                                           |
# |         description: This is the background of the label. It can be  |
# |                      used for color or gradient, not img!            |
# |                                                                      |
# |     mdn_rel_bg_kv:                                                   |
# |         type: <relativelayout>                                       |
# |         description: This is the relativelayout of the background.   |
# |                      This is only the parent container               |
# |                                                                      |
# |     mdn_bg_img_kv:                                                   |
# |         type: <AsyncImage> or <CoverImage>                           |
# |         description: This is the background image of the label, if   |
# |                      a background image exists                       |
# |                                                                      |
# |     mdn_rel_bg_img_kv:                                               |
# |         type: <relativelayout>                                       |
# |         description: This is the relativelayout of the background img|
# |                      This is only the parent container               |
# |                                                                      |
# |     mdn_label_kv:                                                    |
# |         type: <label>                                                |
# |         description: This is the actual label widget. This displays  |
# |                      the text                                        |
# |                                                                      |
# |     mdn_rel_label_kv:                                                |
# |         type: <relativelayout>                                       |
# |         description: This is the relativelayout of the label         |
# |                      This is only the parent container               |
# |                                                                      |
# |     mdn_id:                                                          |
# |         type: 'str'                                                  |
# |         description: This is the unique id for this widget. This     |
# |                      will be stored in the screen's 'screen_ids' var |
# |                                                                      |
# |     mdn_breakpoints:                                                 |
# |         type: 'dict'                                                 |
# |         description: This is the breakpoints for each of the device  |
# |                      sizes. This will be created if it can't be get  |
# |                      from the app variable                           |
# |                                                                      |
# |     mdn_outline:                                                     |
# |         type: 'list'                                                 |
# |         description: This holds the params for outline               |
# |         eg. [[235, 64, 52], 10]                                      |
# |                                                                      |
# |     mdn_outline_joint:                                               |
# |         type: 'str'                                                  |
# |         description: This holds the params for outline joint         |
# |         Options are: mitre, round, bevel                             | 
# |                                                                      |
# |     mdn_radius:                                                      |
# |         type: 'list'                                                 |
# |         description: This holds the params for radius                |
# |         eg. [20, 35, 20, 35]                                         |
# |                                                                      |
# |     mdn_size:                                                        |
# |         type: 'list'                                                 |
# |         description: This holds the params for size                  |
# |         eg. ["50%", "200un"]                                         |
# |                                                                      |
# |     mdn_bg:                                                          |
# |         type: 'dict'                                                 |
# |         description: This holds the params for dict                  |
# |         eg. color: {"desktop": , "tablet": None, "mobile": None}     |
# |                                                                      |
# |     mdn_font_color:                                                  |
# |         type: 'list'                                                 |
# |         description: This holds the params for text color            |
# |         eg. [20, 30, 54, 1]                                          |
# |                                                                      |
# |     mdn_font_size:                                                   |
# |         type: 'int'                                                  |
# |         description: This holds the params for font size             |
# |         eg. 30                                                       |
# |                                                                      |
# |     mdn_font_style:                                                  |
# |         type: 'list'                                                 |
# |         description: This holds the params for font style            |
# |         Options are: italic, bold, underline                         |
# |                                                                      |
# |     mdn_text:                                                        |
# |         type: 'str'                                                  |
# |         description: This is the actual text of the label widget     |
# |                                                                      |
# |     mdn_line_height:                                                 |
# |         type: 'float'                                                |
# |         description: This determines the line height of the text     |
# |                                                                      |
# |     mdn_text_align:                                                  |
# |         type: 'list'                                                 |
# |         description: This determines the align of the text           |
# |         eg. ["center", "center"]                                     |
# |                                                                      |
# |     mdn_text_size:                                                   |
# |         type: 'str'                                                  |
# |         description: This determines the size of the text size. By   |
# |                      default its '100%', so it will take up the      |
# |                      entire label.                                   |
# |                                                                      |
# |     mdn_text_bg:                                                     |
# |         type: 'list'                                                 |
# |         description: This is background for the text or label widget |
# |                      Color only works for this param, not img or     |
# |                      gradients                                       |
# |         eg. [142, 16, 232, 1]                                        |
# |                                                                      |
# +----------------------------------------------------------------------+

class MDN_Label(Label):
    """
    Description:
        MDN_Label aka(Modern Label) is a new modernized label class with many different tools and features. This classs will store the app and the ids that belong to the class\n
    Local Variables:
        mdn_app,
        mdn_bg_kv,
        mdn_rel_bg_kv,
        mdn_bg_img_kv,
        mdn_rel_bg_img_kv,
        mdn_label_kv,
        mdn_rel_label_kv,
        mdn_id,
        mdn_breakpoints,
        mdn_outline,
        mdn_outline_joint,
        mdn_radius,
        mdn_size,
        mdn_bg,
        mdn_font_color,
        mdn_font_size,
        mdn_font_style,
        mdn_text,
        mdn_line_height,
        mdn_text_align,
        mdn_text_size,
        mdn_text_bg
    """
    # init function
    def __init__(self, **kwargs):
        super().__init__()
        # ========= DEFAULT PARAMETERS ========= #
        # Set the columns
        self.cols = 1

        # # Set the rows
        self.rows = 4

        # Set the size_hint
        self.size_hint = (None, None)

        # Set the app
        try: self.mdn_app = kwargs["mdn_app"]
        except: self.mdn_app = None

        # Set bg & rel_bg widget
        self.mdn_bg_kv = None
        self.mdn_rel_bg_kv = None

        # Set bg_image & rel_bg_image widget
        self.mdn_bg_img_kv = None
        self.mdn_rel_bg_img_kv = None

        # Set label & rel_label widget
        self.mdn_label_kv = None
        self.mdn_rel_label_kv = None 

        # Set the id
        if self.mdn_app:
            if "mdn_id" in kwargs: 
                self.mdn_id = kwargs["mdn_id"]
                try: self.mdn_app.mdn_screenmanager.get_screen(self.mdn_app.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self
                except: pass
            else: 
                self.mdn_id = 'mdn_label_{}'.format("".join(random.choice(string.ascii_lowercase) for i in range(10)))
                self.mdn_app.mdn_screenmanager.get_screen(self.mdn_app.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self
        else:
            self.mdn_id = None

        # Set the breakpoints
        if self.mdn_app:
            if "mdn_breakpoints" in kwargs: self.mdn_breakpoints = kwargs["mdn_breakpoints"]
            elif self.mdn_app.mdn_device_breakpoints: self.mdn_breakpoints = self.mdn_app.mdn_device_breakpoints
            else: self.mdn_breakpoints = self.mdn_app.mdn_device_breakpoints = {"desktop": [3000], "tablet": [1000, 2999], "mobile": [0, 999]}
        else:
            self.mdn_breakpoints = None
        # ========= LABEL PARAMETERS ========= #
        # Set the "mdn_outline" variable...
        self.mdn_outline = {
            "desktop": [[0, 0, 0, 0], 0],
            "tablet": [[0, 0, 0, 0], 0],
            "mobile": [[0, 0, 0, 0], 0],
        }

        # Set the "mdn_outline_joint" variable...
        self.mdn_outline_joint = {
            "desktop": "miter",
            "tablet": "miter",
            "mobile": "miter",
        }

        # Set the "mdn_radius" variable...
        self.mdn_radius = {
            "desktop": [0, 0, 0, 0],
            "tablet": [0, 0, 0, 0],
            "mobile": [0, 0, 0, 0],
        }

        # Set the "mdn_size" variable...
        self.mdn_size = {
            "desktop": ["100%", "100%"],
            "tablet": ["100%", "100%"],
            "mobile": ["100%", "100%"],
        }

        # Set the "mdn_bg" variable...
        self.mdn_bg = {
            "color": {"desktop": None, "tablet": None, "mobile": None},
            "gradient": {"desktop": None, "tablet": None, "mobile": None},
            "image": {"desktop": None, "tablet": None, "mobile": None}
        }
        # ========= TEXT PARAMETERS ========= #
        # Set the "mdn_font_color" variable...
        self.mdn_font_color = {
            "desktop": [0, 0, 0, 1],
            "tablet": [0, 0, 0, 1],
            "mobile": [0, 0, 0, 1],
        }

        # Set the "mdn_font_size" variable...
        if self.mdn_app:
            try: 
                self.mdn_font_size = {
                    "desktop": self.mdn_app.mdn_default_font_size["desktop"],
                    "tablet": self.mdn_app.mdn_default_font_size["tablet"],
                    "mobile": self.mdn_app.mdn_default_font_size["mobile"],
                }
            except: 
                self.mdn_font_size = {
                    "desktop": 30,
                    "tablet": 25,
                    "mobile": 20,
                }
        else:
            self.mdn_font_size = {
                "desktop": 30,
                "tablet": 25,
                "mobile": 20,
            }

        # Set the "mdn_font_style" variable
        self.mdn_font_style = {
            "desktop": [],
            "tablet": [],
            "mobile": [],
        }

        # Set the "mdn_text" variable...
        self.mdn_text = {
            "desktop": None,
            "tablet": None,
            "mobile": None,
        }

        # Set the "mdn_line_height" variable...
        self.mdn_line_height = {
            "desktop": 1.0,
            "tablet": 1.0,
            "mobile": 1.0,
        }

        # Set the "mdn_text_size" variable...
        self.mdn_text_size = {
            "desktop": "100%",
            "tablet": "100%",
            "mobile": "100%",
        }

        # Set the "mdn_text_bg" variable...
        self.mdn_text_bg = {
            "desktop": None,
            "tablet": None,
            "mobile": None,
        }

        # Set the "mdn_text_align" variable...
        self.mdn_text_align = {
            "desktop": ["center", "center"],
            "tablet": ["center", "center"],
            "mobile": ["center", "center"],
        }

        # If the 'mdn_app' isn't set, then take this path
        if not self.mdn_app:
            self._mdn_get_mdn_app(kwargs)
            return

        # Update the graphics
        self._get_parent()
        self.mdn_update(kwargs)
        self.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)
        self.mdn_app.mdn_screenmanager.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)

    # mdn_update method
    def mdn_update(self, kwargs):
        """
            MDN_Update is public function. Here you pass the arguments you wish to update or initialize.\n
            Example use: 
                Here we are calling the label is created and we are calling the mdn_update function to update the mdn_text variable
                    Example 1: mdn_update(mdn_text = 'hello')

                Here we are creating the label and initializing the mdn_text variable at the same time     
                    Example 2: MDN_Button(mdn_text = 'hello')
        """
        # ========== LABEL PARAMETERS ========== #
        if "mdn_outline" in kwargs: self._mdn_update_param("mdn_outline", kwargs["mdn_outline"])
        if "mdn_outline_joint" in kwargs: self._mdn_update_param("mdn_outline_joint", kwargs["mdn_outline_joint"])
        if "mdn_radius" in kwargs: self._mdn_update_param("mdn_radius", kwargs["mdn_radius"])
        if "mdn_size" in kwargs: self._mdn_update_param("mdn_size", kwargs["mdn_size"])
        if "mdn_bg" in kwargs: self._mdn_update_param("mdn_bg", kwargs["mdn_bg"])
        # ========= TEXT PARAMETERS ========= #
        if "mdn_font_color" in kwargs: self._mdn_update_param("mdn_font_color", kwargs["mdn_font_color"])
        if "mdn_font_size" in kwargs: self._mdn_update_param("mdn_font_size", kwargs["mdn_font_size"])
        if "mdn_font_style" in kwargs: self._mdn_update_param("mdn_font_style", kwargs["mdn_font_style"])
        if "mdn_text" in kwargs: self._mdn_update_param("mdn_text", kwargs["mdn_text"])
        if "mdn_line_height" in kwargs: self._mdn_update_param("mdn_line_height", kwargs["mdn_line_height"])
        if "mdn_text_size" in kwargs: self._mdn_update_param("mdn_text_size", kwargs["mdn_text_size"])
        if "mdn_text_bg" in kwargs: self._mdn_update_param("mdn_text_bg", kwargs["mdn_text_bg"])
        if "mdn_text_align" in kwargs: self._mdn_update_param("mdn_text_align", kwargs["mdn_text_align"])
        self._mdn_update_graphic()    

    # _mdn_update_param method
    def _mdn_update_param(self, arg_name, arg_value):
        """
            MDN_Update_Param is private function. The purpose of this function is to actually update the variables. NOTE: This only updates the values, but not the graphics. But the graphics won't change unless the values change, so even though this function doesn't update the graphics directly it updates the values, so the graphics will change.\n
            Example use: 
                Here the label is created and we are calling the mdn_update function to update the mdn_text variable
                    Example 1: 
                        mdn_text = {'desktop': '', 'tablet': '', 'mobile': ''}
                        mdn_update(mdn_text = 'hello')
                        mdn_update -> mdn_update_param
                        mdn_text = {'desktop': 'hello', 'tablet': 'hello', 'mobile': 'hello'}
        """
        # This variable 'mdn_update_variable_ref' is a reference to the actual variable
        # Modifing this one, will modify the real variable, because the variable type is a dict
        mdn_update_variable_ref = None

        # Assign the mdn_update_variable_ref variable to the actual variable
        if arg_name == "mdn_outline": mdn_update_variable_ref = self.mdn_outline
        if arg_name == "mdn_outline_joint": mdn_update_variable_ref = self.mdn_outline_joint
        if arg_name == "mdn_radius": mdn_update_variable_ref = self.mdn_radius
        if arg_name == "mdn_size": mdn_update_variable_ref = self.mdn_size
        if arg_name == "mdn_bg": mdn_update_variable_ref = self.mdn_bg
        if arg_name == "mdn_font_color": mdn_update_variable_ref = self.mdn_font_color
        if arg_name == "mdn_font_size": mdn_update_variable_ref = self.mdn_font_size
        if arg_name == "mdn_font_style": mdn_update_variable_ref = self.mdn_font_style
        if arg_name == "mdn_text": mdn_update_variable_ref = self.mdn_text
        if arg_name == "mdn_line_height": mdn_update_variable_ref = self.mdn_line_height
        if arg_name == "mdn_text_size": mdn_update_variable_ref = self.mdn_text_size
        if arg_name == "mdn_text_bg": mdn_update_variable_ref = self.mdn_text_bg
        if arg_name == "mdn_text_align": mdn_update_variable_ref = self.mdn_text_align

        # If 'mdn_update_variable_ref' == None, then return function
        if mdn_update_variable_ref == None: return

        # If 'arg_name' is not 'mdn_bg' then take this path
        if arg_name != "mdn_bg":
            if type(arg_value) != dict:
                for mdn_breakpoint in ["desktop", "tablet", "mobile"]: mdn_update_variable_ref[mdn_breakpoint] = arg_value
            else:
                for mdn_breakpoint in list(arg_value.keys()): mdn_update_variable_ref[mdn_breakpoint] = arg_value[mdn_breakpoint]
            if arg_name == "mdn_radius": self._mdn_convert_radius(self.mdn_radius)
            if arg_name == "mdn_text_radius": self._mdn_convert_radius(self.mdn_text_radius)
            return
        # Elif 'arg_name' is 'mdn_bg' then take this path
        elif arg_name == "mdn_bg":
            for bg_type in list(arg_value.keys()):
                if type(arg_value[bg_type]) != dict:
                    for mdn_breakpoint in ["desktop", "tablet", "mobile"]: mdn_update_variable_ref[bg_type][mdn_breakpoint] = arg_value[bg_type]
                else:
                    for mdn_breakpoint in list(arg_value[bg_type].keys()): 
                        mdn_update_variable_ref[bg_type][mdn_breakpoint] = arg_value[bg_type][mdn_breakpoint]

    # _mdn_get_mdn_app method
    def _mdn_get_mdn_app(self, *args):
        """
            Mdn_Get_Mdn_App is a private method. This will get the 'mdn_app' variable from the screen. This will continue to loop and prevent any other function from running until gets the variable
        """
        # If parent window doesn't exist right now, then keep looping
        if not self.get_parent_window():
            Clock.schedule_once(partial(self._mdn_get_mdn_app, args), .5)
            return

        # Get the args variable
        args = args[0][0]

        # Set the 'mdn_app' variable
        self.mdn_app = Window.children[0].current_screen.mdn_app
    
        # Set the id
        if "mdn_id" in args: 
            self.mdn_id = args["mdn_id"]
            self.mdn_app.mdn_screenmanager.get_screen(self.mdn_app.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self
        elif not self.mdn_id: 
            self.mdn_id = 'mdn_label_{}'.format("".join(random.choice(string.ascii_lowercase) for i in range(10)))
            self.mdn_app.mdn_screenmanager.get_screen(self.mdn_app.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self

        # Set the breakpoints
        if not self.mdn_breakpoints:
            if "mdn_breakpoints" in args: self.mdn_breakpoints = args["mdn_breakpoints"]
            elif self.mdn_app.mdn_device_breakpoints: self.mdn_breakpoints = self.mdn_app.mdn_device_breakpoints
            else: self.mdn_breakpoints = self.mdn_app.mdn_device_breakpoints = {"desktop": [3000], "tablet": [1000, 2999], "mobile": [0, 999]}

        # Set the "mdn_font_size" variable...
        if not self.mdn_font_size:
            try: 
                self.mdn_font_size = {
                    "desktop": self.mdn_app.mdn_default_font_size["desktop"],
                    "tablet": self.mdn_app.mdn_default_font_size["tablet"],
                    "mobile": self.mdn_app.mdn_default_font_size["mobile"],
                }
            except: 
                self.mdn_font_size = {
                    "desktop": 30,
                    "tablet": 25,
                    "mobile": 20,
                }
        self._get_parent()
        self.mdn_update(args)
        self.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)
        self.parent.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)
        self.mdn_app.mdn_screenmanager.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)

    # _get_parent method
    def _get_parent(self, *args):
        """
            Get_Parent is a private method. The purpose of this function is to get the parent. This is in order so that if the parent updates, the widget will also update
        """
        if not self.parent:
            Clock.schedule_once(self._get_parent, 1)
            return

        self.parent.bind(pos = self._mdn_update_graphic, size = self._mdn_update_graphic)

    # _mdn_convert_radius method
    def _mdn_convert_radius(self, radius):
        """
            Mdn_Convert_Radius is private function. The purpose of this function is to convert the radius variable to an array with four objects/numbers.\n
            Example use: 
                Example: 
                    mdn_radius = {'desktop': [0, 0, 0, 0], 'tablet': [0, 0, 0, 0], 'mobile': [0, 0, 0, 0]}
                    mdn_update(mdn_radius = [30, 20])
                    mdn_update -> mdn_update_param -> mdn_convert_radius
                    mdn_radius = {'desktop': [30, 20, 30, 20], 'tablet': [30, 20, 30, 20], 'mobile': [30, 20, 30, 20]}
        """
        # Loop through and check if each radius needs to be modified
        for mdn_breakpoint in ["desktop", "tablet", "mobile"]:
            if len(radius[mdn_breakpoint]) == 1: radius[mdn_breakpoint] = [radius[mdn_breakpoint][0], radius[mdn_breakpoint][0], radius[mdn_breakpoint][0], radius[mdn_breakpoint][0]]
            if len(radius[mdn_breakpoint]) == 2: radius[mdn_breakpoint] = [radius[mdn_breakpoint][0], radius[mdn_breakpoint][1], radius[mdn_breakpoint][0], radius[mdn_breakpoint][1]]
            if len(radius[mdn_breakpoint]) == 3: radius[mdn_breakpoint] = [radius[mdn_breakpoint][0], radius[mdn_breakpoint][1], radius[mdn_breakpoint][2], radius[mdn_breakpoint][1]]

    # _mdn_get_device_size method
    def _mdn_get_device_size(self):
        """
            Mdn_Get_Device_Size is a private function. The purpose of this function is to determine the appropriate device label according to the size of the app window.\n
            Example:
                Window.size = (500, 1000)
                print(mdn_get_device_size()) -> 'mobile'
        """
        if Window.width >= self.mdn_breakpoints["mobile"][0] and Window.width <= self.mdn_breakpoints["mobile"][1]: return "mobile"
        if Window.width >= self.mdn_breakpoints["tablet"][0] and Window.width <= self.mdn_breakpoints["tablet"][1]: return "tablet"
        return "desktop"

    # _mdn_get_rgba method
    def _mdn_get_rgba(self, rgba):
        """
            Mdn_Get_RGBA is a private function. The purpose of this function is to convert an rgba and divide it by 255 so it can be used by the kivy module\n
        """
        new_rgba = []
        for i in range(0, 3):new_rgba.append(rgba[i]/255)
        new_rgba.append(rgba[3])
        return new_rgba

    # _mdn_update_graphic method
    def _mdn_update_graphic(self, *args):
        """
            Mdn_Update_Graphic is a private function. The purpose of this function is to call all the subfunctions that are able to update the label graphics or ui\n
        """
        # If parent does not exists, return and run again .05sec later
        if not self.parent: 
            Clock.schedule_once(self._mdn_update_graphic, .05)
            return
        
        # Call all the subfunctions needed to change the graphic/ui
        self._mdn_update_label_graphic_size()
        self._mdn_update_label_graphic_outline()
        self._mdn_update_label_graphic_bg()
        self._mdn_update_label_graphic_text()

    # _mdn_update_label_graphic_size method
    def _mdn_update_label_graphic_size(self, *args):
        """
            Mdn_Update_Label_Size is a private function. The purpose of this function is to update the graphic/ui size of the label\n
        """
        # Get device size
        mdn_device_size = self._mdn_get_device_size()

        # 'mdn_size_ref' will be a reference variable of the real variable for the current device size
        mdn_size_ref = self.mdn_size[mdn_device_size]

        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size
        # The purpose of this variable is to get the width of the outline and shrink the size of the label by the size of the outline
        # This to prevent the label from spanning out of its container
        # Example:
        #   If the label is 26x30 and has an outline of 10units, then without considering the outline the label actually would be 36x40, because the outline has a width of 10units. But with the following statements of code we are getting the outline, multiplying it by 2, because there is an outline on each side of the label, then we shrink the label according to the outline. So instead of making the label 26x30 instead the label will be 16x20, so the outline will make the label be 26x30. Kindof like box-sizing:border-box in css,
 
        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size 
        mdn_outline_ref = self.mdn_outline[mdn_device_size][1]*2

        # 'mdn_text_ref' will be a reference variable of the real variable for the current device size 
        mdn_text_ref = self.mdn_text[mdn_device_size]

        # If the size, should be the size of the text, then take this path
        if mdn_size_ref == "min_size":
            if mdn_text_ref:
                if not self.mdn_label_kv:
                    Clock.schedule_once(self._mdn_update_label_graphic_size, .01)
                    return
                self.size = self.mdn_label_kv.texture_size
                return

        # If the width should be the size of the width of the text, then take this path
        if mdn_size_ref[0] == "min_width":
            if mdn_text_ref:
                if not self.mdn_label_kv:
                    Clock.schedule_once(self._mdn_update_label_graphic_size, 1)
                    return
                self.width = self.mdn_label_kv.texture_size[0]
        else:
            # Update the width
            if 'un' in mdn_size_ref[0]: self.width = int(mdn_size_ref[0][:mdn_size_ref[0].index("un")])-mdn_outline_ref
            else: self.width = self.parent.width*(int(mdn_size_ref[0][:mdn_size_ref[0].index("%")])/100)-mdn_outline_ref

        # If the height should be the size of the height of the text, then take this path
        if mdn_size_ref[1] == "min_height":
            if mdn_text_ref:
                if not self.mdn_label_kv:
                    Clock.schedule_once(self._mdn_update_label_graphic_size, 1)
                    return
                self.mdn_label_kv.text_size = [100, self.mdn_label_kv.texture_size[1]]
                self.height = self.mdn_label_kv.texture_size[1]
        else:
            # Update the height
            if 'un' in mdn_size_ref[1]: self.height = int(mdn_size_ref[1][:mdn_size_ref[1].index("un")])
            else: self.height = self.parent.height*(int(mdn_size_ref[1][:mdn_size_ref[1].index("%")])/100)-mdn_outline_ref

    # _mdn_update_label_graphic_outline method
    def _mdn_update_label_graphic_outline(self):
        """
            Mdn_Update_Label_Outline is a private function. The purpose of this function is to update the graphic/ui outline of the label\n
        """
        # Get device size
        mdn_device_size = self._mdn_get_device_size()

        # 'mdn_radius_ref' will be a reference variable of the real variable for the current device size
        mdn_radius_ref = self.mdn_radius[mdn_device_size]

        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size
        mdn_outline_ref = self.mdn_outline[mdn_device_size]

        # 'mdn_outline_joint_ref' will be a reference variable of the real variable for the current device size
        mdn_outline_joint_ref = self.mdn_outline_joint[mdn_device_size]

        # Create the outline
        self.canvas.after.clear()
        if mdn_outline_ref[0][3] == 0 or mdn_outline_ref[1] == 0: return
        with self.canvas.after:
            Color(*self._mdn_get_rgba(mdn_outline_ref[0]))
            if mdn_radius_ref != [0, 0, 0, 0]:
                Line(rounded_rectangle = [self.x, self.y, self.width, self.height, *mdn_radius_ref], width = mdn_outline_ref[1])
            else:
                Line(rectangle = [self.x, self.y, self.width, self.height], width = mdn_outline_ref[1], joint = mdn_outline_joint_ref)  

    # _mdn_update_label_graphic_bg method
    def _mdn_update_label_graphic_bg(self):
        """
            Mdn_Update_Label_Outline is a private function. The purpose of this function is to update the graphic/ui background of the label\n
        """
        # Get device size
        mdn_device_size = self._mdn_get_device_size()

        # 'mdn_bg_ref' will be a reference variable of the real variable for the current device size
        mdn_bg_ref = {
            "color": self.mdn_bg["color"][mdn_device_size],
            "gradient": self.mdn_bg["gradient"][mdn_device_size],
            "image": self.mdn_bg["image"][mdn_device_size]
        }

        # 'mdn_radius_ref' will be a reference variable of the real variable for the current device size
        mdn_radius_ref = self.mdn_radius[mdn_device_size]

        # If image is set for the background, then take this path
        if mdn_bg_ref["image"] and mdn_bg_ref["image"][0]:
            if not self.mdn_bg_img_kv:
                self.mdn_bg_img_kv = AsyncImage() if mdn_bg_ref["image"][1] != "cover" else FitImage() 
                self.mdn_rel_bg_img_kv = RelativeLayout()
                self.mdn_rel_bg_img_kv.height = 1
                self.mdn_rel_bg_img_kv.size_hint = (1, None)
                self.mdn_bg_img_kv.size_hint = (None, None)
                self.mdn_rel_bg_img_kv.add_widget(self.mdn_bg_img_kv)
                self.add_widget(self.mdn_rel_bg_img_kv, index = 3)
            if mdn_bg_ref["image"][1] == "cover" and self.mdn_bg_img_kv.__class__.__name__ != "FitImage":
                self.mdn_bg_img_kv = FitImage()
                self.mdn_bg_img_kv.size_hint = (None, None)
                self.mdn_rel_bg_img_kv.clear_widgets()
                self.mdn_rel_bg_img_kv.add_widget(self.mdn_bg_img_kv)
            elif mdn_bg_ref["image"][1] != "cover" and self.mdn_bg_img_kv.__class__.__name__ == "FitImage":
                self.mdn_bg_img_kv = AsyncImage()
                self.mdn_bg_img_kv.size_hint = (None, None)
                self.mdn_rel_bg_img_kv.clear_widgets()
                self.mdn_rel_bg_img_kv.add_widget(self.mdn_bg_img_kv)
            if mdn_bg_ref["image"][1] == "stretch":
                self.mdn_bg_img_kv.keep_ratio = False
                self.mdn_bg_img_kv.allow_stretch = True
            self.mdn_bg_img_kv.size = self.size
            self.mdn_bg_img_kv.pos = [self.pos[0], self.pos[1]+2]
            self.mdn_bg_img_kv.source = mdn_bg_ref["image"][0]
        else:
            if self.mdn_bg_img_kv: self.mdn_bg_img_kv.source = "py_includes/blank.png"

        # If gradient is set for the background, then take this path
        if mdn_bg_ref["gradient"]:
            if not self.mdn_bg_kv:
                self.mdn_bg_kv = GridLayout()
                self.mdn_rel_bg_kv = RelativeLayout()
                self.mdn_rel_bg_kv.height = 1
                self.mdn_rel_bg_kv.size_hint = (1, None)
                self.mdn_bg_kv.size_hint = (1, None)
                self.mdn_rel_bg_kv.add_widget(self.mdn_bg_kv)
                self.add_widget(self.mdn_rel_bg_kv, index = 0)
            self.mdn_bg_kv.size = self.size
            self.mdn_bg_kv.pos = [self.pos[0], self.pos[1]+2]
            [gradient_arg, radius_arg] = [mdn_bg_ref["gradient"], mdn_radius_ref]
            [mdn_gradient, gradient] = [gradient_arg, []]
            gradient_texture = Texture.create(size = (len(mdn_gradient[0]), len(mdn_gradient)), colorfmt = "rgba")
            for palette in mdn_gradient:
                for color in palette: gradient+=color
            buf = bytes(gradient)
            gradient_texture.blit_buffer(buf, colorfmt = 'rgba', bufferfmt = 'ubyte')
            self.mdn_bg_kv.canvas.clear()
            with self.mdn_bg_kv.canvas: 
                if radius_arg != [0, 0, 0, 0]:
                    self.mdn_bg_kv.rect = RoundedRectangle(pos = self.mdn_bg_kv.pos, size = self.mdn_bg_kv.size, texture = gradient_texture, radius = radius_arg)
                else:
                    self.mdn_bg_kv.rect = Rectangle(pos = self.mdn_bg_kv.pos, size = self.mdn_bg_kv.size, texture = gradient_texture)
        else:
            if self.mdn_bg_kv: self.mdn_bg_kv.canvas.clear()

        # If color is set for the background and gradient is not set, then take this path
        if mdn_bg_ref["color"] and not mdn_bg_ref["gradient"]:
            if not self.mdn_bg_kv:
                self.mdn_bg_kv = GridLayout()
                self.mdn_rel_bg_kv = RelativeLayout()
                self.mdn_rel_bg_kv.height = 1
                self.mdn_rel_bg_kv.size_hint = (1, None)
                self.mdn_bg_kv.size_hint = (1, None)
                self.mdn_rel_bg_kv.add_widget(self.mdn_bg_kv)
                self.add_widget(self.mdn_rel_bg_kv, index = 1)
            self.mdn_bg_kv.size = self.size
            self.mdn_bg_kv.pos = [self.pos[0], self.pos[1]+2]
            self.mdn_bg_kv.canvas.clear()
            with self.mdn_bg_kv.canvas:
                Color(*self._mdn_get_rgba(mdn_bg_ref["color"]))
                if mdn_radius_ref != [0, 0, 0, 0]:
                    self.mdn_bg_kv.rect = RoundedRectangle(pos = self.mdn_bg_kv.pos, size = self.mdn_bg_kv.size, radius = mdn_radius_ref)
                else:
                    self.mdn_bg_kv.rect = Rectangle(pos = self.mdn_bg_kv.pos, size = self.mdn_bg_kv.size)
        elif not mdn_bg_ref["color"] and not mdn_bg_ref["gradient"]:
            if self.mdn_bg_kv: self.mdn_bg_kv.canvas.clear()

    # _mdn_update_label_graphic_text method
    def _mdn_update_label_graphic_text(self):
        """
            Mdn_Update_Label_Text is a private function. The purpose of this function is to call subfunctions to update all the graphics/ui to text of the label.
        """
        self._mdn_update_label_graphic_remove_or_add_text()
        self._mdn_update_label_graphic_text_styles()
        self._mdn_update_label_graphic_text_size()

    # mdn_update_label_graphic_remove_or_add_text method
    def _mdn_update_label_graphic_remove_or_add_text(self):
        """
            Mdn_Update_Label_Text is a private function. The purpose of this function is to add or remove the text.
        """        
        # Get device size
        mdn_device_size = self._mdn_get_device_size()

        # 'mdn_text_ref' will be a reference variable of the real variable for the current device size
        mdn_text_ref = self.mdn_text[mdn_device_size]

        # If self.mdn_label_kv is initialized but mdn_text_ref == None, then take this path
        if self.mdn_label_kv and mdn_text_ref == None:
            self.remove_widget(self.mdn_label_kv)
            self.mdn_label_kv = None
            self.mdn_rel_label_kv = None

        # If self.mdn_label_kv is not initialized but mdn_text_ref != None, then take this path
        if not self.mdn_label_kv and mdn_text_ref:
            self.mdn_label_kv = Label(line_height = self.mdn_line_height[mdn_device_size])
            self.mdn_label_kv.size_hint = (None, None)
            self.add_widget(self.mdn_label_kv)

    # _mdn_update_label_graphic_text_size method
    def _mdn_update_label_graphic_text_size(self):
        """
            Mdn_Update_Label_Graphic_Text is a private function. The purpose of this function to update the size of the text widget.
        """ 
        # Get device size
        mdn_device_size = self._mdn_get_device_size()        

        # 'mdn_size_ref' will be a reference variable of the real variable for the current device size
        mdn_size_ref = self.mdn_size[mdn_device_size]

        # 'mdn_text_size_ref' will be a reference variable of the real variable for the current device size
        mdn_text_size_ref = self.mdn_text_size[mdn_device_size]

        # If self.mdn_label_kv is initialized, then take this path
        if self.mdn_label_kv:
            # Update the positions as well
            self.mdn_label_kv.pos = self.pos

            # If the self.mdn_size_ref variable should be the size of the text, then take this path
            if mdn_size_ref == "min_size":
                self.mdn_label_kv.text_size = [None, None]
                self.mdn_label_kv.size = self.mdn_label_kv.texture_size
                return

            # If the label width should be the width of the text and the icon is gone, then take this path
            if mdn_size_ref[0] == "min_width":
                self.mdn_label_kv.text_size = [None, self.size[1]]
                self.mdn_label_kv.size[0] = self.mdn_label_kv.texture_size[0]

            # If the icon doesn't exist, then take this path and update the width
            else:
                if 'un' in mdn_text_size_ref: self.mdn_label_kv.width = int(mdn_text_size_ref[:mdn_text_size_ref.index("un")])
                else: self.mdn_label_kv.width = self.width*(int(mdn_text_size_ref[:mdn_text_size_ref.index("%")])/100)
                
            # If the label height should be the height of the text and the icon is gone, then take this path
            if mdn_size_ref[1] == "min_height":
                self.mdn_label_kv.text_size = [self.size[0], None]
                self.mdn_label_kv.size[1] = self.mdn_label_kv.texture_size[1]

            # If the icon doesn't exist, then take this path and update the height
            else:
                if 'un' in mdn_text_size_ref: self.mdn_label_kv.height = int(mdn_text_size_ref[:mdn_text_size_ref.index("un")])
                else: self.mdn_label_kv.height = self.height*(int(mdn_text_size_ref[:mdn_text_size_ref.index("%")])/100)

    # _mdn_update_label_graphic_text_styles method
    def _mdn_update_label_graphic_text_styles(self):
        """
            Mdn_Update_Label_Graphic_Text_Styles is a private function. The purpose of this function to update all the styles of the text widget.
        """ 
        # Get device size
        mdn_device_size = self._mdn_get_device_size() 

        # 'mdn_size_ref' will be a reference variable of the real variable for the current device size
        mdn_size_ref = self.mdn_size[mdn_device_size]

        # 'mdn_text_ref' will be a reference variable of the real variable for the current device size
        mdn_text_ref = self.mdn_text[mdn_device_size]

        # 'mdn_font_color_ref' will be a reference variable of the real variable for the current device size
        mdn_font_color_ref = self.mdn_font_color[mdn_device_size]

        # 'mdn_font_size_ref' will be a reference variable of the real variable for the current device size
        mdn_font_size_ref = self.mdn_font_size[mdn_device_size]

        # 'mdn_font_style_ref' will be a reference variable of the real variable for the current device size
        mdn_font_style_ref = self.mdn_font_style[mdn_device_size]

        # 'mdn_text_align_ref' will be a reference variable of the real variable for the current device size
        mdn_text_align_ref = self.mdn_text_align[mdn_device_size]

        # 'mdn_text_bg_ref' will be a reference variable of the real variable for the current device size
        mdn_text_bg_ref = self.mdn_text_bg[mdn_device_size]

        # If mdn_label_kv is not initialized, then return
        if not self.mdn_label_kv: return

        self.mdn_label_kv.text = mdn_text_ref
        self.mdn_label_kv.font_size = mdn_font_size_ref
        self.mdn_label_kv.color = self._mdn_get_rgba(mdn_font_color_ref)
        self.mdn_label_kv.underline = True
        if "bold" in mdn_font_style_ref: self.mdn_label_kv.bold = True
        else: self.mdn_label_kv.bold = False
        if "italic" in mdn_font_style_ref: self.mdn_label_kv.italic = True
        else: self.mdn_label_kv.italic = False
        if "underline" in mdn_font_style_ref: self.mdn_label_kv.underline = True
        else: self.mdn_label_kv.underline = False
        if mdn_size_ref != "min_content":
            mdn_text_width = None if mdn_size_ref[0] == "min_width" else self.mdn_label_kv.size[0]
            mdn_text_height = None if mdn_size_ref[1] == "min_height" else self.mdn_label_kv.size[1]
            self.mdn_label_kv.text_size = [mdn_text_width, mdn_text_height]
        self.mdn_label_kv.halign = mdn_text_align_ref[0]
        self.mdn_label_kv.valign = mdn_text_align_ref[1]
        self.mdn_label_kv.canvas.before.clear()
        if not mdn_text_bg_ref: return
        with self.mdn_label_kv.canvas.before:
            Color(*self._mdn_get_rgba(mdn_text_bg_ref))
            self.mdn_label_kv.rect = Rectangle(pos = self.mdn_label_kv.pos, size = self.mdn_label_kv.size)