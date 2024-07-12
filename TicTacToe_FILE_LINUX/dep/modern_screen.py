from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import CardTransition
from kivy.uix.screenmanager import SwapTransition
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import WipeTransition
from kivy.uix.screenmanager import FallOutTransition
from kivy.uix.screenmanager import RiseInTransition

# ---------------------------------------------------------------------- #
#                                                                        #
#                           Modern Screen Class                          #
#                                                                        #
# ---------------------------------------------------------------------- #
# +----------------------------------------------------------------------+ 
# | Description:                                                         |
# |      MDN_Screen aka(Modern Screen) is a new modernized screen class  |
# | with many different tools and feautres. This class will store the    |
# | app and the ids that belong to the class                             |
# |                                                                      |
# | Local Variables:                                                     |
# |     mdn_app:                                                         |
# |         type: <kivy_app>                                             |
# |         description: This is a reference of the app                  |
# |                                                                      |
# |     mdn_name:                                                        |
# |         type: 'str'                                                  |
# |         description: This is the name of screen for programming      |
# |                                                                      |
# |     mdn_title:                                                       |
# |         type: 'str'                                                  |
# |         description: This is the title of the window when displaying |
# |                      this current screen                             |
# |                                                                      |
# |     mdn_transition:                                                  |
# |         type: 'str'                                                  |
# |         description: The transition from one screen to another       |
# |                                                                      |
# |     mdn_screen_ids:                                                  |
# |         type: 'dict'                                                 |
# |         description: The stored collection of ids, that were created |
# |                      in python programming and not the kivy file     |
# |                                                                      |
# +----------------------------------------------------------------------+

class MDN_Screen(Screen):
    """
    Description:
        MDN_Screen aka(Modern Screen) is a new modernized screen class with many different tools and feautres. This class with store the app and the ids that belong to the class\n
    Local Variables:
        mdn_app, 
        mdn_name, 
        mdn_title, 
        mdn_transition,
        mdn_screen_ids
    """
    # init function
    def __init__(self, **kwargs):
        super().__init__()
        # Set the 'mdn_app' variable
        self.mdn_app = None

        # Set the 'mdn_name' variable
        self.mdn_name = "new_window"

        # Set the 'mdn_title' variable
        self.mdn_title = "My New Window"

        # Set the 'mdn_transition' variable
        self.mdn_transition = {"type": "SlideTransition", "direction": "left"}

        # Set the 'mdn_screen_ids' variable
        self.mdn_screen_ids = {}

        # Call update functions
        self._mdn_update_screen_params(kwargs)

    # _mdn_update_screen_params method
    def _mdn_update_screen_params(self, kwargs):
        """
            Mdn_Update_Screen_Params is a private method. The purpose of the method is to update the parameters of this class.
        """
        # # Get the arguments from the parameter *args
        # args = args[0]

        # Assign kwargs["mdn_app"] to the self.mdn_app
        if "mdn_app" in kwargs: self.mdn_app = kwargs["mdn_app"]

        # Assign kwargs["mdn_name"] to the self.mdn_name
        if "mdn_name" in kwargs: self.mdn_name = kwargs["mdn_name"]

        # Assign kwargs["mdn_title"] to the self.mdn_title
        if "mdn_title" in kwargs: self.mdn_title = kwargs["mdn_title"]

        # Assign kwargs["mdn_transition"] to the self.mdn_transition
        if "mdn_transition" in kwargs: self.mdn_transition = kwargs["mdn_transition"]

        # Assign kwargs["mdn_screen_ids"] to the self.mdn_screen_ids
        if "mdn_screen_ids" in kwargs: self.mdn_screen_ids = kwargs["mdn_screen_ids"]

        # Call the update method
        self._mdn_update_screen()

    # _mdn_update_screen method
    def _mdn_update_screen(self):
        """
           Mdn_Update_Screen is a private method. The purpose of this method is to update the screen and the graphic parameters.
        """
        # Set the name of this screen class
        self.name = self.mdn_name

        # Set the title of the app window
        self.mdn_app.title = self.mdn_title

    # mdn_switch method
    def mdn_switch(self, name_of_screen, title_of_screen, transition_direction = None, transition_type = None, *args):
        """
           Mdn_Switch is a public method. The purpose of this method is to switch to a different screen to another
        """
        # Set the app-window title with the new screen
        self.mdn_app.title = title_of_screen

        # Get the transittion for the screen. If 'transition_type' is set, then use that, otherwise use the default 'self.mdn_transition["type"]'
        use_transition_type = transition_type if transition_type else self.mdn_transition["type"]

        # Set the screenmanager transition
        if use_transition_type == "None": self.mdn_app.mdn_screenmanager.transition = NoTransition()
        if use_transition_type == "Slide": self.mdn_app.mdn_screenmanager.transition = SlideTransition()
        if use_transition_type == "Card": self.mdn_app.mdn_screenmanager.transition = CardTransition()
        if use_transition_type == "Swap": self.mdn_app.mdn_screenmanager.transition = SwapTransition()
        if use_transition_type == "Fade": self.mdn_app.mdn_screenmanager.transition = FadeTransition()
        if use_transition_type == "Wipe": self.mdn_app.mdn_screenmanager.transition = WipeTransition()
        if use_transition_type == "FallOut": self.mdn_app.mdn_screenmanager.transition = FallOutTransition()
        if use_transition_type == "RiseIn": self.mdn_app.mdn_screenmanager.transition = RiseInTransition()

        # Set the direction of the transition. This only works for following animations (Slide, Swap, Wipe)
        if use_transition_type in ("Slide", "Swap", "Wipe"):
            self.mdn_app.mdn_screenmanager.transition.direction = self.mdn_transition["direction"] if not transition_direction else transition_direction

        # Set the current screen to the screenmanager
        self.mdn_app.mdn_screenmanager.current = name_of_screen

    # mdn_remove_widget method
    def mdn_remove_widget(self, name):
        """
           Mdn_Remove_Widget is a public method. The purpose of this method is to remove the the widget from the screen and the id from the screen's 'mdn_screen_ids' variable.
        """
        # Remove the widget from the screen
        self.remove_widget(name)

        # If the screen id exists, then remove it from the 'mdn_screen_ids' list
        try: self.mdn_screen_ids.pop(name)
        except: print("{}: ID did not exist!".format(name))