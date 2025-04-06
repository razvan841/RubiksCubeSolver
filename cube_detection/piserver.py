import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HTTP_PORT = 8080

class MyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, motor_commands, *args, **kwargs):
        self.motor_commands = motor_commands
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Convert the commands to JSON
        response = json.dumps(self.motor_commands)

        # Send the response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode())
        print(f"Served a request with response: {response}")

def run_http_server(motor_commands):
    print(f"Starting HTTP server on port {HTTP_PORT}...")
    handler = lambda *args, **kwargs: MyRequestHandler(motor_commands, *args, **kwargs)
    server = HTTPServer(("0.0.0.0", HTTP_PORT), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("HTTP server stopped.")

if __name__ == "__main__":
    print("Setting up the Wi-Fi network and HTTP server...")
    motor_commands = [
        [1, 1, 2],  # Motor 1, forward, 2x 90-degree turns
        [2, 0, 3],  # Motor 2, reverse, 3x 90-degree turns
    ]
    run_http_server(motor_commands)