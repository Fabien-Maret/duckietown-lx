from typing import Tuple

import numpy as np


def get_motor_left_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")

    # These variables define the base and height of a triangle in the matrix.
    # The triangle represents the area where the Duckiebot perceives an obstacle.
    # The base of the triangle widens as we move down, simulating deeper perception (closer objects).
    base_start = 250                    # Start of the triangle base (narrow at the top).
    base_end = 550                      # End of the triangle base (wider as we go down).
    triangle_height = 100               # This controls how far from the top of the matrix the perception starts. It doesn't start at the very top, because objects that are that far are not relevant.
    max_y = 480                         # Maximum y-coordinate (bottom of the image).

    # Loop over the the y-coordinates, starting from the triangle's height to the maximum y-value.
    # The triangle gets wider as we move down, representing an increased perception range for nearer objects.
    for y in range(triangle_height, max_y):
        # x_start defines how much the triangle expands as we go down, representing depth perception.
        x_start = int(base_end - (y - triangle_height) * (base_end - base_start) / (max_y - triangle_height))
        x_end = base_start              # The base widens as y increases, simulating a broader field of view closer to the robot.

        # Introduce a curved hypotenuse to smooth out corrections, representing a stronger response as objects get close.
        # This simulates more significant correction as objects approach, using a cosine function for curvature.
        curve = base_end - int((base_end - base_start) * (1 - np.cos(np.pi * (y - triangle_height) / (max_y - triangle_height))) / 2)
        
        # Set the perception for this y-coordinate, marking where the left motor should slow down (negative feedback).
        res[y, curve:base_end] = -1     # The closer the object, the stronger the negative feedback (-1).

    return res


def get_motor_right_matrix(shape: Tuple[int, int]) -> np.ndarray:
    # TODO: write your function instead of this one
    res = np.zeros(shape=shape, dtype="float32")

     # These variables define the base and height of the triangle for the right motor.
     # The triangle widens as we move down, simulating a broader perception range as objects approach.
    base_start = 90                     # Start of the triangle base (narrow at the top).
    base_end = 390                      # End of the triangle base (wider at the bottom).
    triangle_height = 100               # Defines how far up the triangle starts.
    max_y = 480                         # Maximum y-coordinate (bottom of the image).

    # Loop over the y-coordinates to create a triangle for depth perception, widening as we go down.
    for y in range(triangle_height, max_y):
        # Define x bounds for each y, expanding the base as the object gets closer.
        x_start = int(base_start + (y - triangle_height) * (base_end - base_start) / (max_y - triangle_height))
        x_end = base_end

        # Introduce a curved hypotenuse to simulate stronger correction for closer objects.
        # This cosine-based curve adds smoothness to the motor behaviour, avoiding sharp corrections.
        curve = base_start + int((x_end - base_start) * (1 - np.cos(np.pi * (y - triangle_height) / (max_y - triangle_height))) / 2)
        
        # Assign negative feedback (-1) where the right motor should slow down, for objects perceived closer.
        res[y, base_start:curve] = -1

    return res