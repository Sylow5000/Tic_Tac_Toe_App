from functools import partial
import random, string
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout

# ---------------------------------------------------------------------- #
#                                                                        #
#                        Modern RelativeLayout Class                     #
#                                                                        #
# ---------------------------------------------------------------------- #
# +----------------------------------------------------------------------+ 
# | Description:                                                         |
# |     MDN_RelativeLayout aka(Modern RelativeLayout) is a new modernized|
# | relative layout class that will be responsive. It will change size   |
# | on window event.                                                     |
# |                                                                      |
# | Local Variables:                                                     |
# |     mdn_size:                                                        |
# |         type: 'list'                                                 |
# |         description: This holds the params for size                  |
# |         eg. ["50%", "200un"]                                         |
# |                                                                      |
# +----------------------------------------------------------------------+

class MDN_RelativeLayout(RelativeLayout):
    """
    Description:
        MDN_RelativeLayout aka(Modern RelativeLayout) is a new modernized relative layout class that will be responsive. It will change size on window event.\n   
    """
    # init function
    def __init__(self, **kwargs):
        super().__init__()
        # ========= DEFAULT PARAMETERS ========= #
        # Set the 'size_hint' parameter
        self.size_hint = (None, None)

        # ========= GRAPHIC PARAMETERS ========= #
        # Set the "mdn_size" variable...
        self.mdn_size = ["100%", "100%"]

        # ========= UPDATE THE GRAPHICS ========= #
        self._get_parent()
        self.mdn_update(kwargs)
        self.bind(pos = partial(self._mdn_update_relativelayout_graphic_size, 0), size = partial(self._mdn_update_relativelayout_graphic_size, 0))

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
        # ========== PARAMETERS ========== #
        if "mdn_size" in kwargs: self._mdn_update_param("mdn_size", kwargs["mdn_size"])
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
        if arg_name == "mdn_size": mdn_update_variable_ref = self.mdn_size

        # If 'mdn_update_variable_ref' == None, then return function
        if mdn_update_variable_ref == None: return

        # If 'arg_name' is not 'mdn_bg' then take this path
        self.mdn_size = arg_value

    # _mdn_update_graphic method
    def _mdn_update_graphic(self, *args):
        """
            Mdn_Update_Graphic is a private function. The purpose of this function is to call all the subfunctions that are able to update the relative layout graphics or ui\n
        """
        # If parent does not exists, return and run again .05sec later
        if not self.parent: 
            Clock.schedule_once(self._mdn_update_graphic, .05)
            return
        
        # Call all the subfunctions needed to change the graphic/ui
        self._mdn_update_relativelayout_graphic_size(0)

    # _mdn_update_relativelayout_graphic_size method
    def _mdn_update_relativelayout_graphic_size(self, *args):
        """
            Mdn_Update_RelativeLayout_Size is a private function. The purpose of this function is to update the graphic/ui size of the relativelayout
        """
        i = args[0]
        # 'mdn_size_ref' will be a reference variable of the real variable for the current device size
        mdn_size_ref = self.mdn_size

        # Update the width
        try:
            if 'un' in mdn_size_ref[0]: self.width = int(mdn_size_ref[0][:mdn_size_ref[0].index("un")])
            else: self.width = self.parent.width*(int(mdn_size_ref[0][:mdn_size_ref[0].index("%")])/100)
        except:
            print("MDN_Relative_Layout Error: Could not update widget width!")

        # Update the height
        try:
            if 'un' in mdn_size_ref[1]: self.height = int(mdn_size_ref[1][:mdn_size_ref[1].index("un")])
            else: self.height = self.parent.height*(int(mdn_size_ref[1][:mdn_size_ref[1].index("%")])/100)
        except:
            print("MDN_Relative_Layout Error: Could not update widget height!")

        if i < 5:
            Clock.schedule_once(partial(self._mdn_update_relativelayout_graphic_size, i+1), 1)

    # _get_parent method
    def _get_parent(self, *args):
        """
            Get_Parent is a private method. The purpose of this function is to get the parent. This is in order so that if the parent updates, the widget will also update
        """
        if not self.parent:
            Clock.schedule_once(self._get_parent, 1)
            return

        self.parent.bind(pos = partial(self._mdn_update_relativelayout_graphic_size, 0), size = partial(self._mdn_update_relativelayout_graphic_size, 0))