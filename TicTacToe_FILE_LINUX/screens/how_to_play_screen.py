import os
import json
import random
import shutil
from array import array
from time import sleep, time
from datetime import datetime
from functools import partial
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_input import MDN_Input
from dep.modern_label import MDN_Label
from dep.modern_button import MDN_Button
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_auto_gridlayout import MDN_Auto_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout
from kivy.graphics import Rectangle, Color, Line, BoxShadow

# ===== How_To_Play_Screen Class ===== #
class How_To_Play_Screen_Class(MDN_Screen):
    # +----------------------------------------+
    # |                                        |
    # |               Init Class               |
    # |                                        |
    # +----------------------------------------+
    # init function
    def __init__(self, **kwargs):
        # Load the theme
        self.load_theme(kwargs)
        super().__init__(**kwargs)
        Clock.schedule_once(self.init_ui, 1)

    # +----------------------------------------+
    # |                                        |
    # |        Create Graphic Functions        |
    # |                                        |
    # +----------------------------------------+
    # init_ui method
    def init_ui(self, *args):
        """
            The purpose of this function is to initialize the screen. It will display all the graphics for the screen. This can be done in .kv file, but due to all the complications, it is faster this method.
        """
        # If the 'self.mdn_app' isn't initialized, then exit this function and call it again in .05s
        if not self.mdn_app:
            print("App not found")
            Clock.schedule_once(self.init_ui, .05)
            return
            
        # If the current screen isn't this screen, then exit this function and call it again in .05s 
        # if self.mdn_app.mdn_screenmanager.current_screen.name != "how_to_play_screen":return

        # Create the background
        bg = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_bg = {"image": [self.theme_dest+self.theme["bg"], "stretch"]}
        )
        self.clear_widgets()
        self.mdn_screen_ids["bg"] = bg
        self.add_widget(bg)

        # Call helper functions
        self.create_header_ui()
        self.create_body_ui()
        self.create_footer_ui()

        # Update UI Screen
        self.update_ui()

    # create_header_ui method
    def create_header_ui(self):
        """
            The purpose of this function is to create the header ui. This will display the image banner for the header
        """
        # Create the header container
        header_container = MDN_GridLayout(
            mdn_app = self.mdn_app, 
            mdn_cols = 1, 
            mdn_size = ["100%", "100un"], 
            mdn_bg = {"image": [self.theme_dest+self.theme["header"], "stretch"]},
        )

        # Create the header inner container
        header_inner_rel_container = RelativeLayout()
        header_inner_container = MDN_GridLayout(
            mdn_app = self.mdn_app, 
            mdn_cols = 1, 
            mdn_size = {"desktop": ["725un", "100un"], "tablet": ["725un", "100un"], "mobile": ["675un", "100un"]}, 
        )
        header_inner_container.pos_hint = {"center_x": .5, "center_y": .5}
        header_inner_rel_container.add_widget(header_inner_container)

        # Create the header label & container
        header_label_rel_container = RelativeLayout()
        header_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "How To Play",
            mdn_size = ["100%", "70%"],
            mdn_font_size = self.theme["header_settings_label"]["font_size"],
            mdn_font_style = self.theme["header_settings_label"]["font_style"],
            mdn_font_color = self.theme["header_settings_label"]["font_color"]
        )
        header_label.pos_hint = {"center_x": .5, "center_y": .45}
        header_label_rel_container.add_widget(header_label)
        
        # Combine widgets
        header_inner_container.mdn_add_widget(header_label_rel_container)
        header_container.mdn_add_widget(header_inner_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(header_container)

    # create_body_ui method
    def create_body_ui(self):
        """
            The purpose of this function is to create the body ui.
        """
        # Create a container
        how_to_play_rule_rel_container = RelativeLayout()
        how_to_play_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]})
        how_to_play_container.pos_hint = {"center_x": .5}
        how_to_play_rule_rel_container.add_widget(how_to_play_container)

        # Create padding
        padding_top = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100un"])

        # Create scrollview
        how_to_play_scrollview_container_outer_container = GridLayout(cols = 1)
        how_to_play_scrollview_container = ScrollView(size_hint = (None, None), effect_cls = ScrollEffect)
        self.mdn_screen_ids["how_to_play_scrollview_container"] = how_to_play_scrollview_container
        how_to_play_scrollview_container.bind(pos = self.update_scrollview_size, size = self.update_scrollview_size)
        how_to_play_scrollview_container_outer_container.add_widget(how_to_play_scrollview_container)

        # Create the inner container that will have the parent as the 'scrollview'
        how_to_play_scrollview_inner_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        how_to_play_scrollview_container.add_widget(how_to_play_scrollview_inner_container)
        self.mdn_screen_ids["how_to_play_scrollview_inner_container"] = how_to_play_scrollview_inner_container
    
        # Create the rules and children and the container
        how_to_play_rules = self.get_how_to_play_rules()
        for rule in how_to_play_rules:
            # Create the relative container and the container
            rule_container = MDN_Auto_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
            
            # Create the title
            rule_title = MDN_Label(
                mdn_app = self.mdn_app,
                mdn_size = ["100%", "min_height"],
                mdn_text = rule["title"],
                mdn_line_height = self.theme["title"]["line_height"],
                mdn_text_align = self.theme["title"]["text_align"],
                mdn_font_size = self.theme["title"]["font_size"],
                mdn_font_style = self.theme["title"]["font_style"],
                mdn_font_color = self.theme["title"]["font_color"],
            )

            # Create the description
            rule_description = MDN_Label(
                mdn_app = self.mdn_app,
                mdn_size = ["100%", "min_height"],
                mdn_text = rule["description"],
                mdn_line_height = self.theme["description"]["line_height"],
                mdn_text_align = self.theme["description"]["text_align"],
                mdn_font_size = self.theme["description"]["font_size"],
                mdn_font_style = self.theme["description"]["font_style"],
                mdn_font_color = self.theme["description"]["font_color"],
            )

            # Combine widgets
            rule_container.add_widget(rule_title)
            rule_container.add_widget(rule_description)
            rule_container.add_widget(MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "50un"]))
            how_to_play_scrollview_inner_container.mdn_add_widget(rule_container)



        # Add Widgets to screen
        how_to_play_container.mdn_add_widget(padding_top)
        how_to_play_container.mdn_add_widget(how_to_play_scrollview_container_outer_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(how_to_play_rule_rel_container)

    # create_footer_ui method
    def create_footer_ui(self):
        """
            The purpose of this function is to create the footer. This will include the buttons that can play the game or go back to the home screen
        """
        # ========== Footer ========== #
        # The suffix will always be "f" for "board size"
        # Create the entire container for this option
        f_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "150un"])
        # Create the container for the buttons
        f_button_container_rel_layout = RelativeLayout()
        f_button_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["700un", "100un"])
        f_button_container.pos_hint = {"center_x": .5}
        f_button_container_rel_layout.add_widget(f_button_container)     
        # Create the btn back
        f_back_btn_rel_layout = RelativeLayout()
        f_back_btn = MDN_Button(mdn_app = self.mdn_app, mdn_text = "Back", mdn_size = self.theme["footer_btn"]["size"], mdn_bg = self.theme["footer_btn"]["bg"], mdn_outline = self.theme["footer_btn"]["outline"], mdn_radius = self.theme["footer_btn"]["radius"])
        f_back_btn.pos_hint = {"center_x": .5, "center_y": .6}
        f_back_btn.bind(on_press = partial(self.change_screen, "back"))
        f_back_btn_rel_layout.add_widget(f_back_btn)     
        # Create the footer padding
        f_gap_1 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "25un"]) 
        f_gap_2 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "25un"]) 
        # ========== Add Widgets To "F_Container" ========== #
        f_button_container.mdn_add_widget(f_back_btn_rel_layout)
        f_container.mdn_add_widget(f_gap_1)
        f_container.mdn_add_widget(f_button_container_rel_layout)
        f_container.mdn_add_widget(f_gap_2)
        # ========== Add Widgets To Inner Container ========== #
        self.mdn_screen_ids["bg"].mdn_add_widget(f_container)


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
            Clock.schedule_once(self.update_ui, .05)
            return

        if self.mdn_app.mdn_screenmanager.current_screen.name != "how_to_play_screen":
            Clock.schedule_once(self.update_ui, .05)
            return

        # Update the background of the screen
        self.mdn_screen_ids["bg"]._mdn_update_graphic()

    # upate_scrollview method
    def update_scrollview_size(self, *args):
        """
            The purpose of this function is to update the scrollview's size
        """
        # Get the scrollview
        how_to_play_scrollview_container = self.mdn_screen_ids["how_to_play_scrollview_container"]

        # Update the size & pos of the 'how_to_play_scrollview_container'
        how_to_play_scrollview_container.size = how_to_play_scrollview_container.parent.size
        how_to_play_scrollview_container.pos = how_to_play_scrollview_container.parent.pos

        # Calculate the height for the 'how_to_play_scrollview_container'
        how_to_play_scrollview_inner_container_height = 0
        for child in self.mdn_screen_ids["how_to_play_scrollview_inner_container"].children:how_to_play_scrollview_inner_container_height+=child.height

        # Update size for 'self.mdn_screen_ids["how_to_play_scrollview_inner_container"]'
        self.mdn_screen_ids["how_to_play_scrollview_inner_container"].mdn_update({"mdn_size": ["100%", "{}un".format(int(how_to_play_scrollview_inner_container_height))]})


    # +----------------------------------------+
    # |                                        |
    # |         Button Event Functions         |
    # |                                        |
    # +----------------------------------------+
    # change_screen method
    def change_screen(self, *args):
        """
            The purpose of this function is to change screens
        """
        if args[0] == "back": self.mdn_switch("home_screen", "Welcome To TicTacToe", None, "RiseIn")


    # +----------------------------------------+
    # |                                        |
    # |         Miscellaneos Functions         |
    # |                                        |
    # +----------------------------------------+
    # get_how_to_play_rules method
    def get_how_to_play_rules(self):
        """
            The purpose of this function is to get the rules for the 'how_to_play_screen'. This is in the 'game_data/rules.json' file.
        """
       # Store the original file
        original_directory = "game_data/"
        original_file = "rules.json"

        # Check to see if file and path exists
        if os.path.isfile(original_directory+original_file): prev_existed = True
        else: prev_existed = False

        # If file doesn't exist, then return
        if not prev_existed:
            print("Sorry the 'rules.json' file doesn't exist!!!")
            return

        # Open the json file
        with open(original_directory+original_file, "r") as rules_file:
            rules_json = json.load(rules_file)
        rules_file.close()  

        # Return rules
        return rules_json["how_to_play_rules"]

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

