from manimlib import *

class SphereOnCircle(Scene):
    def construct(self):
        # Set the camera in the default XY plane focused on the origin
        self.camera.frame.set_euler_angles(phi=0, theta=0)  # Default position
        self.camera.frame.move_to(ORIGIN)  # Focus on the origin

        # Create a circle with radius 1
        circle = Circle(radius=1, color=WHITE)
        circle.rotate(90 * DEGREES, axis=UP)

        # Create a small red sphere
        sphere = Sphere(radius=0.1, color=RED).move_to(circle.point_from_proportion(0))

        # Function to update the yellow line's position dynamically
        def get_yellow_line():
            return Line(ORIGIN, sphere.get_center(), color=YELLOW)

        # Function to update the blue line's position dynamically
        def get_blue_line():
            sphere_pos = sphere.get_center()
            # The blue line is a 3D vector:
            # x = time unit, y = length of the line from origin to sphere, z = sphere's z-position
            return Line(
                start=np.array([0, 0, 0]),
                end=np.array([0, sphere_pos[1], sphere_pos[2]]),
                color=BLUE
            )

        # Function to update the length text dynamically
        def get_length_text():
            length = np.linalg.norm(sphere.get_center())  # Length from origin to sphere
            return Text(f"Length: {length:.2f}", font_size=24).to_edge(DOWN)

        # Function to update the Dot's position dynamically
        def get_moving_dot():
            y_pos = sphere.get_center()[1]
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
        self.add(axes)

        # Add labels for the axes
        x_label = Text("X").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y").next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z").next_to(axes.z_axis.get_end(), OUT)
        self.add(x_label, y_label, z_label)

        # Store the lengths of the blue line at 0.15-second intervals
        lines_per_cycle = 40
        interval_time = 0.15
        total_time = lines_per_cycle * interval_time
        lengths = []
        x_values = []
        blue_lines = VGroup()
        connecting_lines = VGroup()
        self.add(blue_lines, connecting_lines)


        # Animate the sphere moving around the circle
        i = -1
        pancount=0
        while True:
            i += 1
            pancount=pancount+1
            if i > lines_per_cycle - 1:
                i = 0
            if(pancount==30):
                  # Return the camera to the start position
                  self.play(
                    self.camera.frame.animate.shift(6 * RIGHT),
                    self.camera.frame.animate.set_euler_angles(
                       phi=45 * DEGREES,  # Tilt up
                       theta=45 * DEGREES,  # Pan right
                       gamma=45 * DEGREES
                     )  # Roll counterclockwise
                  )
            if(pancount==120):
                 # Move the camera along the X-axis
                 self.play(
                   self.camera.frame.animate.shift(3 * RIGHT),
                   run_time=5,
                   rate_func=linear
                 )
            if(pancount==180):
                  # Return the camera to the start position
                  self.play(
                    self.camera.frame.animate.set_euler_angles(
                       phi=30 * DEGREES,  # Tilt up
                       theta=60 * DEGREES,  # Pan right
                       gamma=-15 * DEGREES
                     ),  # Roll counterclockwise
                     run_time=3
                  )
            if(pancount==200):
              # Set the camera in the default XY plane focused on the origin
              self.play(
                 self.camera.frame.set_euler_angles(
                    phi=0,
                    theta=0
                 ),  # Default position
                 run_time=3
              )
              self.camera.frame.move_to(ORIGIN)  # Focus on the origin




            proportion = i / lines_per_cycle
            sphere_pos = sphere.get_center()
            length = np.linalg.norm(sphere_pos)  # Length from origin to sphere
            lengths.append(length)
            x_values.append(0 if i == 0 else 0.05 + i * 0.05)

            # Add new blue line
            new_line = Line(
                start=np.array([0, 0, 0]),
                end=np.array([0, sphere_pos[1], sphere_pos[2]]),
                color=BLUE
            )
            blue_lines.add(new_line)
            blue_lines.shift(RIGHT * 0.05)

            # Add connecting line (white line) only if there are at least two blue lines
            if len(blue_lines) >= 2:
                # Get the endpoints of the latest two blue lines
                point1 = blue_lines[-2].get_end()  # Previous blue line endpoint
                point2 = blue_lines[-1].get_end()  # Latest blue line endpoint
                # Create a line connecting the two endpoints in 3D space
                connecting_line = Line(point1, point2, color=WHITE, stroke_width=2)  # Increased stroke width for visibility
                connecting_lines.add(connecting_line)
                connecting_lines.shift(RIGHT * 0.05)

            # Move the sphere
            self.play(
                sphere.animate.move_to(circle.point_from_proportion(proportion)),
                run_time=interval_time,
                rate_func=linear
            )
