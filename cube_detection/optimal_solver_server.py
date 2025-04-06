import socket
import os
import ast
import threading
import json
from dotenv import load_dotenv
from cube_model import RubiksCube

load_dotenv()

port = int(os.getenv('PORT'))
host = os.getenv('IP_ADDRESS')

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                response = {'error': 'Invalid request format'}

            request = json.loads(data)
            print(f"Received from {addr}: {request}")

            cube_state = request['message']
            matrix = ast.literal_eval(cube_state)
            print(matrix)

            cube = RubiksCube()
            cube.set_cube_state(matrix)
            moves = cube.solve_cube()

            if 'message' in request:
                response = {'response': moves}
            else:
                response = {'error': 'Invalid request format'}

            conn.send(json.dumps(response).encode('utf-8'))
        except (ConnectionResetError, json.JSONDecodeError):
            break

    print(f"Connection with {addr} closed")
    conn.close()

def start_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == '__main__':
    start_server()
