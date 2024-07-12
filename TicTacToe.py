print("Weird?")

# Import Libraries
import os
import json
import random
import requests
from subprocess import call
from dep.modern_app import MDN_App
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import Home_Screen_Class
from screens.stat_screen import Stat_Screen_Class
from screens.profile_screen import Profile_Screen_Class
from screens.settings_screen import Settings_Screen_Class
from screens.how_to_play_screen import How_To_Play_Screen_Class
from screens.multiplayer_options import Multiplayer_Options_Class
from screens.multiplayer_game import Multiplayer_Game_Screen_Class
from screens.single_player_options import Single_Player_Options_Class
from screens.single_player_game import Single_Player_Game_Screen_Class

# +----------------------------------------------------------+
# |                                                          |
# |                     Create Functions                     |
# |                                                          |
# +----------------------------------------------------------+
# get_the_current_version function
def load_the_current_version():
    """
        The purpose of this function is to get the current version of the app. If the app doesn't have a current version, then create the first version otherwise get the version from the TecKnowfy website.
    """
    # Check the 'current_update.json' file exists
    if not os.path.exists("./current_update.json"):

        # Create the object to fill 'current_update.json' file
        current_update_object = {
            "add_files": [],
            "remove_files": [],
            "replace_files": [],
            "version": 0.9,
            "version_name": "Tic_Tac_Toe_Alpha_0.9"
        }

        # Convert the 'current_update_object' to json code
        current_update_object_json = json.dumps(current_update_object)

        # Create the 'current_update.json' file and write to it
        with open("./current_update.json", "w") as current_update_file:
            current_update_file.write(current_update_object_json)
        current_update_file.close()

    # This var will determine if an update.py exists in the 'downloaded_update.json'
    update_file_exists = False

    # Download the update.json file from the TecKnowfy.com website
    response = requests.get("https://tecknowfy.com/Tic_Tac_Toe_Game/app_files/update.json", {"downloadformat": "json"})

    # Create/Replace a new file called "update.json"
    with open("downloaded_update.json", mode = "wb") as update_json_file: update_json_file.write(response.content)

    # Get the content from the downloaded 'downloaded_update.json' file
    with open("downloaded_update.json") as download_update_file:
        download_update_json = json.load(download_update_file)
    download_update_file.close()

    # Load the content from the 'current_update.json' file
    with open("current_update.json") as current_update_file:
        current_update_json = json.load(current_update_file)
    current_update_file.close()

    # Load the files into different variablse
    add_files = download_update_json["add_files"]
    remove_files = download_update_json["remove_files"]
    replace_files = download_update_json["replace_files"]
    downloaded_version = download_update_json["version"]
    current_version = current_update_json["version"]

    # If the 'current_version' is the same as the 'downloaded_version' then exit this function
    if downloaded_version == current_version: 
        os.remove("downloaded_update.json")
        return False

    # Add files to the app
    for file in add_files:
        # Download the hosted file
        response = requests.get(file["hosted_filepath"]+file["filename"])

        # If the download was successful, then create the file
        if response.status_code == 200:
            with open(file["filepath"]+file["filename"], mode = "wb") as adding_file:
                adding_file.write(response.content)
            adding_file.close()
            
        # If 'file["filename"]' is 'update.py, then after looping and deleting,adding,replacing files then run the 'update.py'
        if file["filename"] == 'update.py': update_file_exists = True

    # Remove files from the app
    for file in remove_files:
        try:
            # If the 'file' is not a directory, then remove the file
            if not os.path.isdir(file): os.remove(file)
            # If the 'file' is a directory, then remove the directory
            else:os.rmdir(file)
        except: pass

    # Replace file in the app
    for file in replace_files:
        # Download the hosted file
        response = requests.get(file["hosted_filepath"]+file["filename"])

        # If the download was successful, then rewrite the file
        if response.status_code == 200:
            with open(file["filepath"]+file["filename"], mode = "w") as replace_file:
                replace_file.write(response.content)
            replace_file.close()

    # If 'update_file_exists' is True, then run the 'update.py' file
    if update_file_exists: call(["python", "update.py"])
    
    # Remove the current version of the 'current_update.json' file
    os.remove("current_update.json")

    # Create a new 'current_update.json' file and fill it with the downloaded content
    with open("current_update.json", "w") as current_update_file:
        download_update_object_json = json.dumps(download_update_json)
        current_update_file.write(download_update_object_json)
    current_update_file.close()

    # Remove the current version of the 'current_update.json' file
    os.remove("downloaded_update.json")

    return downloaded_version

# load_cache_data function
def load_cache_data():
    """
        The purpose of this function is to load cached data if it is possible, otherwise don't load anything
    """
    # If cache data doesn't exist, then exit this function
    if not os.path.exists("./cache.json"): return False
        
    # Load the current theme from the stored cache
    with open("cache.json", "r") as json_file:
        json_code = json.load(json_file)
    json_file.close()

    return json_code

# +----------------------------------------------------------+
# |                                                          |
# |                 Initialize the Variables                 |
# |                                                          |
# +----------------------------------------------------------+
# Get the current version or download the current version of this app
current_version = load_the_current_version()

# If cached data exists, then take this path
cache_data = load_cache_data()

# If no cache_data exists, then load default theme
if not cache_data:
    with open("themes/default/theme.json") as theme_json_file:
        theme_code = json.load(theme_json_file)
    theme_json_file.close()


# +----------------------------------------------------------+
# |                                                          |
# |              Create the Class of the Screens             |
# |                                                          |
# +----------------------------------------------------------+
# ============= Home_Screen Class ============= #
class Home_Screen(Home_Screen_Class):
    pass

# =============== Single_Player_Options Class ============== #
class Single_Player_Options(Single_Player_Options_Class):
    def change_screen(self, *args):
        # If the player chose random 'play_as', then choose randomly between 'x' or 'o'
        if self.play_as == "x_o": 
            self.play_as = random.choice(("x", "o"))
            self.computer_play_as = "x" if self.play_as == "o" else "o"

        # Transfer all the variables and data from 'Single_Player_Options_Ins' class to the 'Single_Player_Game_Screen_Ins' class
        Single_Player_Game_Screen_Ins.selected_computer_difficulty = self.computer_difficulty
        Single_Player_Game_Screen_Ins.computer_levels = self.computer_levels
        Single_Player_Game_Screen_Ins.computer_play_as = self.computer_play_as
        Single_Player_Game_Screen_Ins.player_play_as = self.play_as
        Single_Player_Game_Screen_Ins.starts_first = self.starts_first
        Single_Player_Game_Screen_Ins.play_mode = self.play_mode
        Single_Player_Game_Screen_Ins.board_size = self.board_size
        Single_Player_Game_Screen_Ins.win_length = self.win_length
        Single_Player_Game_Screen_Ins.selected_move_timer = self.move_timer
        Single_Player_Game_Screen_Ins.timers_for_moves = self.timers_for_moves
        Single_Player_Game_Screen_Ins.init_ui()
        return super().change_screen(*args)

# ============= Single_Player_Game_Screen Class ============= #
class Single_Player_Game_Screen(Single_Player_Game_Screen_Class):
    pass

# =============== Multiplayer_Options Class ============== #
class Multiplayer_Options(Multiplayer_Options_Class):
    def change_screen(self, *args):
        # If the player chose random 'play_as', then choose randomly between 'x' or 'o'
        if self.play_as == "x_o": 
            self.play_as = random.choice(("x", "o"))
            self.computer_play_as = "x" if self.play_as == "o" else "o"

        # Transfer all the variables and data from 'Single_Player_Options_Ins' class to the 'Single_Player_Game_Screen_Ins' class
        Multiplayer_Game_Screen_Ins.selected_computer_difficulty = self.computer_difficulty
        Multiplayer_Game_Screen_Ins.computer_levels = self.computer_levels
        Multiplayer_Game_Screen_Ins.computer_play_as = self.computer_play_as
        Multiplayer_Game_Screen_Ins.player_play_as = self.play_as
        Multiplayer_Game_Screen_Ins.starts_first = self.starts_first
        Multiplayer_Game_Screen_Ins.play_mode = self.play_mode
        Multiplayer_Game_Screen_Ins.board_size = self.board_size
        Multiplayer_Game_Screen_Ins.win_length = self.win_length
        Multiplayer_Game_Screen_Ins.selected_move_timer = self.move_timer
        Multiplayer_Game_Screen_Ins.timers_for_moves = self.timers_for_moves
        Multiplayer_Game_Screen_Ins.init_ui()
        return super().change_screen(*args)

# =============== Multiplayer_Game_Screen Class ============== #
class Multiplayer_Game_Screen(Multiplayer_Game_Screen_Class):
    def change_screen(self, *args):
        # If the player chose random 'play_as', then choose randomly between 'x' or 'o'
        if self.play_as == "x_o": 
            self.play_as = random.choice(("x", "o"))
            self.computer_play_as = "x" if self.play_as == "o" else "o"

        # Transfer all the variables and data from 'Single_Player_Options_Ins' class to the 'Single_Player_Game_Screen_Ins' class
        Multiplayer_Game_Screen_Ins.selected_computer_difficulty = self.computer_difficulty
        Multiplayer_Game_Screen_Ins.computer_levels = self.computer_levels
        Multiplayer_Game_Screen_Ins.computer_play_as = self.computer_play_as
        Multiplayer_Game_Screen_Ins.player_play_as = self.play_as
        Multiplayer_Game_Screen_Ins.starts_first = self.starts_first
        Multiplayer_Game_Screen_Ins.play_mode = self.play_mode
        Multiplayer_Game_Screen_Ins.board_size = self.board_size
        Multiplayer_Game_Screen_Ins.win_length = self.win_length
        Multiplayer_Game_Screen_Ins.selected_move_timer = self.move_timer
        Multiplayer_Game_Screen_Ins.timers_for_moves = self.timers_for_moves
        Multiplayer_Game_Screen_Ins.init_ui()
        return super().change_screen(*args)

# ============= How_To_Play_Screen Class ============= #
class How_To_Play_Screen(How_To_Play_Screen_Class):
    pass

# ============= Stat_Screen_Class Class ============= #
class Stat_Screen(Stat_Screen_Class):
    pass

# ============= Profile_Screen_Class Class ============= #
class Profile_Screen(Profile_Screen_Class):
    pass

# ============= Settings_Screen_Class Class ============= #
class Settings_Screen(Settings_Screen_Class):
    pass

# ========== Screenmanager_Widget Class ========== #
class Screenmanager_Widget(ScreenManager):
    pass

# ================ Main_App Class ================ #
class Main_App(MDN_App):
    def build(self): return Screen_Manager_Ins


# +----------------------------------------------------------+
# |                                                          |
# |              Create Instance of the Screens              |
# |                                                          |
# +----------------------------------------------------------+
# Init 'Screen_Manager_Ins' variable
Screen_Manager_Ins = Screenmanager_Widget()

# Init 'Main_App_Ins' variable
Main_App_Ins = Main_App(
    mdn_app_name = "The_New_App",
    mdn_screenmanager = Screen_Manager_Ins,
    mdn_window_resizable = True,
    mdn_min_window_size = (300, 300),
    mdn_max_window_size = (1000, 1000),
    mdn_device_breakpoints = {"desktop": [3000], "tablet": [726, 2999], "mobile": [0, 725]},
    mdn_window_size = (400, 700),
    mdn_window_pos = "center",
    mdn_app_icon = "py_includes/icon.png",
    mdn_allow_screensaver = False,
    mdn_default_font_size = {"desktop": 30, "tablet": 30, "mobile": 30}
)

# Init 'Home_Screen_Ins' variable
Home_Screen_Ins = Home_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "home_screen", 
    mdn_title = "Home Screen", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["home"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Single_Player_Options_Ins' variable
Single_Player_Options_Ins = Single_Player_Options(
    mdn_app = Main_App_Ins, 
    mdn_name = "single_player_options_screen", 
    mdn_title = "Home", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["single_player_options"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Single_Player_Game_Screen_Ins' variable
Single_Player_Game_Screen_Ins = Single_Player_Game_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "single_player_game_screen", 
    mdn_title = "Home", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["single_player_game"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Multiplayer_Options_Ins' variable
Multiplayer_Options_Ins = Multiplayer_Options(
    mdn_app = Main_App_Ins, 
    mdn_name = "multiplayer_options_screen", 
    mdn_title = "Home", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["multiplayer_options"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Multiplayer_Game_Screen_Ins' variable
Multiplayer_Game_Screen_Ins = Multiplayer_Game_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "multiplayer_game_screen", 
    mdn_title = "Home", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["multiplayer_game"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Multiplayer_Options_Ins' variable
Multiplayer_Options_Ins = Multiplayer_Options(
    mdn_app = Main_App_Ins, 
    mdn_name = "multiplayer_options_screen", 
    mdn_title = "Home", 
    mdn_transition = {"type": "Slide", "direction": "left"},
    theme = theme_code["theme"]["screen_info"]["multiplayer_options"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Settings_Screen_Ins' variable
Settings_Screen_Ins = Settings_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "settings_screen", 
    mdn_title = "Settings", 
    mdn_transition = {"type": "RiseIn", "direction": "none"},
    theme = theme_code["theme"]["screen_info"]["settings"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Stat_Screen_Ins' variable
Stat_Screen_Ins = Stat_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "stat_screen", 
    mdn_title = "Stats & Analytics", 
    mdn_transition = {"type": "RiseIn", "direction": "none"},
    theme = theme_code["theme"]["screen_info"]["stat"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'How_To_Play_Screen_Ins' variable
How_To_Play_Screen_Ins = How_To_Play_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "how_to_play_screen", 
    mdn_title = "How To Play", 
    mdn_transition = {"type": "RiseIn", "direction": "none"},
    theme = theme_code["theme"]["screen_info"]["how_to_play"],
    general_theme = theme_code["theme"]["general_info"]
)

# Init 'Profile_Screen_Ins' variable
Profile_Screen_Ins = Profile_Screen(
    mdn_app = Main_App_Ins, 
    mdn_name = "profile_screen", 
    mdn_title = "Profile", 
    mdn_transition = {"type": "RiseIn", "direction": "none"},
    theme = theme_code["theme"]["screen_info"]["profile"],
    general_theme = theme_code["theme"]["general_info"]
)

# +----------------------------------------------------------+
# |                                                          |
# |            Add Screens to the Screen_Manager             |
# |                                                          |
# +----------------------------------------------------------+
Screen_Manager_Ins.add_widget(Home_Screen_Ins)
Screen_Manager_Ins.add_widget(Single_Player_Options_Ins)
Screen_Manager_Ins.add_widget(Single_Player_Game_Screen_Ins)
Screen_Manager_Ins.add_widget(Multiplayer_Options_Ins)
Screen_Manager_Ins.add_widget(Multiplayer_Game_Screen_Ins)
Screen_Manager_Ins.add_widget(Settings_Screen_Ins)
Screen_Manager_Ins.add_widget(Stat_Screen_Ins)
Screen_Manager_Ins.add_widget(How_To_Play_Screen_Ins)
Screen_Manager_Ins.add_widget(Profile_Screen_Ins)

# ============= Set Default Screen ============== #
Screen_Manager_Ins.current = Home_Screen_Ins.mdn_name
Main_App_Ins.title = Home_Screen_Ins.mdn_title

# # ================= Run The App ================= #
print(__name__)
if __name__ == "__main__": 
    Main_App_Ins.run()