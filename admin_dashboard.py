# admin_dashboard.py
import tkinter as tk
from tkinter import messagebox
import socket
import threading       
import pickle
import os
import time
from datetime import datetime, timedelta

# Server settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 9095

# Global variables and locks
clients_lock = threading.Lock()
clients = {}  # {client_address: {"socket": socket_obj, "name": "PC-1", "status": "Connected", "time_left": 0}}

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
        self.stopped = False

        # Frame for PC list with labels
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(list_frame, text="Connected PCs (Name | Status | IP)").pack(anchor=tk.W)
        
        # List of connected PCs with scrollbar
        list_container = tk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pc_list = tk.Listbox(list_container, width=50, height=20, yscrollcommand=scrollbar.set)
        self.pc_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.pc_list.yview)

        # Control buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="Start Session", command=self.start_session)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.end_btn = tk.Button(btn_frame, text="End Session", command=self.end_session)
        self.end_btn.pack(side=tk.LEFT, padx=5)

        self.lock_btn = tk.Button(btn_frame, text="Lock Screen", command=self.lock_screen)
        self.lock_btn.pack(side=tk.LEFT, padx=5)
        
        self.reconnect_btn = tk.Button(btn_frame, text="Refresh List", command=self.update_pc_list)
        self.reconnect_btn.pack(side=tk.LEFT, padx=5)
        
        # Start server thread
        threading.Thread(target=self.start_server, daemon=True).start()
        
        # Start update GUI thread
        threading.Thread(target=self.update_gui_periodically, daemon=True).start()

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"Server started on {HOST}:{PORT}, waiting for connections...")
        
        while not self.stopped:
            try:
                client_socket, client_address = server.accept()
                print(f"Connected to {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
            except Exception as e:
                print(f"Server accept error: {e}")
                if self.stopped:
                    break
                time.sleep(1)
        
        server.close()
        print("Server stopped")

    def handle_client(self, client_socket, client_address):
        """Handle a connected client"""
        # Check if this IP is already known
        existing_client = None
        ip = client_address[0]
        
        # Wait for client to send computer name
        try:
            # First message from client should be the computer name
            client_hostname = client_socket.recv(1024).decode().strip()
            if not client_hostname:
                client_hostname = f"PC-{len(clients) + 1}"
        except:
            client_hostname = f"PC-{len(clients) + 1}"
        
        print(f"Client {ip} identified as {client_hostname}")
        
        with clients_lock:
            # Check if this IP matches any known client
            for addr, client_data in clients.items():
                if addr[0] == ip:
                    existing_client = client_data
                    # Update the address with current one (with correct port)
                    del clients[addr]
                    break
            
            # If client is new, create entry
            if existing_client is None:
                clients[client_address] = {
                    "socket": client_socket,
                    "name": client_hostname,
                    "status": "Connected",
                    "time_left": 0
                }
            else:
                # Update existing client
                existing_client["socket"] = client_socket
                existing_client["status"] = "Connected"
                clients[client_address] = existing_client
        
        self.update_pc_list()
        
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Received from {client_address}: {data}")
                # Handle client messages here
        except ConnectionResetError:
            print(f"Client {client_address} disconnected")
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            with clients_lock:
                if client_address in clients:
                    clients[client_address]["socket"] = None
                    clients[client_address]["status"] = "Disconnected"
            
            self.update_pc_list()
            client_socket.close()

    def update_pc_list(self):
        """Update the PC list in GUI"""
        self.pc_list.delete(0, tk.END)
        with clients_lock:
            for addr, client in clients.items():
                status = client["status"]
                display_text = f"{client['name']} | {status} | {addr[0]}"
                self.pc_list.insert(tk.END, display_text)
                
                # Color code based on status
                if status == "Connected":
                    self.pc_list.itemconfig(tk.END, {'bg': '#d4ffcc'})  # Light green
                else:
                    self.pc_list.itemconfig(tk.END, {'bg': '#ffcccc'})  # Light red

    def update_gui_periodically(self):
        """Update GUI periodically to reflect connection status"""
        while not self.stopped:
            self.update_pc_list()
            time.sleep(5)

    def start_session(self):
        selected_index = self.get_selected_pc_index()
        if selected_index is not None:
            selected_text = self.pc_list.get(selected_index)
            client_name = selected_text.split(" | ")[0]
            
            with clients_lock:
                for addr, client in clients.items():
                    if client["name"] == client_name:
                        if client["socket"] and client["status"] == "Connected":
                            try:
                                client["socket"].send("START_SESSION".encode())
                                messagebox.showinfo("Success", f"Started session for {client_name}")
                            except:
                                messagebox.showerror("Error", f"Failed to send command to {client_name}")
                        else:
                            messagebox.showerror("Error", f"Client {client_name} is not connected")
                        break

    def end_session(self):
        selected_index = self.get_selected_pc_index()
        if selected_index is not None:
            selected_text = self.pc_list.get(selected_index)
            client_name = selected_text.split(" | ")[0]
            
            with clients_lock:
                for addr, client in clients.items():
                    if client["name"] == client_name:
                        if client["socket"] and client["status"] == "Connected":
                            try:
                                client["socket"].send("END_SESSION".encode())
                                messagebox.showinfo("Success", f"Ended session for {client_name}")
                            except:
                                messagebox.showerror("Error", f"Failed to send command to {client_name}")
                        else:
                            messagebox.showerror("Error", f"Client {client_name} is not connected")
                        break

    def lock_screen(self):
        selected_index = self.get_selected_pc_index()
        if selected_index is not None:
            selected_text = self.pc_list.get(selected_index)
            client_name = selected_text.split(" | ")[0]
            
            with clients_lock:
                for addr, client in clients.items():
                    if client["name"] == client_name:
                        if client["socket"] and client["status"] == "Connected":
                            try:
                                client["socket"].send("LOCK_SCREEN".encode())
                                messagebox.showinfo("Success", f"Locked screen for {client_name}")
                            except:
                                messagebox.showerror("Error", f"Failed to send command to {client_name}")
                        else:
                            messagebox.showerror("Error", f"Client {client_name} is not connected")
                        break

    def get_selected_pc_index(self):
        """Get the index of the selected PC in the list"""
        try:
            return self.pc_list.curselection()[0]
        except (tk.TclError, IndexError):
            messagebox.showerror("Error", "No PC selected")
            return None

# Run the Admin Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")  # Set initial window size
    app = AdminDashboard(root)
    
    def on_closing():
        app.stopped = True
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()