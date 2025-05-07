# admin_dashboard.py
import tkinter as tk
from tkinter import messagebox
import socket
import threading
import pickle
import os
from datetime import datetime, timedelta

# Server settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 12345

# Global variables
clients = {}  # {client_address: {"name": "PC-1", "status": "Idle", "time_left": 0}}

# Save schedules to a file
SCHEDULE_FILE = "schedules.pkl"

def save_schedules(schedules):
    with open(SCHEDULE_FILE, "wb") as f:
        pickle.dump(schedules, f)

def load_schedules():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "rb") as f:
            return pickle.load(f)
    return {}

# GUI for Admin Dashboard
class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Golf Simulator Admin Dashboard")
        self.schedules = load_schedules()

        # List of connected PCs
        self.pc_list = tk.Listbox(root, width=50, height=20)
        self.pc_list.pack(pady=10)

        # Control buttons
        self.start_btn = tk.Button(root, text="Start Session", command=self.start_session)
        self.start_btn.pack(pady=5)

        self.end_btn = tk.Button(root, text="End Session", command=self.end_session)
        self.end_btn.pack(pady=5)

        self.lock_btn = tk.Button(root, text="Lock Screen", command=self.lock_screen)
        self.lock_btn.pack(pady=5)

        # Start server thread
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Server started, waiting for connections...")
        while True:
            client_socket, client_address = server.accept()
            print(f"Connected to {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if data:
                    print(f"Received from {client_address}: {data}")
                    # Handle client messages here
        except ConnectionResetError:
            print(f"Client {client_address} disconnected")
        finally:
            client_socket.close()

    def start_session(self):
        selected_pc = self.get_selected_pc()
        if selected_pc:
            print(f"Starting session for {selected_pc}")
            # Send start session command to client

    def end_session(self):
        selected_pc = self.get_selected_pc()
        if selected_pc:
            print(f"Ending session for {selected_pc}")
            # Send end session command to client

    def lock_screen(self):
        selected_pc = self.get_selected_pc()
        if selected_pc:
            print(f"Locking screen for {selected_pc}")
            # Send lock screen command to client

    def get_selected_pc(self):
        try:
            return self.pc_list.get(self.pc_list.curselection())
        except tk.TclError:
            messagebox.showerror("Error", "No PC selected")
            return None

# Run the Admin Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()