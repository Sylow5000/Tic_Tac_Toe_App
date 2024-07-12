from functools import partial
import random, string
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.relativelayout import RelativeLayout
from dep.hoverable import HoverBehavior
from dep.modern_button import MDN_Button

class NewTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the mdn_insert_char_types
        self.mdn_input_parent = None
        self.mdn_has_specified_length = False
        self.mdn_specified_length = 0
        self.mdn_use_alpha_char = True
        self.mdn_use_numeric_char = True
        self.mdn_use_special_char = True
        self.mdn_use_specific_char = True
        self.mdn_alpha_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.mdn_numeric_char = "0123456789"
        self.mdn_special_char = "`~!@#$%^&*()-_=+{[}]\\|;:'\",<.>/?"
        self.mdn_specific_char = ""
        self.mdn_convert_char_lowercase = True
        self.mdn_convert_char_uppercase = True

    # insert_text function
    def insert_text(self, substring, from_undo = False):

        substring = self.mdn_input_parent.mdn_insert_text(substring, from_undo)

        if not substring: return

        if self.text == substring[2]: self.text = ""

        return super().insert_text(substring[0], from_undo)



class MDN_Input(GridLayout, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__()
        # ========= DEFAULT PARAMETERS ========= #
        # Set columns
        self.cols = 2

        # Set the size_hint
        self.size_hint = (None, None)

        # Set the mdn_app
        try:
            self.mdn_app = kwargs["mdn_app"]
        except:
            print("MDN_Input Error: (MDN_App was not initialized in the __init__ function!")
            return

        # Set the mdn_screenmanager
        self.mdn_screenmanager = self.mdn_app.mdn_screenmanager

        # Set the mdn_hovered
        self.mdn_hovered = False

        # Set the mdn_hovered
        self.mdn_focused = False

        # Set the mdn_textinput
        self.mdn_textinput = None
        
        # Set the mdn_rel_textinput
        self.mdn_rel_textinput = None

        # Set the textinput_button
        self.mdn_textinput_button = None
        
        # Set the rel_textinput_button
        self.mdn_rel_textinput_button = None

        # Set the mdn_id
        if "mdn_id" in kwargs: 
            self.mdn_id = kwargs["mdn_id"]
            self.mdn_screenmanager.get_screen(self.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self
        else: 
            self.mdn_id = 'mdn_textinput_{}'.format("".join(random.choice(string.ascii_lowercase) for i in range(10)))
            self.mdn_screenmanager.get_screen(self.mdn_screenmanager.current).mdn_screen_ids[self.mdn_id] = self

        # Set the mdn_breakpoints
        if "breakpoints" in kwargs: self.mdn_breakpoints = kwargs["breakpoints"]
        else: self.mdn_breakpoints = self.mdn_app.mdn_device_breakpoints

        # Set the mdn_insert_char_types
        self.mdn_no_spaces = False
        self.mdn_has_specified_length = False
        self.mdn_specified_length = 0
        self.mdn_use_alpha_char = True
        self.mdn_use_numeric_char = True
        self.mdn_use_special_char = True
        self.mdn_use_specific_char = True
        self.mdn_alpha_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.mdn_numeric_char = "0123456789"
        self.mdn_special_char = "`~!@#$%^&*()-_=+{[}]\\|;:'\",<.>/?"
        self.mdn_specific_char = ""
        self.mdn_convert_char_lowercase = True
        self.mdn_convert_char_uppercase = True

        # ========= TEXT_INPUT PARAMETERS ========= #
        # Set the mdn_check_cursor
        self.mdn_check_cursor = {"desktop": True, "tablet": True, "mobile": True}

        # Set the mdn_change_cursor
        self.mdn_change_cursor = {"desktop": True, "tablet": True, "mobile": True}

        # Set the mdn_use_hover_ui
        self.mdn_use_hover_ui = {"desktop": True, "tablet": True, "mobile": True}

        # Set the mdn_use_focus_ui
        self.mdn_use_focus_ui = {"desktop": True, "tablet": True, "mobile": True}

        # Set the mdn_multiline
        self.mdn_multiline = {"desktop": True, "tablet": True, "mobile": True}

        # Set the mdn_size
        self.mdn_size = {"desktop": ["100%", "100%"], "tablet": ["100%", "100%"], "mobile": ["100%", "100%"]}

        # Set the mdn_outline
        self.mdn_outline = {
            "desktop": [[0, 0, 0, 0], 0],
            "tablet": [[0, 0, 0, 0], 0],
            "mobile": [[0, 0, 0, 0], 0],
            "hover": [[0, 0, 0, 0], 0],
            "focus": [[0, 0, 0, 0], 0],
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the mdn_outline_joint
        self.mdn_outline_joint = {
            "desktop": "miter",
            "tablet": "miter",
            "mobile": "miter",
            "hover": "miter",
            "focus": "miter",
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the mdn_radius
        self.mdn_radius = {
            "desktop": [0, 0, 0, 0],
            "tablet": [0, 0, 0, 0],
            "mobile": [0, 0, 0, 0],
            "hover": [0, 0, 0, 0],
            "focus": [0, 0, 0, 0],
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the mdn_children_size
        self.mdn_children_size = {
            "desktop": {"input": "max_width", "button": "100un"},
            "tablet": {"input": "max_width", "button": "100un"},
            "mobile": {"input": "max_width", "button": "100un"}
        }

        # Set the mdn_bg
        self.mdn_bg = {
            "desktop": [255, 255, 255, 1],
            "tablet": [255, 255, 255, 1],
            "mobile": [255, 255, 255, 1],
            "hover": [255, 255, 255, 1],
            "focus": [155, 155, 155, 1],
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the mdn_button_pos
        self.mdn_button_pos = {
            "desktop": "right",
            "tablet": "right",
            "mobile": "right"
        }

        # Set the mdn_button_visible
        self.mdn_button_visible = {
            "desktop": True,
            "tablet": True,
            "mobile": True
        }

        # Set the mdn_children_gap
        self.mdn_children_gap = {
            "desktop": "0un",
            "tablet": "0un",
            "mobile": "0un"
        }

        # Set the mdn_font_size
        try: self.mdn_font_size = Window.mdn_default_font_size
        except: self.mdn_font_size = {
                    "desktop": 30,
                    "tablet": 25,
                    "mobile": 20,
                }

        # Set the mdn_font_color
        self.mdn_font_color = {
            "desktop": [0, 0, 0, 1],
            "tablet": [0, 0, 0, 1],
            "mobile": [0, 0, 0, 1],
            "focus": [0, 0, 0, 1],
            "hover": [0, 0, 0, 1],
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the "mdn_text_align" variable...
        self.mdn_text_align = {
            "desktop": {"halign": "left", "valign": "top"},
            "tablet": {"halign": "left", "valign": "top"},
            "mobile": {"halign": "left", "valign": "top"},
            "hover": "center",
            "focus": "center",
            "use_hover_ui": True,
            "use_focus_ui": True
        }

        # Set the mdn_placeholder
        self.mdn_placeholder = {
            "desktop": "",
            "tablet": "",
            "mobile": "",
        }

        # Set the mdn_placeholder_color
        self.mdn_placeholder_color = {
            "desktop": [0, 0, 0, 1],
            "tablet": [0, 0, 0, 1],
            "mobile": [0, 0, 0, 1],
            "hover": [0, 0, 0, 1],
            "use_hover_ui": True
        }

        self.mdn_update(**kwargs)
        self.bind(on_enter = self.mdn_on_enter)
        self.bind(on_leave = self.mdn_on_leave)
        Window.bind(on_cursor_leave = self.mdn_on_leave)
        self.bind(pos = self.mdn_update_bind, size = self.mdn_update_bind)
        self.mdn_screenmanager.bind(pos = self.mdn_update_bind, size = self.mdn_update_bind)
        
    # =============== UPDATE FUNCTIONS =============== #

    # mdn_update fuction
    def mdn_update(self, **kwargs):
        """
            MDN_Update is public function. Here you pass the arguments you wish to update or initialize.\n
            Example use: 
                Here we are calling the button is created and we are calling the mdn_update function to update the mdn_text variable
                    Example 1: mdn_update(mdn_text = 'hello')

                Here we are creating the button and initializing the mdn_text variable at the same time     
                    Example 2: MDN_Input(mdn_text = 'hello')
        """
        # ========== BUTTON PARAMETERS ========== #
        if "mdn_change_cursor" in kwargs: self.mdn_update_param("mdn_change_cursor", kwargs["mdn_change_cursor"])
        if "mdn_check_cursor" in kwargs: self.mdn_update_param("mdn_check_cursor", kwargs["mdn_check_cursor"])
        if "mdn_multiline" in kwargs: self.mdn_update_param("mdn_multiline", kwargs["mdn_multiline"])
        if "mdn_use_focus_ui" in kwargs: self.mdn_update_param("mdn_use_focus_ui", kwargs["mdn_use_focus_ui"])
        if "mdn_use_hover_ui" in kwargs: self.mdn_update_param("mdn_use_hover_ui", kwargs["mdn_use_hover_ui"])
        if "mdn_use_hover_ui" in kwargs: self.mdn_change_all_use_hover_ui_options()
        if "mdn_use_focus_ui" in kwargs: self.mdn_change_all_use_focus_ui_options()
        if "mdn_size" in kwargs: self.mdn_update_param("mdn_size", kwargs["mdn_size"])
        if "mdn_outline" in kwargs: self.mdn_update_param("mdn_outline", kwargs["mdn_outline"])
        if "mdn_outline_joint" in kwargs: self.mdn_update_param("mdn_outline_joint", kwargs["mdn_outline_joint"])
        if "mdn_radius" in kwargs: self.mdn_update_param("mdn_radius", kwargs["mdn_radius"])
        if "mdn_children_size" in kwargs: self.mdn_update_param("mdn_children_size", kwargs["mdn_children_size"])
        if "mdn_bg" in kwargs: self.mdn_update_param("mdn_bg", kwargs["mdn_bg"])
        # ========= TEXT PARAMETERS ========= #
        if "mdn_button_pos" in kwargs: self.mdn_update_param("mdn_button_pos", kwargs["mdn_button_pos"])
        if "mdn_button_visible" in kwargs: self.mdn_update_param("mdn_button_visible", kwargs["mdn_button_visible"])
        if "mdn_children_gap" in kwargs: self.mdn_update_param("mdn_children_gap", kwargs["mdn_children_gap"])
        if "mdn_font_size" in kwargs: self.mdn_update_param("mdn_font_size", kwargs["mdn_font_size"])
        if "mdn_font_style" in kwargs: self.mdn_update_param("mdn_font_style", kwargs["mdn_font_style"])
        if "mdn_font_color" in kwargs: self.mdn_update_param("mdn_font_color", kwargs["mdn_font_color"])
        if "mdn_text" in kwargs: self.mdn_update_param("mdn_text", kwargs["mdn_text"])
        if "mdn_text_align" in kwargs: self.mdn_update_param("mdn_text_align", kwargs["mdn_text_align"])
        if "mdn_placeholder" in kwargs: self.mdn_update_param("mdn_placeholder", kwargs["mdn_placeholder"])
        if "mdn_placeholder_color" in kwargs: self.mdn_update_param("mdn_placeholder_color", kwargs["mdn_placeholder_color"])
        # ========= INPUT PARAMETERS ========= #
        if "mdn_has_specified_length" in kwargs: self.mdn_update_param("mdn_has_specified_length", kwargs["mdn_has_specified_length"])
        if "mdn_specified_length" in kwargs: self.mdn_update_param("mdn_specified_length", kwargs["mdn_specified_length"])
        if "mdn_use_alpha_char" in kwargs: self.mdn_update_param("mdn_use_alpha_char", kwargs["mdn_use_alpha_char"])
        if "mdn_use_numeric_char" in kwargs: self.mdn_update_param("mdn_use_numeric_char", kwargs["mdn_use_numeric_char"])
        if "mdn_use_special_char" in kwargs: self.mdn_update_param("mdn_use_special_char", kwargs["mdn_use_special_char"])
        if "mdn_use_specific_char" in kwargs: self.mdn_update_param("mdn_use_specific_char", kwargs["mdn_use_specific_char"])
        if "mdn_specific_char" in kwargs: self.mdn_update_param("mdn_specific_char", kwargs["mdn_specific_char"])
        if "mdn_convert_char_lowercase" in kwargs: self.mdn_update_param("mdn_convert_char_lowercase", kwargs["mdn_convert_char_lowercase"])
        if "mdn_convert_char_uppercase" in kwargs: self.mdn_update_param("mdn_convert_char_uppercase", kwargs["mdn_convert_char_uppercase"])
        if "mdn_no_spaces" in kwargs: self.mdn_update_param("mdn_no_spaces", kwargs["mdn_no_spaces"])
        self.mdn_update_graphic()  
        self.mdn_update_multiline_allowed()
        self.mdn_insert_characters()

    # mdn_update_bind function
    def mdn_update_bind(self, *args):
        """
            Mdn_Update_Bind is a private function. The purpose of this function is to update everything. This is bound to the movement and size of the screen or window\n
        """
        self.mdn_update_graphic()
        self.mdn_update_multiline_allowed()

    # mdn_update_param function
    def mdn_update_param(self, arg_name, arg_value):
        """
            MDN_Update_Param is private function. The purpose of this function is to actually update the variables. NOTE: This only updates the values, but not the graphics. But the graphics won't change unless the values change, so even though this function doesn't update the graphics directly it updates the values, so the graphics will change.\n
            Example use: 
                Here the button is created and we are calling the mdn_update function to update the mdn_text variable
                    Example 1: 
                        mdn_text = {'desktop': '', 'tablet': '', 'mobile': ''}
                        mdn_update(mdn_text = 'hello')
                        mdn_update -> mdn_update_param
                        mdn_text = {'desktop': 'hello', 'tablet': 'hello', 'mobile': 'hello'}
        """
        # This variable 'mdn_update_variable_ref' is a reference to the actual variable
        # Modifing this one, will modify the real variable, because the variable type is a dict
        mdn_update_variable_ref = None

        mdn_textinput_var = ["mdn_no_spaces", "mdn_has_specified_length","mdn_specified_length","mdn_use_alpha_char","mdn_use_numeric_char","mdn_use_special_char", "mdn_use_specific_char","mdn_specific_char","mdn_convert_char_lowercase","mdn_convert_char_uppercase"]

        # Assign the mdn_update_variable_ref variable to the actual variable
        if arg_name == "mdn_change_cursor": mdn_update_variable_ref = self.mdn_change_cursor
        if arg_name == "mdn_check_cursor": mdn_update_variable_ref = self.mdn_check_cursor
        if arg_name == "mdn_use_hover_ui": mdn_update_variable_ref = self.mdn_use_hover_ui
        if arg_name == "mdn_use_focus_ui": mdn_update_variable_ref = self.mdn_use_focus_ui
        if arg_name == "mdn_multiline": mdn_update_variable_ref = self.mdn_multiline
        if arg_name == "mdn_outline": mdn_update_variable_ref = self.mdn_outline
        if arg_name == "mdn_outline_joint": mdn_update_variable_ref = self.mdn_outline_joint
        if arg_name == "mdn_radius": mdn_update_variable_ref = self.mdn_radius
        if arg_name == "mdn_children_size": mdn_update_variable_ref = self.mdn_children_size
        if arg_name == "mdn_size": mdn_update_variable_ref = self.mdn_size
        if arg_name == "mdn_bg": mdn_update_variable_ref = self.mdn_bg
        if arg_name == "mdn_button_pos": mdn_update_variable_ref = self.mdn_button_pos
        if arg_name == "mdn_button_visible": mdn_update_variable_ref = self.mdn_button_visible
        if arg_name == "mdn_children_gap": mdn_update_variable_ref = self.mdn_children_gap
        if arg_name == "mdn_font_size": mdn_update_variable_ref = self.mdn_font_size
        if arg_name == "mdn_font_style": mdn_update_variable_ref = self.mdn_font_style
        if arg_name == "mdn_font_color": mdn_update_variable_ref = self.mdn_font_color
        if arg_name == "mdn_text_align": mdn_update_variable_ref = self.mdn_text_align
        if arg_name == "mdn_placeholder": mdn_update_variable_ref = self.mdn_placeholder
        if arg_name == "mdn_placeholder_color": mdn_update_variable_ref = self.mdn_placeholder_color
        if arg_name in mdn_textinput_var: mdn_update_variable_ref = True

        # If 'mdn_update_variable_ref' == None, then return function
        if mdn_update_variable_ref == None: return

        # If 'arg_name' is not 'mdn_bg' then take this path
        if arg_name != "mdn_check_cursor" and arg_name != "mdn_children_size" and arg_name not in mdn_textinput_var:
            if type(arg_value) != dict:
                for mdn_breakpoint in ["desktop", "tablet", "mobile"]: mdn_update_variable_ref[mdn_breakpoint] = arg_value
            else:
                for mdn_breakpoint in list(arg_value.keys()): mdn_update_variable_ref[mdn_breakpoint] = arg_value[mdn_breakpoint]
            if arg_name == "mdn_radius": self.mdn_convert_radius(self.mdn_radius)
            if arg_name == "mdn_text_radius": self.mdn_convert_radius(self.mdn_text_radius)
            return
        
        # If 'arg_name' is 'mdn_text_align', then take this path
        elif arg_name == "mdn_text_align":

            # Check if the keys of the 'arg_value' are breakpoints, if so, then take this path
            if list(arg_value.keys())[0] in ["desktop", "tablet", "mobile"]:

                # Loop through all the options in the 'arg_value'['mdn_breakpoints']. There can only be two options at max. These options are: 'halign' or 'vertical'
                for mdn_breakpoint in list(arg_value.keys()):

                    # If 'halign' option exists, then take this path
                    if "halign" in arg_value[mdn_breakpoint]:
                        self.mdn_text_align[mdn_breakpoint]["halign"] = arg_value[mdn_breakpoint]["halign"]

                    # If 'valign' option exists, then take this path
                    if "valign" in arg_value[mdn_breakpoint]:
                        self.mdn_text_align[mdn_breakpoint]["valign"] = arg_value[mdn_breakpoint]["valign"]

            else:
                # Loop through all the breakpoints and change the size of the input or/and button
                for mdn_breakpoint in ["desktop", "tablet", "mobile"]:

                    # If 'halign' option exists, then take this path
                    if "halign" in arg_value:
                        self.mdn_text_align[mdn_breakpoint]["halign"] = arg_value["halign"]

                    # If 'valign' option exists, then take this path
                    if "valign" in arg_value:
                        self.mdn_text_align[mdn_breakpoint]["valign"] = arg_value["valign"]

        # If 'arg_name' is 'mdn_children_size', then take this path 
        elif arg_name == "mdn_children_size":
            # Check if the keys of the 'arg_value' are breakpoints, if so, then take this path
            if list(arg_value.keys())[0] in ["desktop", "tablet", "mobile"]:

                # Loop through all the options in the 'arg_value'['mdn_breakpoints']. There can only be two options at max. These options are: 'button' or 'input'
                for mdn_breakpoint in list(arg_value.keys()):

                    # If 'button' option exists, then take this path
                    if "button" in arg_value[mdn_breakpoint]:
                        self.mdn_children_size[mdn_breakpoint]["button"] = arg_value[mdn_breakpoint]["button"]

                    # If 'input' option exists, then take this path
                    if "input" in arg_value[mdn_breakpoint]:
                        self.mdn_children_size[mdn_breakpoint]["input"] = arg_value[mdn_breakpoint]["input"]

            else:
                # Loop through all the breakpoints and change the size of the input or/and button
                for mdn_breakpoint in ["desktop", "tablet", "mobile"]:

                    # If 'button' option exists, then take this path
                    if "button" in arg_value:
                        self.mdn_children_size[mdn_breakpoint]["button"] = arg_value["button"]

                    # If 'input' option exists, then take this path
                    if "input" in arg_value:
                        self.mdn_children_size[mdn_breakpoint]["input"] = arg_value["input"]

        # If 'arg_name' is 'mdn_check_cursor', then take this path 
        elif arg_name == "mdn_check_cursor":
            self.mdn_check_cursor = arg_value

        # If 'arg_name' in this list, then take this path
        elif arg_name in mdn_textinput_var:
            print("great", arg_name, arg_value)
            if arg_name == "mdn_no_spaces": self.mdn_no_spaces = arg_value
            if arg_name == "mdn_has_specified_length": self.mdn_has_specified_length = arg_value
            if arg_name == "mdn_specified_length": self.mdn_specified_length = arg_value
            if arg_name == "mdn_use_alpha_char": self.mdn_use_alpha_char = arg_value
            if arg_name == "mdn_use_numeric_char": self.mdn_use_numeric_char = arg_value
            if arg_name == "mdn_use_special_char": self.mdn_use_special_char = arg_value
            if arg_name == "mdn_use_specific_char": self.mdn_use_specific_char = arg_value
            if arg_name == "mdn_specific_char": self.mdn_specific_char = arg_value
            if arg_name == "mdn_convert_char_lowercase": self.mdn_convert_char_lowercase = arg_value
            if arg_name == "mdn_convert_char_uppercase": self.mdn_convert_char_uppercase = arg_value
        
            
    # =============== SYSTEM FUNCTIONS =============== #

    # mdn_get_rgba function
    def mdn_get_rgba(self, rgba):
        """
            Mdn_Get_RGBA is a private function. The purpose of this function is to convert an rgba and divide it by 255 so it can be used by the kivy module\n
        """
        new_rgba = []
        for i in range(0, 3):new_rgba.append(rgba[i]/255)
        new_rgba.append(rgba[3])
        return new_rgba

    # mdn_get_device_size function
    def mdn_get_device_size(self):
        """
            Mdn_Get_Device_Size is a private function. The purpose of this function is to determine the appropriate device label according to the size of the app window.\n
            Example:
                Window.size = (500, 1000)
                print(mdn_get_device_size()) -> 'mobile'
        """
        if Window.width >= self.mdn_breakpoints["mobile"][0] and Window.width <= self.mdn_breakpoints["mobile"][1]: return "mobile"
        if Window.width >= self.mdn_breakpoints["tablet"][0] and Window.width <= self.mdn_breakpoints["tablet"][1]: return "tablet"
        return "desktop"

    # mdn_update_multiline_allowed function
    def mdn_update_multiline_allowed(self):
        """
            Mdn_Update_Multiline_Allowed is a private function. The purpose of this function is to update if textinput is allowed to multiline or not\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_multiline_ref' will be a reference variable of the real variable for the current device size
        mdn_multiline_ref = self.mdn_multiline[mdn_device_size]  

        if self.mdn_textinput:
            self.mdn_textinput.multiline = mdn_multiline_ref      

    # mdn_keep_cursor_changed function   
    def mdn_keep_cursor_changed(self, *args):
        """
            Mdn_Hover is a private function. The purpose of this function is to keep the cursor a hand when the button is hovered. Of course this will only work if self.mdn_change_cursor is set True. This function will only make a difference if there are several buttons or widgets that hover behaviors right beside each other. If there aren't widgets that hover behaviors right beside each other, then function won't do anything, besides take up more CPU power. This function is off by default, but turn it on set the mdn_check_cursor = True\n
        """

        # if self.mdn_change_cursor: Window.set_system_cursor("ibeam")

        i = 0
        if len(args) >= 1: i = args[0]+1
        # If self.mdn_hovered, then call this function every one-tenth of second one 50 times
        if self.mdn_hovered and i <= 50: 
            Clock.schedule_once(partial(self.mdn_keep_cursor_changed, i), .01)
            return  

    # mdn_check_if_hovered function
    def mdn_check_if_hovered(self, *args):
        """
            Mdn_Check_If_Hovered is a private function. The purpose of the function is to check if the cursor is over the text input widget is it over the button if button exists. If it isn't over the textbox then don't change the cursor.
        """

        if not self.mdn_textinput: return

        if (Window.mouse_pos[0] >= self.mdn_textinput.pos[0] and Window.mouse_pos[0] <= self.mdn_textinput.pos[0]+self.mdn_textinput.size[0]) and (Window.mouse_pos[1] >= self.pos[1] and Window.mouse_pos[1] <= self.pos[1]+self.mdn_textinput.size[1]):
            Window.set_system_cursor("ibeam")
            return True
        else:
            Window.set_system_cursor("arrow")
            return False

    # mdn_convert_radius function
    def mdn_convert_radius(self, radius):
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
            if len(radius[mdn_breakpoint]) == 2: radius[mdn_breakpoint] = [radius[mdn_breakpoint][1],radius[mdn_breakpoint][0],radius[mdn_breakpoint][1],radius[mdn_breakpoint][0]]
            if len(radius[mdn_breakpoint]) == 3: 
                radius[mdn_breakpoint] = [radius[mdn_breakpoint][1],radius[mdn_breakpoint][2],radius[mdn_breakpoint][1],radius[mdn_breakpoint][0]]
            if len(radius[mdn_breakpoint]) == 4: 
                radius[mdn_breakpoint] = [radius[mdn_breakpoint][3],radius[mdn_breakpoint][2],radius[mdn_breakpoint][1],radius[mdn_breakpoint][0]]

    # mdn_insert_characters function
    def mdn_insert_characters(self, *args):
        """
            Mdn_Insert_Characters is a private function. This primary purpose of this function is to copy all the variables from this current variable to the textinput widget.\n
            Example:

                self.mdn_use_alpha_char = True\n
                self.textinput.mdn_use_alpha_char = False

                Process:
                   self.textinput.mdn_use_alpha_char ->  mdn_insert_characters -> self.textinput.mdn_use_alpha_char = True
        """
        if not self.mdn_textinput: return
        self.mdn_textinput.mdn_no_spaces = self.mdn_no_spaces
        self.mdn_textinput.mdn_has_specified_length = self.mdn_has_specified_length
        self.mdn_textinput.mdn_specified_length = self.mdn_specified_length
        self.mdn_textinput.mdn_use_alpha_char = self.mdn_use_alpha_char
        self.mdn_textinput.mdn_use_numeric_char = self.mdn_use_numeric_char
        self.mdn_textinput.mdn_use_special_char = self.mdn_use_special_char
        self.mdn_textinput.mdn_alpha_char = self.mdn_alpha_char
        self.mdn_textinput.mdn_has_specified_length = self.mdn_has_specified_length
        self.mdn_textinput.mdn_numeric_char = self.mdn_numeric_char
        self.mdn_textinput.mdn_special_char = self.mdn_special_char
        self.mdn_textinput.mdn_convert_char_lowercase = self.mdn_convert_char_lowercase
        self.mdn_textinput.mdn_convert_char_uppercase = self.mdn_convert_char_uppercase

    # mdn_insert_text function
    def mdn_insert_text(self, substring, from_undo = False):
        """
            Insert_Text is private function. The purpose of this function is to add characters to the text input widget.\n
        """

        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # If the length of the text is greater than the specified length don't insert any characters into the input widget    
        if self.mdn_has_specified_length and len(self.mdnt_textinput.text) >= self.mdn_specified_length: return

        # Convert text to lowercase, if 'mdn_convert_char_lowercase' is true and alpha char exists in substring
        if self.mdn_convert_char_lowercase and substring in self.mdn_alpha_char: substring = substring.lower()
        
        # Convert text to uppercase, if 'mdn_convert_char_uppercase' is true and alpha char exists in substring
        if self.mdn_convert_char_uppercase and substring in self.mdn_alpha_char: substring = substring.upper()   
        
        # If mdn_use_specific_char == True, then check if substring in the mdn_specific_char var, if so then add to the input
        if self.mdn_use_specific_char:
            if substring in self.mdn_specific_char:
                return (substring, from_undo, self.mdn_placeholder[mdn_device_size])
        
        # If mdn_use_alpha_char == True, then check if substring in the mdn_alpha_char var, if so then add to the input
        if self.mdn_use_alpha_char:
            if substring in self.mdn_alpha_char:
                return (substring, from_undo, self.mdn_placeholder[mdn_device_size])

        # If mdn_use_numeric_char == True, then check if substring in the mdn_numeric_char var, if so then add to the input
        if self.mdn_use_numeric_char:
            if substring in self.mdn_numeric_char:
                return (substring, from_undo, self.mdn_placeholder[mdn_device_size])
    
        # If mdn_use_special_char == True, then check if substring in the mdn_special_char var, if so then add to the input
        if self.mdn_use_special_char:
            if substring in self.mdn_special_char:
                return (substring, from_undo, self.mdn_placeholder[mdn_device_size])

        # If the spaces are allowed and the substring is a space then, take this path    
        if not self.mdn_no_spaces and substring == " ": 
            return (substring, from_undo, self.mdn_placeholder[mdn_device_size])

        return None

     
    # =============== MOUSE FUNCTIONS =============== #

    # mdn_on_enter function
    def mdn_on_enter(self, *args):
        """
            Mdn_On_Enter is a private function. The purpose of this function is to change all the graphics/ui when button is hovered\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # Set self.mdn_hovered == True, because the input has been hovered
        self.mdn_hovered = True

        # If cursor should be changed, then take this path
        if self.mdn_change_cursor[mdn_device_size]: 
            mdn_is_hovered = self.mdn_check_if_hovered()

            if mdn_is_hovered:
                # Call a function that will loop 50times, while the cursor is over the input.
                if self.mdn_check_cursor[mdn_device_size]: self.mdn_keep_cursor_changed()

                # Update all the graphics
                self.mdn_update_graphic("hover")

    # mdn_on_leave function
    def mdn_on_leave(self, *args):
        """
            Mdn_On_Leave is a private function. The purpose of this function is to change all the graphics/ui when button is not hovered\n
        """
        self.mdn_hovered = False
        Window.set_system_cursor("arrow")
        self.mdn_update_graphic("leave")

    # mdn_on_focus function
    def mdn_on_focus(self, *args):
        """
            Mdn_On_Focus is a private function. The purpose of this function is to change all the graphics/ui when the textbox is focused\n
        """
        self.mdn_focused = self.mdn_textinput.focus
        Window.set_system_cursor("ibeam")
        self.mdn_update_graphic()        

    # mdn_change_all_use_hover_ui_options function
    def mdn_change_all_use_hover_ui_options(self):
        """
            Mdn_Change_All_Use_Hover_Ui_Options is a private function. The purpose of this function is to go throughout all the widgets and change the use_hover_ui option to the self.mdn_use_hover_ui. So a user doesn't have to specify what happens when hovered, the button will just keep the ui the same.\n
                Eg 1: 
                    button_one = MDN_Button(mdn_text = 'hello')
                    print(button_one.mdn_text) -> {'desktop': 'hello', 'tablet': 'hello', 'mobile': 'hello', 'hover': '', use_hover_ui: True}
                    button_one is hovered
                    button_one.text = ''
                The reason for this is because the option hover wasn't set to anything, but setting use_hover_ui to False, the text for the button will still be 'hello'
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_use_hover_ui_ref' will be a reference variable of the real variable for the current device size
        mdn_use_hover_ui_ref = self.mdn_use_hover_ui[mdn_device_size]

        # Store all the variables
        mdn_widgets = [self.mdn_outline, self.mdn_outline_joint, self.mdn_radius, self.mdn_bg, self.mdn_text_align, self.mdn_placeholder_color, self.mdn_font_color]

        # Loop through all the widgets and change the use_hover_ui option
        for mdn_widget in mdn_widgets: mdn_widget["use_hover_ui"] = mdn_use_hover_ui_ref

    # mdn_change_all_use_focus_ui_options function
    def mdn_change_all_use_focus_ui_options(self):
        """
            Mdn_Change_All_Use_Hover_Ui_Options is a private function. The purpose of this function is to go throughout all the widgets and change the use_focus_ui option to the self.mdn_use_focus_ui. So a user doesn't have to specify what happens when focused, the button will just keep the ui the same.\n
                Eg 1: 
                    button_one = MDN_Button(mdn_text = 'hello')
                    print(button_one.mdn_text) -> {'desktop': 'hello', 'tablet': 'hello', 'mobile': 'hello', 'focus': '', use_focus_ui: True}
                    button_one is focused
                    button_one.text = ''
                The reason for this is because the option focus wasn't set to anything, but setting use_focus_ui to False, the text for the button will still be 'hello'
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_use_focus_ui_ref' will be a reference variable of the real variable for the current device size
        mdn_use_focus_ui_ref = self.mdn_use_focus_ui[mdn_device_size]

        # Store all the variables

        mdn_widgets = [self.mdn_outline, self.mdn_outline_joint, self.mdn_radius, self.mdn_bg, self.mdn_font_color, self.mdn_text_align]

        # Loop through all the widgets and change the use_focus_ui option
        for mdn_widget in mdn_widgets: mdn_widget["use_focus_ui"] = mdn_use_focus_ui_ref

    # =============== GRAPHIC FUNCTIONS =============== #

    # mdn_update_graphic function
    def mdn_update_graphic(self, *args):
        """
            Mdn_Update_Graphic is a private function. The purpose of this function is to call all the subfunctions that are able to update the button graphics or ui\n
        """
        # If parent does not exists, return and run again .5sec later
        if not self.parent: 
            Clock.schedule_once(self.mdn_update_graphic, .5)
            return

        # Call all the subfunctions needed to change the graphic/ui
        self.mdn_update_input_graphic_size()
        self.mdn_update_input_graphic_outline()
        self.mdn_update_input_graphic_bg()
        self.mdn_update_input_children_layout()
        self.mdn_update_input_children_size()
        self.mdn_update_textinput_gap_pos()
        self.mdn_update_textinput_font_styles()

    # mdn_update_input_graphic_size function
    def mdn_update_input_graphic_size(self):
        """
            Mdn_Update_Input_Graphic_Size is a private function. The purpose of this function is to update the graphic/ui size of the input\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_size_ref' will be a reference variable of the real variable for the current device size
        mdn_size_ref = self.mdn_size[mdn_device_size]

        # Update the width
        if 'un' in mdn_size_ref[0]: self.width = float(mdn_size_ref[0][:mdn_size_ref[0].index("un")])
        else: self.width = self.parent.width*(float(mdn_size_ref[0][:mdn_size_ref[0].index("%")])/100)

        # Update the height
        if 'un' in mdn_size_ref[1]: self.height = float(mdn_size_ref[1][:mdn_size_ref[1].index("un")])
        else: self.height = self.parent.height*(float(mdn_size_ref[1][:mdn_size_ref[1].index("%")])/100)

    # mdn_update_input_graphic_outline function
    def mdn_update_input_graphic_outline(self):
        """
            Mdn_Update_Input_Graphic_Outline is a private function. The purpose of this function is to update the graphic/ui outline of the input\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_children_gap_ref' will be a reference variable of the real variable for the current device size
        mdn_children_gap_ref = self.mdn_children_gap[mdn_device_size]

        # 'mdn_radius_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_radius["use_hover_ui"]: mdn_radius_ref = self.mdn_radius["hover"]
        elif self.mdn_focused and self.mdn_radius["use_focus_ui"]: mdn_radius_ref = self.mdn_radius["focus"]
        else: mdn_radius_ref = self.mdn_radius[mdn_device_size]

        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_outline["use_hover_ui"]: mdn_outline_ref = self.mdn_outline["hover"]
        elif self.mdn_focused and self.mdn_outline["use_focus_ui"]: mdn_outline_ref = self.mdn_outline["focus"]
        else: mdn_outline_ref = self.mdn_outline[mdn_device_size]

        # 'mdn_outline_joint_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_outline_joint["use_hover_ui"]: mdn_outline_joint_ref = self.mdn_outline_joint["hover"]
        elif self.mdn_focused and self.mdn_outline_joint["use_focus_ui"]: mdn_outline_joint_ref = self.mdn_outline_joint["focus"]
        else: mdn_outline_joint_ref = self.mdn_outline_joint[mdn_device_size]

        # Clear any outlines
        if self.mdn_textinput:
            self.canvas.after.clear()
            self.mdn_textinput.canvas.after.clear()

        # Create the outlines
        if mdn_children_gap_ref == "0un" or mdn_children_gap_ref == "0%":
            if mdn_outline_ref[0][3] == 0 or mdn_outline_ref[1] == 0: return
            with self.canvas.after:
                Color(*self.mdn_get_rgba(mdn_outline_ref[0]))
                if mdn_radius_ref != [0, 0, 0, 0]:
                    Line(rounded_rectangle = [self.x, self.y, self.width, self.height, *mdn_radius_ref], width = mdn_outline_ref[1])
                else:
                    Line(rectangle = [self.x, self.y, self.width, self.height], width = mdn_outline_ref[1], joint = mdn_outline_joint_ref)
        else:
            if self.mdn_textinput:
                if mdn_outline_ref[0][3] == 0 or mdn_outline_ref[1] == 0: return
                with self.mdn_textinput.canvas.after:
                    Color(*self.mdn_get_rgba(mdn_outline_ref[0]))
                    if mdn_radius_ref != [0, 0, 0, 0]:
                        Line(rounded_rectangle = [self.mdn_textinput.x, self.mdn_textinput.y, self.mdn_textinput.width, self.mdn_textinput.height, *mdn_radius_ref], width = mdn_outline_ref[1])
                    else:
                        Line(rectangle = [self.mdn_textinput.x, self.mdn_textinput.y, self.mdn_textinput.width, self.mdn_textinput.height], width = mdn_outline_ref[1], joint = mdn_outline_joint_ref)             

    # mdn_update_input_graphic_bg function
    def mdn_update_input_graphic_bg(self):
        """
            Mdn_Update_Input_Graphic_Bg is a private function. The purpose of this function is to update the graphic/ui background of the input. This will only update background colors. 
            Textures aren't allowed!
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_bg_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_bg["use_hover_ui"]: mdn_bg_ref = self.mdn_bg["hover"]
        elif self.mdn_focused and self.mdn_bg["use_focus_ui"]: mdn_bg_ref = self.mdn_bg["focus"]
        else: mdn_bg_ref = self.mdn_bg[mdn_device_size]

        # Remove background color
        self.canvas.before.clear()

        # Check if background color should be added
        if mdn_bg_ref or mdn_bg_ref[3] == 0:

            # Add a background color
            with self.canvas.before:
                Color(*self.mdn_get_rgba(mdn_bg_ref))
                self.rect = Rectangle(size = self.size, pos = self.pos)

    # mdn_update_input_children_layout function
    def mdn_update_input_children_layout(self):
        """
            Mdn_Update_Input_Children_Layout is a private function. The purpose of this function is to update the graphic/ui layout of the children. This will either put the button to the left or the right side of the textinput widget
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_button_visible_ref' will be a reference variable of the real variable for the current device size
        mdn_button_visible_ref = self.mdn_button_visible[mdn_device_size]

        # 'mdn_button_pos_ref' will be a reference variable of the real variable for the current device size
        mdn_button_pos_ref = self.mdn_button_pos[mdn_device_size]

        # 'mdn_widget_priority' determines which widget is shown first, the button or the input
        mdn_priority = ["button", "input"] if mdn_button_pos_ref == "left" else ["input", "button"]

        # If the 'mdn_textinput' hasn't been initialized, then take this path
        if not self.mdn_textinput:
            self.mdn_rel_textinput = RelativeLayout()
            self.mdn_textinput = NewTextInput()
            self.mdn_textinput.size_hint = (None, None)
            self.mdn_textinput.mdn_input_parent = self
            self.mdn_rel_textinput.add_widget(self.mdn_textinput)
            self.mdn_textinput.bind(focus = self.mdn_on_focus)

        # If the 'mdn_textinput' hasn't been initialized, then take this path
        if not self.mdn_textinput_button and mdn_button_visible_ref:
            self.mdn_textinput_button = MDN_Button(
                mdn_text = "Press Me",
                mdn_size = ["100%", "100%"],
                mdn_bg = {"color": [46, 60, 184, 1]},
                mdn_use_hover_ui = False
            )

        # If 'mdn_button_visible_ref' is False and the button is visible, then remove it
        if not mdn_button_visible_ref and self.mdn_textinput_button:
            self.remove_widget(self.mdn_textinput_button)
    
        # If no children are present, then add the button and the input to the MDN_Input class
        if not self.children:
            for widget in mdn_priority:
                if widget == "input": self.add_widget(self.mdn_rel_textinput)
                if widget == "button" and mdn_button_visible_ref: self.add_widget(self.mdn_textinput_button)

        # If only one child element is present, then add the button to the MDN_Input class
        elif self.children and len(self.children) == 1 and mdn_button_visible_ref:
            self.add_widget(self.mdn_textinput_button)

        # If two children are present, the check do their pos need to be swapped
        if self.children and len(self.children) == 2:

            # If the child elements are in the wrong position, then swap them
            if (self.children[1].__class__.__name__ and mdn_button_pos_ref ==  "right") or (self.children[0].__class__.__name__ == "MDN_Button" and mdn_button_pos_ref == "left"):
                self.clear_widgets()
                for widget in mdn_priority:
                    if widget == "input": self.add_widget(self.mdn_rel_textinput)
                    if widget == "button": self.add_widget(self.mdn_textinput_button)

    # mdn_update_input_children_size function
    def mdn_update_input_children_size(self):
        """
            Mdn_Update_Input_Children_Size is a private function. The purpose of this function is to update the graphic/ui size of the children. This will include the width of the input and heigh and width of the  button\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()        

        # 'mdn_children_size_ref' will be a reference variable of the real variable for the current device size
        mdn_children_size_ref = self.mdn_children_size[mdn_device_size]

        # 'mdn_children_gap_ref' will be a reference variable of the real variable for the current device size
        mdn_children_gap_ref = self.mdn_children_gap[mdn_device_size]

        # 'mdn_button_visible_ref' will be a reference variable of the real variable for the current device size
        mdn_button_visible_ref = self.mdn_button_visible[mdn_device_size]

        # 'mdn_outline_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_outline["use_hover_ui"]: mdn_outline_ref = self.mdn_outline["hover"]
        elif self.mdn_focused and self.mdn_outline["use_focus_ui"]: mdn_outline_ref = self.mdn_outline["focus"]
        else: mdn_outline_ref = self.mdn_outline[mdn_device_size]

        # Update the width of the button
        if mdn_button_visible_ref: 
            self.mdn_textinput_button.mdn_update({"mdn_size": [mdn_children_size_ref["button"], "100%"]})

        # Create the 'mdn_gap' and set it zero. This will determine how much gap there should be between the button and the textinput widget.
        mdn_gap = 0
        if mdn_children_gap_ref:
            if "un" in mdn_children_gap_ref: 
                mdn_gap = float(mdn_children_gap_ref[:mdn_children_gap_ref.index("un")])
            elif "%" in mdn_children_gap_ref: 
                mdn_gap = self.width*(float(mdn_children_gap_ref[:mdn_children_gap_ref.index("%")])/100)

        # Update the height: This will take up 100% of the height including the outline
        self.mdn_textinput.height = self.height

        # Update the width: Check if it is a fixed number
        if "un" in mdn_children_size_ref["input"] and mdn_button_visible_ref:
            self.mdn_textinput.width = float(mdn_children_size_ref["input"][:mdn_children_size_ref["input"].index("un")]) - mdn_gap

        # Update the width: Check if it is a percentage
        elif "%" in mdn_children_size_ref["input"] and mdn_button_visible_ref:
            self.mdn_textinput.width = self.width * (float(mdn_children_size_ref["input"][:mdn_children_size_ref["input"].index("%")])/100) - mdn_gap - mdn_outline_ref[1]

        # Update the width: Check if it is 'max_width'
        elif mdn_children_size_ref["input"] == "max_width" and mdn_button_visible_ref:
            self.mdn_textinput.width = self.width - self.mdn_textinput_button.width - mdn_gap

        # Update the width: If the button isn't visible, then span the whole class
        elif not mdn_button_visible_ref:
            self.mdn_textinput.width = self.width

    # mdn_update_textinput_gap_pos function
    def mdn_update_textinput_gap_pos(self):
        """
            Mdn_Update_Textinput_Gap_Pos is a private function. The purpose of this function is to update the graphic/ui gap between the two child elements. If the textinput is on the right and there is a gap on the right, then switch the gap to the left\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()          

        # 'mdn_children_gap_ref' will be a reference variable of the real variable for the current device size
        mdn_children_gap_ref = self.mdn_children_gap[mdn_device_size]

        # 'mdn_button_visible_ref' will be a reference variable of the real variable for the current device size
        mdn_button_visible_ref = self.mdn_button_visible[mdn_device_size]

        # 'mdn_button_pos' will be a reference variable of the real variable for the current device size
        mdn_button_pos_ref = self.mdn_button_pos[mdn_device_size]

        # Create the 'mdn_gap' and set it zero. This will determine how much gap there should be between the button and the textinput widget.
        mdn_gap = 0
        if mdn_children_gap_ref:
            if "un" in mdn_children_gap_ref: 
                mdn_gap = float(mdn_children_gap_ref[:mdn_children_gap_ref.index("un")])
            elif "%" in mdn_children_gap_ref: 
                mdn_gap = self.width*(float(mdn_children_gap_ref[:mdn_children_gap_ref.index("%")])/100)

        # If there is no gap, then exit this funciton
        if mdn_children_gap_ref == "0un" or mdn_children_gap_ref == "0%": return

        # If there is no button, then exit this funciton
        if not mdn_button_visible_ref: return

        # If the button is on the left, then move the gap to the left
        # And if the button is to the right, then move the gap to the right
        if mdn_button_pos_ref == "left":
            self.mdn_textinput.pos = [mdn_gap, 0]
        else:
            self.mdn_textinput.pos = [0, 0]

    # mdn_update_textinput_font_styles function
    def mdn_update_textinput_font_styles(self):
        """
            Mdn_Update_Textinput_Font_Styles is a private function. The purpose of this function is to update the graphic/ui font color, font style, font size, placeholder, placeholder color, text align, text\n
        """
        # Get device size
        mdn_device_size = self.mdn_get_device_size()

        # 'mdn_multiline_ref' will be a reference variable of the real variable for the current device size
        mdn_multiline_ref = self.mdn_multiline[mdn_device_size] 

        # 'mdn_font_color_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_font_color["use_hover_ui"]: mdn_font_color_ref = self.mdn_font_color["hover"]
        elif self.mdn_focused and self.mdn_font_color["use_focus_ui"]: mdn_font_color_ref = self.mdn_font_color["focus"]
        else: mdn_font_color_ref = self.mdn_font_color[mdn_device_size]

        # 'mdn_font_size_ref' will be a reference variable of the real variable for the current device size
        mdn_font_size_ref = self.mdn_font_size[mdn_device_size]

        # 'mdn_placeholder_ref' will be a reference variable of the real variable for the current device size
        mdn_placeholder_ref = self.mdn_placeholder[mdn_device_size]

        # 'mdn_placeholder_color_ref' will be a reference variable of the real variable for the current device size
        if self.mdn_hovered and self.mdn_placeholder_color["use_hover_ui"]: mdn_placeholder_color_ref = self.mdn_placeholder_color["hover"]
        else: mdn_placeholder_color_ref = self.mdn_placeholder_color[mdn_device_size]

        # 'mdn_text_align_ref' will be a reference variable of the real variable for the current device size
        mdn_text_align_ref = self.mdn_text_align[mdn_device_size]

        # If textinput widget doesn't exist, then exit out of this function
        if not self.mdn_textinput: return

        # If there is no text, then display placeholder and placeholder color
        if not self.mdn_textinput.text or self.mdn_textinput.text == mdn_placeholder_ref: 
            self.mdn_textinput.text = mdn_placeholder_ref
            self.mdn_textinput.foreground_color = self.mdn_get_rgba(mdn_placeholder_color_ref)

        # If there is text, then display text and font color
        elif self.mdn_textinput.text and self.mdn_textinput.text != mdn_placeholder_ref:
            self.mdn_textinput.foreground_color = self.mdn_get_rgba(mdn_font_color_ref)

        # Set the size for the textinput
        self.mdn_textinput.font_size = mdn_font_size_ref

        # Set the halign for the text for the input widget
        self.mdn_textinput.halign = mdn_text_align_ref["halign"]

        if mdn_multiline_ref: return
        if len(self.mdn_textinput._lines) != 1 and len(self.mdn_textinput._lines) != 0: return

        leftover_height = self.mdn_textinput.height - self.mdn_textinput.line_height
        self.mdn_textinput.padding = [10, leftover_height/2, 10, 0]