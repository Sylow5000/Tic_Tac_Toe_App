import os
import json
import glob
from functools import partial
from kivy.clock import Clock
from kivy.uix.fitimage import FitImage
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_button import MDN_Button
from dep.modern_label import MDN_Label
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout

# =========== Stat Screen Class =========== #
class Stat_Screen_Class(MDN_Screen):
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
        Clock.schedule_once(self.init_ui, .1)
        Clock.schedule_once(self.update_ui, 1)

        # Set's type of stats to display
        self.type_stats_against_cpu = "casual"

        # Get the stats against the cpu
        self.stats_against_cpu = {
            "casual":{
                "easy": {"win": 30, "draw": 0, "loss": 3, "score": 100},
                "normal": {"win": 2, "draw": 0, "loss": 0, "score": 40},
                "hard": {"win": 0, "draw": 50, "loss": 10, "score": 5},
            },
            "pro":{
                "easy": {"win": 50, "draw": 59, "loss": 5, "score": 1006},
                "normal": {"win": 6, "draw": 1, "loss": 7, "score": 234},
                "hard": {"win": 10, "draw": 0, "loss": 0, "score": 106},                
            }
        }
        self.load_games()

        # Get the top 3 names of everyone on the leaderboard
        self.leaderboard_stats = {
            "1st": {"name": "Silas", "score": "1250pt"},
            "2nd": {"name": "Jeff", "score": "1005pt"},
            "3rd": {"name": "Billy", "score": "985pt"},
        }


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
        header_label = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100%", "80%"],
            mdn_bg = {"image": [self.theme_dest+self.theme["header_label"], "fit"]},
        )
        header_label.pos_hint = {"center_x": .5, "center_y": .55}
        header_label_rel_container.add_widget(header_label)
        
        # Create the tictactoe logo
        tictactoe_logo_rel_container = RelativeLayout(size_hint = (.25, 1))
        tictactoe_logo = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["100un", "50un"],
            mdn_bg = {"image": [self.theme_dest+self.theme["header_logo"], "fit"]},
        )
        tictactoe_logo.pos_hint = {"center_x": .5, "center_y": .55}
        tictactoe_logo_rel_container.add_widget(tictactoe_logo)

        # Combine widgets
        header_container.mdn_add_widget(bck_btn_rel_container)
        header_container.mdn_add_widget(header_label_rel_container)
        header_container.mdn_add_widget(tictactoe_logo_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(header_container)

    # create_body_ui method
    def create_body_ui(self):
        """
            The purpose of this function is to create the body ui.
        """
        # Create a container
        body_rel_container = RelativeLayout()
        body_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]})
        body_container.pos_hint = {"center_x": .5}
        body_rel_container.add_widget(body_container)

        # Create padding
        padding_top = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "50un"])

        # Create scrollview
        scrollview_container_outer_container_rel_container = RelativeLayout()
        scrollview_container_outer_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100%"])
        scrollview_container = ScrollView(size_hint = (None, None), effect_cls = ScrollEffect)
        self.mdn_screen_ids["scrollview_container"] = scrollview_container
        scrollview_container.bind(pos = self.update_scrollview_size, size = self.update_scrollview_size)
        scrollview_container_outer_container.mdn_add_widget(scrollview_container)
        scrollview_container_outer_container_rel_container.add_widget(scrollview_container_outer_container)

        # Create the inner container that will have the parent as the 'scrollview'
        scrollview_inner_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
        scrollview_container.add_widget(scrollview_inner_container)
        self.mdn_screen_ids["scrollview_inner_container"] = scrollview_inner_container  

        # Create the 'stat_container'
        stat_container = self.create_body_ui_stats_vs_cpu()

        # Create padding between containers
        item_padding_1 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "50un"])

        # Create the 'leaderboard_container'
        leaderboard_container = self.create_body_ui_leaderboard()

        # Create padding between containers
        item_padding_2 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "50un"])

        # # Create the 'view_container'
        # view_container = self.create_body_ui_view_game()

        # Add Widgets to screen
        scrollview_inner_container.mdn_add_widget(stat_container) 
        scrollview_inner_container.mdn_add_widget(item_padding_1) 
        scrollview_inner_container.mdn_add_widget(leaderboard_container) 
        scrollview_inner_container.mdn_add_widget(item_padding_2) 
        # scrollview_inner_container.mdn_add_widget(view_container) 
        body_container.mdn_add_widget(padding_top)
        body_container.mdn_add_widget(scrollview_container_outer_container_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(body_rel_container)

        # Initialize stats
        self.display_type_cpu_stats(self.type_stats_against_cpu, "default")

    # create_body_ui_stats_vs_cpu method
    def create_body_ui_stats_vs_cpu(self):
        """
            The purpose of this function is to create the stats and the container that will display the results as a table
        """
        # Create the container that will hold the stats against the CPU
        stat_container = MDN_GridLayout(
           mdn_app = self.mdn_app,
           mdn_size = ["100%", "600un"],
        ) 

        # Create the stat header 
        stat_container_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Stats Against CPU",
            mdn_size = ["100%", "min_height"],
            mdn_font_size = self.theme["stat_container"]["title"]["font_size"],
            mdn_font_style = self.theme["stat_container"]["title"]["font_style"],
            mdn_font_color = self.theme["stat_container"]["title"]["font_color"]
        )

        # Create the margin between the header and stat container
        title_container_gap = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "20un"])

        # Create the actual stat CPU container
        actual_stat_CPU_container_rel_container = RelativeLayout()
        actual_stat_CPU_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_rows = 6,
            mdn_size = ["99%", "99%"],
            mdn_outline = self.theme["stat_container"]["container"]["outline"],
            mdn_bg = self.theme["stat_container"]["container"]["bg"]
        )
        actual_stat_CPU_container.pos_hint = {"center_x": .5, "center_y": .5}
        actual_stat_CPU_container_rel_container.add_widget(actual_stat_CPU_container)

        # Create the header row
        header_row = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 2,
            mdn_size = ["100%", "90un"],
        )

        # Create the casual btn for the header row
        casual_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Casual",
            mdn_size = ["50%", "100%"],
            mdn_bg = self.theme["stat_container"]["btn"]["normal"]["bg"],
            mdn_font_size = self.theme["stat_container"]["btn"]["normal"]["font_size"],
            mdn_font_style = self.theme["stat_container"]["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["stat_container"]["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["casual_btn"] = casual_btn
        casual_btn.bind(on_release = partial(self.display_type_cpu_stats, "casual"))

        # Create the pro btn for the header row
        pro_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Pro",
            mdn_size = ["50%", "100%"],
            mdn_bg = self.theme["stat_container"]["btn"]["normal"]["bg"],
            mdn_font_size = self.theme["stat_container"]["btn"]["normal"]["font_size"],
            mdn_font_style = self.theme["stat_container"]["btn"]["normal"]["font_style"],
            mdn_font_color = self.theme["stat_container"]["btn"]["normal"]["font_color"]
        )
        self.mdn_screen_ids["pro_btn"] = pro_btn
        pro_btn.bind(on_release = partial(self.display_type_cpu_stats, "pro"))
        header_row.mdn_add_widget(casual_btn)
        header_row.mdn_add_widget(pro_btn)

        # Create first row
        first_row_rel_container = RelativeLayout()
        first_row = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 5, mdn_size = ["100%", "100%"])
        first_row_rel_container.add_widget(first_row)
        for col in ["", "Win", "Draw", "Loss", "Score"]:
            first_row_column = MDN_Label(
                mdn_app = self.mdn_app,
                mdn_text = col,
                mdn_size = ["20%", "100%"],
                mdn_font_size = self.theme["stat_container"]["text"]["font_size"],
                mdn_font_style = self.theme["stat_container"]["text"]["font_style"],
                mdn_font_color = self.theme["stat_container"]["text"]["font_color"],
            )
            first_row.mdn_add_widget(first_row_column)
        

        # Combine widgets to 'actual_stat_CPU_container'
        actual_stat_CPU_container.mdn_add_widget(header_row)
        actual_stat_CPU_container.mdn_add_widget(first_row_rel_container)

        # Loop thru and create rows
        for i in range(0, 3):
            # Store the cpu level
            cpu_level = (("Easy" if i == 0 else "Normal") if i != 2 else "Hard")

            # Create a row
            row_rel_container = RelativeLayout()
            row = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 5, mdn_size = ["100%", "100%"])
            row_rel_container.add_widget(row)

            # Loop thru
            for col in ["", "win", "draw", "loss", "score"]:
                col_label = MDN_Label(
                    mdn_app = self.mdn_app,
                    mdn_size = ["20%", "100%"],
                    mdn_text = cpu_level if col == "" else str(self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()][col]) + ("pt" if col == "score" else ""),
                    mdn_font_size = self.theme["stat_container"]["text"]["font_size"],
                    mdn_font_style = self.theme["stat_container"]["text"]["font_style"],
                    mdn_font_color = self.theme["stat_container"]["text"]["font_color"],
                    mdn_line_height = self.theme["stat_container"]["text"]["line_height"]
                )
                self.mdn_screen_ids["{}_{}".format(cpu_level.lower(), col)] = col_label
                row.mdn_add_widget(col_label)
            actual_stat_CPU_container.mdn_add_widget(row_rel_container)

        # Create the footer row
        footer_row = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "90un"])
        divide_line = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_size = ["100%", self.theme["stat_container"]["divider"]["height"]],
            mdn_bg = self.theme["stat_container"]["divider"]["color"]
        )
        total_results_rel_container = RelativeLayout()
        total_results_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "100%"])
        total_results_container.pos_hint = {"center_x": .5, "center_y": .5}
        total_results_rel_container.add_widget(total_results_container)
        total_results_total_score = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_size = ["50%", "100%"],
            mdn_text = "Total Score: ",
            mdn_font_size = self.theme["stat_container"]["text"]["font_size"],
            mdn_font_style = self.theme["stat_container"]["text"]["font_style"],
            mdn_font_color = self.theme["stat_container"]["text"]["font_color"],
            mdn_line_height = self.theme["stat_container"]["text"]["line_height"]
        )
        self.mdn_screen_ids["total_results_total_score"] = total_results_total_score
        total_results_win_rate = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_size = ["50%", "100%"],
            mdn_text = "Win Rate: 50%",
            mdn_font_size = self.theme["stat_container"]["text"]["font_size"],
            mdn_font_style = self.theme["stat_container"]["text"]["font_style"],
            mdn_font_color = self.theme["stat_container"]["text"]["font_color"],
            mdn_line_height = self.theme["stat_container"]["text"]["line_height"]
        )
        self.mdn_screen_ids["total_results_win_rate"] = total_results_win_rate
        total_results_container.mdn_add_widget(total_results_total_score)
        total_results_container.mdn_add_widget(total_results_win_rate)
        footer_row.mdn_add_widget(divide_line)
        footer_row.mdn_add_widget(total_results_rel_container)

        # Combine widgets
        actual_stat_CPU_container.mdn_add_widget(footer_row)
        stat_container.mdn_add_widget(stat_container_label)
        stat_container.mdn_add_widget(title_container_gap)
        stat_container.mdn_add_widget(actual_stat_CPU_container_rel_container)

        return stat_container

    # create_body_ui_leaderboard method
    def create_body_ui_leaderboard(self):
        """
            The purpose of this function is to create the leaderboard that will display the results as a table
        """
       # Create the container that will hold the stats against the CPU
        leaderboard_container = MDN_GridLayout(
           mdn_app = self.mdn_app,
           mdn_size = ["100%", "350un"],
        )

        # Create the leaderboard header 
        leaderboard_container_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Leaderboard",
            mdn_size = ["100%", "min_height"],
            mdn_font_size = self.theme["ldr_brd"]["title"]["font_size"],
            mdn_font_style = self.theme["ldr_brd"]["title"]["font_style"],
            mdn_font_color = self.theme["ldr_brd"]["title"]["font_color"]
        )

        # Create the margin between the header and stat container
        title_container_gap = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "20un"])

        # Create the actual leaderboard CPU container
        actual_leaderboard_container_rel_container = RelativeLayout()
        actual_leaderboard_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_rows = 4,
            mdn_size = ["99%", "99%"],
            mdn_bg = self.theme["ldr_brd"]["container"]["bg"],
            mdn_outline = self.theme["ldr_brd"]["container"]["outline"]
        )
        actual_leaderboard_container.pos_hint = {"center_x": .5, "center_y": .5}
        actual_leaderboard_container_rel_container.add_widget(actual_leaderboard_container)

        # Create the header row
        leaderboard_header_row = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 3,
            mdn_size = ["100%", "80un"],
            mdn_bg = self.theme["ldr_brd"]["header"]["bg"]
        )

        # Create the first column
        ldr_brd_col_1_rel_layout = RelativeLayout()

        # Create the second column and container
        ldr_brd_col_2_rel_layout = RelativeLayout()
        ldr_brd_col_2 = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Player",
            mdn_font_size = self.theme["ldr_brd"]["header"]["font_size"],
            mdn_font_color = self.theme["ldr_brd"]["header"]["font_color"],
            mdn_font_style = self.theme["ldr_brd"]["header"]["font_style"]
        )
        ldr_brd_col_2.pos_hint = {"center_x": .5, "center_y": .5}
        ldr_brd_col_2_rel_layout.add_widget(ldr_brd_col_2)

        # Create the third column and container
        ldr_brd_col_3_rel_layout = RelativeLayout()
        ldr_brd_col_3 = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "Score",
            mdn_font_size = self.theme["ldr_brd"]["header"]["font_size"],
            mdn_font_color = self.theme["ldr_brd"]["header"]["font_color"],
            mdn_font_style = self.theme["ldr_brd"]["header"]["font_style"]
        )
        ldr_brd_col_3.pos_hint = {"center_x": .5, "center_y": .5}
        ldr_brd_col_3_rel_layout.add_widget(ldr_brd_col_3)

        # Add columns to the header row
        leaderboard_header_row.mdn_add_widget(ldr_brd_col_1_rel_layout)
        leaderboard_header_row.mdn_add_widget(ldr_brd_col_2_rel_layout)
        leaderboard_header_row.mdn_add_widget(ldr_brd_col_3_rel_layout)

        # Create the body element
        leaderboard_body_container_rel_container = RelativeLayout()
        leaderboard_body_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1)
        leaderboard_body_container.pos_hint = {"center_x": .5, "center_y": .5}
        leaderboard_body_container_rel_container.add_widget(leaderboard_body_container)

        # Loop thru and create 3 rows
        for i in range(0, 3):
            ldr_brd_body_row_rel_container = RelativeLayout()
            ldr_brd_body_row = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 3)
            ldr_brd_body_row_rel_container.add_widget(ldr_brd_body_row)
            ldr_brd_pos = ("2nd" if i == 1 else "3rd") if i != 0 else "1st"
            ldr_brd_body_row_pos_label = MDN_Label(
                mdn_app = self.mdn_app, 
                mdn_size = ["33%", "100%"], 
                mdn_text = ldr_brd_pos,
                mdn_font_size = self.theme["ldr_brd"]["text"]["font_size"],
                mdn_font_color = self.theme["ldr_brd"]["text"]["font_color"],
                mdn_font_style = self.theme["ldr_brd"]["text"]["font_style"]
            )
            ldr_brd_body_row_name_label = MDN_Label(
                mdn_app = self.mdn_app, 
                mdn_size = ["33%", "100%"], 
                mdn_text = self.leaderboard_stats[ldr_brd_pos]["name"],
                mdn_font_size = self.theme["ldr_brd"]["text"]["font_size"],
                mdn_font_color = self.theme["ldr_brd"]["text"]["font_color"],
                mdn_font_style = self.theme["ldr_brd"]["text"]["font_style"]
            )
            ldr_brd_body_row_score_label = MDN_Label(
                mdn_app = self.mdn_app, 
                mdn_size = ["33%", "100%"], 
                mdn_text = self.leaderboard_stats[ldr_brd_pos]["score"],
                mdn_font_size = self.theme["ldr_brd"]["text"]["font_size"],
                mdn_font_color = self.theme["ldr_brd"]["text"]["font_color"],
                mdn_font_style = self.theme["ldr_brd"]["text"]["font_style"]
            )
            ldr_brd_body_row.mdn_add_widget(ldr_brd_body_row_pos_label)
            ldr_brd_body_row.mdn_add_widget(ldr_brd_body_row_name_label)
            ldr_brd_body_row.mdn_add_widget(ldr_brd_body_row_score_label)
            leaderboard_body_container.mdn_add_widget(ldr_brd_body_row_rel_container)

        # Combine Widgets
        actual_leaderboard_container.mdn_add_widget(leaderboard_header_row)
        actual_leaderboard_container.mdn_add_widget(leaderboard_body_container_rel_container)
        leaderboard_container.mdn_add_widget(leaderboard_container_label)
        leaderboard_container.mdn_add_widget(title_container_gap)
        leaderboard_container.mdn_add_widget(actual_leaderboard_container_rel_container)

        return leaderboard_container

    # create_body_ui_view_game method
    def create_body_ui_view_game(self):
        """
            The purpose of this function is to create the view buttons
        """
        # Create the container that will hold the stats against the CPU
        view_container = MDN_GridLayout(
           mdn_app = self.mdn_app,
           mdn_size = ["100%", "200un"],
        )

        # Create the view header 
        view_container_label = MDN_Label(
            mdn_app = self.mdn_app,
            mdn_text = "View",
            mdn_font_size = 30,
            mdn_font_style = ["bold", "underline"],
            mdn_font_color = [0, 0, 0, 1],
            mdn_size = ["100%", "min_height"]
        )

        # Create the margin between the header and view container
        title_container_gap = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "10un"])

        # Create the actual view CPU container
        actual_view_container_rel_container = RelativeLayout()
        actual_view_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 3,
            mdn_size = ["99%", "99%"],
        )
        actual_view_container.pos_hint = {"center_x": .5, "center_y": .5}
        actual_view_container_rel_container.add_widget(actual_view_container)

        # Create the 'saved_matches' btn
        saved_matches_btn_rel_container = RelativeLayout()
        saved_matches_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Saved Matches",
            mdn_font_color = [255, 255, 255, 1],
            mdn_bg = {"color": [149, 138, 246, 1]},
            mdn_outline = [[149, 92, 247, 1], 2],
            mdn_size = ["85%", "110un"],
            mdn_radius = [10]
        )
        saved_matches_btn.pos_hint = {"center_x": .5, "center_y": .5}
        saved_matches_btn_rel_container.add_widget(saved_matches_btn)

        # Create the 'all_matches' btn
        all_matches_btn_rel_container = RelativeLayout()
        all_matches_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "All Matches",
            mdn_font_color = [255, 255, 255, 1],
            mdn_bg = {"color": [149, 138, 246, 1]},
            mdn_outline = [[149, 92, 247, 1], 2],
            mdn_size = ["85%", "110un"],
            mdn_radius = [10]
        )
        all_matches_btn.pos_hint = {"center_x": .5, "center_y": .5}
        all_matches_btn_rel_container.add_widget(all_matches_btn)

        # Create the 'local_matches' btn
        local_matches_btn_rel_container = RelativeLayout()
        local_matches_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_text = "Local Matches",
            mdn_font_color = [255, 255, 255, 1],
            mdn_bg = {"color": [149, 138, 246, 1]},
            mdn_outline = [[149, 92, 247, 1], 2],
            mdn_size = ["85%", "110un"],
            mdn_radius = [10]
        )
        local_matches_btn.pos_hint = {"center_x": .5, "center_y": .5}
        local_matches_btn_rel_container.add_widget(local_matches_btn)

        # Combine widgets
        actual_view_container.mdn_add_widget(saved_matches_btn_rel_container)
        actual_view_container.mdn_add_widget(all_matches_btn_rel_container)
        actual_view_container.mdn_add_widget(local_matches_btn_rel_container)
        view_container.mdn_add_widget(view_container_label)
        view_container.mdn_add_widget(title_container_gap)
        view_container.mdn_add_widget(actual_view_container_rel_container)

        return view_container


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

        if self.mdn_app.mdn_screenmanager.current_screen.name != "stat_screen":
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
        scrollview_container = self.mdn_screen_ids["scrollview_container"]

        # Update the size & pos of the 'scrollview_container'
        scrollview_container.size = scrollview_container.parent.size
        scrollview_container.pos = scrollview_container.parent.pos

        # Calculate the height for the 'scrollview_container'
        scrollview_inner_container_height = 0
        for child in self.mdn_screen_ids["scrollview_inner_container"].children:scrollview_inner_container_height+=child.height

        # Update size for 'self.mdn_screen_ids["scrollview_inner_container"]'
        self.mdn_screen_ids["scrollview_inner_container"].mdn_update({"mdn_size": ["100%", "{}un".format(int(scrollview_inner_container_height))]})

        Clock.schedule_once(self.update_scrollview_size)



    # +----------------------------------------+
    # |                                        |
    # |              Button Events             |
    # |                                        |
    # +----------------------------------------+
    # display_type_cpu_stats method
    def display_type_cpu_stats(self, type_of_stats, *args):
        """
            The purpose of this function is to display the cpu type of results (It can be either: casual or pro)
        """
        # If 'self.type_stats_against_cpu' is the same 'type_of_stats', that means it currently being displayed, which means it doesn't need to be displayed again
        if self.type_stats_against_cpu == type_of_stats and ("default" not in args): return

        if "default" in args:
            prev_type_of_stats = "pro" if type_of_stats == "casual" else "casual"
            self.type_stats_against_cpu = prev_type_of_stats

        # This will hold the total score
        total_score = 0

        # This will record the total amount of games
        total_game = 0

        # This will record the total amount of win
        total_win = 0

        # Dehighlight the current button
        self.mdn_screen_ids["{}_btn".format(self.type_stats_against_cpu)].mdn_update({
            "mdn_font_color": self.theme["stat_container"]["btn"]["normal"]["font_color"],
            "mdn_font_style": self.theme["stat_container"]["btn"]["normal"]["font_style"],
            "mdn_bg": self.theme["stat_container"]["btn"]["normal"]["bg"]
        })

        # Set the 'self.type_stats_against_cpu' to the 'type_of_stats', which can be either: casual or pro
        self.type_stats_against_cpu = type_of_stats

        # Highlight the current button
        self.mdn_screen_ids["{}_btn".format(self.type_stats_against_cpu)].mdn_update({
            "mdn_font_color": self.theme["stat_container"]["btn"]["hover"]["font_color"],
            "mdn_font_style": self.theme["stat_container"]["btn"]["hover"]["font_style"],
            "mdn_bg": self.theme["stat_container"]["btn"]["hover"]["bg"]
        })

        # Re-display the stats again
        for i in range(0, 3):
            # Store the cpu level
            cpu_level = (("Easy" if i == 0 else "Normal") if i != 2 else "Hard")

            # Change the text for the wins
            self.mdn_screen_ids["{}_win".format(cpu_level.lower())].mdn_update({
                "mdn_text": str(self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["win"])
            })

            # Change the text for the draws
            self.mdn_screen_ids["{}_draw".format(cpu_level.lower())].mdn_update({
                "mdn_text": str(self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["draw"])
            })

            # Change the text for the loss
            self.mdn_screen_ids["{}_loss".format(cpu_level.lower())].mdn_update({
                "mdn_text": str(self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["loss"])
            })

            # Change the text for the score
            self.mdn_screen_ids["{}_score".format(cpu_level.lower())].mdn_update({
                "mdn_text": str(self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["score"])
            })

            # Add to the total scroe
            total_score+=self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["score"]

            # Add to the total game
            total_game+=self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["win"]+\
                self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["draw"]+\
                self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["loss"]

            # Add to the total win
            total_win+=self.stats_against_cpu[self.type_stats_against_cpu][cpu_level.lower()]["win"]

        # Display total score
        self.mdn_screen_ids["total_results_total_score"].mdn_update({"mdn_text": "Total Score: {}".format(total_score)})

        # Display average win rate
        if total_game != 0:
            self.mdn_screen_ids["total_results_win_rate"].mdn_update({"mdn_text": "Win Rate: {}%".format(round((total_win / total_game) * 100), 2)})
        else:
            self.mdn_screen_ids["total_results_win_rate"].mdn_update({"mdn_text": "Win Rate: 0%"})

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

    # load_games method
    def load_games(self):
        """
            The purpose of this function is to load all the matches
        """
        if not os.path.isfile("game_data/matches.json"):
            # Load the theme from matches.json
            with open("game_data/matches.json", "w") as json_file:
                json_code = {
                    "matches": {
                        "easy": {"win": [], "draw": [], "loss": []},
                        "normal": {"win": [], "draw": [], "loss": []},
                        "hard": {"win": [], "draw": [], "loss": []}
                    }
                }
                json_object = json.dumps(json_code, indent=4)
                json_file.write(json_object)
            json_file.close()

        # Load the theme from matches.json
        with open("game_data/matches.json", "r") as json_file:
            json_code = json.load(json_file)
        json_file.close()

        # Create a variable that will hold the stats
        self.stats_against_cpu = {
            "pro": {
                "easy": {"win": 0, "draw": 0, "loss": 0, "score": 0},
                "normal": {"win": 0, "draw": 0, "loss": 0, "score": 0},
                "hard": {"win": 0, "draw": 0, "loss": 0, "score": 0}
            },
            "casual": {
                "easy": {"win": 0, "draw": 0, "loss": 0, "score": 0},
                "normal": {"win": 0, "draw": 0, "loss": 0, "score": 0},
                "hard": {"win": 0, "draw": 0, "loss": 0, "score": 0}
            }
        }
        print(json_code)
        # Loop thru all the stats
        for cpu_difficulty in list(json_code["matches"].keys()):
            
            for match_result in ["win", "draw", "loss"]:

                for game in json_code["matches"][cpu_difficulty][match_result]:

                    self.stats_against_cpu[game["play_mode"]][cpu_difficulty][match_result]+=1
                    self.stats_against_cpu[game["play_mode"]][cpu_difficulty]["score"]+=game["score"]
            


