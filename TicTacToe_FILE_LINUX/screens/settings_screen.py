import json
from glob import glob
from functools import partial
from kivy.clock import Clock
from kivy.uix.fitimage import FitImage
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_button import MDN_Button
from dep.modern_label import MDN_Label
from dep.modern_input import MDN_Input
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout

# =========== Settings Screen Class =========== #
class Settings_Screen_Class(MDN_Screen):
   # +----------------------------------------+
   # |                                        |
   # |               Init Class               |
   # |                                        |
   # +----------------------------------------+
    # init function
    def __init__(self, **kwargs):
        # Load all the theme from kwargs
        self.load_theme(kwargs)

        # Load all the themes
        self.get_available_themes()

        # Start the app
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_ui, .1)
        Clock.schedule_once(self.update_ui, 1)

        # Create a var that will hold the row theme height
        self.body_theme_scrollview_inner_container_height = 225


    # +----------------------------------------+
    # |                                        |
    # |            Graphic Functions           |
    # |                                        |
    # +----------------------------------------+
    # init_ui method
    def init_ui(self, *args):
        """
            The purpose of this function is to initialize the screen. It will display all the graphics for the screen. This can be done in .kv file, but due to all the complications, it is faster this method.
        """
        # Create the background
        bg = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_bg = {"image": [self.theme_dest+self.theme["bg"], "stretch"]})
        self.mdn_screen_ids["bg"] = bg
        self.add_widget(bg)

        # Call helper functions
        self.create_header_ui()
        self.create_body_ui()

    # create_header_ui method
    def create_header_ui(self):
        """
            The purpose of this function is to create the header ui. This will display the image banner for the header
        """
        # Create the header container
        header_container = MDN_GridLayout(
            mdn_app = self.mdn_app, 
            mdn_cols = 3, 
            mdn_size = ["100%", "100un"], 
            mdn_bg = {"image": [self.theme_dest+self.theme["header_bg"], "stretch"]},
        )

        # Create the back button
        bck_btn_rel_container = RelativeLayout(size_hint = (.25, 1))
        bck_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["100un", "25un"],
            mdn_bg = {"image": [self.theme_dest+self.theme["header_bck_btn"], "fit"]},
        )
        bck_btn.bind(on_press = partial(self.change_screen, "bck"))
        bck_btn.pos_hint = {"center_x": .5, "center_y": .55}
        bck_btn_rel_container.add_widget(bck_btn)

        # Create the header label & it's relative container
        header_label_rel_container = RelativeLayout(size_hint = (.5, 1))
        header_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100%", "80%"],
            mdn_text = "Display Settings",
            mdn_font_size = self.theme["header_label"]["font_size"],
            mdn_font_color = self.theme["header_label"]["font_color"],
            mdn_font_style = self.theme["header_label"]["font_style"]
        )
        header_label.pos_hint = {"center_x": .5, "center_y": .45}
        header_label_rel_container.add_widget(header_label)
        
        # Create the settings icon
        setting_icon_2_rel_container = RelativeLayout(size_hint = (.25, 1))
        setting_icon_2 = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100un", "40un"],
            mdn_bg = {"image": [self.theme_dest+self.theme["header_setting_icon"], "fit"]},
        )
        setting_icon_2.pos_hint = {"center_x": .5, "center_y": .55}
        setting_icon_2_rel_container.add_widget(setting_icon_2)

        # Combine widgets
        header_container.mdn_add_widget(bck_btn_rel_container)
        header_container.mdn_add_widget(header_label_rel_container)
        header_container.mdn_add_widget(setting_icon_2_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(header_container)

    # create_body_ui method
    def create_body_ui(self):
        """
            The purpose of this function is to create the body ui.
        """
        # Create the body container
        body_rel_container = RelativeLayout()
        body_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]})
        body_container.pos_hint = {"center_x": .5}
        body_rel_container.add_widget(body_container)

        # Create the theme container
        body_theme_rel_container = self.create_body_theme_ui()

        # # Create the font size container
        # body_font_size_rel_container = self.create_body_font_ui()

        body_container.mdn_add_widget(body_theme_rel_container)
        # body_container.mdn_add_widget(body_font_size_rel_container)

        self.mdn_screen_ids["bg"].mdn_add_widget(body_rel_container)

    # create_body_theme_ui method
    def create_body_theme_ui(self):
        """
            The purpose of this function is to create the body theme ui.
        """
        # Create the theme container
        body_theme_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "100%"])
        body_theme_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
        body_theme_rel_container.add_widget(body_theme_container)

        # Create the top padding
        body_theme_top_padding = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "40un"])
        body_theme_container.mdn_add_widget(body_theme_top_padding)

        # Create the theme label
        body_theme_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Themes",
            mdn_size = ["100%", "120un"],
            mdn_font_size = self.theme["themes_label"]["font_size"],
            mdn_font_style = self.theme["themes_label"]["font_style"],
            mdn_font_color = self.theme["themes_label"]["font_color"]
        )
        body_theme_container.mdn_add_widget(body_theme_label)

        # Create the scrollview
        body_theme_scrollview_rel_container = RelativeLayout()
        body_theme_scrollview_container_outer_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100%"], mdn_bg = {"color": [255, 0, 0, 0]})
        self.mdn_screen_ids["body_theme_scrollview_container_outer_container"] = body_theme_scrollview_container_outer_container
        body_theme_scrollview_container = ScrollView(size_hint = (None, None), effect_cls = ScrollEffect)
        self.mdn_screen_ids["body_theme_scrollview_container"] = body_theme_scrollview_container
        body_theme_scrollview_container.bind(pos = self.update_scrollview_size, size = self.update_scrollview_size)
        body_theme_scrollview_container_outer_container.add_widget(body_theme_scrollview_container)
        body_theme_scrollview_rel_container.add_widget(body_theme_scrollview_container_outer_container)
        body_theme_container.mdn_add_widget(body_theme_scrollview_rel_container)

        # Create the inner container that will have the parent as the 'scrollview'
        body_theme_scrollview_inner_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100%"])
        body_theme_scrollview_container_outer_container.bind(size = self.create_theme_row, pos = self.create_theme_row)
        body_theme_scrollview_container.add_widget(body_theme_scrollview_inner_container)
        self.mdn_screen_ids["body_theme_scrollview_inner_container"] = body_theme_scrollview_inner_container 

        # Return
        return body_theme_rel_container

    # dreate_body_theme_ui method
    def create_body_font_ui(self):
        """
            The purpose of this function is to create the body font ui.
        """
        # Create the font container
        body_font_rel_container = RelativeLayout(size_hint = (1, .6))
        body_font_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
        body_font_rel_container.add_widget(body_font_container)

        # Create the font container divider
        body_font_divider = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "5un"], mdn_bg = {"color": [0, 0, 0, 1]})
        body_font_container.mdn_add_widget(body_font_divider)

        # Create the top padding
        body_font_top_padding = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "40un"])
        body_font_container.mdn_add_widget(body_font_top_padding)

        # Create the theme label
        body_font_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Font",
            mdn_font_size = 40,
            mdn_size = ["100%", "120un"]
        )
        body_font_container.mdn_add_widget(body_font_label)

        # Create the body font option container
        body_font_option_rel_container = RelativeLayout()
        body_font_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        body_font_option_rel_container.add_widget(body_font_option_container)
        body_font_container.mdn_add_widget(body_font_option_rel_container)

        # Create the label container and the label container
        body_font_option_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        body_font_option_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Size:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = 40
        )
        body_font_option_label.pos_hint = {"center_x": .5, "center_y": .8}
        body_font_option_label_rel_layout.add_widget(body_font_option_label)
        body_font_option_container.mdn_add_widget(body_font_option_label_rel_layout)

        # Create the option container
        body_font_option_setting_rel_container = RelativeLayout(size_hint = (.7, 1))
        body_font_option_setting_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["400un", "100%"])
        body_font_option_setting_rel_container.add_widget(body_font_option_setting_container)
        body_font_option_container.mdn_add_widget(body_font_option_setting_rel_container)

        # Create the back btn container and the button
        body_font_option_back_btn_rel_layout = RelativeLayout()
        body_font_option_back_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = "themes/default/resources/general/arrow_l.png",
            mdn_size = ["100%", "65un"]
        )
        body_font_option_back_btn.pos_hint = {"center_x": .5, "center_y": .8}
        body_font_option_back_btn_rel_layout.add_widget(body_font_option_back_btn)    
        body_font_option_setting_container.mdn_add_widget(body_font_option_back_btn_rel_layout) 

        # Create the computer difficulty label
        body_font_option_computer_difficulty_rel_layout = RelativeLayout()
        body_font_option_computer_difficulty = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "1",
            mdn_font_color = [58, 168, 252, 1],
            mdn_font_size = 32
        )
        self.mdn_screen_ids["body_font_option_computer_difficulty"] = body_font_option_computer_difficulty
        body_font_option_computer_difficulty.pos_hint = {"center_x": .5, "center_y": .8}
        body_font_option_computer_difficulty_rel_layout.add_widget(body_font_option_computer_difficulty)
        body_font_option_setting_container.mdn_add_widget(body_font_option_computer_difficulty_rel_layout) 

        # Create the fwd btn container and the button
        body_font_option_fwd_btn_rel_layout = RelativeLayout()
        body_font_option_fwd_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = "themes/default/resources/general/arrow_r.png",
            mdn_size = ["100%", "65un"]
        )
        body_font_option_fwd_btn.pos_hint = {"center_x": .5, "center_y": .8}
        body_font_option_fwd_btn_rel_layout.add_widget(body_font_option_fwd_btn)    
        body_font_option_setting_container.mdn_add_widget(body_font_option_fwd_btn_rel_layout)   


        return body_font_rel_container    


    # +----------------------------------------+
    # |                                        |
    # |          Update UI Functions           |
    # |                                        |
    # +----------------------------------------+
    # update_ui method
    def update_ui(self, *args):
        """
            The purpose of this function is to update all the widgets that are on the screen. For some reason, they won't update unless the window resizes or something triggers the event
        """
        if not self.mdn_app:
            Clock.schedule_once(self.update_ui, 1)
            return

        if self.mdn_app.mdn_screenmanager.current_screen.name != "profile_screen":
            Clock.schedule_once(self.update_ui, 1)
            return

        self.update_scrollview_size()
        self.mdn_screen_ids["bg"]._mdn_update_graphic()

    # upate_scrollview method
    def update_scrollview_size(self, *args):
        """
            The purpose of this function is to update the scrollview's size
        """
        
        # Get the scrollview
        scrollview_container = self.mdn_screen_ids["body_theme_scrollview_container"]

        # Update the size & pos of the 'scrollview_container'
        scrollview_container.size = scrollview_container.parent.size
        scrollview_container.pos = scrollview_container.parent.pos

        # Calculate the height for the 'scrollview_container'
        scrollview_inner_container_height = 0
        for child in self.mdn_screen_ids["body_theme_scrollview_inner_container"].children: scrollview_inner_container_height+=self.body_theme_scrollview_inner_container_height

        # Update size for 'self.mdn_screen_ids["scrollview_inner_container"]'
        self.mdn_screen_ids["body_theme_scrollview_inner_container"].mdn_update({"mdn_size": ["100%", "{}un".format(int(scrollview_inner_container_height))]})

    # create_theme_row method
    def create_theme_row(self, *args):
        """
            The purpose of this function is to create the row for the themes
        """
        try:
            # Get and Store the selected theme
            with open("cache.json") as cache_file:
                cache_json = json.load(cache_file)
            cache_file.close()

            # Store the current theme from the cached data
            current_theme_key = cache_json["theme"]["theme_key"]
        except: current_theme_key = "default"

        # Get the 'body_theme_scrollview_container_outer_container' from the mdn_screen variables 
        body_theme_scrollview_container_outer_container = self.mdn_screen_ids["body_theme_scrollview_container_outer_container"]

        # Get the 'body_theme_scrollview_container_inner_container' from the mdn_screen variables 
        body_theme_scrollview_inner_container = self.mdn_screen_ids["body_theme_scrollview_inner_container"]

        # Clear all the widgets from the inner container
        body_theme_scrollview_inner_container.clear_widgets()

        # Create a var that will keep track of how many themes go in a row
        row_theme_count = 2 if body_theme_scrollview_container_outer_container._mdn_get_device_size() == "mobile" else 3

        # Create number of rows for the themes
        number_of_rows = int(len(self.available_themes) / row_theme_count) if len(self.available_themes) % row_theme_count == 0 else \
        int(len(self.available_themes) / row_theme_count) + 1
        number_of_rows = 1 if len(self.available_themes) > 0 and len(self.available_themes) < row_theme_count else number_of_rows  

        # Create a var that will hold all the themes
        theme_count = 0

        # Loop thru the number of 'number_of_rows'
        for i in range(number_of_rows):

            # Create a row for the three or two themes
            scrollview_theme_row_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "{}un".format(self.body_theme_scrollview_inner_container_height)])
            scrollview_theme_row = MDN_GridLayout(
                mdn_app = self.mdn_app,
                mdn_size = ["100%", "200un"],
                mdn_cols = row_theme_count,
            )
            scrollview_theme_row.pos_hint = {"center_x": .5, "center_y": .5}
            scrollview_theme_row_rel_container.add_widget(scrollview_theme_row)

            # Loop thru the 'row_theme_count'
            for j in range(row_theme_count):

                # Create the theme item
                scrollview_theme_item_rel_container = RelativeLayout()
                if theme_count < len(self.available_themes):
                    scrollview_theme_item = MDN_Label(
                        mdn_app = self.mdn_app,
                        mdn_size = ["190un", "190un"], 
                        mdn_text = self.available_themes[list(self.available_themes.keys())[theme_count]]["name"],
                        mdn_font_size = self.theme["scrollview_theme_item_label"]["font_size"],
                        mdn_font_color = self.theme["scrollview_theme_item_label"]["font_color"],
                        mdn_font_style = self.theme["scrollview_theme_item_label"]["font_style"],
                        mdn_outline = self.theme["scrollview_theme_item_label"]["outline"]["selected"] if self.available_themes[list(self.available_themes.keys())[theme_count]]["key"] == current_theme_key else self.theme["scrollview_theme_item_label"]["outline"]["normal"],
                        mdn_bg = {"image": [self.available_themes[list(self.available_themes.keys())[theme_count]]["thumbnail"], "stretch"]},
                        mdn_line_height = 1.0
                    )
                    scrollview_theme_item.pos_hint = {"center_x": .5, "center_y": .5}
                    scrollview_theme_item_rel_container.add_widget(scrollview_theme_item)

                # Add widgets
                scrollview_theme_row.mdn_add_widget(scrollview_theme_item_rel_container)
                theme_count+=1   

            # Add row to the inner container
            body_theme_scrollview_inner_container.mdn_add_widget(scrollview_theme_row_rel_container)

    # +----------------------------------------+
    # |                                        |
    # |              Button Events             |
    # |                                        |
    # +----------------------------------------+
    # change_profile_option method
    def change_profile_option(self, profile_option_field, *args):
        """
            The purpose of this function is to edit the profile field
        """
        return
        # Get the parent container from the 'mdn_screens_ids
        parent_rel_container = self.mdn_screen_ids["profile_option_input_{}_rel_container".format(profile_option_field)]

        # Clear the widgets from the parent container
        parent_rel_container.clear_widgets()

        # Hold this variable
        self.profile_option_field = profile_option_field

        if self.mdn_screen_ids["profile_option_input_{}".format(self.profile_option_field.lower())].__class__.__name__ == "MDN_Input":

            profile_option_field_input = MDN_Label(
                mdn_app = self.mdn_app,
                mdn_text = self.profile_option_field,
                mdn_size = ["99%", "80un"],
                mdn_outline = [[0, 0, 0, 1], 2],
                mdn_bg = {"color": [255, 255, 255, 1]},
                mdn_text_align = ["center", "bottom"]
            )

            self.mdn_screen_ids["profile_option_input_{}".format(self.profile_option_field.lower())] = profile_option_field_input
            profile_option_field_input.pos_hint = {"center_x": .5, "center_y": .5}
            parent_rel_container.add_widget(profile_option_field_input)
            return


        # Create the input container
        profile_option_field_input = MDN_Input(
            mdn_app = self.mdn_app,
            mdn_placeholder = profile_option_field, 
            mdn_size = ["99%", "80un"],
            mdn_outline = [[0, 0, 0, 1], 1], 
            mdn_button_visible = False, 
            mdn_multiline = False
        )
        profile_option_field_input.bind(on_leave = partial(self.change_profile_option, self.profile_option_field))
        profile_option_field_input.pos_hint = {"center_x": .5, "center_y": .5}



        # Combine widgets
        parent_rel_container.add_widget(profile_option_field_input)
        
        # new = MDN_Label(mdn_app = self.mdn_app, mdn_placeholder = profile_option_field, mdn_size = ["99%", "80un"], mdn_outline = [[0, 0, 0, 1], 1], mdn_button_visible = False, mdn_multiline = False)

        # profile_option_field_button.parent.add_widget(new)

    # change_screen method
    def change_screen(self, *args):
        """
            The purpose of this function is to change screens
        """
        if args[0] == "bck": self.mdn_switch("home_screen", "Welcome To TicTacToe", "right")


    # +----------------------------------------+
    # |                                        |
    # |        Miscellaneous Functions         |
    # |                                        |
    # +----------------------------------------+
    # load_theme method
    def load_theme(self, kwargs):
        """
            The purpose of this function is to load the theme from the args
        """
        # Load all the theme from kwargs
        self.theme = kwargs["theme"]

        # Load all the general theme items from kwargs
        self.general_theme = kwargs["general_theme"]

        # Create the theme destination
        self.theme_dest = "themes/{}/".format(self.general_theme["folder_dest"])

        # Remove the themes from the kwargs
        if "theme" in kwargs: kwargs.pop("theme")
        if "general_theme" in kwargs: kwargs.pop("general_theme")

        return kwargs


    # get_available_themes method
    def get_available_themes(self):
        """
            The purpose of this function is to get and load all the available themes from the theme folder
        """
        # Create a var that will hold the available themes
        self.available_themes = {}

        # Get all the themes from the theme folder
        themes = glob("themes/*/")

        # Get all the theme info and store it in 'self.available_themes'
        for theme in themes:

            # Open each theme's json file
            with open(theme+"theme.json") as theme_file:
                theme_json = json.load(theme_file)
            theme_file.close()

            # Store info in the 'self.available_themes'
            self.available_themes[theme_json["theme"]["general_info"]["name"].lower()] = {
                "thumbnail": theme+theme_json["theme"]["general_info"]["thumbnail"],
                "key": theme_json["theme"]["general_info"]["key"],
                "name": theme_json["theme"]["general_info"]["name"]
            }