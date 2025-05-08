# simulator_client.py
import socket
import threading
import tkinter as tk
import os
import time
from datetime import datetime, timedelta

# Server settings
SERVER_HOST = "192.168.1.100"  # Replace with Admin Dashboard's IP
SERVER_PORT = 9095

# Global variables
session_active = False
time_left = 0

# Connect to the server
def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server")
    threading.Thread(target=listen_to_server, args=(client,), daemon=True).start()
    return client

def listen_to_server(client):
    global session_active, time_left
    try:
        while True:
            data = client.recv(1024).decode()
            if data:
                print(f"Received from server: {data}")
                # Handle commands from server
    except ConnectionResetError:
        print("Disconnected from server")
    finally:
        client.close()

# GUI for countdown timer
class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Timer")
        self.label = tk.Label(root, text="Waiting for session...", font=("Arial", 24))
        self.label.pack(pady=20)

        # Update timer every second
        self.update_timer()

    def update_timer(self):
        global session_active, time_left
        if session_active:
            if time_left > 0:
                self.label.config(text=f"Time Left: {time_left} seconds")
                time_left -= 1
            else:
                self.label.config(text="Time's Up!")
                session_active = False
                lock_workstation()
        self.root.after(1000, self.update_timer)

def lock_workstation():
    os.system("rundll32.exe user32.dll,LockWorkStation")

# Run the Simulator Client
if __name__ == "__main__":
    client_socket = connect_to_server()
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()