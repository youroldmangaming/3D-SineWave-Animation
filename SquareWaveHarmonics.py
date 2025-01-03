from manimlib import *

class SphereOnCircle(Scene):
    def construct(self):
        # Set the camera orientation
        # self.camera.frame.set_euler_angles(
        #     phi=-15 * DEGREES,  # Tilt downward by 10 degrees (90 - 10 = 80)
        #     theta=-5 * DEGREES  # Rotate slightly to the left
        # )

        # Base radius for the first graph
        r0 = 1.0

        # Number of copies
        num_copies = 5

        # Base vertical spacing for the first graph
        base_vertical_spacing = 5

        # List to store all spheres and their components
        spheres = []
        circles = []
        yellow_lines = []
        blue_lines = []
        length_texts = []
        moving_arrows = []
        all_lines = []  # Store all blue lines for each instance
        all_connecting_lines = []  # Store all connecting lines for each instance
        gap = 0.2

        # Define the vertical position for the resultant graph
        resultant_vertical_position = -2  # Positioned below the first graph

        for copy_idx in range(num_copies):
            # Calculate the radius for this graph
            radius = r0 / (2 * copy_idx + 1)  # r1 = r0/1, r2 = r0/3, r3 = r0/5, etc.

            # Calculate the vertical spacing for this graph (proportional to the radius)

           # Calculate the vertical spacing for this graph (proportional to the radius)
            if copy_idx == 0:
                vertical_spacing = 0
                DOT_Size=.08
            elif copy_idx == 1:
                vertical_spacing = 1.33 + gap
                DOT_Size=.07
            elif copy_idx == 2:
                vertical_spacing = 0.95 + gap
                DOT_Size=.065
            elif copy_idx == 3:
                vertical_spacing = 0.76 + gap
                DOT_Size=.065
            elif copy_idx == 4:
                vertical_spacing = 0.64 + gap
                DOT_Size=.065





            # Define the center for this copy
            center = np.array([0, copy_idx * vertical_spacing, 0])

            # Create a circle with the calculated radius, centered at the current center
            circle = Circle(radius=radius, color=WHITE).move_to(center)
            circles.append(circle)

            # Create a small red sphere (using Dot for better visibility), scaled proportionally to the circle's radius
            sphere = Dot(color=RED, radius=DOT_Size).move_to(circle.point_from_proportion(0))
            spheres.append(sphere)

            # Function to update the yellow line's position dynamically
            def get_yellow_line(sphere=sphere, center=center):
                return Line(center, sphere.get_center(), color=YELLOW)

            # Function to update the blue line's position dynamically
            def get_blue_line(sphere=sphere, center=center):
                sphere_pos = sphere.get_center()
                endpoint = np.array([sphere_pos[0], center[1], 0])  # Same x, y=center_y, z=0
                return Line(sphere_pos, endpoint, color=BLUE)

            # Function to update the Arrow's position dynamically
            def get_moving_arrow(sphere=sphere, center=center):
                y_pos = sphere.get_center()[1] - center[1]  # Relative to center
                return Arrow(
                    start=center,  # Start at the center
                    end=center + np.array([0, y_pos, 0]),  # End at (center_x, center_y + y_pos, 0)
                    color=TEAL_A,
                    buff=0,  # No space between the arrow tip and the end point
                    stroke_width=2  # Thickness of the arrow
                )

            # Use always_redraw to ensure the lines, text, and arrow update their positions during animation
            yellow_line = always_redraw(get_yellow_line)
            blue_line = always_redraw(get_blue_line)
            moving_arrow = always_redraw(get_moving_arrow)

            # Add the circle, the sphere, the lines, and the moving arrow to the scene
            self.add(circle, sphere, yellow_line, blue_line, moving_arrow)

            # Store components for later use
            yellow_lines.append(yellow_line)
            blue_lines.append(blue_line)
            moving_arrows.append(moving_arrow)

            # Initialize lists to store lines for this instance
            all_lines.append([])
            all_connecting_lines.append([])

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

        # Base interval time for the first graph
        base_interval_time = 0.15

        # Number of samples per cycle for the first graph
        samples_per_cycle = 60

        # Total time for one full cycle of the first graph
        total_time = samples_per_cycle * base_interval_time

        # Initialize lists to store resultant values and their corresponding lines
        resultant_values = []
        resultant_lines = []
        resultant_connecting_lines = []  # Store connecting lines for the resultant graph

        # Animate the spheres moving around their respective circles in a continuous loop
        i = 0
        while True:
            # Create a list of animations for all spheres
            animations = []
            resultant_value = 0  # Initialize the resultant value for this time step

            for copy_idx in range(num_copies):
                # Calculate the scaled cycle time for this graph
                scale_factor = 2 * copy_idx + 1  # 1, 3, 5, 7, 9
                cycle_time = total_time / scale_factor

                # Calculate the proportion of the circle completed
                proportion = (i * base_interval_time) / cycle_time

                # Wrap the proportion to keep it within [0, 1]
                proportion = proportion % 1

                # Add the sphere's movement to the animations list
                animations.append(
                    spheres[copy_idx].animate.move_to(circles[copy_idx].point_from_proportion(proportion))
                )

                # Update lines for this instance
                self.update_lines(copy_idx, spheres[copy_idx], circles[copy_idx], all_lines[copy_idx], all_connecting_lines[copy_idx])

                # Add the delta (Y-coordinate of the sphere minus Y-coordinate of the circle's center) to the resultant value
                resultant_value += spheres[copy_idx].get_center()[1] - circles[copy_idx].get_center()[1]

            # Store the resultant value for this time step
            resultant_values.append(resultant_value)

            # Shift all existing resultant lines to the right
            for line in resultant_lines:
                line.shift(RIGHT * 0.05)

            # Create a new resultant line at the first position
            new_resultant_line = Line(
                start=np.array([0, resultant_vertical_position, 0]),
                end=np.array([0, resultant_vertical_position + resultant_value, 0]),
                color=PURPLE
            )
            resultant_lines.insert(0, new_resultant_line)
            self.add(new_resultant_line)

            # Gradually fade the oldest resultant lines
            for idx, line in enumerate(resultant_lines):
                opacity = max(0, 1 - (idx / 60))  # Fade based on position in history
                line.set_opacity(opacity)

            # Remove fully transparent resultant lines
            while resultant_lines and resultant_lines[-1].get_opacity() <= 0:
                self.remove(resultant_lines.pop())

            # Draw a line between the tops of the latest two resultant lines
            if len(resultant_lines) >= 2:
                # Get the top points of the latest two resultant lines
                point1 = resultant_lines[0].get_end()  # Top of the latest line
                point2 = resultant_lines[1].get_end()  # Top of the previous line
                point1[0] = 0  # Ensure the x-coordinate is 0

                # Create a line between the two points
                resultant_connecting_line = Line(point1, point2, color=WHITE, stroke_width=1)
                resultant_connecting_lines.insert(0, resultant_connecting_line)
                self.add(resultant_connecting_line)

            # Shift all existing resultant connecting lines to the right
            for connecting_line in resultant_connecting_lines:
                connecting_line.shift(RIGHT * 0.05)

            # Remove resultant connecting lines that are out of view
            while resultant_connecting_lines and resultant_connecting_lines[-1].get_start()[0] < 0:
                self.remove(resultant_connecting_lines.pop())

            # Play all animations concurrently
            self.play(*animations, run_time=base_interval_time, rate_func=linear)

            # Increment the frame counter
            i += 1

    def update_lines(self, copy_idx, sphere, circle, lines, connecting_lines):
        # Calculate the length of the blue line (absolute value of the y-coordinate)
        length = sphere.get_center()[1] - circle.get_center()[1]

        # Shift all existing blue lines to the right
        for line in lines:
            line.shift(RIGHT * 0.05)

        # Create a new blue line at the first position
        new_line = Line(
            start=np.array([0, circle.get_center()[1], 0]),
            end=np.array([0, sphere.get_center()[1], 0]),
            color=BLUE
        )
        lines.insert(0, new_line)
        self.add(new_line)

        # Gradually fade the oldest blue lines
        for idx, line in enumerate(lines):
            opacity = max(0, 1 - (idx / 60))  # Fade based on position in history
            line.set_opacity(opacity)

        # Remove fully transparent blue lines
        while lines and lines[-1].get_opacity() <= 0:
            self.remove(lines.pop())

        # Draw a line between the tops of the latest two blue lines
        if len(lines) >= 2:
            # Get the top points of the latest two blue lines
            point1 = lines[0].get_end()  # Top of the latest line
            point2 = lines[1].get_end()  # Top of the previous line
            point1[0] = 0

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














