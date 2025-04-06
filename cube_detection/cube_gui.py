import tkinter as tk
from tkinter import Canvas
import random

class RubiksCubeGUI:
    def __init__(self, root, cube):
        self.root = root
        self.cube = cube
        self.face_size = 60
        self.colors = {
            'W': 'white',
            'Y': 'yellow',
            'G': 'green',
            'B': 'blue',
            'O': 'orange',
            'R': 'red'
        }
        self.solve_moves = []
        self.current_move_index = 0
        self.create_widgets()
        self.draw_cube()

    def create_widgets(self):
        self.canvas = Canvas(self.root, width=1200, height=700, bg="gray")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        moves = ['R', "R'", 'L', "L'", 'U', "U'", 'D', "D'", 'F', "F'", 'B', "B'"]
        row, col = 0, 0
        for move in moves:
            button = tk.Button(button_frame, text=move, command=lambda move=move: self.make_move(move))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:
                col = 0
                row += 1

        scramble_button = tk.Button(button_frame, text="Scramble", command=self.scramble_cube)
        scramble_button.grid(row=row, column=col, padx=5, pady=5)
        col += 1

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_cube)
        solve_button.grid(row=row, column=col, padx=5, pady=5)

        col += 1

        next_button = tk.Button(button_frame, text="Next", command=self.next_move)
        next_button.grid(row=row, column=col, padx=5, pady=5)
        col += 1

        display_button = tk.Button(button_frame, text="Display", command=self.display_cube_state)
        display_button.grid(row=row, column=col, padx=5, pady=5)

    def draw_cube(self):
        self.canvas.delete("all")

        offsets = {
            0: (4, 0.5),  # Left
            1: (4, 4),    # Front
            2: (4, 7.5),  # Right
            3: (4, 11),   # Back
            4: (7.5, 4),  # Down
            5: (0.5, 4),  # Up
        }

        for face_index, (row_offset, col_offset) in offsets.items():
            face = self.cube.cube[face_index]
            for i, row in enumerate(face):
                for j, color in enumerate(row):
                    x0 = (col_offset + j) * self.face_size
                    y0 = (row_offset + i) * self.face_size
                    x1 = x0 + self.face_size
                    y1 = y0 + self.face_size
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colors[color], outline="black")

    def make_move(self, move):
        if move == 'R':
            self.cube.right()
        elif move == "R'":
            self.cube.right_prime()
        elif move == 'L':
            self.cube.left()
        elif move == "L'":
            self.cube.left_prime()
        elif move == 'U':
            self.cube.up()
        elif move == "U'":
            self.cube.up_prime()
        elif move == 'D':
            self.cube.down()
        elif move == "D'":
            self.cube.down_prime()
        elif move == 'F':
            self.cube.front()
        elif move == "F'":
            self.cube.front_prime()
        elif move == 'B':
            self.cube.back()
        elif move == "B'":
            self.cube.back_prime()
        elif move == "R2":
            self.cube.right()
            self.cube.right()
        elif move == 'L2':
            self.cube.left()
            self.cube.left()
        elif move == "F2":
            self.cube.front()
            self.cube.front()
        elif move == 'B2':
            self.cube.back()
            self.cube.back()
        elif move == "U2":
            self.cube.up()
            self.cube.up()
        elif move == 'D2':
            self.cube.down()
            self.cube.down()
        self.draw_cube()

    def scramble_cube(self):
        self.cube.scramble_cube()
        self.draw_cube()
        print("Scrambled!")
        return

    def display_cube_state(self):
        cube_data = self.cube.cube
        flattened_cube = []
        for face in cube_data:
            flattened_face = [color for row in face for color in row]
            flattened_cube.append(flattened_face)

        print(flattened_cube)

    def solve_cube(self):
        print("Solving the cube...")
        self.solve_moves = self.cube.solve_cube()
        self.current_move_index = 0
        print(f"Solve moves: {self.solve_moves}")

    def next_move(self):
        if self.current_move_index < len(self.solve_moves):
            move = self.solve_moves[self.current_move_index]
            self.make_move(move)
            self.current_move_index += 1
            print(f"Performed move: {move}")
        else:
            print("All moves completed!")

if __name__ == "__main__":
    from cube_model import RubiksCube
    root = tk.Tk()
    root.title("Rubik's Cube GUI")
    cube = RubiksCube()
    app = RubiksCubeGUI(root, cube)
    root.mainloop()
