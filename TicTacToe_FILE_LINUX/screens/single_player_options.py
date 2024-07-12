import os
import json
from kivy.clock import Clock
from functools import partial
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_label import MDN_Label
from dep.modern_button import MDN_Button
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout

# ======== Single Player Options Class ======== #
class Single_Player_Options_Class(MDN_Screen):
   # +----------------------------------------+
   # |                                        |
   # |               Init Class               |
   # |                                        |
   # +----------------------------------------+
    # init function
    def __init__(self, **kwargs):
        # Load all the theme from kwargs
        self.load_theme(kwargs)
        super().__init__(**kwargs)

        # Create variables
        self.computer_difficulty = 0
        self.play_as = "x"
        self.starts_first = "player"
        self.advanced_options_opened = False
        self.play_mode = "casual"
        self.board_size = 3
        self.win_length = 3
        self.move_timer = "-10"  

        # If cache data exists, then take this path
        if os.path.exists("cache.json"):

            # Load the current theme from the stored cache
            with open("cache.json", "r") as json_file:
                json_code = json.load(json_file)
            json_file.close()

            # Check to see if single_player_options_data exists
            if "single_player_options" in json_code:
                # Load the data into the vars
                self.computer_difficulty = json_code["single_player_options"]["difficulty"]
                self.play_as = json_code["single_player_options"]["play_as"]
                self.starts_first = json_code["single_player_options"]["starts_first"]
                self.advanced_options_opened = json_code["single_player_options"]["show_advance_options"]
                self.play_mode = json_code["single_player_options"]["play_mode"]
                self.board_size = json_code["single_player_options"]["board_size"]
                self.win_length = json_code["single_player_options"]["win_length"]
                self.move_timer = json_code["single_player_options"]["move_timer"]

        # Set the 'computer_levels' var
        self.computer_levels = ["Easy", "Normal", "Hard"]

        # Set the 'computer_play_as' var
        self.computer_play_as = "x" if self.play_as == "o" else "o"

        # Set the 'timers_for_moves' var
        self.timers_for_moves = ["2", "3", "4", "5"]

        # ===== UI Option Containers ===== #
        self.bs_container_rel_layout = None
        self.wl_container_rel_layout = None
        self.gt_container_rel_layout = None
        self.mt_container_rel_layout = None
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
        # Create the background
        bg = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_bg = {"image":[self.theme_dest+self.theme["bg"],"stretch"]}
        )
        self.mdn_screen_ids["bg"] = bg
        self.add_widget(bg)

        # Create UI Screen 
        self.create_header_ui()
        self.create_body_ui()
        self.create_footer_ui()

        # Change The Highlighted UI Graphics
        self.change_play_as_type(self.play_as, "default")
        self.change_starts_first(self.starts_first, "default")
        self.show_advanced_options("default")

    # create_header_ui method
    def create_header_ui(self):
        """
            The purpose of this function is to create the header ui. This will display the image banner for the header
        """
        # Create the header container
        header_container = MDN_GridLayout(
            mdn_app = self.mdn_app, 
            mdn_cols = 3, 
            mdn_size = ["100%", "120un"], 
            mdn_bg = {"image": [self.theme_dest+self.theme["header"], "stretch"]},
        )

        # Create the header label relative container
        header_label_rel_container = RelativeLayout()

        # Create the header label
        header_label = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100%", "60%"],
            mdn_bg = {"image": [self.theme_dest+self.theme["header_label"], "fit"]},
        )
        header_label.pos_hint = {"center_x": .5, "center_y": .55}
        
        # Combine widgets
        header_label_rel_container.add_widget(header_label)
        header_container.mdn_add_widget(header_label_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(header_container)

    # create_body_ui method
    def create_body_ui(self):
        """
            The purpose of this function is to create the default options. This includes the computer difficulty, player type, and who starts first.
            The suffix will always be "d" for "difficulty"
        """
        # Create the body container
        body_container_rel_layout = RelativeLayout()
        body_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]})
        body_container_rel_layout.add_widget(body_container)
        body_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["body_container"] = body_container

        # Create the padding at the top of the body container
        body_container_top_pading = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["80%", "20un"])
        self.mdn_screen_ids["body_container"].mdn_add_widget(body_container_top_pading)

        # Create scrollview
        body_scrollview_container_outer_container = GridLayout(cols = 1)
        body_scrollview_container = ScrollView(size_hint = (None, None), effect_cls = ScrollEffect)
        self.mdn_screen_ids["body_scrollview_container"] = body_scrollview_container
        body_scrollview_container.bind(pos = self.update_scrollview_size, size = self.update_scrollview_size)
        body_scrollview_container_outer_container.add_widget(body_scrollview_container)

        # Create the inner container that will have the parent as the 'scrollview'
        body_scrollview_inner_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        body_scrollview_container.add_widget(body_scrollview_inner_container)
        self.mdn_screen_ids["body_scrollview_inner_container"] = body_scrollview_inner_container

        # Create The Default Options Container
        default_options_container_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "390un"])
        default_options_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
        default_options_container.pos_hint = {"center_x": .5, "center_y": .5}
        default_options_container_rel_layout.add_widget(default_options_container)

        # Create the entire container for this option
        d_container_rel_layout = self.create_difficutly_option()

        # Create the entire container for this option
        pa_container_rel_layout = self.create_play_as_option()

        # Create the entire container for this option
        sf_container_rel_layout = self.create_starts_first_option()

        # Create Advanced Option
        advanced_options_container = self.create_advanced_option()

        # More Options Container 
        more_options_container_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "520un"])
        more_options_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
        more_options_container_rel_layout.add_widget(more_options_container)
        self.mdn_screen_ids["more_options_container"] = more_options_container

        # Add Widgets To Screen #
        default_options_container.add_widget(d_container_rel_layout)
        default_options_container.add_widget(pa_container_rel_layout)
        default_options_container.add_widget(sf_container_rel_layout)
        self.mdn_screen_ids["body_scrollview_inner_container"].mdn_add_widget(default_options_container_rel_layout)
        self.mdn_screen_ids["body_scrollview_inner_container"].mdn_add_widget(advanced_options_container)
        self.mdn_screen_ids["body_scrollview_inner_container"].mdn_add_widget(more_options_container_rel_layout)
        body_container.mdn_add_widget(body_scrollview_container_outer_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(body_container_rel_layout)

    # create_footer_ui method
    def create_footer_ui(self):
        """
            The purpose of this function is to create the footer. This will include the buttons that can play the game or go back to the home screen
        """
        # ========== Footer ========== #
        # The suffix will always be "f" for "board size"
        # Create the entire container for this option
        f_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "200un"])

        # Create the container for the buttons
        f_button_container_rel_layout = RelativeLayout()
        f_button_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["700un", "100un"])
        f_button_container.pos_hint = {"center_x": .5}
        f_button_container_rel_layout.add_widget(f_button_container)  

        # Create the btn back
        f_back_btn_rel_layout = RelativeLayout()
        f_back_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Back",
            mdn_bg = self.theme["footer_btn"]["bck_btn"]["bg"],
            mdn_size = self.theme["footer_btn"]["bck_btn"]["size"],
            mdn_radius = self.theme["footer_btn"]["bck_btn"]["radius"],
            mdn_outline = self.theme["footer_btn"]["bck_btn"]["outline"],
            mdn_font_size = self.theme["footer_btn"]["bck_btn"]["font_size"],
            mdn_font_color = self.theme["footer_btn"]["bck_btn"]["font_color"],
            mdn_font_style = self.theme["footer_btn"]["bck_btn"]["font_style"],
        )
        f_back_btn.pos_hint = {"center_x": .6, "center_y": .6}
        f_back_btn.bind(on_press = partial(self.change_screen, "back"))
        f_back_btn_rel_layout.add_widget(f_back_btn) 

        # Create the btn play
        f_play_btn_rel_layout = RelativeLayout()
        f_play_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Play",
            mdn_bg = self.theme["footer_btn"]["play_btn"]["bg"],
            mdn_size = self.theme["footer_btn"]["play_btn"]["size"],
            mdn_radius = self.theme["footer_btn"]["play_btn"]["radius"],
            mdn_outline = self.theme["footer_btn"]["play_btn"]["outline"],
            mdn_font_size = self.theme["footer_btn"]["play_btn"]["font_size"],
            mdn_font_color = self.theme["footer_btn"]["play_btn"]["font_color"],
            mdn_font_style = self.theme["footer_btn"]["play_btn"]["font_style"],
        )
        f_play_btn.pos_hint = {"center_x": .4, "center_y": .6}
        f_play_btn.bind(on_press = partial(self.change_screen, "play"))
        f_play_btn_rel_layout.add_widget(f_play_btn) 

        # Create the footer padding
        f_gap_1 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "50un"]) 
        f_gap_2 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "50un"]) 

        # ========== Add Widgets To "F_Container" ========== #
        f_button_container.mdn_add_widget(f_back_btn_rel_layout)
        f_button_container.mdn_add_widget(f_play_btn_rel_layout)
        f_container.mdn_add_widget(f_gap_1)
        f_container.mdn_add_widget(f_button_container_rel_layout)
        f_container.mdn_add_widget(f_gap_2)

        # ========== Add Widgets To Inner Container ========== #
        self.mdn_screen_ids["body_container"].mdn_add_widget(f_container)

    # create_difficutly_option method
    def create_difficutly_option(self):
        """
            The purpose of this function is to create the difficulty option
        """
        # ========== Create Difficulty Option ========== #
        # The suffix will always be "d" for "difficulty"
        # Create the entire container for this option
        d_container_rel_layout = RelativeLayout()
        d_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        d_container.pos_hint = {"center_x": .5, "center_y": .5}
        d_container_rel_layout.add_widget(d_container)

        # Create the label container and the label container
        d_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        d_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Difficulty:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        d_label.pos_hint = {"center_x": .4}
        d_label_rel_layout.add_widget(d_label)

        # Create the option container
        d_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        d_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["400un", "100%"])
        d_option_container.pos_hint = {"center_x": .5}
        d_option_container_rel_layout.add_widget(d_option_container)

        # Create the back btn container and the button
        d_back_btn_rel_layout = RelativeLayout()
        d_back_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["left"]["icon"],
            mdn_size = self.theme["arrow_btn"]["left"]["size"]
        )
        d_back_btn.bind(on_press = partial(self.change_computer_difficulty, "back"))
        d_back_btn.pos_hint = {"center_x": .5, "center_y": .5}
        d_back_btn_rel_layout.add_widget(d_back_btn)

        # Create the computer difficulty label
        d_computer_difficulty_rel_layout = RelativeLayout()
        d_computer_difficulty = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = self.computer_levels[self.computer_difficulty],
            mdn_font_color = self.theme["primary_font_color"],
            mdn_font_size = self.theme["primary_font_size"]
        )
        self.mdn_screen_ids["d_computer_difficulty"] = d_computer_difficulty
        d_computer_difficulty.pos_hint = {"center_x": .5, "center_y": .5}
        d_computer_difficulty_rel_layout.add_widget(d_computer_difficulty)

        # Create the fwd btn container and the button
        d_fwd_btn_rel_layout = RelativeLayout()
        d_fwd_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["right"]["icon"],
            mdn_size = self.theme["arrow_btn"]["right"]["size"]
        )
        d_fwd_btn.bind(on_press = partial(self.change_computer_difficulty, "fwd"))
        d_fwd_btn.pos_hint = {"center_x": .5, "center_y": .5}
        d_fwd_btn_rel_layout.add_widget(d_fwd_btn)

        # Add Widgets To The "d_option_container"
        d_option_container.mdn_add_widget(d_back_btn_rel_layout)
        d_option_container.mdn_add_widget(d_computer_difficulty_rel_layout)
        d_option_container.mdn_add_widget(d_fwd_btn_rel_layout)

        # Add Widgets To The Screen
        d_container.mdn_add_widget(d_label_rel_layout)
        d_container.mdn_add_widget(d_option_container_rel_layout)

        return d_container_rel_layout        

    # create_play_as_option method
    def create_play_as_option(self):
        """
            The purpose of this function is to create the play as option
        """
       # ========== Create Play As Option ========== #
        # The suffix will always be "pa" for "play as"
        # Create the entire container for this option
        pa_container_rel_layout = RelativeLayout()
        pa_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        pa_container.pos_hint = {"center_x": .5, "center_y": .5}
        pa_container_rel_layout.add_widget(pa_container)

        # Create the label container and the label container
        pa_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        pa_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Play As:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        pa_label.pos_hint = {"center_x": .4}
        pa_label_rel_layout.add_widget(pa_label)

        # Create the option container
        pa_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        pa_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["400un", "100%"])
        pa_option_container.pos_hint = {"center_x": .5}
        pa_option_container_rel_layout.add_widget(pa_option_container)

        # Create the play as button o
        pa_btn_o_rel_layout = RelativeLayout()
        pa_btn_o = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_icon = self.theme_dest+self.theme["play_as_btn"]["o"]["dark"]["icon"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_icon_size = self.theme["play_as_btn"]["o"]["dark"]["icon_size"]
        )
        self.mdn_screen_ids["pa_btn_o"] = pa_btn_o
        pa_btn_o.bind(on_press = partial(self.change_play_as_type, "o"))
        pa_btn_o.pos_hint = {"center_x": .5, "center_y": .5}
        pa_btn_o_rel_layout.add_widget(pa_btn_o)

        # Create the play as button x
        pa_btn_x_rel_layout = RelativeLayout()
        pa_btn_x = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_icon = self.theme_dest+self.theme["play_as_btn"]["x"]["dark"]["icon"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_icon_size = self.theme["play_as_btn"]["x"]["dark"]["icon_size"]
        )
        self.mdn_screen_ids["pa_btn_x"] = pa_btn_x
        pa_btn_x.bind(on_press = partial(self.change_play_as_type, "x"))
        pa_btn_x.pos_hint = {"center_x": .5, "center_y": .5}
        pa_btn_x_rel_layout.add_widget(pa_btn_x)

        # Create the play as random x or o
        pa_btn_x_o_rel_layout = RelativeLayout()
        pa_btn_x_o = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["100un", "70un"],
            mdn_icon = self.theme_dest+self.theme["play_as_btn"]["x_o"]["dark"]["icon"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_icon_size = self.theme["play_as_btn"]["x_o"]["dark"]["icon_size"]
        )
        self.mdn_screen_ids["pa_btn_x_o"] = pa_btn_x_o
        pa_btn_x_o.bind(on_press = partial(self.change_play_as_type, "x_o"))
        pa_btn_x_o.pos_hint = {"center_x": .5, "center_y": .5}
        pa_btn_x_o_rel_layout.add_widget(pa_btn_x_o)

        # Add Widgets To The "pa_option_container"
        pa_option_container.mdn_add_widget(pa_btn_o_rel_layout)
        pa_option_container.mdn_add_widget(pa_btn_x_rel_layout)
        pa_option_container.mdn_add_widget(pa_btn_x_o_rel_layout)

        # Add Widgets To The Screen
        pa_container.mdn_add_widget(pa_label_rel_layout)
        pa_container.mdn_add_widget(pa_option_container_rel_layout)  

        return pa_container_rel_layout    

    # create_starts_first_option method
    def create_starts_first_option(self):
        """
            The purpose of this function is to create the starts first option
        """
        # ========== Create Starts First Option ========== #
        # The suffix will always be "sf" for "starts first"
        # Create the entire container for this option
        sf_container_rel_layout = RelativeLayout()
        sf_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        sf_container.pos_hint = {"center_x": .5, "center_y": .5}
        sf_container_rel_layout.add_widget(sf_container)

        # Create the label container and the label container
        sf_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        sf_label = MDN_Label(
            mdn_app = self.mdn_app, 
            mdn_text = "Starts First:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        sf_label.pos_hint = {"center_x": .4}
        sf_label_rel_layout.add_widget(sf_label)

        # Create the option container
        sf_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        sf_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["400un", "100%"])
        sf_option_container.pos_hint = {"center_x": .5}
        sf_option_container_rel_layout.add_widget(sf_option_container)

        # Create the starts first button "Player"
        sf_btn_player_rel_layout = RelativeLayout()
        sf_btn_player = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Player",
            mdn_size = ["170un", "80un"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["sf_btn_player"] = sf_btn_player
        sf_btn_player.bind(on_press = partial(self.change_starts_first, "player"))
        sf_btn_player.pos_hint = {"center_x": .5, "center_y": .5}
        sf_btn_player_rel_layout.add_widget(sf_btn_player)

        # Create the starts first button "Computer"
        sf_btn_computer_rel_layout = RelativeLayout()
        sf_btn_computer = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Computer",
            mdn_size = ["170un", "80un"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["sf_btn_computer"] = sf_btn_computer
        sf_btn_computer.bind(on_press = partial(self.change_starts_first, "computer"))
        sf_btn_computer.pos_hint = {"center_x": .5, "center_y": .5}
        sf_btn_computer_rel_layout.add_widget(sf_btn_computer)

        # Add Widgets To The "sf_option_container"
        sf_option_container.mdn_add_widget(sf_btn_player_rel_layout)
        sf_option_container.mdn_add_widget(sf_btn_computer_rel_layout)

        # Add Widgets To The Screen
        sf_container.mdn_add_widget(sf_label_rel_layout)
        sf_container.mdn_add_widget(sf_option_container_rel_layout)

        return sf_container_rel_layout

    # create_advanced_option method
    def create_advanced_option(self):
        """
            The purpose of this function is to create the advanced options
        """
        # Create the advanced options container
        advanced_options_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100un"])

        # Create the advanced options button
        advanced_btn_rel_layout = RelativeLayout()
        advanced_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Show Advanced Options",
            mdn_size = ["min_width", "100%"],
            mdn_font_size = self.theme["advanced_btn"]["font_size"],
            mdn_font_color = self.theme["advanced_btn"]["font_color"]
        )
        self.mdn_screen_ids["toggle_advanced_btn"] = advanced_btn
        advanced_btn.bind(on_press = self.show_advanced_options)
        advanced_btn.pos_hint = {"center_x": .5, "center_y": .5}
        advanced_btn_rel_layout.add_widget(advanced_btn)
        advanced_options_container.mdn_add_widget(advanced_btn_rel_layout) 

        return advanced_options_container    

    # create_play_mode_option method
    def create_play_mode_option(self):
        """
            The purpose of this function is to create the play mode options
        """
        # ========== Create Play Mode Option ========== #
        # The suffix will always be "pm" for "play mode"
        # Create the entire container for this option
        self.pm_container_rel_layout = RelativeLayout()
        pm_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        pm_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.pm_container_rel_layout.add_widget(pm_container)
        self.mdn_screen_ids["pm_container_rel_layout"] = self.pm_container_rel_layout

        # Create the label container and the label container
        pm_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        pm_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Play Mode:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        pm_label.pos_hint = {"center_x": .4}
        pm_label_rel_layout.add_widget(pm_label)

        # Create the option container
        pm_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        pm_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["400un", "100%"])
        pm_option_container.pos_hint = {"center_x": .5}
        pm_option_container_rel_layout.add_widget(pm_option_container)

        # Create the starts first button "Casual"
        pm_btn_casual_rel_layout = RelativeLayout()
        pm_btn_casual = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Casual",
            mdn_size = ["170un", "80un"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["pm_btn_casual"] = pm_btn_casual
        pm_btn_casual.bind(on_press = partial(self.change_play_mode, "casual"))
        pm_btn_casual.pos_hint = {"center_x": .5, "center_y": .5}
        pm_btn_casual_rel_layout.add_widget(pm_btn_casual)

        # Create the starts first button "Pro"
        pm_btn_pro_rel_layout = RelativeLayout()
        pm_btn_pro = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Pro",
            mdn_size = ["170un", "80un"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["pm_btn_pro"] = pm_btn_pro
        pm_btn_pro.bind(on_press = partial(self.change_play_mode, "pro"))
        pm_btn_pro.pos_hint = {"center_x": .5, "center_y": .5}
        pm_btn_pro_rel_layout.add_widget(pm_btn_pro)

        # Add Widgets To The "pm_option_container"
        pm_option_container.mdn_add_widget(pm_btn_casual_rel_layout)
        pm_option_container.mdn_add_widget(pm_btn_pro_rel_layout)

        # Add Widgets To The Screen
        pm_container.mdn_add_widget(pm_label_rel_layout)
        pm_container.mdn_add_widget(pm_option_container_rel_layout) 

        return self.pm_container_rel_layout 

    # create_board_size_option method
    def create_board_size_option(self):
        """
            The purpose of this function is to create the board size options
        """
        # ========== Create Board Size Option ========== #
        # The suffix will always be "bs" for "board size"
        # Create the entire container for this option
        self.bs_container_rel_layout = RelativeLayout()
        bs_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        bs_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.bs_container_rel_layout.add_widget(bs_container)
        self.mdn_screen_ids["bs_container_rel_layout"] = self.bs_container_rel_layout

        # Create the label container and the label container
        bs_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        bs_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Board Size:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        bs_label.pos_hint = {"center_x": .4}
        bs_label_rel_layout.add_widget(bs_label)

        # Create the option container
        bs_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        bs_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["400un", "100%"])
        bs_option_container.pos_hint = {"center_x": .5}
        bs_option_container_rel_layout.add_widget(bs_option_container)

        # Create the back btn container and the button
        bs_back_btn_rel_layout = RelativeLayout()
        bs_back_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["left"]["icon"],
            mdn_size = self.theme["arrow_btn"]["left"]["size"]
        )
        bs_back_btn.bind(on_press = partial(self.change_board_size, "back"))
        bs_back_btn.pos_hint = {"center_x": .5, "center_y": .5}
        bs_back_btn_rel_layout.add_widget(bs_back_btn)

        # Create the computer difficulty label
        bs_computer_difficulty_rel_layout = RelativeLayout()
        bs_board_size_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = str(self.board_size),
            mdn_font_size = self.theme["primary_font_size"],
            mdn_font_color = self.theme["primary_font_color"]
        )
        self.mdn_screen_ids["bs_board_size_label"] = bs_board_size_label
        bs_board_size_label.pos_hint = {"center_x": .5, "center_y": .5}
        bs_computer_difficulty_rel_layout.add_widget(bs_board_size_label)

        # Create the fwd btn container and the button
        bs_fwd_btn_rel_layout = RelativeLayout()
        bs_fwd_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["right"]["icon"],
            mdn_size = self.theme["arrow_btn"]["right"]["size"]
        )
        bs_fwd_btn.bind(on_press = partial(self.change_board_size, "fwd"))
        bs_fwd_btn.pos_hint = {"center_x": .5, "center_y": .5}
        bs_fwd_btn_rel_layout.add_widget(bs_fwd_btn)

        # Add Widgets To The "b_option_container"
        bs_option_container.mdn_add_widget(bs_back_btn_rel_layout)
        bs_option_container.mdn_add_widget(bs_computer_difficulty_rel_layout)
        bs_option_container.mdn_add_widget(bs_fwd_btn_rel_layout)

        # Add Widgets To The Screen
        bs_container.mdn_add_widget(bs_label_rel_layout)
        bs_container.mdn_add_widget(bs_option_container_rel_layout)  

        return self.bs_container_rel_layout

    # create_win_length_option method
    def create_win_length_option(self):
        """
            The purpose of this function is to create the win length options
        """
        # ========== Create Winning Length Option ========== #
        # The suffix will always be "wl" for "win length"
        # Create the entire container for this option
        self.wl_container_rel_layout = RelativeLayout()
        wl_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        wl_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.wl_container_rel_layout.add_widget(wl_container)
        self.mdn_screen_ids["wl_container_rel_layout"] = self.wl_container_rel_layout

        # Create the label container and the label container
        wl_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        wl_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Win Length:",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        wl_label.pos_hint = {"center_x": .4}
        wl_label_rel_layout.add_widget(wl_label)

        # Create the option container
        wl_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        wl_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["400un", "100%"])
        wl_option_container.pos_hint = {"center_x": .5}
        wl_option_container_rel_layout.add_widget(wl_option_container)

        # Create the back btn container and the button
        wl_back_btn_rel_layout = RelativeLayout()
        wl_back_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["left"]["icon"],
            mdn_size = self.theme["arrow_btn"]["left"]["size"]
        )
        wl_back_btn.bind(on_press = partial(self.change_win_length, "back"))
        wl_back_btn.pos_hint = {"center_x": .5, "center_y": .5}
        wl_back_btn_rel_layout.add_widget(wl_back_btn)

        # Create the computer difficulty label
        wl_computer_difficulty_rel_layout = RelativeLayout()
        wl_board_size_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = str(self.win_length),
            mdn_font_size = self.theme["primary_font_size"],
            mdn_font_color = self.theme["primary_font_color"]
        )
        self.mdn_screen_ids["wl_board_size_label"] = wl_board_size_label
        wl_board_size_label.pos_hint = {"center_x": .5, "center_y": .5}
        wl_computer_difficulty_rel_layout.add_widget(wl_board_size_label)

        # Create the fwd btn container and the button
        wl_fwd_btn_rel_layout = RelativeLayout()
        wl_fwd_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_icon = self.theme_dest+self.theme["arrow_btn"]["right"]["icon"],
            mdn_size = self.theme["arrow_btn"]["right"]["size"]
        )
        wl_fwd_btn.bind(on_press = partial(self.change_win_length, "fwd"))
        wl_fwd_btn.pos_hint = {"center_x": .5, "center_y": .5}
        wl_fwd_btn_rel_layout.add_widget(wl_fwd_btn)

        # Add Widgets To The "wl_option_container"
        wl_option_container.mdn_add_widget(wl_back_btn_rel_layout)
        wl_option_container.mdn_add_widget(wl_computer_difficulty_rel_layout)
        wl_option_container.mdn_add_widget(wl_fwd_btn_rel_layout)

        # Add Widgets To The Screen
        wl_container.mdn_add_widget(wl_label_rel_layout)
        wl_container.mdn_add_widget(wl_option_container_rel_layout)  

        return self.wl_container_rel_layout

    # create_move_timer_option method
    def create_move_timer_option(self):
        """
            The purpose of this function is to create the move timer options
        """
        # ========== Create Move Timer Option ========== #
        # The suffix will always be "mt" for "move timer"
        # Create the entire container for this option
        self.mt_container_rel_layout = RelativeLayout()
        mt_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        mt_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.mt_container_rel_layout.add_widget(mt_container)
        self.mdn_screen_ids["mt_container_rel_layout"] = self.mt_container_rel_layout

        # Create the label container and the label container
        mt_label_rel_layout = RelativeLayout(size_hint = (.3, 1))
        mt_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Move Timer (Sec):",
            mdn_size = ["90%", "100%"],
            mdn_font_size = self.theme["option_label"]["font_size"],
            mdn_font_style = self.theme["option_label"]["font_style"],
            mdn_font_color = self.theme["option_label"]["font_color"],
            mdn_text_align = self.theme["option_label"]["text_align"]
        )
        mt_label.pos_hint = {"center_x": .4}
        mt_label_rel_layout.add_widget(mt_label)

        # Create the option container
        mt_option_container_rel_layout = RelativeLayout(size_hint = (.7, 1))
        mt_option_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 5,mdn_size = ["450un", "100%"])
        mt_option_container.pos_hint = {"center_x": .55}
        mt_option_container_rel_layout.add_widget(mt_option_container)

        # Create the btn 5
        mt_btn_none_rel_layout = RelativeLayout()
        mt_btn_none = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_icon_size = self.theme["move_timer_btn"]["dark"]["icon_size"],
            mdn_icon = self.theme_dest+self.theme["move_timer_btn"]["dark"]["icon"],
        )
        mt_btn_none.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["mt_btn_none"] = mt_btn_none
        mt_btn_none.bind(on_press = partial(self.change_move_timer, "-10"))
        mt_btn_none_rel_layout.add_widget(mt_btn_none)

        # Create the btn 1
        mt_btn_1_rel_layout = RelativeLayout()
        mt_btn_1 = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_text = self.timers_for_moves[0],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_style = self.theme["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"],
        )
        mt_btn_1.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["mt_btn_1"] = mt_btn_1
        mt_btn_1.bind(on_press = partial(self.change_move_timer, "1"))
        mt_btn_1_rel_layout.add_widget(mt_btn_1)

        # Create the btn 2
        mt_btn_2_rel_layout = RelativeLayout()
        mt_btn_2 = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_text = self.timers_for_moves[1],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_style = self.theme["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"],
        )
        mt_btn_2.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["mt_btn_2"] = mt_btn_2
        mt_btn_2.bind(on_press = partial(self.change_move_timer, "2"))
        mt_btn_2_rel_layout.add_widget(mt_btn_2)

        # Create the btn 3
        mt_btn_3_rel_layout = RelativeLayout()
        mt_btn_3 = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_text = self.timers_for_moves[2],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_style = self.theme["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"],
        )
        mt_btn_3.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["mt_btn_3"] = mt_btn_3
        mt_btn_3.bind(on_press = partial(self.change_move_timer, "3"))
        mt_btn_3_rel_layout.add_widget(mt_btn_3)

        # Create the btn 4
        mt_btn_4_rel_layout = RelativeLayout()
        mt_btn_4 = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["70un", "70un"],
            mdn_text = self.timers_for_moves[3],
            mdn_bg = self.theme["btn"]["normal"]["bg"],
            mdn_radius = self.theme["btn"]["normal"]["radius"],
            mdn_outline = self.theme["btn"]["normal"]["outline"],
            mdn_font_style = self.theme["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["btn"]["normal"]["font_color"],
        )
        mt_btn_4.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["mt_btn_4"] = mt_btn_4
        mt_btn_4.bind(on_press = partial(self.change_move_timer, "4"))
        mt_btn_4_rel_layout.add_widget(mt_btn_4)

        mt_option_container.mdn_add_widget(mt_btn_none_rel_layout)
        mt_option_container.mdn_add_widget(mt_btn_1_rel_layout)
        mt_option_container.mdn_add_widget(mt_btn_2_rel_layout)
        mt_option_container.mdn_add_widget(mt_btn_3_rel_layout)
        mt_option_container.mdn_add_widget(mt_btn_4_rel_layout)
        mt_container.mdn_add_widget(mt_label_rel_layout)
        mt_container.mdn_add_widget(mt_option_container_rel_layout)

        return self.mt_container_rel_layout

    # show_advanced_options method
    def show_advanced_options(self, *args):
        """
            The purpose of this function is to display the advanced options
        """
        # If advanced options are open, then remove them
        if self.advanced_options_opened and not "default" in args:
            if len(self.mdn_screen_ids["more_options_container"].children) == 2:
                self.mdn_screen_ids["more_options_container"].children[0].clear_widgets()
            else: self.mdn_screen_ids["more_options_container"].clear_widgets()
            self.advanced_options_opened = False
            self.mdn_screen_ids["toggle_advanced_btn"].mdn_update({"mdn_text": "Show Advanced Options"})
            return

        if not self.advanced_options_opened: return

        # If advanced options are close, then display them
        self.advanced_options_opened = True
        self.mdn_screen_ids["toggle_advanced_btn"].mdn_update({"mdn_text": "Hide Advanced Options"})

        # If the 'bs_container_rel_layout' isn't set, then take this path
        if not self.bs_container_rel_layout:
            # Create the entire container for this option
            self.pm_container_rel_layout = self.create_play_mode_option()  

            # Create the entire container for this option
            self.bs_container_rel_layout = self.create_board_size_option()  

            # Create the entire container for this option
            self.wl_container_rel_layout = self.create_win_length_option()

            # Create the entire container for this option
            self.mt_container_rel_layout = self.create_move_timer_option()

        # Add Options To The More Options Container
        self.mdn_screen_ids["more_options_container"].mdn_add_widget(self.pm_container_rel_layout)
        self.mdn_screen_ids["more_options_container"].mdn_add_widget(self.bs_container_rel_layout)
        self.mdn_screen_ids["more_options_container"].mdn_add_widget(self.wl_container_rel_layout)
        self.mdn_screen_ids["more_options_container"].mdn_add_widget(self.mt_container_rel_layout)
        self.change_play_mode(self.play_mode, "default")
        # self.change_win_length(self.win_length, "default")
        self.change_move_timer(self.move_timer, "-10")


    # +----------------------------------------+
    # |                                        |
    # |        Update Graphic Functions        |
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

        if self.mdn_app.mdn_screenmanager.current_screen.name != "single_player_options_screen":
            Clock.schedule_once(self.update_ui, 1)
            return

        self.mdn_screen_ids["bg"]._mdn_update_graphic()

    # upate_scrollview method
    def update_scrollview_size(self, *args):
        """
            The purpose of this function is to update the scrollview's size
        """
        # Get the scrollview
        body_scrollview_container = self.mdn_screen_ids["body_scrollview_container"]

        # Update the size & pos of the 'body_scrollview_container'
        body_scrollview_container.size = body_scrollview_container.parent.size
        body_scrollview_container.pos = body_scrollview_container.parent.pos

        # Calculate the height for the 'body_scrollview_container'
        body_scrollview_inner_container_height = 0
        for child in self.mdn_screen_ids["body_scrollview_inner_container"].children:body_scrollview_inner_container_height+=child.height

        # Update size for 'self.mdn_screen_ids["body_scrollview_inner_container"]'
        self.mdn_screen_ids["body_scrollview_inner_container"].mdn_update({"mdn_size": ["100%", "{}un".format(int(body_scrollview_inner_container_height))]})


    # +----------------------------------------+
    # |                                        |
    # |         Button Event Functions         |
    # |                                        |
    # +----------------------------------------+
    # change_computer_difficulty method
    def change_computer_difficulty(self, *args):
        """
            The purpose of this function is to change the computer difficulty 
        """
        # Change the computer difficulty
        if args[0] == "back": current_difficulty = len(self.computer_levels)-1 if self.computer_difficulty == 0 else self.computer_difficulty-1
        else: current_difficulty = 0 if self.computer_difficulty == len(self.computer_levels)-1 else self.computer_difficulty+1
        self.computer_difficulty = current_difficulty
        self.mdn_screen_ids["d_computer_difficulty"].mdn_update({"mdn_text": self.computer_levels[current_difficulty]})

    # change_play_as_type method
    def change_play_as_type(self, *args):
        """
            The purpose of this function is to change the player type.
        """
        # Return the function if the the button pressed is already selected
        if self.play_as == args[0] and not "default" in args: return

        # Change the graphics of the current highlighted button to default graphics 
        self.mdn_screen_ids["pa_btn_{}".format(self.play_as)].mdn_update({
            "mdn_outline": self.theme["btn"]["normal"]["outline"],
            "mdn_bg": self.theme["btn"]["normal"]["bg"],
            "mdn_icon": self.theme_dest+self.theme["play_as_btn"][self.play_as]["dark"]["icon"],
            "mdn_icon_size": self.theme["play_as_btn"][self.play_as]["dark"]["icon_size"]
        })

        # Change the self.play_as variable
        self.play_as = args[0]

        # Change the self.computer_play_as variable
        self.computer_play_as = "x" if self.play_as == "o" else "o"

        # Change the graphics of the pressed button to the highlighted graphics 
        self.mdn_screen_ids["pa_btn_{}".format(self.play_as)].mdn_update({
            "mdn_outline": self.theme["btn"]["highlight"]["outline"],
            "mdn_bg": self.theme["btn"]["highlight"]["bg"],
            "mdn_icon": self.theme_dest+self.theme["play_as_btn"][self.play_as]["light"]["icon"],
            "mdn_icon_size": self.theme["play_as_btn"][self.play_as]["dark"]["icon_size"]
        })

    # change_starts_first method
    def change_starts_first(self, *args):
        """
            The purpose of this function is to change who starts first.
        """
        # Return the function if the the button pressed is already selected
        if self.starts_first == args[0] and not "default" in args: return

        # Change the graphics of the current highlighted button to default graphics 
        self.mdn_screen_ids["sf_btn_{}".format(self.starts_first)].mdn_update({
            "mdn_outline": self.theme["btn"]["normal"]["outline"],
            "mdn_bg": self.theme["btn"]["normal"]["bg"],
            "mdn_font_color": self.theme["btn"]["normal"]["font_color"]
        })

        # Change the self.play_as variable
        self.starts_first = args[0]

        # Change the graphics of the pressed button to the highlighted graphics 
        self.mdn_screen_ids["sf_btn_{}".format(self.starts_first)].mdn_update({
            "mdn_outline": self.theme["btn"]["highlight"]["outline"],
            "mdn_bg": self.theme["btn"]["highlight"]["bg"],
            "mdn_font_color": self.theme["btn"]["highlight"]["font_color"]
        })

    # change_play_mode method
    def change_play_mode(self, *args):
        """
            The purpose of this function is to change the play mode (casual / pro).
        """
        # Return the function if the the button pressed is already selected
        if self.play_mode == args[0] and not "default" in args: return

        # Change the graphics of the current highlighted button to default graphics 
        self.mdn_screen_ids["pm_btn_{}".format(self.play_mode)].mdn_update({
            "mdn_outline": self.theme["btn"]["normal"]["outline"],
            "mdn_bg": self.theme["btn"]["normal"]["bg"],
            "mdn_font_color": self.theme["btn"]["normal"]["font_color"]
        })

        # Change the self.play_as variable
        self.play_mode = args[0]

        # Change the graphics of the pressed button to the highlighted graphics 
        self.mdn_screen_ids["pm_btn_{}".format(self.play_mode)].mdn_update({
            "mdn_outline": self.theme["btn"]["highlight"]["outline"],
            "mdn_bg": self.theme["btn"]["highlight"]["bg"],
            "mdn_font_color": self.theme["btn"]["highlight"]["font_color"]
        })

    # change_board_size method
    def change_board_size(self, *args):
        """
            The purpose of this method is to change the size of the board
        """
        # Change the computer difficulty
        if args[0] == "back": 
            board_size = 8 if self.board_size == (3 if 3 >= self.win_length else self.win_length) else self.board_size-1
        else: 
            board_size = (3 if 3 >= self.win_length else self.win_length) if self.board_size == 8 else self.board_size+1
        self.board_size = board_size
        self.mdn_screen_ids["bs_board_size_label"].mdn_update({"mdn_text": str(self.board_size)})

    # change_win_length method
    def change_win_length(self, *args):
        """
            The purpose of this method is to change the win length for the game
        """
        # Change the win length
        if args[0] == "back": 
            peek_number = self.board_size if self.board_size < 5 else 5
            win_length = peek_number if self.win_length == 3 else self.win_length-1
        else: win_length = 3 if self.win_length == 5 or self.win_length == self.board_size else self.win_length+1
        self.win_length = win_length
        self.mdn_screen_ids["wl_board_size_label"].mdn_update({"mdn_text": str(self.win_length)})

    # change_move_timer method
    def change_move_timer(self, *args):
        """
            The purpose of this function is to change the move timer variable
        """
        # Return the function if the the button pressed is already selected
        if self.move_timer == args[0] and not "-10" in args: return

        # Store the current button in a variable
        mt_current_btn = self.mdn_screen_ids["mt_btn_{}".format(self.move_timer if self.move_timer != "-10" else "none")]

        # Change the graphics of the current highlighted button to default graphics
        mt_current_btn.mdn_update({
            "mdn_outline": self.theme["btn"]["normal"]["outline"],
            "mdn_bg": self.theme["btn"]["normal"]["bg"],
        })

        # If it's a button with an icon, then change the icon, If it's a button with text, then change the font color
        if self.move_timer == "-10": mt_current_btn.mdn_update({"mdn_icon": self.theme_dest+self.theme["move_timer_btn"]["dark"]["icon"]})
        else: mt_current_btn.mdn_update({"mdn_font_color": self.theme["btn"]["normal"]["font_color"]})

        # Change the self.game_timer variable
        self.move_timer = args[0]
        mt_current_btn = self.mdn_screen_ids["mt_btn_{}".format(self.move_timer if self.move_timer != "-10" else "none")]

        # Change the border and outline of the pressed button to the highlighted graphics
        mt_current_btn.mdn_update({
            "mdn_outline": self.theme["btn"]["highlight"]["outline"],
            "mdn_bg": self.theme["btn"]["highlight"]["bg"],
        })

        # If it's a button with an icon, then change the icon, If it's a button with text, then change the font color
        if self.move_timer == "-10": mt_current_btn.mdn_update({"mdn_icon": self.theme_dest+self.theme["move_timer_btn"]["light"]["icon"]})
        else: mt_current_btn.mdn_update({"mdn_font_color": self.theme["btn"]["highlight"]["font_color"]})

    # change_screen method
    def change_screen(self, *args):
        """
            The purpose of this function is to change screens
        """
        if args[0] == "back": self.mdn_switch("home_screen", "Welcome To TicTacToe", "right")
        else: self.mdn_switch("single_player_game_screen", "Single Player")


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
