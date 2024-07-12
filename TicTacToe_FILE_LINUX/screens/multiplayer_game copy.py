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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_input import MDN_Input
from dep.modern_label import MDN_Label
from dep.modern_button import MDN_Button
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout
from classes.computer_ai import Computer_AI
from classes.timer_module import Timer_Module
from classes.win_line_anim_module import Win_Line_Anim_Module
from kivy.graphics import Rectangle, Color, Line, BoxShadow

# ===== Multiplayer_Game_Screen Class ===== #
class Multiplayer_Game_Screen_Class(MDN_Screen):
    # +----------------------------------------+
    # |                                        |
    # |               Init Class               |
    # |                                        |
    # +----------------------------------------+
    # init function
    def __init__(self, **kwargs):
        self.load_theme(kwargs)
        super().__init__(**kwargs)
        # This variable will record the total amount of moves in the game
        self.total_game_moves = 0

        # This variable will record the selected computer difficulty
        self.selected_computer_difficulty = None

        # This variable will record all the options for computer levels 
        self.computer_levels = None

        # This variable will record what icon the player will be playing as. This icon goes on the board
        self.player_play_as = None

        # This variable will record what icon the computer will be playing as. This icon goes on the board
        self.computer_play_as = None

        # This variable will determine who starts first. The player or the computer (eg. 'C' or 'P')
        self.starts_first = None

        # This variable will determine the size of the board. (eg. 5x5, 8x8, 3x3)
        self.board_size = None

        # This variable will determine how many symbols in a row it takes for the player to win (eg. 4 in a row, 5 in a row)
        self.win_length = None

        self.play_mode = None

        # This variable will record the selected timer for each move for the player
        self.selected_move_timer = None

        # This variable will record all the options for move timers
        self.timers_for_moves = None

        # This will determine if the game is over or not. Game can ended as a "draw", "win", or "loss"
        self.game_over = False

        # This variable will record when the player's turn started and will hold that time
        self.player_turn_time_start = None

        # This variable will record the total amount of time for the player to move
        self.player_total_time = {
            "p1": 0,
            "p2": 0
        }

        # This will record how many moves it took for the player to move and the times for each. Each time represents a move, because every time displays how long it took for the player to move. So the more times there are in this variable, that the player moved a lot
        self.player_avg_move_time = {
            "p1": [],
            "p2": []
        }

        # This will initialize the 'Computer_AI' class for the game
        self.computer_ai = Computer_AI()

        # This is the board. This will be divided into columns and row of the board size. It will be an array
        # Copied by numpy it would look like this...
        # +-----------+
        # | X | O | O |
        # | O | X | O |
        # | X | X | X |
        # +-----------+
        # Default would look like this...
        # [
        #   ["X", "O", "O"]
        #   ["O", "X", "O"]
        #   ["X", "X", "X"]
        # ]
        self.board_positions = []

        # This variable will record how many cells are still left on the board
        self.board_available_cell_positions = []

        # This variable will determine if the board is visible or hidden
        self.board_visible = True

        # This variable will record the player's last move
        self.player_last_move = None
        
        # This variable is responsible for holding all the delay times before the computer makes a move
        self.computer_move_delays = []

        # This variable will record who's turn it currently is
        self.current_turn = "P"

        # This variable will determine if the game is paused or not
        self.game_paused = False

        # This variable will determine what is the maximum ideal time for a player to move, before the points are greatly reduced
        self.stopwatch_ideal_move_time = 5

        # This will record the winning player
        self.winning_player = None

        # This will record and hold the score of both players: computer and the player
        self.score_player = {"C": 0, "P": 0}

        # This will record and hold the score of both players: computer and the player
        self.game_moves = []

        # This will display that the overlay is closed
        self.overlay_open = False

        # This will hold all the data about the player
        self.player_info = {
            "profile_nickname": "Silas",
            "profile_pic": None
        }

        # This will record and hold the score of both players: computer and the player
        self.score_data = {
            "easy": {
                "move_point": 10,
                "win": {"c_first": 5, "p_first": 2},
                "draw": {"c_first": 2, "p_first": -5},
                "loss": {"c_first": -10, "p_first": -20},
            },
            "normal": {
                "move_point": 15, 
                "win": {"c_first": 15, "p_first": 5},
                "draw": {"c_first": 5, "p_first": 0},
                "loss": {"c_first": 0, "p_first": -10},
            }, 
            "hard": {
                "move_point": 20,
                "win": {"c_first": 30, "p_first": 10},
                "draw": {"c_first": 10, "p_first": 5},
                "loss": {"c_first": 0, "p_first": -10},
            },
            "casual": 1,
            "pro": 1.5
        }


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
            Clock.schedule_once(self.init_ui, .05)
            return
            
        # If the current screen isn't this screen, then exit this function and call it again in .05s 
        if self.mdn_app.mdn_screenmanager.current_screen.name != "multiplayer_game_screen":
            Clock.schedule_once(self.init_ui, .05)
            return

        # Reset all variables
        self.reset_screen_variables()

        # Create the background
        bg = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_bg = {"image":[self.theme_dest+self.theme["bg"],"stretch"]}
        )
        self.clear_widgets()
        self.mdn_screen_ids["bg"] = bg
        self.add_widget(bg)

        # Create UI Screen 
        self.create_header_ui()
        self.create_body_ui()
        self.create_footer_ui()
        self.create_overlay_ui()

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
            mdn_cols = 3, 
            mdn_size = {"desktop": ["725un", "100un"], "tablet": ["725un", "100un"], "mobile": ["675un", "100un"]}, 
        )
        header_inner_container.pos_hint = {"center_x": .5, "center_y": .5}
        header_inner_rel_container.add_widget(header_inner_container)

        # Create the tic_tac_toe logo & container
        bck_btn_rel_container = RelativeLayout(size_hint = (.2, 1))
        bck_btn = MDN_Button(mdn_app = self.mdn_app, mdn_icon = self.theme_dest+self.theme["header_bck_btn"], mdn_size = ["100un", "25un"], mdn_change_cursor = False)
        bck_btn.bind(on_press = self.exit_game)
        bck_btn.pos_hint = {"center_x": 1, "center_y": .55}
        bck_btn_rel_container.add_widget(bck_btn)

        # Create the header label & container
        header_label_rel_container = RelativeLayout()
        header_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Multiplayer Player",
            mdn_size = ["100%", "70%"],
            mdn_font_size = self.theme["header_settings_label"]["font_size"],
            mdn_font_style = self.theme["header_settings_label"]["font_style"],
            mdn_font_color = self.theme["header_settings_label"]["font_color"]
        )
        header_label.pos_hint = {"center_x": .5, "center_y": .55}
        header_label_rel_container.add_widget(header_label)

        # Create the settings icon & container
        tic_tac_toe_logo_rel_container = RelativeLayout(size_hint = (.2, 1))
        tic_tac_toe_logo = MDN_Button(mdn_app = self.mdn_app, mdn_icon = self.theme_dest+self.theme["tictactoe_logo"], mdn_size = ["60un", "60un"], mdn_change_cursor = False)
        tic_tac_toe_logo.pos_hint = {"center_x": 0, "center_y": .55}
        tic_tac_toe_logo_rel_container.add_widget(tic_tac_toe_logo)
        
        # Combine widgets
        header_inner_container.mdn_add_widget(bck_btn_rel_container)
        header_inner_container.mdn_add_widget(header_label_rel_container)
        header_inner_container.mdn_add_widget(tic_tac_toe_logo_rel_container)
        header_container.mdn_add_widget(header_inner_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(header_container)

    # create_body_ui method
    def create_body_ui(self):
        """
            The purpose of this function is to create the body ui.
        """
        # Create the body & container
        body_container_rel_layout = RelativeLayout()
        body_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]}
        )
        body_container_rel_layout.add_widget(body_container)
        body_container.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["body_container"] = body_container

        # Create the body container padding
        body_container_top_pading = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["80%", "50un"])

        # Create the container that will hold all the stats and timers
        stat_and_timer_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "500un"])
        stat_and_timer_container.pos_hint = {"center_x": .5, "center_y": .5}

        # Create Character Profile Container
        character_profile_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["100%", "50%"])
        # Create the player_profile_container
        player_profile_container = self.create_player_profile("Player 1", self.theme_dest+self.theme["profile"]["default_profile"], self.theme_dest+self.theme["profile"]["default_char_{}".format(self.player_play_as)], .38)
        # Create the dividing line
        profile_dividing_line_rel_container = RelativeLayout(size_hint = (None, 1), width = 10)
        profile_dividing_line = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_bg = {"color": [0, 0, 0, 1]}, mdn_size = ["10un", "80%"])
        profile_dividing_line.pos_hint = {"center_x": .5, "center_y": .5}
        profile_dividing_line_rel_container.add_widget(profile_dividing_line)
        # Create the computer_profile_container
        computer_profile_container = self.create_player_profile("Player 2", self.theme_dest+self.theme["profile"]["default_profile"], self.theme_dest+self.theme["profile"]["default_char_{}".format(self.computer_play_as)], .62)    
        # Combine Widgets
        character_profile_container.mdn_add_widget(player_profile_container)    
        character_profile_container.mdn_add_widget(profile_dividing_line_rel_container)    
        character_profile_container.mdn_add_widget(computer_profile_container)    

        # Create Timer & Stat Container
        timer_and_stat_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3, mdn_size = ["100%", "50%"])
        # Create the score and container for the player
        player_score_container = self.create_player_score(.6, "P")
        # Create the container for the timer
        timer_rel_container = MDN_RelativeLayout(mdn_size = ("40%", "100%"))
        timer_container = Timer_Module(mdn_app = self.mdn_app, mdn_cols = 1, mdn_outline = [[255, 255, 255, 1], 5], mdn_size = ["190un", "190un"])
        self.mdn_screen_ids["timer_container"] = timer_container
        timer_container.pos_hint = {"center_x": .5, "center_y": .6}
        # Create the label (side note) for the timer
        timer_label_rel_container = RelativeLayout()
        self.mdn_screen_ids["timer_label_rel_container"] = timer_label_rel_container
        timer_label = MDN_Label(mdn_app = self.mdn_app, mdn_text = "Hurry Up!", mdn_font_color = [255, 0, 0, 1], mdn_font_style = ["bold"], mdn_font_size = 28)
        self.mdn_screen_ids["timer_label"] = timer_label
        timer_label.pos_hint = {"center_x": .5, "center_y": .3}
        timer_label_rel_container.add_widget(timer_label)
        # Create the clock label for the timer
        timer_clock_label_rel_container = RelativeLayout()
        timer_clock_label = MDN_Label(
            mdn_app = self.mdn_app, 
            mdn_text = str(self.timers_for_moves[int(self.selected_move_timer)-1])if self.selected_move_timer != "-10" and int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3 else "00:00", 
            mdn_font_color = [255, 0, 0, 1] if self.selected_move_timer != "-10" and int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3 else [255, 255, 255, 1], 
            mdn_font_size = 35 if self.selected_move_timer != "-10" and int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3 else 50
        )
        if self.selected_move_timer == "-10": timer_clock_label.mdn_update({"mdn_font_size": 40})
        self.mdn_screen_ids["timer_clock_label_rel_container"] = timer_clock_label_rel_container
        self.mdn_screen_ids["timer_clock_label"] = timer_clock_label
        timer_clock_label.pos_hint = {"center_x": .5, "center_y": .7 if self.selected_move_timer != "-10" and int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3 else .5}
        timer_clock_label_rel_container.add_widget(timer_clock_label)
        # Combine timer widgets together and add them to screen
        if self.selected_move_timer != "-10" and int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3: timer_container.mdn_add_widget(timer_label_rel_container)
        timer_container.mdn_add_widget(timer_clock_label_rel_container)
        timer_rel_container.add_widget(timer_container)       
        # Create the score and container for the player
        computer_score_container = self.create_player_score(.4, "C")
        # Add widgets to the timer_options_container
        timer_and_stat_container.mdn_add_widget(player_score_container)
        timer_and_stat_container.mdn_add_widget(timer_rel_container)
        timer_and_stat_container.mdn_add_widget(computer_score_container)
        # timer_options_rel_container.add_widget(timer_options_container)

        # Create the container for the board
        board_rel_container = RelativeLayout(size_hint = (1, .6))
        board_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = self.board_size,
            mdn_bg = {"image": [self.theme_dest+self.theme["boards"]["board_{}".format(self.board_size)], "fit"]},
            mdn_size = {"desktop": ["650un", "650un"], "tablet": ["650un", "650un"], "mobile": ["550un", "550un"]})
        self.mdn_screen_ids["board_container"] = board_container
        board_container.pos_hint = {"center_x": .5, "center_y": .5}
        board_rel_container.add_widget(board_container)

        # Combine Widgets
        stat_and_timer_container.mdn_add_widget(character_profile_container)
        stat_and_timer_container.mdn_add_widget(timer_and_stat_container)
        body_container.mdn_add_widget(body_container_top_pading)
        body_container.mdn_add_widget(stat_and_timer_container)
        body_container.mdn_add_widget(board_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(body_container_rel_layout)

    # create_footer_ui method
    def create_footer_ui(self):
        """
            The purpose of this function is to create the footer ui. Which will only be a gap between the end of the screen and the board
        """
        # Create the footer & container
        footer_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "100un"]) 
        self.mdn_screen_ids["bg"].mdn_add_widget(footer_container) 

    # create_overlay_ui method
    def create_overlay_ui(self):
        """
            The purpose of this function is to create the overlay ui. This will display the countdown overlay and the game over overlay
        """
        # Create the overlay relative containers
        overlay_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "1un"])
        overlay_rel_container_2 = MDN_RelativeLayout(mdn_size = ["100%", "1un"])
        self.mdn_screen_ids["overlay_rel_container"] = overlay_rel_container
        self.mdn_screen_ids["overlay_rel_container_2"] = overlay_rel_container_2

        # Create the first overlay
        overlay_container = FloatLayout()
        overlay_container.size_hint = (None, None)
        self.mdn_screen_ids["overlay_container"] = overlay_container
        overlay_container.pos_hint = {"center_x": .5, "center_y": .5}
        overlay_container.bind(pos = self.update_overlay, size = self.update_overlay)
        self.mdn_screen_ids["bg"].bind(pos = self.update_overlay, size = self.update_overlay)
        
        # Create the countdown label and it's container
        countdown_label_rel_container = RelativeLayout()
        countdown_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "3",
            mdn_font_size = self.theme["countdown"]["font_size"],
            mdn_font_color = self.theme["countdown"]["font_color"],
            mdn_font_style = self.theme["countdown"]["font_style"]
        )
        self.mdn_screen_ids["countdown_label"] = countdown_label
        countdown_label.pos_hint = {"center_x": .5, "center_y": .5}
        countdown_label_rel_container.add_widget(countdown_label)

        # Combine Widgets Together
        overlay_container.add_widget(countdown_label_rel_container)
        overlay_rel_container.add_widget(overlay_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(overlay_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(overlay_rel_container_2)

    # create_player_profile method
    def create_player_profile(self, profile_nickname, profile_pic, character_profile_pic, profile_pos = .5):
        """
            The purpose of this function is create the profile for the user or the computer. This function will create the ui.
        """
        # Create the player profile container
        player_profile_rel_container = RelativeLayout(size_hint = (1, 1))
        player_profile_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100%", "100%"]
        )
        player_profile_container.pos_hint = {"center_x": .5, "center_y": .5}
        player_profile_rel_container.add_widget(player_profile_container)
        # Create the player profile nickname
        player_nickname_rel_container = RelativeLayout(size_hint = (1, None), height = 50)
        player_nickname = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = profile_nickname,
            mdn_size = ["100%", "50un"],
            mdn_font_style = self.theme["profile"]["font_style"], 
            mdn_font_color = self.theme["profile"]["font_color"]
        )
        player_nickname.pos_hint = {"center_x": profile_pos, "center_y": .5}
        player_nickname_rel_container.add_widget(player_nickname)
        player_profile_container.mdn_add_widget(player_nickname_rel_container)
        # Create the player profile picture
        player_profile_pic_rel = RelativeLayout()
        player_profile_pic = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_bg = {"image": [profile_pic, "fit"]},
            mdn_cols = 1,
            mdn_size = self.theme["profile"]["size"],
            mdn_outline = self.theme["profile"]["outline"],
            mdn_radius = self.theme["profile"]["radius"]
        )
        player_profile_pic.pos_hint = {"center_x": profile_pos, "center_y": .5}
        player_profile_pic_rel.add_widget(player_profile_pic)
        player_profile_container.mdn_add_widget(player_profile_pic_rel)
        # Create the player profile character picture
        player_profile_character_pic_rel = MDN_RelativeLayout(mdn_size = ["100%", "10un"])
        player_profile_character_pic = AsyncImage(source = character_profile_pic, size_hint = (None, None), size = [50, 50])
        player_profile_character_pic.pos_hint = {"center_x": profile_pos, "center_y": 1}
        player_profile_character_pic_rel.add_widget(player_profile_character_pic)
        player_profile_container.mdn_add_widget(player_profile_character_pic_rel)
        # Return the profile pic container
        return player_profile_rel_container

    # create_player_score method
    def create_player_score(self, pos, player):
        """
            The purpose of this function is create the score and container for the user or the computer. This function will create the ui.
        """
        # Create the player score container
        player_score_rel_containter = MDN_RelativeLayout(mdn_size = ("30%", "100%"))
        player_score_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100%"])
        player_score_container.pos_hint = {"center_x": .5, "center_y": .45}
        # Create the player "score" label. This will hold the literal "score"
        player_score_label_rel_container = RelativeLayout()
        player_score_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "SCORE",
            mdn_font_style = self.theme["stats"]["score_literal_label"]["font_style"],
            mdn_font_color = self.theme["stats"]["score_literal_label"]["font_color"],
            mdn_font_size = self.theme["stats"]["score_literal_label"]["font_size"]
        )
        player_score_label.pos_hint = {"center_x": pos, "center_y": .5}
        player_score_label_rel_container.add_widget(player_score_label)
        # Create the player score label. This will hold the current score
        player_actual_score_label_rel_container = RelativeLayout()
        player_actual_score_label = MDN_Label(
            mdn_app = self.mdn_app, 
            mdn_text = str(self.score_player[player]), 
            mdn_font_style = self.theme["stats"]["score_label"]["font_style"],
            mdn_font_color = self.theme["stats"]["score_label"]["font_color"],
            mdn_font_size = self.theme["stats"]["score_label"]["font_size"]
        )
        player_actual_score_label.pos_hint = {"center_x": pos, "center_y": 1}
        player_actual_score_label_rel_container.add_widget(player_actual_score_label)
        self.mdn_screen_ids["player_actual_score_label_{}".format(player)] = player_actual_score_label
        # Add widgets
        player_score_container.mdn_add_widget(player_score_label_rel_container)
        player_score_container.mdn_add_widget(player_actual_score_label_rel_container)
        player_score_rel_containter.add_widget(player_score_container)
        # Return
        return player_score_rel_containter

    # create_cell_spaces method
    def create_cell_spaces(self):
        """
            The purpose of this function is to literally create all the boxes for tic tac toe board. The max amount of boxes it will create is 64 boxes.
        """
        for i in range(self.board_size*self.board_size):
            box_id = "box_{}".format(i)
            box_rel_container = RelativeLayout()
            box = MDN_Button(mdn_app = self.mdn_app, mdn_change_cursor = False, mdn_id = box_id)
            box.play_type = None
            box.bind(on_press = partial(self.player_pressed_box))
            box_rel_container.add_widget(box)
            self.mdn_screen_ids[box_id] = box
            self.mdn_screen_ids["board_container"].mdn_add_widget(box_rel_container)

    # create_final_results method
    def create_final_results(self, *args):
        """
            The purpose of this function is to display the final results
        """
        # Get the winning state of the player, not the computer. If the computer is the winner, then the player state will be set to loss
        if self.winning_player == None: player_win_state = "draw"
        else: player_win_state = "win" if self.winning_player == "P" else "loss"

        if "final_result_content_container" in self.mdn_screen_ids and self.overlay_open:
            self.mdn_screen_ids["final_result_content_wrapper_container"].clear_widgets()
            self.mdn_screen_ids["final_result_content_wrapper_container"].mdn_add_widget(self.mdn_screen_ids["final_result_content_container"])
            return

        # Open the overlay
        self.overlay_open = True

        # Get the second relative layout for overlays. 
        # Note: The first overlay container is being used to draw the line
        overlay_rel_container_2 = self.mdn_screen_ids["overlay_rel_container_2"]

        # +---------- Final Results Overlay ----------+
        # This is going to create the overlay for the final results
        final_result_overlay = FloatLayout()
        final_result_overlay.size_hint = (None, None)
        final_result_overlay.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["final_result_overlay"] = final_result_overlay
        final_result_overlay.bind(pos = self.update_final_results_overlay, size = self.update_final_results_overlay)

        # +---------- Final Results Container ----------+
        # Create the final_results container that will hold all the widgets
        final_result_rel_container = RelativeLayout()
        final_result_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_bg = {"image": [self.theme_dest+self.theme["final_results"]["bg"], "stretch"]},
            mdn_size = ["550un", "60%"],
            mdn_radius = self.theme["final_results"]["radius"],
            mdn_outline = self.theme["final_results"]["outline"]
        )
        self.mdn_screen_ids["final_result_container"] = final_result_container
        final_result_container.pos_hint = {"center_x": .5, "center_y": .5}
        final_result_container.bind(pos = self.update_final_results_container, size = self.update_final_results_container)

        # +---------- Final Results Wrapper Container ----------+
        # Create the final_results container that will hold all the widgets
        final_result_content_wrapper_rel_container = RelativeLayout()
        final_result_content_wrapper_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        self.mdn_screen_ids["final_result_content_wrapper_container"] = final_result_content_wrapper_container
        final_result_content_wrapper_container.pos_hint = {"center_x": .5, "center_y": .5}

        # +---------- Final Results Container ----------+
        # Create the final_results container that will hold all the widgets
        final_result_content_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        self.mdn_screen_ids["final_result_content_container"] = final_result_content_container
        final_result_content_container.pos_hint = {"center_x": .5, "center_y": .5}        

        # +---------- Final Results Header ----------+
        # Create the final results header
        final_result_header_img_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "130un"])
        final_result_header_img = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["80%", "100%"],
            mdn_bg = {"image": [self.theme_dest+self.theme["final_results"]["header"], "fit"]}
        )
        self.mdn_screen_ids["final_result_header_img_rel_container"] = final_result_header_img_rel_container
        final_result_header_img.pos_hint = {"center_x": .5, "center_y": .4}
        final_result_header_img_rel_container.add_widget(final_result_header_img)

        # +---------- Final Results Message ----------+
        # Create the message container
        final_result_message_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "100un"])
        final_result_message_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["80%", "100%"])
        final_result_message_container.pos_hint = {"center_x": .5}
        self.mdn_screen_ids["final_result_message_container"] = final_result_message_container
        # Create the actual message
        final_result_message_label_rel_container = RelativeLayout()
        final_result_message = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Player 1 Wins!" if self.winning_player == "P" else "Player 2 Wins!",
            mdn_font_size = self.theme["final_results"]["win_message"]["font_size"],
            mdn_font_color = self.theme["final_results"]["win_message"]["font_color"][self.winning_player],
            mdn_font_style = self.theme["final_results"]["win_message"]["font_style"]
        )
        self.mdn_screen_ids["final_result_message"] = final_result_message
        final_result_message_label_rel_container.add_widget(final_result_message)
        # Create the shadow message
        final_result_shadow_message_label_rel_container = RelativeLayout()
        final_result_shadow_message = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = final_result_message.mdn_text,
            mdn_font_size = self.theme["final_results"]["win_message"]["font_size"],
            mdn_font_color = self.theme["final_results"]["win_message"]["shadow"],
            mdn_font_style = self.theme["final_results"]["win_message"]["font_style"]
        )
        self.mdn_screen_ids["final_result_shadow_message"] = final_result_shadow_message
        final_result_shadow_message_label_rel_container.add_widget(final_result_shadow_message)
        final_result_shadow_message.bind(pos = self.update_final_result_shadow_message, size = self.update_final_result_shadow_message)
        # Combine all the widgets together
        final_result_message_container.mdn_add_widget(final_result_shadow_message_label_rel_container)
        final_result_message_container.mdn_add_widget(final_result_message_label_rel_container)
        final_result_message_rel_container.add_widget(final_result_message_container)

        # +---------- Final Results Advanced Options & Buttons ----------+
        # Create the advanced options and buttons
        final_result_button_rel_container = RelativeLayout()
        final_result_button_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["80%", "100%"])
        final_result_button_container.pos_hint = {"center_x": .5, "center_y": .5}
        # Create the play button and container
        fin_res_play_btn_rel_container = RelativeLayout()
        fin_res_play_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Play Again",
            mdn_font_color = self.theme["final_results"]["btn"]["font_color"],
            mdn_font_style = self.theme["final_results"]["btn"]["font_style"],
            mdn_font_size = self.theme["final_results"]["btn"]["font_size"],
            mdn_size = self.theme["final_results"]["btn"]["size"],
            mdn_bg = self.theme["final_results"]["btn"]["bg"],
            mdn_radius = self.theme["final_results"]["btn"]["radius"],
            mdn_shadow = self.theme["final_results"]["btn"]["shadow"]
        )
        fin_res_play_btn.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_play_btn.bind(on_press = self.play_again)
        fin_res_play_btn_rel_container.add_widget(fin_res_play_btn)
        # Create the main menu button and container
        fin_res_main_menu_btn_rel_container = RelativeLayout()
        fin_res_main_menu_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Main Menu",
            mdn_font_color = self.theme["final_results"]["btn"]["font_color"],
            mdn_font_style = self.theme["final_results"]["btn"]["font_style"],
            mdn_font_size = self.theme["final_results"]["btn"]["font_size"],
            mdn_size = self.theme["final_results"]["btn"]["size"],
            mdn_bg = self.theme["final_results"]["btn"]["bg"],
            mdn_radius = self.theme["final_results"]["btn"]["radius"],
            mdn_shadow = self.theme["final_results"]["btn"]["shadow"]
        )
        fin_res_main_menu_btn.bind(on_release = self.go_to_main_menu)
        fin_res_main_menu_btn.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_main_menu_btn_rel_container.add_widget(fin_res_main_menu_btn)
        # Create the view board button and container
        fin_res_view_board_btn_rel_container = RelativeLayout()
        fin_res_view_board_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "View Board",
            mdn_font_color = self.theme["final_results"]["btn"]["font_color"],
            mdn_font_style = self.theme["final_results"]["btn"]["font_style"],
            mdn_font_size = self.theme["final_results"]["btn"]["font_size"],
            mdn_size = self.theme["final_results"]["btn"]["size"],
            mdn_bg = self.theme["final_results"]["btn"]["bg"],
            mdn_radius = self.theme["final_results"]["btn"]["radius"],
            mdn_shadow = self.theme["final_results"]["btn"]["shadow"]
        )
        fin_res_view_board_btn.bind(on_release = partial(self.view_board, "view_board_btn"))
        fin_res_view_board_btn.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_view_board_btn_rel_container.add_widget(fin_res_view_board_btn)
        # Create the save game button and container
        fin_res_save_game_btn_rel_container = RelativeLayout()
        fin_res_save_game_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Save Game",
            mdn_font_color = self.theme["final_results"]["btn"]["font_color"],
            mdn_font_style = self.theme["final_results"]["btn"]["font_style"],
            mdn_font_size = self.theme["final_results"]["btn"]["font_size"],
            mdn_size = self.theme["final_results"]["btn"]["size"],
            mdn_bg = self.theme["final_results"]["btn"]["bg"],
            mdn_radius = self.theme["final_results"]["btn"]["radius"],
            mdn_shadow = self.theme["final_results"]["btn"]["shadow"]
        )
        fin_res_save_game_btn.bind(on_release = self.create_save_game)
        fin_res_save_game_btn.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_save_game_btn_rel_container.add_widget(fin_res_save_game_btn)
        # Add buttons to the 'final_result_button_container' variable
        final_result_button_container.mdn_add_widget(fin_res_play_btn_rel_container)
        final_result_button_container.mdn_add_widget(fin_res_main_menu_btn_rel_container)
        final_result_button_container.mdn_add_widget(fin_res_view_board_btn_rel_container)
        # final_result_button_container.mdn_add_widget(fin_res_save_game_btn_rel_container)
        final_result_button_rel_container.add_widget(final_result_button_container)

        # +---------- Final Results Stats (Part 1) ----------+
        # Create the results and stats container
        final_result_stats_and_results_rel_container = RelativeLayout()
        final_result_stats_and_results_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["80%", "100%"], mdn_cols = 1)
        final_result_stats_and_results_container.pos_hint = {"center_x": .5, "center_y": .5}
        final_result_stats_and_results_rel_container.add_widget(final_result_stats_and_results_container)
        # Create the "Result Divider" container
        fin_res_result_divider_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 3,
            mdn_size = ["100%", "40un"]
        )
        # Create the "Left Side Divider" that is part of the "Result Divider"
        left_side_line_divider_rel_container = RelativeLayout()
        left_side_line_divider = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "{}un".format(self.theme["final_results"]["dividing_lines"]["thickness"])], mdn_bg = self.theme["final_results"]["dividing_lines"]["bg"])
        left_side_line_divider.pos_hint = {"center_x": .5, "center_y": .5}
        left_side_line_divider_rel_container.add_widget(left_side_line_divider)
        # Create the "Right Side Divider" that is part of the "Result Divider"
        right_side_line_divider_rel_container = RelativeLayout()
        right_side_line_divider = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "{}un".format(self.theme["final_results"]["dividing_lines"]["thickness"])], mdn_bg = self.theme["final_results"]["dividing_lines"]["bg"])
        right_side_line_divider.pos_hint = {"center_x": .5, "center_y": .5}
        right_side_line_divider_rel_container.add_widget(right_side_line_divider)
        # Create the Label for the "Result Divider"
        result_divider_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_size = ["30%", "100%"],
            mdn_text = "Results",
            mdn_font_style = self.theme["final_results"]["results_literal"]["font_style"],
            mdn_font_size = self.theme["final_results"]["results_literal"]["font_size"],
            mdn_font_color = self.theme["final_results"]["results_literal"]["font_color"]
        )
        # Combine all the widgets
        fin_res_result_divider_container.mdn_add_widget(left_side_line_divider_rel_container)
        fin_res_result_divider_container.mdn_add_widget(result_divider_label)
        fin_res_result_divider_container.mdn_add_widget(right_side_line_divider_rel_container)
        final_result_stats_and_results_container.mdn_add_widget(fin_res_result_divider_container)
        # +---------- Final Results Stats (Part 2) ----------+
        # Create the stats container. This container will hold the score and total time
        final_result_stats_and_results_rel_container_part_2_1 = RelativeLayout()
        final_result_stats_and_results_container_part_2_1 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "100%"], mdn_cols = 2)
        final_result_stats_and_results_container_part_2_1.pos_hint = {"center_x": .5, "center_y": .5}
        final_result_stats_and_results_rel_container_part_2_1.add_widget(final_result_stats_and_results_container_part_2_1)
        # Create the score label
        current_score = self.score_player["P"]
        additional_pt = self.score_data[self.computer_levels[self.selected_computer_difficulty].lower()][player_win_state]["{}_first".format(self.starts_first[0].lower())]
        current_score+=additional_pt
        self.score_player["P"] = current_score

        fin_res_score_label_rel_container = RelativeLayout(size_hint = (.4, 1))
        fin_res_score_label = MDN_Label(mdn_app = self.mdn_app, mdn_text = "Score: {}pt".format(current_score), mdn_font_size = self.theme["final_results"]["results_info"]["font_size"], mdn_font_style = self.theme["final_results"]["results_info"]["font_style"], mdn_font_color = self.theme["final_results"]["results_info"]["font_color"])
        fin_res_score_label.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_score_label_rel_container.add_widget(fin_res_score_label)
        # Create the total_time label
        fin_res_total_time_label_rel_container = RelativeLayout(size_hint = (.6, 1))
        fin_res_total_time_label = MDN_Label(mdn_app = self.mdn_app, mdn_text = "Total Time: {}s".format(round(self.player_total_time, 2)), mdn_font_size = self.theme["final_results"]["results_info"]["font_size"], mdn_font_style = self.theme["final_results"]["results_info"]["font_style"], mdn_font_color = self.theme["final_results"]["results_info"]["font_color"])
        fin_res_total_time_label.pos_hint = {"center_x": .5, "center_y": .5}
        fin_res_total_time_label_rel_container.add_widget(fin_res_total_time_label)
        final_result_stats_and_results_container_part_2_1.mdn_add_widget(fin_res_score_label_rel_container)
        final_result_stats_and_results_container_part_2_1.mdn_add_widget(fin_res_total_time_label_rel_container)
        final_result_stats_and_results_container.mdn_add_widget(final_result_stats_and_results_rel_container_part_2_1)

        # Create the average time label
        fin_res_avg_move_time_label_rel_container = RelativeLayout()
        fin_res_avg_move_time_label = MDN_Label(mdn_app = self.mdn_app, mdn_text = "Avg. Move Time: {}s".format(round(self.player_total_time / len(self.player_avg_move_time), 2)), mdn_font_size = self.theme["final_results"]["results_info"]["font_size"], mdn_font_style = self.theme["final_results"]["results_info"]["font_style"], mdn_font_color = self.theme["final_results"]["results_info"]["font_color"])
        fin_res_avg_move_time_label.pos_hint = {"center_x": .5, "center_y": .7}
        fin_res_avg_move_time_label_rel_container.add_widget(fin_res_avg_move_time_label)
        final_result_stats_and_results_container.mdn_add_widget(fin_res_avg_move_time_label_rel_container)

        # Combine the widgets together
        # final_result_container.mdn_add_widget(final_result_header_img_top_padding)
        final_result_content_container.mdn_add_widget(final_result_header_img_rel_container)
        final_result_content_container.mdn_add_widget(final_result_message_rel_container)
        final_result_content_container.mdn_add_widget(final_result_button_rel_container)
        final_result_content_container.mdn_add_widget(final_result_stats_and_results_rel_container)
        final_result_content_wrapper_container.mdn_add_widget(final_result_content_container)
        final_result_content_wrapper_rel_container.add_widget(final_result_content_wrapper_container)
        final_result_container.mdn_add_widget(final_result_content_wrapper_rel_container)
        final_result_rel_container.add_widget(final_result_container)
        final_result_overlay.add_widget(final_result_rel_container)
        overlay_rel_container_2.add_widget(final_result_overlay)
        self.record_game_results()

    # create_save_game method
    def create_save_game(self, *args):
        """
            The purpose of this function is to create the save game option UI
        """
        # Get the final_result_content_wrapper_container from the self.mdn_screen_ids
        final_result_content_wrapper_container = self.mdn_screen_ids["final_result_content_wrapper_container"]
        final_result_content_wrapper_container.clear_widgets()

        # Create a wrapper for all the content. This makes it easy to remove all the widgets at once
        save_game_option_wrapper_rel_container = RelativeLayout()
        save_game_option_wrapper_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "80%"])
        save_game_option_wrapper_container.pos_hint = {"center_y": .5}
        save_game_option_wrapper_rel_container.add_widget(save_game_option_wrapper_container)
        self.mdn_screen_ids["save_game_option_wrapper_rel_container"] = save_game_option_wrapper_rel_container
        self.mdn_screen_ids["save_game_option_wrapper_container"] = save_game_option_wrapper_container

        # Create the final results header
        save_game_option_header_img_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "130un"])
        save_game_option_header_img = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["80%", "100%"],
            mdn_bg = {"image": [self.theme_dest+self.theme["final_results"]["header"], "fit"]}
        )
        save_game_option_header_img.pos_hint = {"center_x": .5, "center_y": .4}
        save_game_option_header_img_rel_container.add_widget(save_game_option_header_img)

        # Create a label that states "Enter a name:"
        save_game_option_name_message_rel_container = RelativeLayout()
        save_game_option_name_message = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_size = ["90%", "100%"],
            mdn_text = "Enter a name",
            mdn_font_color = self.theme["save_game"]["message"]["font_color"],
            mdn_font_style = self.theme["save_game"]["message"]["font_style"],
            mdn_font_size = self.theme["save_game"]["message"]["font_size"]
        )
        save_game_option_name_message.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["save_game_option_name_message"] = save_game_option_name_message
        save_game_option_name_message_rel_container.add_widget(save_game_option_name_message)

        # Create textinput
        saved_game_option_textinput_rel_container = RelativeLayout()
        saved_game_option_textinput = MDN_Input(
            mdn_app = self.mdn_app,
            mdn_no_spaces = True,
            mdn_button_visible = False,
            mdn_multiline = False,
            mdn_size = ["80%", "90un"],
            mdn_use_special_char = False,
            mdn_use_specific_char = True,
            mdn_specific_char = "_",
            mdn_outline = self.theme["save_game"]["input"]["outline"],
            mdn_radius = self.theme["save_game"]["input"]["radius"]
        )
        self.mdn_screen_ids["saved_game_option_textinput"] = saved_game_option_textinput
        self.mdn_screen_ids["saved_game_option_textinput_rel_container"] = saved_game_option_textinput_rel_container
        saved_game_option_textinput.pos_hint = {"center_x": .5, "center_y": .7}
        saved_game_option_textinput_rel_container.add_widget(saved_game_option_textinput)

        # Create save_or_cancel_container
        saved_game_save_or_cancel_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "200un"])
        self.mdn_screen_ids["saved_game_save_or_cancel_container"] = saved_game_save_or_cancel_container

        # Create the cancel button
        cancel_btn_rel_container = RelativeLayout()
        cancel_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Cancel",
            mdn_size = ["160un", "80un"],
            mdn_outline = self.theme["save_game"]["btn"]["outline"],
            mdn_bg = self.theme["save_game"]["btn"]["bg"],
            mdn_radius = self.theme["save_game"]["btn"]["radius"]
        )
        cancel_btn.pos_hint = {"center_x": .6, "center_y": .5}
        cancel_btn.bind(on_release = self.create_final_results)
        cancel_btn_rel_container.add_widget(cancel_btn)

        # Create the save button
        save_btn_rel_container = RelativeLayout()
        save_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Save",
            mdn_size = ["160un", "80un"],
            mdn_outline = self.theme["save_game"]["btn"]["outline"],
            mdn_bg = self.theme["save_game"]["btn"]["bg"],
            mdn_radius = self.theme["save_game"]["btn"]["radius"]
        )
        save_btn.pos_hint = {"center_x": .4, "center_y": .5}
        save_btn.bind(on_release = self.save_game)
        save_btn_rel_container.add_widget(save_btn)

        # Add the header back to the screen again
        saved_game_save_or_cancel_container.mdn_add_widget(cancel_btn_rel_container)
        saved_game_save_or_cancel_container.mdn_add_widget(save_btn_rel_container)
        save_game_option_wrapper_container.mdn_add_widget(save_game_option_header_img_rel_container)
        save_game_option_wrapper_container.mdn_add_widget(save_game_option_name_message_rel_container)
        save_game_option_wrapper_container.mdn_add_widget(saved_game_option_textinput_rel_container)
        save_game_option_wrapper_container.mdn_add_widget(saved_game_save_or_cancel_container)
        final_result_content_wrapper_container.mdn_add_widget(save_game_option_wrapper_rel_container)
    


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

        if self.mdn_app.mdn_screenmanager.current_screen.name != "multiplayer_game_screen":
            Clock.schedule_once(self.update_ui, .05)
            return

        self.mdn_screen_ids["bg"]._mdn_update_graphic()
        self.create_cell_spaces()
        self.init_game_play()

    # update_overlay method
    def update_overlay(self, *args):
        """
            The purpose of this function is to update the ui for the overlay
        """
        # Get the 'overlay_container' from the self.mdn_screen_ids
        overlay_container = self.mdn_screen_ids["overlay_container"]
        
        # Update the size of 'overlay_container'
        overlay_container.size = self.mdn_screen_ids["bg"].size

        # Clear the canvas of 'overlay_container'
        overlay_container.canvas.before.clear()

        # Create the background of 'overlay_container'
        with overlay_container.canvas.before:
            Color(0, 0, 0, .5)
            overlay_container.rect = Rectangle(pos = self.mdn_screen_ids["bg"].pos, size = self.mdn_screen_ids["bg"].size)

    # update_overlay method
    def update_final_results_overlay(self, *args):
        """
            The purpose of this function is to update the ui for the final results overlay
        """
        # Get the 'final_result_overlay' from the self.mdn_screen_ids
        final_result_overlay = self.mdn_screen_ids["final_result_overlay"]
        
        # Update the size of 'final_result_overlay'
        final_result_overlay.size = self.mdn_screen_ids["bg"].size

        # Clear the canvas of 'final_result_overlay'
        final_result_overlay.canvas.before.clear()

        # Create the background of 'final_result_overlay'
        with final_result_overlay.canvas.before:
            Color(0, 0, 0, .5)
            final_result_overlay.rect = Rectangle(pos = self.mdn_screen_ids["bg"].pos, size = self.mdn_screen_ids["bg"].size)

    # update_final_results_container method
    def update_final_results_container(self, *args):
        final_result_container = self.mdn_screen_ids["final_result_container"]
        final_result_container.canvas.after.clear()
        with final_result_container.canvas.after:
            Color(*final_result_container._mdn_get_rgba(self.theme["final_results"]["shadow"]["color"])) 
            BoxShadow(
                pos = final_result_container.pos,
                size = final_result_container.size,
                offset = self.theme["final_results"]["shadow"]["offset"],
                spread_radius = self.theme["final_results"]["shadow"]["spread_radius"],
                border_radius = self.theme["final_results"]["shadow"]["border_radius"],
                blur_radius = self.theme["final_results"]["shadow"]["blur_radius"],
                inset = self.theme["final_results"]["shadow"]["inset"])

            Color(*final_result_container._mdn_get_rgba(final_result_container.mdn_outline["mobile"][0]))
            if final_result_container.mdn_radius["mobile"] != [0, 0, 0, 0]:
                Line(
                    rounded_rectangle = [
                        final_result_container.x, 
                        final_result_container.y, 
                        final_result_container.width, 
                        final_result_container.height, 
                        *final_result_container.mdn_radius["mobile"]
                    ],
                    width = final_result_container.mdn_outline["mobile"][1]
                )
            else:
                Line(
                    rectangle = [
                        final_result_container.x,
                        final_result_container.y,
                        final_result_container.width,
                        final_result_container.height
                    ],
                    width = final_result_container.mdn_outline["mobile"][1],
                    joint = final_result_container.mdn_outline_joint["mobile"]
                ) 

    # update_final_result_shadow_message method
    def update_final_result_shadow_message(self, *args):
        """
            The purpose of this function is to update the 'final_result_shadow_message' from the 'mdn_screen_ids'
        """
        # Get the 'final_result_shadow_message' from the 'mdn_screen_ids' variable
        final_result_shadow_message = self.mdn_screen_ids["final_result_shadow_message"]

        # Get the 'final_result_message' from the 'mdn_screen_ids' variable
        final_result_message = self.mdn_screen_ids["final_result_message"]

        # Get the 'final_result_message_container' from the 'mdn_screen_ids' variable
        final_result_message_container = self.mdn_screen_ids["final_result_message_container"]

        # Change the position of the 'final_result_message'
        final_result_message.pos = [
            (final_result_message_container.width/2 - final_result_message.width/2),
            (final_result_message_container.height/2 - final_result_message.height/2)
        ]

        # Change the position of the 'final_result_shadow_message'
        final_result_shadow_message.pos = [
            (final_result_message_container.width/2 - final_result_message.width/2)-3,
            (-final_result_message_container.height/2 + final_result_message.height/2)+1
        ]

    # update_tic_tac_toe_win_line method
    def update_tic_tac_toe_win_line(self, *args):
        """
            The purpose of this function is to update the ui for the overlay
        """
        if args[0] > 3: return
       
        # Get the winning line indexes. This will be used to get the positions of the boxes, so we can draw the line
        winning_line_indexes = self.get_winning_line(self.board_positions, self.board_size, self.win_length)

        # Create the variable that will hold the first cell, which can be found in the 'mdn_screen_ids'
        first_cell = self.mdn_screen_ids["box_{}".format(winning_line_indexes[0][0]*self.board_size+winning_line_indexes[0][1])]

        # Create the variable that will hold the end cell, which can be found in the 'mdn_screen_ids'
        second_cell = self.mdn_screen_ids["box_{}".format(winning_line_indexes[1][0]*self.board_size+winning_line_indexes[1][1])]

        # This variable will be responsible for holding the starting position for the line
        start_pos = array('d', first_cell.to_window(*first_cell.pos))

        # This variable will be responsible for holding the starting position for the line
        end_pos = array('d', second_cell.to_window(*second_cell.pos))

        # This variable will hold the width of the first cell, which is the width of all the cells on the board
        cell_size = self.mdn_screen_ids["box_0"].width

        # Get the 'tic_tac_toe_win_line_container' from the 'self.mdn_screen_ids'
        tic_tac_toe_win_line_container = self.mdn_screen_ids["tic_tac_toe_win_line_container"]

        # If the line is a horizontal or vertical line, then add half the cell width to it, so the line is in the center
        for i in range(0, 2):
            if start_pos[i] == end_pos[i]: 
                start_pos[i]+=cell_size/2
                end_pos[i]+=cell_size/2

        # If the line is a horizontal or vertical line, then add half the cell width to it, so the line is in the center
        if start_pos[1] == end_pos[1]: end_pos[0]+=cell_size
        elif start_pos[0] == end_pos[0]: start_pos[1]+=cell_size
        elif start_pos[1] > end_pos[1] and start_pos[0] > end_pos[0]: 
            start_pos[1]+=cell_size
            start_pos[0]+=cell_size
        elif start_pos[1] > end_pos[1] and start_pos[0] < end_pos[0]:
            start_pos[1]+=cell_size
            end_pos[0]+=cell_size

        # Update the starting and ending point
        tic_tac_toe_win_line_container.starting_point = start_pos
        tic_tac_toe_win_line_container.ending_point = end_pos

        # Update the line after 3 seconds
        Clock.schedule_once(partial(self.update_tic_tac_toe_win_line, args[0]+1), 3)

    # update_timer_ui method
    def update_timer_ui(self):
        "The purpose of this function is to update the timer UI"
        # Get the timer clock from the timer
        timer_clock_label = self.mdn_screen_ids["timer_clock_label"] 

        # Get the text from the 'timer_clock_label'
        timer_clock_label_text = int(timer_clock_label.mdn_text["desktop"])  

        # Update the text for 'timer_clock_label'
        timer_clock_label.mdn_update({
            "mdn_font_size": 35 if int(timer_clock_label_text) <= 3 else 50,
            "mdn_font_color": (255, 0, 0, 1) if int(timer_clock_label_text) <=3 else (255, 255, 255, 1),
            "mdn_font_style": ["bold" if int(self.timers_for_moves[int(self.selected_move_timer)-1]) <= 3 else ""]
        })  

        # If timer is less than 3, and the label is not a child element of the timer, then clear all the widgets from the timer and add the label widget
        if int(timer_clock_label_text) <= 3 and not self.mdn_screen_ids["timer_label_rel_container"] in self.mdn_screen_ids["timer_container"].children:
            self.mdn_screen_ids["timer_container"].clear_widgets()
            self.mdn_screen_ids["timer_container"].mdn_add_widget(self.mdn_screen_ids["timer_label_rel_container"])
            self.mdn_screen_ids["timer_container"].mdn_add_widget(self.mdn_screen_ids["timer_clock_label_rel_container"])  
        elif int(timer_clock_label_text) > 3 and self.mdn_screen_ids["timer_label_rel_container"] in self.mdn_screen_ids["timer_container"].children:
            self.mdn_screen_ids["timer_container"].clear_widgets()
            self.mdn_screen_ids["timer_container"].mdn_add_widget(self.mdn_screen_ids["timer_clock_label_rel_container"])

        # Update the position of the 'timer_clock_label'
        timer_clock_label.pos_hint = {"center_x": .5, "center_y": .7 if int(timer_clock_label.mdn_text["desktop"]) <= 3 else .5}              


    # +----------------------------------------+
    # |                                        |
    # |         Create Event Functions         |
    # |                                        |
    # +----------------------------------------+
    # press_box method
    def player_pressed_box(self, *args):
        """
            The purpose of this function is to place the x or o in the correct box on the board
        """
        # Check if box has been pressed once or if the game is over, if so, then return
        if args[0].play_type or self.game_over: return

        # Keep track of the current score for the player
        self.keep_score()

        # Make the player move
        self.make_player_move(args)

        # Set the current turn for the computer
        self.current_turn = "C"

        # # Keep track of the current score for the player
        # self.keep_score()

        # # Make the computer move
        # self.make_computer_move()

        # # Set the current turn for the computer
        # self.current_turn = "P"

        # Get the timer from the 'mdn_screen_ids'
        timer = self.mdn_screen_ids["timer_container"]

        # Set the timer angle back to 360
        timer.stop_angle = 360

        # If game isn't over, then set the clock label back to 'move_timer'
        if not self.game_over:

            # Get the timer clock label from the 'mdn_screen_ids'
            timer_clock_label = self.mdn_screen_ids["timer_clock_label"]

            # Update the text for the timer
            timer_clock_label.mdn_update({"mdn_text": "{}".format("00:00" if self.selected_move_timer == "-10" else int(self.timers_for_moves[int(self.selected_move_timer)-1]))})

        # Check if game is over and is a draw
        if len(self.board_available_cell_positions) == 0 and not self.game_over:
            print("Draw!!!!!")
            self.game_over = True
            return

    # start_move_timer method
    def start_move_timer(self, *args):
        """
            The purpose of this function is to start the timer for the player's move
        """
        # Return if it's the computer's turn or if the game is over
        if self.game_over: return

        # If timer was paused, then start it again
        if self.game_paused:return

        # Get the timer widget
        timer = self.mdn_screen_ids["timer_container"]

        # Get the timer clock from the timer
        timer_clock_label = self.mdn_screen_ids["timer_clock_label"]

        # Reset the current_seconds
        self.current_second = args[0]

        # If current_second == 70sec, then take this path 
        if self.current_second == 70 or self.current_second == 0:

            # Get the text from the 'timer_clock_label'
            timer_clock_label_text = int(timer_clock_label.mdn_text["desktop"])

            # Update the text for 'timer_clock_label'
            timer_clock_label.mdn_update({"mdn_text": "{}".format(int(timer_clock_label_text)-1)})

            # Update the timer ui
            self.update_timer_ui()
    
            # Reset the current_seconds
            self.current_second = 0

        # Update the position of the 'timer_clock_label'
        timer_clock_label.pos_hint = {"center_x": .5, "center_y": .7 if int(timer_clock_label.mdn_text["desktop"]) <= 3 else .5}

        # If angle - 5 divided by 'move_time' is greater than 0, then take this path
        if timer.stop_angle-(5/int(self.timers_for_moves[int(self.selected_move_timer)-1])) >= 0:
            timer.stop_angle-=5/int(self.timers_for_moves[int(self.selected_move_timer)-1])
        # If angle - 5 divided by 'move_time' is less than 0, then set the angle to 0
        else: timer.stop_angle = 0

        # Update timer widget outline
        timer._mdn_update_gridlayout_graphic_outline()

        # If angle is less than 0 or is 0, then take this path
        if timer.stop_angle <= 0:

            self.keep_score()

            # Increment total_game_moves by 1
            self.total_game_moves["p1" if self.current_turn == "P" else "p2"]+=1

            # Calculate the total amount of time
            self.player_total_time["p1" if self.current_turn == "P" else "p2"]+= time() - self.player_turn_time_start

            # Set the 'current_turn' to the 'player'
            self.current_turn = "C"

            # self.keep_score()
            self.player_turn_time_start = time()

            # Set timer angle to 360
            timer.stop_angle = 360

            # Set the current_second back zero
            self.current_second = 0

            # Update the text for 'timer_clock_label'
            timer_clock_label.mdn_update({"mdn_text": "{}".format(int(self.timers_for_moves[int(self.selected_move_timer)-1]))})

            self.update_timer_ui()

            # Update timer widget graphics
            timer._mdn_update_gridlayout_graphic_outline()

            # # Let the computer make it's move
            # self.make_computer_move()

            # Set the 'current_turn' to the 'player'
            self.current_turn = "C"

            # Start the timer for the player
            self.start_move_timer(self.current_second+1)   

        # If angle is greater than 0, then take this path
        else:
            Clock.schedule_once(partial(self.start_move_timer, self.current_second+1), .01)

    # start_stopwatch method
    def start_stopwatch(self, *args):
        """
            The purpose of this function is to create a stopwatch for the game. This is for if there is no timer for the game.
        """
        # Return if it's the computer's turn or if the game is over
        if self.game_over: return

        # If stopwatch was paused, then start it again
        if self.game_paused: return

        # Get the current seconds from args
        self.current_second = args[0]

        # Get the timer widget
        timer = self.mdn_screen_ids["timer_container"]

        # Get the timer clock from the timer
        timer_clock_label = self.mdn_screen_ids["timer_clock_label"]

        # Get the timer relative container
        timer_label_rel_container = self.mdn_screen_ids["timer_label_rel_container"]

        # If timer label exists, then remove it from the screen
        if timer_label_rel_container in timer.children:
            timer.remove_widget(timer_label_rel_container)
            timer_clock_label.pos_hint = {"center_x": .5, "center_y": .5}
            timer_clock_label.mdn_update({"mdn_font_size": 40})

        # Increment second by 1
        self.current_second+=1

        # Get the minutes
        minute = "0{}".format(int(self.current_second/60)) if int(self.current_second/60) < 10 else int(self.current_second/60)

        # Get the seconds
        seconds = "0{}".format(int(self.current_second%60)) if int(self.current_second%60) < 10 else int(self.current_second%60)

        # If game is over 60 min, then quit game
        if int(minute) >= 60: 
            # Set game over to True
            self.game_over = True
            # Set the label to "Game Expired"
            timer_clock_label.mdn_update({"mdn_text": "Game expired"})
            return

        timer_clock_label.mdn_update({"mdn_text": "{}:{}".format(minute, seconds)})

        Clock.schedule_once(partial(self.start_stopwatch, self.current_second), 1)

    # play_again method
    def play_again(self, *args):
        """
            The purpose of this function is to reset the game and start again
        """
        # If self.freeze, then return
        if self.board_visible: return

        # Reset the variables
        self.reset_screen_variables()

        # Initialize The UI
        self.init_ui()

    # exit_game method
    def exit_game(self, *args):
        """
            The purpose of this function is to exit the game
        """
        # Get the second relative layout for overlays. 
        # Note: The first overlay container is being used to draw the line
        overlay_rel_container_2 = self.mdn_screen_ids["overlay_rel_container_2"]

        # Open the overlay
        self.overlay_open = True

        # Pause game
        self.game_paused = True

        # Set the 'board_visible' to False
        self.board_visible = False

        # +---------- Exit Results Overlay ----------+
        # This is going to create the overlay
        exit_game_overlay = FloatLayout()
        exit_game_overlay.size_hint = (None, None)
        exit_game_overlay.pos_hint = {"center_x": .5, "center_y": .5}
        self.mdn_screen_ids["final_result_overlay"] = exit_game_overlay
        exit_game_overlay.bind(pos = self.update_final_results_overlay, size = self.update_final_results_overlay)

        # +---------- Exit Results Wrapper Container ----------+
        # Create the exit_games container that will hold all the widgets
        exit_game_content_wrapper_rel_container = RelativeLayout()
        exit_game_content_wrapper_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        self.mdn_screen_ids["exit_game_content_wrapper_container"] = exit_game_content_wrapper_container
        exit_game_content_wrapper_container.pos_hint = {"center_x": .5, "center_y": .5}
        exit_game_content_wrapper_rel_container.add_widget(exit_game_content_wrapper_container)

        # +---------- Final Results Container ----------+
        # Create the final_results container that will hold all the widgets
        final_result_rel_container = RelativeLayout()
        final_result_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_bg = {"image": [self.theme_dest+self.theme["final_results"]["bg"], "stretch"]},
            mdn_size = ["550un", "400un"],
            mdn_radius = self.theme["final_results"]["radius"],
            mdn_outline = self.theme["final_results"]["outline"]
        )
        self.mdn_screen_ids["final_result_container"] = final_result_container
        final_result_container.pos_hint = {"center_x": .5, "center_y": .5}
        final_result_container.bind(pos = self.update_final_results_container, size = self.update_final_results_container)
        final_result_rel_container.add_widget(final_result_container)

        # +---------- Final Results Warning Label ----------+
        exit_game_warning_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_size = ["100%", "120un"],
            mdn_text = "Do You Wish To Quit?",
            mdn_font_size = 33,
            mdn_font_style = ["bold", "underline"],
            mdn_font_color = [0, 0, 0, 1]
        )

        # +---------- Final Results Button Container ----------+
        exit_game_warning_btn_rel_container = RelativeLayout()
        exit_game_warning_btn_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100%", "100%"],
        )
        exit_game_warning_btn_rel_container.add_widget(exit_game_warning_btn_container)

        # +---------- Final Results Exit Button ----------+
        exit_game_btn_rel_container = RelativeLayout()
        exit_game_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Exit Game",
            mdn_outline = self.theme["exit_game"]["exit_btn"]["outline"],
            mdn_font_color = self.theme["exit_game"]["exit_btn"]["font_color"],
            mdn_font_style = self.theme["exit_game"]["exit_btn"]["font_style"],
            mdn_font_size = self.theme["exit_game"]["exit_btn"]["font_size"],
            mdn_size = self.theme["exit_game"]["exit_btn"]["size"],
            mdn_bg = self.theme["exit_game"]["exit_btn"]["bg"],
            mdn_radius = self.theme["exit_game"]["exit_btn"]["radius"],
            mdn_shadow = self.theme["exit_game"]["exit_btn"]["shadow"]
        )
        exit_game_btn.bind(on_release = self.go_to_main_menu)
        exit_game_btn.pos_hint = {"center_x": .5, "center_y": .7}
        exit_game_btn_rel_container.add_widget(exit_game_btn)

        # +---------- Final Results Cancel Button ----------+
        cancel_game_btn_rel_container = RelativeLayout()
        cancel_game_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Cancel",
            mdn_outline = self.theme["exit_game"]["cancel_btn"]["outline"],
            mdn_font_color = self.theme["exit_game"]["cancel_btn"]["font_color"],
            mdn_font_style = self.theme["exit_game"]["cancel_btn"]["font_style"],
            mdn_font_size = self.theme["exit_game"]["cancel_btn"]["font_size"],
            mdn_size = self.theme["exit_game"]["cancel_btn"]["size"],
            mdn_bg = self.theme["exit_game"]["cancel_btn"]["bg"],
            mdn_radius = self.theme["exit_game"]["cancel_btn"]["radius"],
            mdn_shadow = self.theme["exit_game"]["cancel_btn"]["shadow"]
        )
        cancel_game_btn.bind(on_release = self.continue_game)
        cancel_game_btn.pos_hint = {"center_x": .5, "center_y": .65}
        cancel_game_btn_rel_container.add_widget(cancel_game_btn)
        exit_game_warning_btn_container.mdn_add_widget(cancel_game_btn_rel_container)
        exit_game_warning_btn_container.mdn_add_widget(exit_game_btn_rel_container)


        # Add Widgets To Screen
        final_result_container.mdn_add_widget(exit_game_warning_label)
        final_result_container.mdn_add_widget(exit_game_warning_btn_rel_container)
        exit_game_content_wrapper_container.mdn_add_widget(final_result_rel_container)
        exit_game_overlay.add_widget(exit_game_content_wrapper_rel_container)
        overlay_rel_container_2.add_widget(exit_game_overlay)

    # continue_game method
    def continue_game(self, *args):
        """
            The purpose of this function is to continue the game
        """
        # Get the second relative layout for overlays. 
        # Note: The first overlay container is being used to draw the line
        overlay_rel_container_2 = self.mdn_screen_ids["overlay_rel_container_2"]

        # Get the 'exit game' overlay
        exit_game_overlay = self.mdn_screen_ids["final_result_overlay"]

        # Close the overlay
        self.overlay_open = False

        # Start game
        self.game_paused = False

        # Set the 'board_visible' to Trie
        self.board_visible = True

        # Remove the widget from the screen
        overlay_rel_container_2.remove_widget(exit_game_overlay)

        if self.selected_move_timer == "-10": self.start_stopwatch(self.current_second)
        else: self.start_move_timer(self.current_second)

    # view_board method
    def view_board(self, *args):
        """
            The purpose of this function is to view the board and get rid of the overlay
        """
        # If the button wasn't responsible for the viewing the board, then exit this function
        if not "view_board_btn" in args: return

        # If self.freeze, then return
        if self.board_visible: return

        # Set the board_visible to True
        self.board_visible = True

        # Get the overlay_rel_container_2 from the 'mdn_screen_ids'
        overlay_rel_container_2 = self.mdn_screen_ids["overlay_rel_container_2"]

        # Get the 'final_result_overlay' from the 'mdn_screen_ids'
        final_result_overlay = self.mdn_screen_ids["final_result_overlay"]

        # Remove the widget from the screen
        overlay_rel_container_2.remove_widget(final_result_overlay)

        # If the player presses view board, then set up a bind event, so when a player touches the window, the board will be hidden again
        Window.bind(on_touch_down = self.hide_board, on_press = self.hide_board)

    # hide_board method
    def hide_board(self, *args):
        """
            The purpose of this function is to hide the board after the game is over and show the results
        """
        # If the board is already hidden, then exit this function
        if not self.board_visible: return

        # If "final_result_overlay" doesn't exist in the 'self.mdn_screen_ids', then create the overlay
        if not "final_result_overlay" in self.mdn_screen_ids: 
            self.create_final_results()
            return

        # Get the overlay_rel_container_2 from the 'mdn_screen_ids'
        overlay_rel_container_2 = self.mdn_screen_ids["overlay_rel_container_2"]

        # Get the 'final_result_overlay' from the 'mdn_screen_ids'
        final_result_overlay = self.mdn_screen_ids["final_result_overlay"]

        # Remove the widget from the screen
        overlay_rel_container_2.add_widget(final_result_overlay)

        Clock.schedule_once(self.unfreeze_final_results_buttons, 1)

    # save_game method
    def save_game(self, *args):
        """
            The purpose of this function is to save the game
        """
        # If self.freeze, then return
        if self.board_visible: return

        # Store the original file
        original_directory = "game_data/"
        original_file = "saved_matches.json"

        # Check to see if file and path exists
        if os.path.isfile(original_directory+original_file): prev_existed = True
        else: prev_existed = False

        # If file doesn't exist, then return
        if not prev_existed:
            print("Sorry the 'saved_matches.json' file doesn't exist!!!")
            return

        # Open the json file
        with open(original_directory+original_file, "r") as saved_matches_file:
            saved_matches_json = json.load(saved_matches_file)
        saved_matches_file.close()

        # Check if key already exists in saved_matches_json
        if self.mdn_screen_ids["saved_game_option_textinput"].mdn_textinput_kv.text in saved_matches_json["saved_matches"]:
            self.mdn_screen_ids["save_game_option_name_message"].mdn_update({"mdn_text": "Saved file already exists with name '{}'!".format(self.mdn_screen_ids["saved_game_option_textinput"].mdn_textinput_kv.text), "mdn_font_color": (255, 0, 0, 1), "mdn_font_size": 32, "mdn_size": ["80%", "100%"]})
            return

        # Remove directory and it's all content if dir exists
        if os.path.isdir(original_directory+"temp/"):shutil.rmtree(original_directory+"temp/")  

        # Copy file   
        os.mkdir(original_directory+"temp/") 
        shutil.copy2(original_directory+original_file, original_directory+"temp/"+original_file)

        # Store data in 'saved_matches_json'
        if self.selected_move_timer == "-10": game_timer = "None"
        else: game_timer = self.timers_for_moves[self.selected_move_timer]
        saved_matches_json["saved_matches"][self.mdn_screen_ids["saved_game_option_textinput"].mdn_textinput_kv.text] = {
            "winner": self.winning_player,
            "score": self.score_player["P"],
            "avg_move_time": round(self.player_total_time / len(self.player_avg_move_time), 2),
            "total_time": round(self.player_total_time, 2),
            "difficulty": self.computer_levels[self.selected_computer_difficulty],
            "starts_first": self.starts_first,
            "play_mode": self.play_mode,
            "board_size": "{}x{}".format(self.board_size, self.board_size),
            "win_length": self.win_length,
            "timer": game_timer,
            "game_moves": self.game_moves,
            "date": [datetime.now().year, datetime.now().month, datetime.now().day]
        }

        # This will determine if writing to the file was successful
        written_to_file_successfully = False

        # Open the json file and write to it
        try:
            # Write to the file
            with open(original_directory+original_file, "w") as matches_file:
                json.dump(saved_matches_json, matches_file)
            matches_file.close()

            # Set it to true, if writing to the file was successful
            written_to_file_successfully = True

        # If writing to the file was unsuccessful, then raise an error
        except: raise

        # If writing to the file was unsuccessful, then take this path
        finally:
            if not written_to_file_successfully and prev_existed:
                print("File could not be written to")
                shutil.copy2(original_directory+'temp/'+original_file, original_file)  

        # Remove directory and it's all content
        shutil.rmtree(original_directory+"temp/") 

        if written_to_file_successfully:

            # Change the saved game message
            self.mdn_screen_ids["save_game_option_name_message"].mdn_update({"mdn_text": "{} was successfully saved!".format(self.mdn_screen_ids["saved_game_option_textinput"].mdn_textinput_kv.text), "mdn_font_color": (0, 150, 23, 1)})

            # Remove the textinput container
            self.mdn_screen_ids["save_game_option_wrapper_container"].remove_widget(
                self.mdn_screen_ids["saved_game_option_textinput_rel_container"]
            )

            # Remove the buttons container
            self.mdn_screen_ids["save_game_option_wrapper_container"].remove_widget(
                self.mdn_screen_ids["saved_game_save_or_cancel_container"]
            )

            # Create the confirm button and add it to the screen
            confirm_button_rel_container = MDN_RelativeLayout(mdn_size = ["100%", "150un"])
            confirm_button = MDN_Button(
                mdn_app = self.mdn_app,
                mdn_text = "Ok",
                mdn_size = ["160un", "80un"],
                mdn_outline = self.theme["save_game"]["btn"]["outline"],
                mdn_bg = self.theme["save_game"]["btn"]["bg"],
                mdn_radius = self.theme["save_game"]["btn"]["radius"]
            )
            
            confirm_button.pos_hint = {"center_x": .5, "center_y": .5}
            confirm_button_rel_container.add_widget(confirm_button)
            confirm_button.bind(on_release = self.create_final_results)
            self.mdn_screen_ids["save_game_option_wrapper_container"].mdn_add_widget(confirm_button_rel_container)

    # go_to_main_menu method
    def go_to_main_menu(self, *args):
        """
            The purpose of this function is to go to the menu
        """
        # If self.freeze, then return
        if self.board_visible: return

        self.mdn_switch("home_screen", "Welcome To TicTacToe", "right")

    # +----------------------------------------+
    # |                                        |
    # |       Create Gameplay Functions        |
    # |                                        |
    # +----------------------------------------+
    # start_game method
    def start_gameplay(self, *args):
        """
            The purpose of this function is to start the game. It will count down from three and then start the game
        """
        # Game hasn't started yet. This will keep the computer and timer/stopwatch from running.
        self.game_over = True

        # Get the seconds from the 'current_second'
        current_second = args[0]

        # If 'current_second' is less than 3, then take this path
        if current_second != 0:

            # Get the countdown_label from the self.mdn_screen_ids
            countdown_label = self.mdn_screen_ids["countdown_label"]

            # Count down and change the text
            countdown_label.mdn_update({"mdn_text": str(current_second)})

            # Call this function a second from now
            Clock.schedule_once(partial(self.start_gameplay, current_second-1), 1)
            return

        # Game has started
        self.game_over = False

        # Remove the overlay from the screen
        self.mdn_screen_ids["overlay_rel_container"].clear_widgets()

        # If the computer starts first, which is (player 2), then take this path
        if self.starts_first == "computer":
            # Record the time of the player's 2 turn
            self.player_turn_time_start = time()

            # Set the 'current_turn' to the 'player'
            self.current_turn = "C"  
        else:
            # Record the time of the player's 2 turn
            self.player_turn_time_start = time()

            # Set the 'current_turn' to the 'player'
            self.current_turn = "P"                    

        if self.selected_move_timer == "-10": self.start_stopwatch(0)
        else:
            # Get the timer clock from the timer
            timer_clock_label = self.mdn_screen_ids["timer_clock_label"]

            # Change seconds for the timer
            timer_clock_label.mdn_update({"mdn_text": "{}".format(int(self.timers_for_moves[int(self.selected_move_timer)-1]))})
            
            self.start_move_timer(1)   

    # game_is_over method
    def game_is_over(self, player):
        """
            This function will run if the game is over. If the player won, computer won, or if it was a draw
        """

        # Get the winning line indexes. This will be used to get the positions of the boxes, so we can draw the line
        winning_line_indexes = self.get_winning_line(self.board_positions, self.board_size, self.win_length)

        # Create the variable that will hold the first cell, which can be found in the 'mdn_screen_ids'
        first_cell = self.mdn_screen_ids["box_{}".format(winning_line_indexes[0][0]*self.board_size+winning_line_indexes[0][1])]

        # Create the variable that will hold the end cell, which can be found in the 'mdn_screen_ids'
        second_cell = self.mdn_screen_ids["box_{}".format(winning_line_indexes[1][0]*self.board_size+winning_line_indexes[1][1])]

        # This variable will be responsible for holding the starting position for the line
        start_pos = array('d', first_cell.to_window(*first_cell.pos))

        # This variable will be responsible for holding the starting position for the line
        end_pos = array('d', second_cell.to_window(*second_cell.pos))

        # This variable will hold the width of the first cell, which is the width of all the cells on the board
        cell_size = self.mdn_screen_ids["box_0"].width

        # If the line is a horizontal or vertical line, then add half the cell width to it, so the line is in the center
        for i in range(0, 2):
            if start_pos[i] == end_pos[i]: 
                start_pos[i]+=cell_size/2
                end_pos[i]+=cell_size/2

        # If the line is a horizontal or vertical line, then add half the cell width to it, so the line is in the center
        if start_pos[1] == end_pos[1]: end_pos[0]+=cell_size
        elif start_pos[0] == end_pos[0]: start_pos[1]+=cell_size
        elif start_pos[1] > end_pos[1] and start_pos[0] > end_pos[0]: 
            start_pos[1]+=cell_size
            start_pos[0]+=cell_size
        elif start_pos[1] > end_pos[1] and start_pos[0] < end_pos[0]:
            start_pos[1]+=cell_size
            end_pos[0]+=cell_size


        # Set the 'game_over' to True
        self.game_over = True

        # Set the 'board_visible' to False
        self.board_visible = False

        # This variable will be the winning line
        tic_tac_toe_win_line_container = Win_Line_Anim_Module(
            mdn_app = self.mdn_app,
            initial_start_point = start_pos, 
            starting_point = start_pos,
            ending_point = end_pos,
            duration = 1,
            line_color = self.theme["win_line_color"][player][self.computer_play_as if player == "C" else self.player_play_as]
        )

        # Add the line to the 'mdn_screen_ids'
        self.mdn_screen_ids["tic_tac_toe_win_line_container"] = tic_tac_toe_win_line_container

        # Add widgets to screen
        self.mdn_screen_ids["overlay_rel_container"].add_widget(tic_tac_toe_win_line_container)

        # Run the animation
        tic_tac_toe_win_line_container.animate_line()

        # Bind the line to window, so it updates its pos according to the window
        Clock.schedule_once(self.bind_tic_tac_toe_win_line_container, tic_tac_toe_win_line_container.duration)

        # Set the 'winning_player' to the current player
        self.winning_player = player

        # Show the results in a second
        Clock.schedule_once(partial(self.create_final_results, player), tic_tac_toe_win_line_container.duration)

    # make_player_move method
    def make_player_move(self, args):
        """
            The purpose of this function is to make the player move. This means display the player graphics, store the player's last move, and a lot more.
        """
        # If there are no available cells, then exit this function
        if len(self.board_available_cell_positions) == 0: return

        # Calculate the total amount of time
        self.player_total_time["p1" if self.current_turn == "P" else "p2"]+= time() - self.player_turn_time_start

        # Calculate the average move time
        self.player_avg_move_time["p1" if self.current_turn == "P" else "p2"].append(time() - self.player_turn_time_start)

        # Get the cell number that the player has pressed
        player_cell_number = int(args[0].mdn_id[4:])

        # Set the cell to 'player' showing that the player has occupied the space/cell
        self.board_positions[int(player_cell_number / self.board_size)][player_cell_number % self.board_size] = self.current_turn      

        # Remove the cell number from the 'board_available_cell_positions' var
        try:
            self.board_available_cell_positions.remove(player_cell_number)
        except:
            print("Tried to remove '{}' from board_available_positions".format(player_cell_number))
            print(self.board_available_cell_positions)
            print(self.board_positions) 

        # Display the correct icon on the board
        args[0].mdn_update({"mdn_icon": self.theme_dest+self.theme["play_as"][self.player_play_as if self.current_turn == "P" else self.computer_play_as]})

        # Set the 'player_last_move' to the cell_number
        self.player_last_move = player_cell_number

        # Increment the number of moves by one
        self.total_game_moves["p1" if self.current_turn == "P" else "p2"]+=1

        # # Record all the moves of the game
        # self.game_moves.append({"player": "P", "cell_number": player_cell_number, "timer": self.mdn_screen_ids["timer_clock_label"].mdn_text["mobile"], "score": self.score_player["P"]})

        # Check if player won the game
        if self.check_win(self.board_positions, self.current_turn, self.board_size, self.win_length): self.game_is_over(self.current_turn)

    def make_computer_move(self):
        """
            The purpose of this function is to make the computer move. This means display the right computer graphics and a lot more. 
        """
        # If there are no available cells, then exit this function
        if len(self.board_available_cell_positions) == 0 or self.game_over: return

        # Let the computer move
        computer_best_move = self.computer_ai.get_best_move()

        # Let the computer wait before making the move
        sleep(self.computer_move_delays[0])
        self.computer_move_delays.pop(0)
     
        # Set the cell to 'player' showing that the player has occupied the space/cell
        self.board_positions[int(computer_best_move / self.board_size)][computer_best_move % self.board_size] = "C" 

        # Remove the cell number from the 'board_available_cell_positions' var
        self.board_available_cell_positions.remove(computer_best_move) 

        # Display the correct icon on the board
        self.mdn_screen_ids["box_{}".format(computer_best_move)].mdn_update({"mdn_icon": self.theme_dest+self.theme["play_as"][self.computer_play_as]})

        # Set the 'cell.play_type' to the current character or play_type that the player is
        self.mdn_screen_ids["box_{}".format(computer_best_move)].play_type = self.computer_play_as
  
        # Increment the number of moves by one
        self.total_game_moves+=1

        # Record all the moves of the game
        self.game_moves.append({"player": "C", "cell_number": computer_best_move, "timer": self.mdn_screen_ids["timer_clock_label"].text, "score": self.score_player["C"]})

        # Check if player won the game
        if self.check_win(self.board_positions, 'C', self.board_size, self.win_length): self.game_is_over("C")
        else:
            self.player_turn_time_start = time()


    # +----------------------------------------+
    # |                                        |
    # |     Create Miscellaneous Functions     |
    # |                                        |
    # +----------------------------------------+
    # init_game_play method
    def init_game_play(self):
        """
            The purpose of this function is to initialize the game play after the graphics and ui have been created
        """

        # Set the board_available_cell_positions to the amount of cells there are on the board
        self.board_available_cell_positions = [i for i in range(0, self.board_size*self.board_size)]

        # Initialize the board positions
        for i in range(0, self.board_size):
            self.board_positions.append([])
            for x in range(0, self.board_size):
                self.board_positions[i].append(' ')

        # Start the gameplay
        Clock.schedule_once(partial(self.start_gameplay, 3), .2)

    # check_win method
    def check_win(self, board, player, n, symbols_to_win):
        # Check rows
        for row in range(n):
            for col in range(n - symbols_to_win + 1):  # Adjust the range
                if all(board[row][col + i] == player for i in range(symbols_to_win)):
                    return True

        # Check columns
        for col in range(n):
            for row in range(n - symbols_to_win + 1):  # Adjust the range
                if all(board[row + i][col] == player for i in range(symbols_to_win)):
                    return True

        # Check diagonals
        for row in range(n - symbols_to_win + 1):  # Adjust the range
            for col in range(n - symbols_to_win + 1):  # Adjust the range
                if all(board[row + i][col + i] == player for i in range(symbols_to_win)):
                    return True
                if all(board[row + i][col + symbols_to_win - 1 - i] == player for i in range(symbols_to_win)):
                    return True

        return False

    # keep_score method
    def keep_score(self):
        """
            The purpose of this function is keep track of the score for the player or computer
        """
        # Get the seconds from the timer clock label from the 'mdn_screen_ids'
        player_actual_score_label = self.mdn_screen_ids["player_actual_score_label_{}".format(self.current_turn)]

        # This variable is responsible for holding the points for each move
        move_point = self.score_data[self.computer_levels[self.selected_computer_difficulty].lower()]["move_point"]

        # Get the seconds from the timer clock label from the 'mdn_screen_ids'
        timer_clock_label_seconds = self.mdn_screen_ids["timer_clock_label"].mdn_text["desktop"]

        if self.selected_move_timer != "-10":

            # Get the current_move_timer
            current_move_timer = self.timers_for_moves[int(self.selected_move_timer)-1]

            # Get the amount of seconds it took for the player to move
            seconds_for_player_to_move = int(current_move_timer) - int(timer_clock_label_seconds) if timer_clock_label_seconds != "0" else move_point

            # This will get the score the player
            new_score = move_point - seconds_for_player_to_move

        else:

            # Get the minutes from the stopwatch
            minutes = timer_clock_label_seconds[:timer_clock_label_seconds.index(":")]
            minutes = int(minutes) * 60

            # Get the seconds from the stopwatch
            seconds = timer_clock_label_seconds[timer_clock_label_seconds.index(":")+1:]

            # Get the total amount of seconds to move
            total_seconds = int(minutes) + int(seconds)

            # If it's the computer's turn, then get set the total_seconds to the the first number in the 'computer_move_delay' variable
            # if self.current_turn == "C": total_seconds = int(self.computer_move_delays[0])

            # If total_seconds is greater than the ideal stopwatch move time, then the points will be greatly reduce.
            # For example, if it took 11 seconds for a player to move, then instead of subtracting 11 seconds off of the player, because you only get 10 points for each move anyways, we will subtract the 'stopwatch_ideal_move_time' from 'the move_time' then divide it by 2, to get a smaller number, but it won't be a negative one.
            if total_seconds > self.stopwatch_ideal_move_time: new_score = int((move_point - self.stopwatch_ideal_move_time) / 2)
            else: new_score = move_point - total_seconds

        # Update the current score of the player
        self.score_player[self.current_turn]+=new_score

        # Update the text of player or the computer
        player_actual_score_label.mdn_update({"mdn_text": str(self.score_player[self.current_turn])})

    # record_game_results method
    def record_game_results(self):
        """
            The purpose of this function is to record the game results in the matches.json file. This will record the 'play_mode', 'score', 'total_time', 'avg_move_time', 'player_win_state', and the 'date'
        """
        # If the game ended as a draw, then set the 'player_win_state' to 'draw'
        if self.winning_player == None: player_win_state = "draw"
        # If the game ended as a win, then set the 'player_win_state' to a 'win', otherwise set it to a 'loss'
        else: player_win_state = "win" if self.winning_player == "P" else "loss"

        # Store the original file
        original_directory = "game_data/"
        original_file = "matches.json"

        # Check to see if file and path exists
        if os.path.isfile(original_directory+original_file):
            os.mkdir(original_directory+"temp/") 
            shutil.copy2(original_directory+original_file, original_directory+"temp/"+original_file)
            prev_existed = True
        else:
            prev_existed = False

        # If file doesn't exist, then return
        if not prev_existed:
            print("Sorry the 'matches.json' file doesn't exist!!!")
            return

        # Open the json file
        with open(original_directory+original_file, "r") as matches_file:
            matches_json = json.load(matches_file)
        matches_file.close()

        # Store the data in "matches.json"
        matches_json["matches"][self.computer_levels[self.selected_computer_difficulty].lower()][player_win_state].append({
            "total_time": round(self.player_total_time, 2),
            "avg_move_time": round(self.player_total_time / len(self.player_avg_move_time), 2),
            "score": self.score_player["P"],
            "starts_first": self.starts_first,
            "play_mode": self.play_mode,
            "date": [datetime.now().year, datetime.now().month, datetime.now().day]
        })

        # This will determine if writing to the file was successful
        written_to_file_successfully = False

        # Open the json file and write to it
        try:
            # Write to the file
            with open(original_directory+original_file, "w") as matches_file:
                json.dump(matches_json, matches_file)
            matches_file.close()

            # Set it to true, if writing to the file was successful
            written_to_file_successfully = True

        # If writing to the file was unsuccessful, then raise an error
        except: raise

        # If writing to the file was unsuccessful, then take this path
        finally:
            if not written_to_file_successfully and prev_existed:
                print("File could not be written to")
                shutil.copy2(original_directory+'temp/'+original_file, original_file)  

        # Remove directory and it's all content
        shutil.rmtree(original_directory+"temp/")   

    # check_line method
    def check_line(self, line):
        """
            The purpose of this function is to check if all the symbols in the line are the same and not empty
        """
        # Check if all elements in the line are equal and not empty
        return all(cell == line[0] and cell != ' ' for cell in line)

    # get_winning_line method
    def get_winning_line(self, board, board_size, symbols_to_win):
        """
            The purpose of this function is to get the coordinates of where the line starts and ends
        """
        # Check rows
        for row in range(board_size):
            for i in range(board_size - symbols_to_win + 1):
                if self.check_line(board[row][i:i + symbols_to_win]):
                    return ((row, i), (row, i + symbols_to_win - 1))

        # Check columns
        for col in range(board_size):
            for i in range(board_size - symbols_to_win + 1):
                if self.check_line([board[row][col] for row in range(i, i + symbols_to_win)]):
                    return ((i, col), (i + symbols_to_win - 1, col))

        # Check diagonals
        for i in range(board_size - symbols_to_win + 1):
            for j in range(board_size - symbols_to_win + 1):
                # Diagonal from top-left to bottom-right
                if self.check_line([board[i + k][j + k] for k in range(symbols_to_win)]):
                    return ((i, j), (i + symbols_to_win - 1, j + symbols_to_win - 1))

                # Diagonal from top-right to bottom-left
                if self.check_line([board[i + k][board_size - 1 - j - k] for k in range(symbols_to_win)]):
                    return ((i, board_size - 1 - j), (i + symbols_to_win - 1, board_size - 1 - j - symbols_to_win + 1))

        return None

    # bind_tic_tac_toe_win_line_container method
    def bind_tic_tac_toe_win_line_container(self, *args):
        """
            Bind the line to window, so it updates its pos according to the window
        """
        # Get the line to the 'mdn_screen_ids'
        tic_tac_toe_win_line_container = self.mdn_screen_ids["tic_tac_toe_win_line_container"]

        # Update the line when the pos and size of the widget or screen changes
        self.mdn_screen_ids["bg"].bind(pos = partial(self.update_tic_tac_toe_win_line, 0), size = partial(self.update_tic_tac_toe_win_line, 0))
        tic_tac_toe_win_line_container.bind(pos = partial(self.update_tic_tac_toe_win_line, 0), size = partial(self.update_tic_tac_toe_win_line, 0))
        self.mdn_app.mdn_screenmanager.bind(pos = partial(self.update_tic_tac_toe_win_line, 0), size = partial(self.update_tic_tac_toe_win_line, 0))

    # unfreeze_final_results_buttons method
    def unfreeze_final_results_buttons(self, *args):
        self.board_visible = False

    # reset_screen_variables method
    def reset_screen_variables(self):
        """
            The purpose of this function is to reset screen variables. 
        """
        # This will determine if the game is over or not. Game can ended as a "draw", "win", or "loss"
        self.game_over = False

        # This variable will record when the player's turn started and will hold that time
        self.player_turn_time_start = None

        # This variable will record the total amount of time for the player to move
        self.player_total_time = 0

        # This will record how many moves it took for the player to move and the times for each. Each time represents a move, because every time displays how long it took for the player to move. So the more times there are in this variable, that the player moved a lot
        self.player_avg_move_time = []

        # This is the board. This will be divided into columns and row of the board size. It will be an array
        # Copied by numpy it would look like this...
        # +-----------+
        # | X | O | O |
        # | O | X | O |
        # | X | X | X |
        # +-----------+
        # Default would look like this...
        # [
        #   ["X", "O", "O"]
        #   ["O", "X", "O"]
        #   ["X", "X", "X"]
        # ]
        self.board_positions = []

        # This variable will record how many cells are still left on the board
        self.board_available_cell_positions = []

        # This variable will determine if the board is visible or hidden
        self.board_visible = True

        # This variable will record the player's last move
        self.player_last_move = None

        # This variable will record who's turn it currently is
        self.current_turn = "P"

        # This variable will determine if the game is paused or not
        self.game_paused = False

        # This variable will determine what is the maximum ideal time for a player to move, before the points are greatly reduced
        self.stopwatch_ideal_move_time = 5

        # This will record the winning player
        self.winning_player = None

        # This will record and hold the score of both players: computer and the player
        self.score_player = {"C": 0, "P": 0}

        # This will display that the overlay is closed
        self.overlay_open = False

        # If the player presses view board, then set up a bind event, so when a player touches the window, the board will be hidden again
        Window.unbind(on_touch_down = self.hide_board, on_press = self.hide_board)

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
