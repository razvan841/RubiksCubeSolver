import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def draw_face(ax, origin, normal, colors):
    """
    Draw a single face of the Rubik's cube with 3x3 sub-squares.
    :param ax: Matplotlib 3D axis
    :param origin: Bottom-left corner of the face
    :param normal: Normal vector of the face (to determine orientation)
    :param colors: 3x3 grid of colors for the face
    """
    rows, cols = len(colors), len(colors[0])
    step = 1 / rows

    for i in range(rows):
        for j in range(cols):
            color = colors[i][j]
            x_offset = (cols - 1 - j) * step
            y_offset = (rows - 1 - i) * step
            if normal == [0, 0, 1]:  # XY plane (Top)
                x_offset = (cols - 1 - j) * step  # Standard column order
                y_offset = i * step
                vertices = [
                    [origin[0] + x_offset, origin[1] + y_offset, origin[2]],
                    [origin[0] + x_offset + step, origin[1] + y_offset, origin[2]],
                    [origin[0] + x_offset + step, origin[1] + y_offset + step, origin[2]],
                    [origin[0] + x_offset, origin[1] + y_offset + step, origin[2]]
                ]
            elif normal == [0, 0, -1]:  # XY plane (Bottom)
                vertices = [
                    [origin[0] + x_offset, origin[1] + y_offset, origin[2]],
                    [origin[0] + x_offset + step, origin[1] + y_offset, origin[2]],
                    [origin[0] + x_offset + step, origin[1] + y_offset + step, origin[2]],
                    [origin[0] + x_offset, origin[1] + y_offset + step, origin[2]]
                ]
            elif normal == [0, 1, 0]:  # XZ plane (Front)
                x_offset = (cols - 1 - j) * step  # Reverse column order
                y_offset = (rows - 1 - i) * step  # Reverse row order
                vertices = [
                    [origin[0] + x_offset, origin[1], origin[2] + y_offset],
                    [origin[0] + x_offset + step, origin[1], origin[2] + y_offset],
                    [origin[0] + x_offset + step, origin[1], origin[2] + y_offset + step],
                    [origin[0] + x_offset, origin[1], origin[2] + y_offset + step]
                ]
            elif normal == [0, -1, 0]:  # XZ plane (Back)
                x_offset = j * step
                vertices = [
                    [origin[0] + x_offset, origin[1], origin[2] + y_offset],
                    [origin[0] + x_offset + step, origin[1], origin[2] + y_offset],
                    [origin[0] + x_offset + step, origin[1], origin[2] + y_offset + step],
                    [origin[0] + x_offset, origin[1], origin[2] + y_offset + step]
                ]
            elif normal == [1, 0, 0]:  # YZ plane (Right)
                x_offset = j * step
                vertices = [
                    [origin[0], origin[1] + x_offset, origin[2] + y_offset],
                    [origin[0], origin[1] + x_offset + step, origin[2] + y_offset],
                    [origin[0], origin[1] + x_offset + step, origin[2] + y_offset + step],
                    [origin[0], origin[1] + x_offset, origin[2] + y_offset + step]
                ]
            elif normal == [-1, 0, 0]:  # YZ plane (Left)
                x_offset = (cols - 1 - j) * step  # Reverse column order for Left face
                vertices = [
                    [origin[0], origin[1] + x_offset, origin[2] + y_offset],
                    [origin[0], origin[1] + x_offset + step, origin[2] + y_offset],
                    [origin[0], origin[1] + x_offset + step, origin[2] + y_offset + step],
                    [origin[0], origin[1] + x_offset, origin[2] + y_offset + step]
                ]
            else:
                continue

            face = Poly3DCollection([vertices], color=color, edgecolor='black')
            ax.add_collection3d(face)

def draw_cube(state):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define face origins and normals
    face_definitions = {
        "Up": ([-0.5, -0.5, 0.5], [0, 0, 1]),
        "Down": ([-0.5, -0.5, -0.5], [0, 0, -1]),
        "Front": ([-0.5, 0.5, -0.5], [0, 1, 0]),
        "Back": ([-0.5, -0.5, -0.5], [0, -1, 0]),
        "Left": ([-0.5, -0.5, -0.5], [-1, 0, 0]),
        "Right": ([0.5, -0.5, -0.5], [1, 0, 0]),
    }

    # Draw each face
    for face, (origin, normal) in face_definitions.items():
        draw_face(ax, origin, normal, state[face])

        # Add text at the center of each face
        if normal == [0, 0, 1]:  # Top
            ax.text(0, 0, 0.7, face, color='black', fontsize=12, ha='center', va='center')
        elif normal == [0, 0, -1]:  # Bottom
            ax.text(0, 0, -0.7, face, color='black', fontsize=12, ha='center', va='center')
        elif normal == [0, 1, 0]:  # Front
            ax.text(0, 0.7, 0, face, color='black', fontsize=12, ha='center', va='center')
        elif normal == [0, -1, 0]:  # Back
            ax.text(0, -0.7, 0, face, color='black', fontsize=12, ha='center', va='center')
        elif normal == [1, 0, 0]:  # Right
            ax.text(0.7, 0, 0, face, color='black', fontsize=12, ha='center', va='center')
        elif normal == [-1, 0, 0]:  # Left
            ax.text(-0.7, 0, 0, face, color='black', fontsize=12, ha='center', va='center')

    # Set the aspect of the plot to be equal
    ax.set_box_aspect([1, 1, 1])

    # Set limits and labels
    ax.set_xlim([-0.75, 0.75])
    ax.set_ylim([-0.75, 0.75])
    ax.set_zlim([-0.75, 0.75])

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Display the cube
    plt.show()


# cube = {'Front': [['red', 'red', 'white'], ['white', 'white', 'red'], ['red', 'red', 'red']], 
#  'Up': [['white', 'blue', 'white'], ['white', 'white', 'red'], ['white', 'white', 'red']], 
#  'Down': [['white', 'blue', 'white'], ['red', 'blue', 'red'], ['red', 'white', 'white']], 
#  'Left': [['white', 'white', 'red'], ['white', 'red', 'white'], ['white', 'white', 'red']], 
#  'Right': [['white', 'red', 'white'], ['red', 'red', 'blue'], ['blue', 'blue', 'blue']], 
#  'Back': [['white', 'yellow', 'red'], ['white', 'yellow', 'blue'], ['blue', 'white', 'blue']]}
# draw_cube(cube)
