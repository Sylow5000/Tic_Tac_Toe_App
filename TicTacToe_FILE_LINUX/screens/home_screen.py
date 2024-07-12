from kivy.clock import Clock
from kivy.uix.fitimage import FitImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.effects.scroll import ScrollEffect
from kivy.uix.relativelayout import RelativeLayout
from dep.modern_button import MDN_Button
from dep.modern_screen import MDN_Screen
from dep.modern_gridlayout import MDN_GridLayout
from dep.modern_relativelayout import MDN_RelativeLayout

# =========== Home Screen Class =========== #
class Home_Screen_Class(MDN_Screen):
   # +----------------------------------------+
   # |                                        |
   # |               Init Class               |
   # |                                        |
   # +----------------------------------------+
   # init function
   def __init__(self, **kwargs):
      # Load all the theme from kwargs
      self.load_theme(kwargs)

      # Start the app
      super().__init__(**kwargs)
      Clock.schedule_once(self.init_ui, .1)
      Clock.schedule_once(self.update_ui, 1)

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
      bg = MDN_GridLayout(
         mdn_app = self.mdn_app,
         mdn_cols = 1,
         mdn_bg = {"image": [self.theme_dest+self.theme["bg"], "stretch"]}
      )
      self.mdn_screen_ids["bg"] = bg
      self.add_widget(bg)

      # Call helper functions
      self.create_header_ui()
      self.create_body_ui()

   # create_header_ui method
   def create_header_ui(self):
      """
         The purpose of this function is to initialize the header ui. This includes the big image on the Home screen.
      """
      # Create the front image
      front_img_rel_layout = RelativeLayout(size_hint = (1, .4))
      front_img = FitImage(source = self.theme_dest+self.theme["header"])
      front_img.pos_hint = {"center_x": .5, "center_y": .5}
      front_img_rel_layout.add_widget(front_img)
      self.mdn_screen_ids["bg"].mdn_add_widget(front_img_rel_layout)

   # create_body_ui method
   def create_body_ui(self):
      """
         The purpose of this function is to initialize the header ui. This includes the number of players that are online and the buttons
      """
      # +-------------------------------------------+
      # Create the button navigation container
      # +-------------------------------------------+
      btn_nav_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "58%"])
      btn_nav = MDN_GridLayout(mdn_app = self.mdn_app, mdn_cols = 1, mdn_size = {"desktop": ["700un", "100%"], "tablet": ["700un", "100%"], "mobile": ["90%", "100%"]})
      btn_nav.pos_hint = {"center_x": .5, "center_y": .5}
      self.mdn_screen_ids["btn_nav"] = btn_nav
      btn_nav_rel_layout.add_widget(btn_nav)
      self.mdn_screen_ids["bg"].mdn_add_widget(btn_nav_rel_layout)

      # Create scrollview
      btn_nav_scrollview_container_outer_container = GridLayout(cols = 1)
      btn_nav_scrollview_container = ScrollView(size_hint = (None, None), effect_cls = ScrollEffect)
      self.mdn_screen_ids["btn_nav_scrollview_container"] = btn_nav_scrollview_container
      btn_nav_scrollview_container.bind(pos = self.update_scrollview_size, size = self.update_scrollview_size)
      btn_nav_scrollview_container_outer_container.add_widget(btn_nav_scrollview_container)

      # Create the inner container that will have the parent as the 'scrollview'
      btn_nav_scrollview_inner_container = MDN_GridLayout(mdn_app = self.mdn_app,mdn_cols = 1,mdn_size = ["100%", "100%"])
      btn_nav_scrollview_container.add_widget(btn_nav_scrollview_inner_container)
      self.mdn_screen_ids["btn_nav_scrollview_inner_container"] = btn_nav_scrollview_inner_container

      # +----------------------------------------------------+
      # Create the option for the single player button 
      # +----------------------------------------------------+
      single_player_btn_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "150un"])
      single_player_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["100%", "110un"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_font_size = self.theme["btn"]["normal"]["font_size"],
         mdn_font_style = self.theme["btn"]["normal"]["font_style"],
         mdn_font_color = self.theme["btn"]["normal"]["font_color"],
         mdn_text = "Single Player"
      )
      single_player_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_font_size": {"hover": self.theme["btn"]["hover"]["font_size"], "use_hover_ui": True},
         "mdn_font_style": {"hover": self.theme["btn"]["hover"]["font_style"], "use_hover_ui": True},
         "mdn_font_color": {"hover": self.theme["btn"]["normal"]["font_color"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True}
      })
      single_player_btn.pos_hint = {"center_x": .5, "center_y": .5}
      single_player_btn.bind(on_press = self.single_player_btn_pressed)
      single_player_btn_rel_layout.add_widget(single_player_btn)

      # +----------------------------------------------------+
      # Create the option for the multiplayer button 
      # +----------------------------------------------------+
      multiplayer_btn_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "150un"])
      multiplayer_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["100%", "110un"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_font_size = self.theme["btn"]["normal"]["font_size"],
         mdn_font_style = self.theme["btn"]["normal"]["font_style"],
         mdn_font_color = self.theme["btn"]["normal"]["font_color"],
         mdn_text = "Multiplayer",
      )
      multiplayer_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_font_size": {"hover": self.theme["btn"]["hover"]["font_size"], "use_hover_ui": True},
         "mdn_font_style": {"hover": self.theme["btn"]["hover"]["font_style"], "use_hover_ui": True},
         "mdn_font_color": {"hover": self.theme["btn"]["normal"]["font_color"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True}
      })
      multiplayer_btn.bind(on_press = self.multiplayer_btn_pressed)
      multiplayer_btn.pos_hint = {"center_x": .5, "center_y": .5}
      multiplayer_btn_rel_layout.add_widget(multiplayer_btn)

      # +----------------------------------------------------+
      # Create the option for the online button 
      # +----------------------------------------------------+
      online_btn_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "150un"])
      online_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["100%", "110un"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["online_btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_font_size = self.theme["btn"]["normal"]["font_size"],
         mdn_font_style = self.theme["btn"]["normal"]["font_style"],
         mdn_font_color = self.theme["btn"]["normal"]["font_color"],
         mdn_text = "Online"
      )
      online_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["online_btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_font_size": {"hover": self.theme["btn"]["hover"]["font_size"], "use_hover_ui": True},
         "mdn_font_style": {"hover": self.theme["btn"]["hover"]["font_style"], "use_hover_ui": True},
         "mdn_font_color": {"hover": self.theme["btn"]["normal"]["font_color"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True}
      })
      online_btn.pos_hint = {"center_x": .5, "center_y": .5}
      online_btn_rel_layout.add_widget(online_btn)

      # +----------------------------------------------------+
      # Create the option for the settings button 
      # +----------------------------------------------------+
      settings_btn_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "150un"])
      settings_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["100%", "110un"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_font_size = self.theme["btn"]["normal"]["font_size"],
         mdn_font_style = self.theme["btn"]["normal"]["font_style"],
         mdn_font_color = self.theme["btn"]["normal"]["font_color"],
         mdn_text = "Settings"
      )
      settings_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_font_size": {"hover": self.theme["btn"]["hover"]["font_size"], "use_hover_ui": True},
         "mdn_font_style": {"hover": self.theme["btn"]["hover"]["font_style"], "use_hover_ui": True},
         "mdn_font_color": {"hover": self.theme["btn"]["normal"]["font_color"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True}
      })
      settings_btn.bind(on_press = self.settings_btn_pressed)
      settings_btn.pos_hint = {"center_x": .5, "center_y": .5}
      settings_btn_rel_layout.add_widget(settings_btn)


      # +----------------------------------------------------+
      # Create the option for the advanced options container
      # +----------------------------------------------------+
      advanced_options_rel_layout = MDN_RelativeLayout(mdn_size = ["100%", "200un"])
      advanced_options_layout = MDN_GridLayout(
         mdn_app = self.mdn_app, 
         mdn_cols = 3, 
         mdn_size = ["100%", "150un"], 
      )
      advanced_options_layout.pos_hint = {"center_x": .5, "center_y": .55}
      advanced_options_rel_layout.add_widget(advanced_options_layout)


      # +----------------------------------------------------+
      # Create the option for the stats button 
      # +----------------------------------------------------+
      stats_btn_rel_layout = RelativeLayout()
      stats_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["95%", "100%"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_icon = self.theme_dest+self.theme["stat_btn"]["normal"]["icon"],
         mdn_icon_size = self.theme["stat_btn"]["normal"]["icon_size"],
      )
      stats_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True},
         "mdn_icon": {"hover": self.theme_dest+self.theme["stat_btn"]["hover"]["icon"], "use_hover_ui": True},
         "mdn_icon_size": {"hover": self.theme["stat_btn"]["hover"]["icon_size"]}
      })
      stats_btn.bind(on_release = self.stat_btn_pressed)
      stats_btn.pos_hint = {"center_x": .5, "center_y": .5}
      stats_btn_rel_layout.add_widget(stats_btn)


      # +----------------------------------------------------+
      # Create the option for the how_to_play button 
      # +----------------------------------------------------+
      how_to_play_btn_rel_layout = RelativeLayout()
      how_to_play_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["95%", "100%"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_font_size = self.theme["btn"]["normal"]["font_size"],
         mdn_font_style = self.theme["btn"]["normal"]["font_style"],
         mdn_font_color = self.theme["btn"]["normal"]["font_color"],
         mdn_text = "How To\nPlay"
      )
      how_to_play_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_font_size": {"hover": self.theme["btn"]["hover"]["font_size"], "use_hover_ui": True},
         "mdn_font_style": {"hover": self.theme["btn"]["hover"]["font_style"], "use_hover_ui": True},
         "mdn_font_color": {"hover": self.theme["btn"]["normal"]["font_color"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True}
      })
      how_to_play_btn.bind(on_release = self.how_to_play_btn_pressed)
      how_to_play_btn.pos_hint = {"center_x": .5, "center_y": .5}
      how_to_play_btn_rel_layout.add_widget(how_to_play_btn)

      # +----------------------------------------------------+
      # Create the option for the profile button 
      # +----------------------------------------------------+
      profile_btn_rel_layout = RelativeLayout()
      profile_btn = MDN_Button(
         mdn_app = self.mdn_app,
         mdn_use_hover_ui = False,
         mdn_size = ["95%", "100%"],
         mdn_radius = self.theme["btn"]["normal"]["radius"],
         mdn_bg = {"image": [self.theme_dest+self.theme["btn"]["normal"]["bg"], "cover"]},
         mdn_outline = self.theme["btn"]["normal"]["outline"],
         mdn_shadow = self.theme["btn"]["normal"]["shadow"],
         mdn_icon = self.theme_dest+self.theme["profile_btn"]["normal"]["icon"],
         mdn_icon_size = self.theme["profile_btn"]["normal"]["icon_size"],
      )
      profile_btn.mdn_update({
         "mdn_radius": {"hover": self.theme["btn"]["hover"]["radius"], "use_hover_ui": True},
         "mdn_bg": {"image": {"hover": [self.theme_dest+self.theme["btn"]["hover"]["bg"], "cover"], "use_hover_ui": True}},
         "mdn_outline": {"hover": self.theme["btn"]["hover"]["outline"], "use_hover_ui": True},
         "mdn_shadow": {"hover": self.theme["btn"]["hover"]["shadow"], "use_hover_ui": True},
         "mdn_icon": {"hover": self.theme_dest+self.theme["profile_btn"]["hover"]["icon"], "use_hover_ui": True},
         "mdn_icon_size": {"hover": self.theme["profile_btn"]["hover"]["icon_size"]}
      })
      profile_btn.bind(on_release = self.profile_btn_pressed)
      profile_btn.pos_hint = {"center_x": .5, "center_y": .5}
      profile_btn_rel_layout.add_widget(profile_btn)


      advanced_options_layout.mdn_add_widget(stats_btn_rel_layout)
      advanced_options_layout.mdn_add_widget(how_to_play_btn_rel_layout)
      advanced_options_layout.mdn_add_widget(profile_btn_rel_layout)

      btn_nav_scrollview_inner_container.mdn_add_widget(single_player_btn_rel_layout)
      btn_nav_scrollview_inner_container.mdn_add_widget(multiplayer_btn_rel_layout)
      btn_nav_scrollview_inner_container.mdn_add_widget(online_btn_rel_layout)
      btn_nav_scrollview_inner_container.mdn_add_widget(settings_btn_rel_layout)
      btn_nav_scrollview_inner_container.mdn_add_widget(advanced_options_rel_layout)
      btn_nav.mdn_add_widget(btn_nav_scrollview_container_outer_container)


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
      self.mdn_screen_ids["btn_nav"]._mdn_update_graphic()

   # upate_scrollview method
   def update_scrollview_size(self, *args):
      """
         The purpose of this function is to update the scrollview's size
      """
      # Get the scrollview
      btn_nav_scrollview_container = self.mdn_screen_ids["btn_nav_scrollview_container"]

      # Update the size & pos of the 'btn_nav_scrollview_container'
      btn_nav_scrollview_container.size = btn_nav_scrollview_container.parent.size
      btn_nav_scrollview_container.pos = btn_nav_scrollview_container.parent.pos

      # Calculate the height for the 'btn_nav_scrollview_container'
      btn_nav_scrollview_inner_container_height = 0
      for child in self.mdn_screen_ids["btn_nav_scrollview_inner_container"].children:btn_nav_scrollview_inner_container_height+=child.height

      # Update size for 'self.mdn_screen_ids["btn_nav_scrollview_inner_container"]'
      self.mdn_screen_ids["btn_nav_scrollview_inner_container"].mdn_update({"mdn_size": ["100%", "{}un".format(int(btn_nav_scrollview_inner_container_height))]})


   # +----------------------------------------+
   # |                                        |
   # |              Button Events             |
   # |                                        |
   # +----------------------------------------+
   # single_player_btn_pressed method
   def single_player_btn_pressed(self, *args):
      """
         Single_Player_Btn_Pressed purpose is to switch the screen to the 'single_player_options_screen' screen
      """
      self.mdn_switch("single_player_options_screen", "Single Player Options")

   # single_player_btn_pressed method
   def multiplayer_btn_pressed(self, *args):
      """
         Multiplayer_Btn_Pressed purpose is to switch the screen to the 'multiplayer_options' screen
      """
      self.mdn_switch("multiplayer_options_screen", "Multiplayer Options")

   # settings_btn_pressed method
   def settings_btn_pressed(self, *args):
      """
         Settings_Btn_Pressed purpose is to switch the screen to the 'settings_screen' screen
      """
      self.mdn_switch("settings_screen", "Settings")

   # stat_btn_pressed method
   def stat_btn_pressed(self, *args):
      """
         Stat_Btn_Pressed purpose is to switch the screen to the 'stat_screen' screen
      """
      self.mdn_switch("stat_screen", "Stats & Analytics", "None", "FallOut")

   # how_to_play_btn_pressed method
   def how_to_play_btn_pressed(self, *args):
      """
         How_To_Play_Btn_Pressed purpose is to switch the screen to the 'how_to_play_options_screen' screen
      """
      self.mdn_switch("how_to_play_screen", "How To Play", "None", "FallOut")

   # profile_btn_pressed method
   def profile_btn_pressed(self, *args):
      """
         Profile_Btn_Pressed purpose is to switch the screen to the 'profile_screen' screen
      """
      self.mdn_switch("profile_screen", "Profile", "None", "FallOut")


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
