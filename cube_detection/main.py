import socket
import json
import threading
import os
import numpy as np
from color_detection import edge_impulse
from matplotlib import pyplot as plt
from cubeplot import draw_cube
from ultralytics import YOLO
import signal
import cv2
from cube_model import RubiksCube
from dotenv import load_dotenv
import piserver
import time
from solver import run

load_dotenv()

SERVER_PORT = int(os.getenv('PORT', 5000))
SERVER_HOST = os.getenv('IP_ADDRESS', '127.0.0.1')

CAMERA_INDEX = 0
MODEL = 'uppaal'

stored_moves = None
shutdown_event = threading.Event()

# Cube state initialization
cube_state = {
    'Front': [['green'] * 3 for _ in range(3)],
    'Up': [['white'] * 3 for _ in range(3)],
    'Down': [['yellow'] * 3 for _ in range(3)],
    'Left': [['orange'] * 3 for _ in range(3)],
    'Right': [['red'] * 3 for _ in range(3)],
    'Back': [['blue'] * 3 for _ in range(3)],
}

model = YOLO(r"cube_detection\cube_detection\detect\model2\weights\best.pt")

sequence = ['Front', 'Up', 'Down', 'Left', 'Right', 'Back']
current_step = 0

def save_colors(face, colors):
    cube_state[face] = np.array(colors).reshape(3, 3).tolist()
    print(f"Colors for {face} saved:", colors)

def uppaal_cube_states(cube_state):
    color_to_int = {
        'red': 0,      # Front
        'yellow': 1,   # Bottom
        'blue': 2,     # Right
        'green': 3,    # Left
        'white': 4,    # Up
        'orange': 5    # Back
    }

    def face_to_int(face):
        return [color_to_int[color] for row in face for color in row]

    front_face = face_to_int(cube_state['Front'])
    back_face = face_to_int(cube_state['Back'])
    right_face = face_to_int(cube_state['Right'])
    left_face = face_to_int(cube_state['Left'])
    up_face = face_to_int(cube_state['Up'])
    down_face = face_to_int(cube_state['Down'])
    return front_face, back_face, right_face, left_face, up_face, down_face

def send_cube_to_uppaal(front_face, back_face, right_face, left_face, up_face, down_face):
    scramble = []
    scramble.extend(front_face)
    scramble.extend(back_face)
    scramble.extend(right_face)
    scramble.extend(left_face)
    scramble.extend(up_face)
    scramble.extend(down_face)


    print("Sending cube state to solver...")
    numbers = run(scramble)
    print(numbers)
    moves = numbers_to_moves(numbers)
    store_moves(moves)
    print(moves)
    return moves

def numbers_to_moves(numbers):
    moves = []
    number_to_move = {
        0: "F",
        1: "F'",
        2: "B",
        3: "B'",
        4: "U",
        5: "U'",
        6: "D",
        7: "D'",
        8: "L",
        9: "L'",
        10: "R",
        11: "R'"

    }
    for number in numbers:
        moves.append(number_to_move[number])
    return moves

def transform_cube_states(cube_state):
    color_map = {
        'blue': 'B',
        'yellow': 'Y',
        'green': 'G',
        'red': 'R',
        'white': 'W',
        'orange': 'O'
    }

    transformed_cube = []

    for face in ['Front', 'Up', 'Down', 'Left', 'Right', 'Back']:
        face_state = cube_state[face]
        transformed_row = []

        for row in face_state:
            for color in row:
                transformed_row.append(color_map.get(color, ''))
        transformed_cube.append(transformed_row)

    return transformed_cube

def store_moves(moves):
    global stored_moves
    stored_moves = moves

def send_cube_state_to_solver(cube_state):
    print("Sending cube state to solver...")
    cube = RubiksCube()
    cube.set_cube_state(cube_state)
    # print("cube state: ", cube.display())
    moves = cube.solve_cube()
    store_moves(moves)

    return moves

# Will send to the esp the list of moves in rubiks cube format
# Replaced the up and up prime moves with the sequences
def moves_to_commands(moves):
    new_moves = []
    up_sequence = [
        "D", "B2", "F2", "D", "R2", "B2", "R2", "L2", "F2", "L2", "D'", "B2", "L2",
        "D2", "L2", "D2", "L2", "R2", "D2", "R2", "D2", "F2", "B2", "D", "R2",
        "L2", "B2", "F2", "D", "R2", "L2"
    ]
    up_prime_sequence = [
        "L2", "R2", "D", "B2", "F2", "D", "B2", "L2", "B2", "F2", "D2", "R2", "D2",
        "R2", "L2", "D2", "L2", "D2", "L2", "B2", "D'", "L2", "F2", "L2", "R2",
        "B2", "R2", "D", "F2", "B2", "D"
    ]

    move_to_command = {
        "F": [1, 1, 1],
        "B": [2, 1, 1],
        "L": [3, 1, 1],
        "R": [4, 1, 1],
        "D": [5, 1, 1],
        "F'": [1, 1, 3],
        "B'": [2, 1, 3],
        "L'": [3, 1, 3],
        "R'": [4, 1, 3],
        "D'": [5, 1, 3],
        "F2": [1, 1, 2],
        "B2": [2, 1, 2],
        "L2": [3, 1, 2],
        "R2": [4, 1, 2],
        "D2": [5, 1, 2]
    }

    for move in moves:
        if move == 'U':
            new_moves.extend([move_to_command[m] for m in up_sequence])
        elif move == "U'":
            new_moves.extend([move_to_command[m] for m in up_prime_sequence])
        elif move == "U2":
            new_moves.extend([move_to_command[m] for m in up_sequence])
            new_moves.extend([move_to_command[m] for m in up_sequence])
        else:
            new_moves.append(move_to_command[move])

    return new_moves

# def handle_connection(conn, addr):
#     print(f"New connection from {addr}")
#     try:
#         data = conn.recv(1024).decode('utf-8')
#         if data:
#             print(f"Received request from Arduino: {data}")
#             if stored_moves:
#                 print("Sending stored moves to Arduino...")

# def handle_connection(conn, addr):
#     print(f"New connection from {addr}")
#     try:
#         data = conn.recv(1024).decode('utf-8')
#         if data:
#             print(f"Received request from Arduino: {data}")
#             if stored_moves:
#                 print("Sending stored moves to Arduino...")
#                 transformed_moves = moves_to_commands(stored_moves)
#                 response = {'response': transformed_moves}
#             else:
#                 response = {'error': 'Moves not available yet.'}
#             conn.send(json.dumps(response).encode('utf-8'))
#         else:
#             conn.send(json.dumps({'error': 'Invalid request'}).encode('utf-8'))
#     except socket.error as e:
#         print(f"Error during Arduino communication: {e}")
#     finally:
#         conn.close()


# def start_server():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#         try:
#             server_socket.bind((SERVER_HOST, SERVER_PORT))
#             server_socket.listen(5)
#             print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

#             while not shutdown_event.is_set():
#                 try:
#                     server_socket.settimeout(1.0)
#                     conn, addr = server_socket.accept()
#                     arduino_thread = threading.Thread(target=handle_connection, args=(conn, addr), daemon=True)
#                     arduino_thread.start()
#                 except socket.timeout:
#                     continue
#                 except Exception as e:
#                     print(f"Error accepting connection: {e}")
#         except Exception as e:
#             print(f"Error starting server: {e}")
#         finally:
#             print("Shutting down server...")

def signal_handler(sig, frame):
    print("Received termination signal. Shutting down...")
    shutdown_event.set()


def scan_and_solve_cube():
    global current_step
    cap = cv2.VideoCapture(CAMERA_INDEX, apiPreference = cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        # Perform YOLO detection
        results = model(frame, save=False, conf=0.25)
        annotated_frame = results[0].plot()
        box = results[0].boxes.xyxy

        # Ensure bounding box exists
        if box.size(0) > 0:
            x1, y1, x2, y2 = map(int, box[0])
            cropped_frame = frame[y1:y2, x1:x2]
        else:
            cropped_frame = None

        # Display annotated frame
        cv2.imshow(f"Scanning: {sequence[current_step]} Face", annotated_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            if cropped_frame is not None:
                cv2.imshow("Captured Image - Press 'y' to save or 'r' to retake", cropped_frame)

                key_confirm = cv2.waitKey(0) & 0xFF
                cv2.destroyWindow("Captured Image - Press 'y' to save or 'r' to retake")

                if key_confirm == ord('y'):
                    print(f"Processing {sequence[current_step]} face...")
                    patches = edge_impulse.extract_patches(cropped_frame)
                    predicted_colors = []

                    for i, patch in enumerate(patches):
                        # Send the raw patch to Edge Impulse for prediction
                        prediction = edge_impulse.get_prediction(patch)
                        if prediction:
                            predicted_color = prediction[0]
                            predicted_colors.append(predicted_color)
                            print(f"Patch {i+1}: Predicted: {predicted_color}")


                    save_colors(sequence[current_step], predicted_colors)
                    current_step += 1

                    if current_step >= len(sequence):
                        print("All faces scanned. Sending to solver...")
                        print("Final Cube Colors:", cube_state)
                        fig = plt.figure()
                        ax = fig.add_subplot(111, projection='3d')
                        cube_copy = cube_state.copy()
                        temp_left = cube_copy['Left']
                        cube_copy['Left'] = cube_copy['Right']
                        cube_copy['Right'] = temp_left
                        draw_cube(cube_copy)
                        if MODEL == 'optimal':
                            try:
                                print("cube state: ", cube_state)
                                correct_states = transform_cube_states(cube_state)

                                send_cube_state_to_solver(correct_states)
                            except Exception as e:
                                print(f"Error solving the cube: {e}")
                            finally:
                                cap.release()
                                cv2.destroyAllWindows()
                                break
                        elif MODEL == 'uppaal':
                            front_face, back_face, right_face, left_face, up_face, down_face = uppaal_cube_states(cube_state)
                            send_cube_to_uppaal(front_face, back_face, right_face, left_face, up_face, down_face)
                            cap.release()
                            cv2.destroyAllWindows()
                            break

                elif key_confirm == ord('r'):
                    print("Retaking the picture...")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Run the solving logic synchronously
        print("Starting cube solving...")
        scan_and_solve_cube()

        # Ensure stored_moves is initialized
        if stored_moves is None:
            raise ValueError("stored_moves is still None after solving. Cannot start server.")

        print("Cube solving complete. Starting the server...")
        piserver.run_http_server(moves_to_commands(stored_moves))
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Server terminated gracefully.")


