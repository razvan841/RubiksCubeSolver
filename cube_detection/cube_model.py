import random
import kociemba

class RubiksCube:
    def __init__(self):
        # Initialize the cube state with the correct face colors
        self.cube = [
            [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],  # Left
            [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],  # Front
            [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],  # Right
            [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],  # Back
            [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],  # Down
            [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']]   # Up
        ]

    def display(self):
        face_names = ['Up', 'Right', 'Front', 'Down', 'Left', 'Back']
        for i in range(6):
            print(f"{face_names[i]} Face:")
            for row in self.cube[i]:
                print(" ".join(row))
            print()

    def to_kociemba_string(self):
        # Kociemba requires the order: Up, Right, Front, Down, Left, Back
        kociemba_order = [5, 2, 1, 4, 0, 3]  # Map to self.cube order
        color_to_face = {
            'W': 'U',  # White -> Up
            'R': 'F',  # Red -> Front
            'G': 'L',  # Green -> Left
            'Y': 'D',  # Yellow -> Down
            'O': 'B',  # Orange -> Back
            'B': 'R'   # Blue -> Right
        }

        result = ""
        for face_idx in kociemba_order:
            face = self.cube[face_idx]
            for row in face:
                for color in row:
                    result += color_to_face[color]
        return result

    def copy_cube_state(self):
        temp_left = []
        for i in range(0,3):
            temp_left.append(self.cube[0][i][:])
        temp_front = []
        for i in range(0,3):
            temp_front.append(self.cube[1][i][:])
        temp_right = []
        for i in range(0,3):
            temp_right.append(self.cube[2][i][:])
        temp_back = []
        for i in range(0,3):
            temp_back.append(self.cube[3][i][:])
        temp_down = []
        for i in range(0,3):
            temp_down.append(self.cube[4][i][:])
        temp_up = []
        for i in range(0,3):
            temp_up.append(self.cube[5][i][:])

        return temp_left, temp_front, temp_right, temp_back, temp_down, temp_up

    def up(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()
        # rotate up
        for i in range(0,3):
            for j in range(0,3):
                self.cube[5][i][j] = temp_up[2-j][i]

        # left side replace
        for i in range(0,3):
            self.cube[0][0][i] = temp_front[0][i]
        # front side replace
        for i in range(0,3):
            self.cube[1][0][i] = temp_right[0][i]
        # right side replace
        for i in range(0,3):
            self.cube[2][0][i] = temp_back[0][i]
        # back side replace
        for i in range(0,3):
            self.cube[3][0][i] = temp_left[0][i]

    def up_prime(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()
        for i in range(0,3):
            for j in range(0,3):
                self.cube[5][i][j] = temp_up[j][2-i]

        for i in range(0,3):
            self.cube[0][0][i] = temp_back[0][i]
        for i in range(0,3):
            self.cube[1][0][i] = temp_left[0][i]
        for i in range(0,3):
            self.cube[2][0][i] = temp_front[0][i]
        for i in range(0,3):
            self.cube[3][0][i] = temp_right[0][i]

    def down(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[4][i][j] = temp_down[2-j][i]
        for i in range(0,3):
            self.cube[0][2][i] = temp_back[2][i]
        for i in range(0,3):
            self.cube[1][2][i] = temp_left[2][i]
        for i in range(0,3):
            self.cube[2][2][i] = temp_front[2][i]
        for i in range(0,3):
            self.cube[3][2][i] = temp_right[2][i]

    def down_prime(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[4][i][j] = temp_down[j][2-i]

        for i in range(0,3):
            self.cube[0][2][i] = temp_front[2][i]
        for i in range(0,3):
            self.cube[1][2][i] = temp_right[2][i]
        for i in range(0,3):
            self.cube[2][2][i] = temp_back[2][i]
        for i in range(0,3):
            self.cube[3][2][i] = temp_left[2][i]

    def left(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[0][i][j] = temp_left[2-j][i]

        for i in range(0,3):
            self.cube[3][i][2] = temp_down[2-i][0]
        for i in range(0,3):
            self.cube[5][i][0] = temp_back[2-i][2]
        for i in range(0,3):
            self.cube[1][i][0] = temp_up[i][0]
        for i in range(0,3):
            self.cube[4][i][0] = temp_front[i][0]

    def left_prime(self):

        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[0][i][j] = temp_left[j][2-i]
        for i in range(0,3):
            self.cube[3][i][2] = temp_up[2-i][0]
        for i in range(0,3):
            self.cube[5][i][0] = temp_front[i][0]
        for i in range(0,3):
            self.cube[1][i][0] = temp_down[i][0]
        for i in range(0,3):
            self.cube[4][i][0] = temp_back[2-i][2]

    def right(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[2][i][j] = temp_right[2-j][i]

        for i in range(0,3):
            self.cube[3][i][0] = temp_up[2-i][2]
        for i in range(0,3):
            self.cube[5][i][2] = temp_front[i][2]
        for i in range(0,3):
            self.cube[1][i][2] = temp_down[i][2]
        for i in range(0,3):
            self.cube[4][i][2] = temp_back[2-i][0]

    def right_prime(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[2][i][j] = temp_right[j][2-i]
        for i in range(0,3):
            self.cube[3][i][0] = temp_down[2-i][2]
        for i in range(0,3):
            self.cube[5][i][2] = temp_back[2-i][0]
        for i in range(0,3):
            self.cube[1][i][2] = temp_up[i][2]
        for i in range(0,3):
            self.cube[4][i][2] = temp_front[i][2]

    def front(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[1][i][j] = temp_front[2-j][i]

        for i in range(0,3):
            self.cube[0][i][2] = temp_down[0][i]
        for i in range(0,3):
            self.cube[5][2][i] = temp_left[2-i][2]
        for i in range(0,3):
            self.cube[2][i][0] = temp_up[2][i]
        for i in range(0,3):
            self.cube[4][0][i] = temp_right[2-i][0]

    def front_prime(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[1][i][j] = temp_front[j][2-i]
        for i in range(0,3):
            self.cube[0][i][2] = temp_up[2][2-i]
        for i in range(0,3):
            self.cube[5][2][i] = temp_right[i][0]
        for i in range(0,3):
            self.cube[2][i][0] = temp_down[0][2-i]
        for i in range(0,3):
            self.cube[4][0][i] = temp_left[i][2]

    def back(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[3][i][j] = temp_back[2-j][i]
        for i in range(0,3):
            self.cube[0][i][0] = temp_up[0][2-i]
        for i in range(0,3):
            self.cube[5][0][i] = temp_right[i][2]
        for i in range(0,3):
            self.cube[2][i][2] = temp_down[2][2-i]
        for i in range(0,3):
            self.cube[4][2][i] = temp_left[i][0]

    def back_prime(self):
        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[3][i][j] = temp_back[j][2-i]

        for i in range(0,3):
            self.cube[0][i][0] = temp_down[2][i]
        for i in range(0,3):
            self.cube[5][0][i] = temp_left[2-i][0]
        for i in range(0,3):
            self.cube[2][i][2] = temp_up[0][i]
        for i in range(0,3):
            self.cube[4][2][i] = temp_right[2-i][2]

    def rotate_cw(self):

        temp_left, temp_front, temp_right, temp_back, temp_down, temp_up = self.copy_cube_state()

        for i in range(0,3):
            for j in range(0,3):
                self.cube[5][i][j] = temp_up[2-j][i]

        for i in range(0,3):
            for j in range(0,3):
                self.cube[4][i][j] = temp_down[j][2-i]

        for i in range(0,3):
            for j in range(0,3):
                self.cube[0][i][j] = temp_front[i][j]
                self.cube[1][i][j] = temp_right[i][j]
                self.cube[2][i][j] = temp_back[i][j]
                self.cube[3][i][j] = temp_left[i][j]

    def rotate_ccw(self):
        for i in range(0,3):
            self.rotate_cw()

    def is_cube_solved(self):
        for s in range(0,6):
            for i in range(0,3):
                for j in range(0,3):
                    if not(self.cube[s][i][j] == self.cube[s][1][1]):
                        return False
        return True

    def set_cube_state(self, states):
        kociemba_order = [5, 2, 1, 4, 0, 3]
        detect_order = [1, 4, 0, 2, 3, 5]
        for i in range(6):
            for row in range(3):
                for col in range(3):
                    self.cube[kociemba_order[i]][row][col] = states[detect_order[i]][row * 3 + col]

    def scramble_cube(self):
        scramble_counter = 25

        i = 0
        while(i < scramble_counter):
            chosen_move = random.randint(0, 11)
            if(chosen_move == 0):
                self.up()
            if(chosen_move == 1):
                self.up_prime()
            if(chosen_move == 2):
                self.down()
            if(chosen_move == 3):
                self.down_prime()
            if(chosen_move == 4):
                self.left()
            if(chosen_move == 5):
                self.left_prime()
            if(chosen_move == 6):
                self.right()
            if(chosen_move == 7):
                self.right_prime()
            if(chosen_move == 8):
                self.back()
            if(chosen_move == 9):
                self.back_prime()
            if(chosen_move == 10):
                self.front()
            if(chosen_move == 11):
                self.front_prime()

            i+=1

    def solve_cube(self):
        kociemba_string = self.to_kociemba_string()
        print(kociemba_string)
        try:
            if self.is_cube_solved():
                print("Cube already solved; No moves necessary!")
                return []
            solution = kociemba.solve(kociemba_string)
            solution_list = solution.split(' ')
            print("Solution List: ", solution_list)
            return solution_list

        except ValueError as e:
            print(f"Invalid cube string: {kociemba_string}. Error: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while solving the cube: {e}")
            return []