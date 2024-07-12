from functools import partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.graphics import Color, Line
from kivy.uix.floatlayout import FloatLayout

# ===== Win_Line_Anim_Module Class ===== #
class Win_Line_Anim_Module(FloatLayout):

    # init method
    def __init__(self, **kwargs):
        super(Win_Line_Anim_Module, self).__init__()
        self.initial_start_point = kwargs["initial_start_point"]
        self.starting_point = kwargs["starting_point"]
        self.ending_point = kwargs["ending_point"]
        self.line_color = kwargs["line_color"]
        self.duration = kwargs["duration"]
        self.mdn_app = kwargs["mdn_app"]
        with self.canvas.after: 
            Color(self.line_color[0]/255, self.line_color[1]/255, self.line_color[2]/255, self.line_color[3])
            self.line = Line(points = [*self.initial_start_point, *self.initial_start_point], width = 5)

    # animate_line method
    def animate_line(self):
        # Create an Animation to change the points of the line
        anim = Animation(
            points = [self.starting_point[0], self.starting_point[1], self.ending_point[0], self.ending_point[1]], 
            duration = self.duration
        )
        
        # Start the animation for the line
        anim.start(self.line)

        # Bind the line to window, so it updates its pos according to the window
        Clock.schedule_once(self.bind_tic_tac_toe_win_line_container, self.duration)

    # bind_tic_tac_toe_win_line_container method
    def bind_tic_tac_toe_win_line_container(self, *args):
        """
            Bind the line to window, so it updates its pos according to the window
        """
        # Bind the line to the Screenmanager resize or change in pos event  
        self.bind(pos = partial(self.update_tic_tac_toe_win_line, 0), size = partial(self.update_tic_tac_toe_win_line, 0))
        self.mdn_app.mdn_screenmanager.bind(pos = partial(self.update_tic_tac_toe_win_line, 0), size = partial(self.update_tic_tac_toe_win_line, 0))

    # update_tic_tac_toe_win_line method
    def update_tic_tac_toe_win_line(self, *args):
        """
            This function is responsible for updating and changing the pos and size of the line
        """
        # Clear the current line from the screen
        self.canvas.after.clear()

        # Create a new line
        with self.canvas.after: 
            Color(self.line_color[0]/255, self.line_color[1]/255, self.line_color[2]/255, self.line_color[3])
            self.line = Line(points = [*self.starting_point, *self.ending_point], width = 5)