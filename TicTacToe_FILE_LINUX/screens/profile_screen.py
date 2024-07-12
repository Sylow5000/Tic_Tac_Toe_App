import os
import cloudinary
import mysql.connector
import cloudinary.uploader
from functools import partial
from kivy.clock import Clock
from datetime import date, datetime, timedelta
from cloudinary.utils import cloudinary_url
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.filechooser import FileChooserIconView
from dep.modern_button import MDN_Button
from dep.modern_label import MDN_Label
from dep.modern_input import MDN_Input
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout
from kivy.graphics import Rectangle, Color, Line, BoxShadow

# =========== Profile Screen Class =========== #
class Profile_Screen_Class(MDN_Screen):
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

        # Init the screen
        Clock.schedule_once(self.init_ui, .1)
        Clock.schedule_once(self.update_ui, 1)

        # Hold the login info
        self.user_login = {
            "username": "",
            "password": ""
        }

        # Store the user data
        self.user_data = {}

        self.profile_has_been_changed = False

        self.profile_option_field = None



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

        # Connect to database
        self.get_user_data()

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
        padding_top = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "30un"])

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

        # Create the profile pic container
        profile_pic_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 2, mdn_size = ["100%", "300un"])
        profile_pic_rel_container = RelativeLayout(size_hint = (.4, 1))
        profile_pic = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_size = ["200un", "200un"],
            mdn_radius = [200],
            mdn_bg = {"image": [self.theme_dest+self.theme["default_player_profile"]["profile_pic"], "cover"]},
            mdn_outline = self.theme["default_player_profile"]["outline"]
        )
        self.mdn_screen_ids["profile_pic"] = profile_pic
        profile_pic.pos_hint = {"center_x": .6, "center_y": .5}
        profile_pic_rel_container.add_widget(profile_pic)

        profile_pic_label_rel_container = RelativeLayout(size_hint = (.6, 1))
        profile_pic_label = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["100%", "min_height"],
            mdn_text = "Change Profile\nPicture",
            mdn_font_size = self.theme["profile_pic_label"]["font_size"],
            mdn_font_style = self.theme["profile_pic_label"]["font_style"],
            mdn_font_color = self.theme["profile_pic_label"]["font_color"]
        )
        profile_pic_label.bind(on_press = self.update_profile_pic)
        profile_pic_label.mdn_line_height = 1.5
        profile_pic_label.pos_hint = {"center_x": .5, "center_y": .5}
        profile_pic_label_rel_container.add_widget(profile_pic_label)
        profile_pic_container.mdn_add_widget(profile_pic_rel_container)
        profile_pic_container.mdn_add_widget(profile_pic_label_rel_container)

        # Create padding
        padding_2 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "50un"])

        # Create the profile user fields container
        profile_user_fields_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "500un"])

        # Loop through and create a container, label, and input widget and add it to the 'profile_user_fields_container'
        for option in ["Firstname", "Lastname", "Username", "Password", "Email"]:
            # Create the container
            profile_option_field_rel_container = RelativeLayout()
            profile_option_field_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_size = ["100%", "100%"], mdn_cols = 2)

            # Create the button container and button
            profile_option_field_button_rel_container = RelativeLayout(size_hint = (.4, 1))
            profile_option_field_button = MDN_Label(
                mdn_app = self.mdn_app,
                mdn_text = option,
                mdn_font_size = self.theme["profile_option_field_button"]["font_size"],
                mdn_font_style = self.theme["profile_option_field_button"]["font_style"],
                mdn_font_color = self.theme["profile_option_field_button"]["font_color"]
            )
            profile_option_field_button.bind(on_press = partial(self.change_profile_option, option.lower()))
            profile_option_field_button.pos_hint = {"center_x": .5, "center_y": .5}

            # Create the input container and input
            profile_option_field_input_rel_container = RelativeLayout(size_hint = (.6, 1))
            self.mdn_screen_ids["profile_option_input_{}_rel_container".format(option.lower())] = profile_option_field_input_rel_container
            profile_option_field_input = MDN_Input(
                mdn_app = self.mdn_app,
                mdn_text = option,
                mdn_size = ["99%", "80un"],
                mdn_multiline = False,
                mdn_outline = self.theme["profile_option_field_input"]["outline"],
                mdn_text_align = {"halign": "center", "valign": "middle"},
                mdn_button_visible = False,
                mdn_use_focus_ui = False,
                mdn_use_hover_ui = False
            )
            self.mdn_screen_ids["profile_option_input_{}".format(option.lower())] = profile_option_field_input
            profile_option_field_input.pos_hint = {"center_x": .5, "center_y": .5}
            # Add all widgets together
            profile_option_field_button_rel_container.add_widget(profile_option_field_button)
            profile_option_field_input_rel_container.add_widget(profile_option_field_input)
            profile_option_field_container.mdn_add_widget(profile_option_field_button_rel_container)
            profile_option_field_container.mdn_add_widget(profile_option_field_input_rel_container)
            profile_option_field_rel_container.add_widget(profile_option_field_container)
            profile_user_fields_container.mdn_add_widget(profile_option_field_rel_container)

        # Create padding
        padding_3 = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100un"])

        # Create the profile user fields container
        profile_user_save_btn_container = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = ["100%", "100un"])
        profile_user_save_btn_rel_container = RelativeLayout()
        profile_user_save_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["80%", "100%"],
            mdn_font_size = self.theme["profile_user_save_btn"]["font_size"],
            mdn_font_style = self.theme["profile_user_save_btn"]["font_style"],
            mdn_font_color = self.theme["profile_user_save_btn"]["font_color"],
            mdn_radius = self.theme["profile_user_save_btn"]["radius"],
            mdn_outline = self.theme["profile_user_save_btn"]["outline"],
            mdn_text = "Update",
            mdn_bg = self.theme["profile_user_save_btn"]["bg"]
        )
        self.mdn_screen_ids["profile_user_save_btn_rel_container"] = profile_user_save_btn_rel_container
        profile_user_save_btn.bind(on_press = self.update_user_data)
        profile_user_save_btn.pos_hint = {"center_x": .5, "center_y": .5}
        profile_user_save_btn_rel_container.add_widget(profile_user_save_btn)
        profile_user_save_btn_container.mdn_add_widget(profile_user_save_btn_rel_container)


        # Add Widgets to screen
        scrollview_inner_container.mdn_add_widget(profile_pic_container)
        scrollview_inner_container.mdn_add_widget(padding_2)
        scrollview_inner_container.mdn_add_widget(profile_user_fields_container)
        scrollview_inner_container.mdn_add_widget(padding_3)
        scrollview_inner_container.mdn_add_widget(profile_user_save_btn_container)
        body_container.mdn_add_widget(padding_top)
        body_container.mdn_add_widget(scrollview_container_outer_container_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(body_rel_container)

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

        # Combine Widgets Together
        overlay_rel_container.add_widget(overlay_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(overlay_rel_container)
        self.mdn_screen_ids["bg"].mdn_add_widget(overlay_rel_container_2)


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

    # update_profile_pic method
    def update_profile_pic(self, *args):
        """
            The purpose of this function is to update the profile picture
        """
        # Create the overlay
        self.create_overlay_ui()

        # Get the float layout
        overlay_container = self.mdn_screen_ids["overlay_container"]

        # Create a rel container
        overlay_container_rel_container = RelativeLayout()

        # Create the inner container
        overlay_inner_container = MDN_GridLayout(
            mdn_app = self.mdn_app,
            mdn_cols = 1,
            mdn_size = ["80%", "60%"],
            mdn_bg = self.theme["filebrowser_container"]["bg"],
            mdn_radius = self.theme["filebrowser_container"]["radius"],
            mdn_outline = self.theme["filebrowser_container"]["outline"]
        )
        overlay_inner_container.pos_hint = {"center_x": .5, "center_y": .5}

        # Create the filechooser
        filechooser_rel_container = RelativeLayout()
        filechooser = FileChooserIconView(show_hidden = False, filters = ["*.png", "*.jpeg", "*.jpg", "*.svg"])
        self.mdn_screen_ids["filechooser"] = filechooser
        filechooser.pos_hint = {"center_x": .5, "center_y": .5}
        filechooser_rel_container.add_widget(filechooser)
        overlay_inner_container.mdn_add_widget(filechooser_rel_container)

        # 
        update_profile_pic_btn = MDN_Button(
            mdn_app = self.mdn_app,
            mdn_size = ["100%", "80un"],
            mdn_radius = self.theme["update_profile_pic_btn"]["radius"],
            mdn_text = "Update",
            mdn_font_style = self.theme["update_profile_pic_btn"]["font_style"],
            mdn_bg = self.theme["update_profile_pic_btn"]["bg"]
        )
        update_profile_pic_btn.bind(on_press = self.select_profile_pic)
        overlay_inner_container.mdn_add_widget(update_profile_pic_btn)

        # Combine widgets
        overlay_container_rel_container.add_widget(overlay_inner_container)
        overlay_container.add_widget(overlay_container_rel_container)

    # update_user_data method        
    def update_user_data(self, *args):
        """
            The purpose of this function is to update the user data once the button is pressed
        """
        return
        # Get all the data from the input fields
        input_texts = [
            self.mdn_screen_ids["profile_option_input_firstname"],
            self.mdn_screen_ids["profile_option_input_lastname"],
            self.mdn_screen_ids["profile_option_input_username"],
            self.mdn_screen_ids["profile_option_input_password"],
            self.mdn_screen_ids["profile_option_input_email"]
        ]

        # Get all the data from self.user_data. This will get the original data that was received from the database
        input_texts_og = [
            self.user_data["firstname"],
            self.user_data["lastname"],
            self.user_data["username"],
            self.user_data["password"],
            self.user_data["email"]
        ]

        # Check if any of the inputs are empty
        for input_text in input_texts:
            if not input_text.mdn_textinput_kv.text:return

        # If the date is less than 30 days than, return this function
        if self.user_data["change_user_profile_last_date"] >= date.today() - timedelta(days = 30): 
            print("The date too close")
            return

        #  Check if the inputs ever changed
        for i in range(0, len(input_texts)):

            # Check if the input is different from the original or the profile_pic has been changed
            if input_texts[i].mdn_textinput_kv.text != input_texts_og[i] or self.profile_has_been_changed:

                # Get the 'profile_user_save_btn_rel_container' from the 'self.mdn_screen_ids'
                profile_user_save_btn_rel_container = self.mdn_screen_ids["profile_user_save_btn_rel_container"]

                # Remove the btn from the screen
                profile_user_save_btn_rel_container.clear_widgets()

                # Create the success label
                profile_successfully_updated = MDN_Label(
                    mdn_app = self.mdn_app,
                    mdn_size = ["100%", "100%"],
                    mdn_font_size = self.theme["profile_successfully_updated"]["font_size"],
                    mdn_font_style = self.theme["profile_successfully_updated"]["font_style"],
                    mdn_font_color = self.theme["profile_successfully_updated"]["font_color"],
                    mdn_text = "Successfully Updated!",
                )   
                profile_successfully_updated.pos_hint = {"center_x": .5, "center_y": .5} 

                # Add widgets to the screen
                profile_user_save_btn_rel_container.add_widget(profile_successfully_updated) 

                # Connect To The Database
                try:
                    db = mysql.connector.connect(
                        host = "82.197.82.45",
                        user = "u465575972_TicTacToe_User",
                        password = "rHAoEgi1kfzRDB8O9WLe",
                        database = "u465575972_TicTacToe_DB"
                    )
                except:
                    print("Couldn't connect to the database")
                    return
                
                # Create the cursor for the database and execute SQL code to use the database
                cursor = db.cursor(dictionary = True)
                cursor.execute(f"USE u465575972_TicTacToe_DB")

                # If the profile_pic hasn't been changed then take this path
                if not self.profile_has_been_changed:

                    # Store the new changes to the tic tac toe database
                    cursor.execute(f"UPDATE Users SET firstname = %(firstname)s, lastname = %(lastname)s, username = %(username)s, password = %(password)s, email = %(email)s WHERE username = %(username)s", {"firstname": input_texts[0].mdn_textinput_kv.text, "lastname": input_texts[1].mdn_textinput_kv.text, "username": input_texts[2].mdn_textinput_kv.text, "password": input_texts[3].mdn_textinput_kv.text, "email": input_texts[4].mdn_textinput_kv.text})

                # If the profile has been changed, then take this path
                else:
                    # Connect To Cloudinary and sign in     
                    cloudinary.config( 
                        cloud_name = "ddertavi5", 
                        api_key = "612842136895311", 
                        api_secret = "HMXwsjLXSJrMPYbWKsXREZzJlk4",
                        secure = True
                    )

                    # Delete the current profile_pic from the server
                    cloudinary.uploader.destroy(
                        self.user_data["profile_pic"][self.user_data["profile_pic"].rindex('/')+1:self.user_data["profile_pic"].rindex('.')]
                    )

                    # Upload the new profile_pic to the server
                    upload_result = cloudinary.uploader.upload(self.mdn_screen_ids["filechooser"].selection[0])

                    # Store the new changes to the tic tac toe database
                    cursor.execute(f"UPDATE Users SET firstname = %(firstname)s, lastname = %(lastname)s, username = %(username)s, password = %(password)s, email = %(email)s, profile_pic = %(profile_pic)s WHERE username = %(username)s", {"firstname": input_texts[0].mdn_textinput_kv.text, "lastname": input_texts[1].mdn_textinput_kv.text, "username": input_texts[2].mdn_textinput_kv.text, "password": input_texts[3].mdn_textinput_kv.text, "email": input_texts[4].mdn_textinput_kv.text, "profile_pic": upload_result["secure_url"]})
                 
                # Store the new changes to the tic tac toe database in "User_Info" Table
                cursor.execute(f"UPDATE User_Info SET change_user_profile_last = %(current_date)s WHERE username = %(username)s", {"current_date": date.today(), "username": self.user_login["username"]})

                # Commit all the changes to the database
                db.commit()

                break

    # select_profile_pic method
    def select_profile_pic(self, *args):
        """
            The purpose of this function to select the image and set as the new profile picture
        """
        # If nothing is selected
        if not self.mdn_screen_ids["filechooser"].selection: return

        # Loop thru all the image extensions
        for img_ext in [".png", ".jpeg", ".jpg", ".svg"]:

            # Check if an image extension exists
            if img_ext in self.mdn_screen_ids["filechooser"].selection[0][-5:]:

                # Check if the file size isn't greater than 1mb
                if os.stat(self.mdn_screen_ids["filechooser"].selection[0]).st_size > 1000000: return

                # Change profile picture
                self.mdn_screen_ids["profile_pic"].mdn_update({"mdn_bg": {"image": [self.mdn_screen_ids["filechooser"].selection[0], "cover"]}})
                self.mdn_screen_ids["overlay_rel_container"].remove_widget(self.mdn_screen_ids["overlay_container"])
                self.profile_has_been_changed = True
                break


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

    # get_user_data method
    def get_user_data(self):
        """
            The purpose of this function is to get the user data from the database
        """
        return
        # Connect To The Database
        try:
            db = mysql.connector.connect(
                host = "82.197.82.45",
                user = "u465575972_TicTacToe_User",
                password = "rHAoEgi1kfzRDB8O9WLe",
                database = "u465575972_TicTacToe_DB"
            )
        except:
            print("Couldn't connect to the database")
            return
        
        # Load the user data
        cursor = db.cursor(dictionary = True)
        cursor.execute(f"USE u465575972_TicTacToe_DB")
        cursor.execute(f"SELECT * FROM Users;")
        db_rows = cursor.fetchall()

        # Loop thru the rows and find the column that matches
        user_found = False
        for row in db_rows:
            if row["username"] == self.user_login["username"] and row["password"] == self.user_login["password"]:
                user_found = True
                for column in ["firstname", "lastname", "username", "password", "email", "profile_pic"]: 
                    if column != "profile_pic":
                        self.mdn_screen_ids["profile_option_input_{}".format(column.lower())].mdn_update({"mdn_placeholder": row[column]})
                    self.user_data[column] = row[column]
                if row["profile_pic"]: self.mdn_screen_ids["profile_pic"].mdn_update({"mdn_bg": {"image": [str(row["profile_pic"]), "cover"]}})
                break

        # Get the change_user_profile_last
        cursor.execute(f"SELECT change_user_profile_last FROM User_Info WHERE username = %(username)s", {"username": self.user_login["username"]})
        change_user_profile_last = cursor.fetchall()

        # Close the connection
        try: db.close()
        except: print("Couldn't close connection")

        # Get from the 'change_user_profile_last'
        self.user_data["change_user_profile_last_date"] = change_user_profile_last[0]["change_user_profile_last"]
        
        # Could not load user info
        if not user_found:
            print("Couldn't load user info")
            return