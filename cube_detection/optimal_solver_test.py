import time
from cube_model import RubiksCube

def main():
    num_cubes = 1000  # Number of cubes to generate and solve
    solve_times = []
    move_counts = []

    for i in range(num_cubes):
        cube = RubiksCube()
        cube.scramble_cube()

        start_time = time.time()
        solution = cube.solve_cube()
        end_time = time.time()

        solve_time = end_time - start_time
        num_moves = len(solution)

        solve_times.append(solve_time)
        move_counts.append(num_moves)

        if (i + 1) % 100 == 0:
            print(f"Solved {i + 1}/{num_cubes} cubes...")

    print(f"\nSolved {num_cubes} cubes.")
    print(f"Average solve time: {sum(solve_times) / len(solve_times):.4f} seconds")
    print(f"Average number of moves: {sum(move_counts) / len(move_counts):.2f}")

if __name__ == "__main__":
    main()
