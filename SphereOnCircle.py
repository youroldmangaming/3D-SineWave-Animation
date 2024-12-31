from manimlib import *
from manim import MathTex

class SphereOnCircle(Scene):
    def construct(self):

        self.camera.frame.set_euler_angles(
            phi=-15 * DEGREES,  # Tilt downward by 10 degrees (90 - 10 = 80)
            theta=-5 * DEGREES  # Rotate slightly to the left
        )

        # Create a circle with radius 1
        circle = Circle(radius=1, color=WHITE)

        # Create a small red sphere (using Dot for better visibility)
        sphere = Dot(color=RED, radius=0.1).move_to(circle.point_from_proportion(0))

        # Function to update the yellow line's position dynamically
        def get_yellow_line():
            return Line(ORIGIN, sphere.get_center(), color=YELLOW)

        # Function to update the blue line's position dynamically
        def get_blue_line():
            # Get the sphere's position
            sphere_pos = sphere.get_center()
            # Calculate the endpoint of the blue line (same x-coordinate, y=0)
            endpoint = np.array([sphere_pos[0], 0, 0])
            # Return the blue line
            return Line(sphere_pos, endpoint, color=BLUE)

        # Function to update the length text dynamically
        def get_length_text():
            # Calculate the length of the blue line (absolute value of the y-coordinate)
            length = abs(sphere.get_center()[1])
            # Create a text label to display the length
            return Text(f"Length: {length:.2f}", font_size=24).to_edge(DOWN)

        # Function to update the Dot's position dynamically
        def get_moving_dot():
            # Get the length of the blue line (y-coordinate of the sphere)
            y_pos = sphere.get_center()[1]
            # Return a Dot at (0, y_pos, 0)
            return Dot(color=GREEN).move_to(np.array([0, y_pos, 0]))

        # Use always_redraw to ensure the lines, text, and Dot update their positions during animation
        yellow_line = always_redraw(get_yellow_line)
        blue_line = always_redraw(get_blue_line)
        length_text = always_redraw(get_length_text)
        moving_dot = always_redraw(get_moving_dot)

        # Add the circle, the sphere, the lines, the length text, and the moving Dot to the scene
        self.add(circle, sphere, yellow_line, blue_line, length_text, moving_dot)

        # Create 3D axes
        axes = ThreeDAxes()

        # Add the axes to the scene
        self.add(axes)

        # Create labels for the axes using Text
        x_label = Text("X").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y").next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z").next_to(axes.z_axis.get_end(), OUT)

        # Add labels to the scene
        self.add(x_label, y_label, z_label)

        # Store the lengths of the blue line at 0.15-second intervals
        lines_per_cycle = 40
        interval_time = 0.15  # Time interval in seconds
        total_time = lines_per_cycle * interval_time  # Total time for one full cycle
        interval_count = int(total_time / interval_time)  # Number of intervals
        lengths = []  # Store the lengths
        x_values = []  # Store the x-axis positions for plotting
        lines = []  # Store the plotted blue lines
        connecting_lines = []  # Store the lines connecting the tops of the blue lines

        # Animate the sphere moving around the circle using MoveAlongPath
        i = -1

        #while True:
        for _ in range(3*lines_per_cycle): #needed for video on commented out otherwise, usig the while infinite loop
            i += 1
            if i > lines_per_cycle-1:
                i = 0

            # Calculate the proportion of the circle completed
            proportion = i / lines_per_cycle

            # Calculate the length of the blue line (absolute value of the y-coordinate)
            length = sphere.get_center()[1]
            lengths.append(length)
            # Calculate the x-axis position for plotting (starting at 0.05, spaced by 0.05)

            if(i==0):
              x_values.append(0)
            else:
              x_values.append(0.05 + i * 0.05)

            # Shift all existing blue lines to the right
            for line in lines:
                line.shift(RIGHT * 0.05)

            # Create a new blue line at the first position
            new_line = Line(
                start=np.array([0, 0, 0]),
                end=np.array([0, length, 0]),
                color=BLUE
            )
            lines.insert(0, new_line)
            self.add(new_line)

            # Gradually fade the oldest blue lines
            for idx, line in enumerate(lines):
                opacity = max(0, 1 - (idx / (lines_per_cycle)))  # Fade based on position in history
                line.set_opacity(opacity)

            # Remove fully transparent blue lines
            while lines and lines[-1].get_opacity() <= 0:
                self.remove(lines.pop())

            # Draw a line between the tops of the latest two blue lines
            if len(lines) >= 2:
                # Get the top points of the latest two blue lines
              point1 = lines[0].get_end()  # Top of the latest line
              point2 = lines[1].get_end()  # Top of the previous line
              point1[0]=0

                # Create a line between the two points
              connecting_line = Line(point1, point2, color=WHITE, stroke_width=1)
              connecting_lines.insert(0, connecting_line)
              self.add(connecting_line)

            # Shift all existing connecting lines to the right
            for connecting_line in connecting_lines:
                 connecting_line.shift(RIGHT * 0.05)

            # Remove connecting lines that are out of view
            while connecting_lines and connecting_lines[-1].get_start()[0] < 0:
                self.remove(connecting_lines.pop())

            # Move the sphere to the new position
            self.play(
                sphere.animate.move_to(circle.point_from_proportion(proportion)),
                run_time=interval_time,
                rate_func=linear
            )
