import tkinter as tk
from tkinter import messagebox
import socket
import threading
import platform
import json
import subprocess
from overlay import SessionOverlay
from tkinter import ttk

class ModernMessageBox(tk.Toplevel):
    def __init__(self, parent, title, message, icon="✓", color="#2ecc71"):
        super().__init__(parent)
        self.title(title)
        
        # Configure window
        self.geometry("400x200")
        self.configure(bg='#ffffff')
        self.attributes('-topmost', True)
        
        # Remove window decorations
        self.overrideredirect(True)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Main frame
        main_frame = tk.Frame(self, bg='#ffffff', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Icon
        icon_label = tk.Label(
            main_frame,
            text=icon,
            font=("Helvetica", 40),
            fg=color,
            bg='#ffffff'
        )
        icon_label.pack(pady=(0, 10))
        
        # Message
        message_label = tk.Label(
            main_frame,
            text=message,
            font=("Helvetica", 16, "bold"),
            fg='#2c3e50',
            bg='#ffffff',
            wraplength=350
        )
        message_label.pack(pady=(0, 20))
        
        # OK button
        ok_button = tk.Button(
            main_frame,
            text="OK",
            font=("Helvetica", 14, "bold"),
            fg='white',
            bg=color,
            relief='flat',
            padx=30,
            pady=10,
            command=self.destroy
        )
        ok_button.pack()
        
        # Add hover effect
        ok_button.bind('<Enter>', lambda e: ok_button.configure(bg=self._darken_color(color)))
        ok_button.bind('<Leave>', lambda e: ok_button.configure(bg=color))
        
        # Auto close after 3 seconds
        self.after(3000, self.destroy)
    
    def _darken_color(self, color):
        # Convert hex to RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        
        # Darken by 20%
        r = int(r * 0.8)
        g = int(g * 0.8)
        b = int(b * 0.8)
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'

class ClientApp:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.overlay = None
        self.root = None

    def connect_to_server(self):
        self.sock.connect((self.server_ip, self.port))
        name = platform.node()
        ip = socket.gethostbyname(socket.gethostname())
        self.sock.send(json.dumps({"name": name, "ip": ip}).encode())

    def listen(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                data = json.loads(msg)
                if data['cmd'] == 'start':
                    self.overlay.start_session(data['minutes'])
                elif data['cmd'] == 'add':
                    self.overlay.update_session(data['minutes'], add_type=True)
                elif data['cmd'] == 'sub':
                    self.overlay.update_session(data['minutes'], add_type=False)
                elif data['cmd'] == 'end':
                    self.overlay.end_session()
                elif data['cmd'] == 'lock':
                    subprocess.call("rundll32.exe user32.dll,LockWorkStation")
                elif data['cmd'] == 'extend':
                    if data.get('approved'):
                        self.overlay.extend_session(data['minutes'])
                        ModernMessageBox(self.root, "Success", "Admin accepted your extension request.", "✓", "#2ecc71")
                    else:
                        ModernMessageBox(self.root, "Notice", "Admin denied your extension request.", "✕", "#e74c3c")
            except Exception as e:
                print("Error receiving data from server.", e)
                break

    def run(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.overlay = SessionOverlay(self.root, self)  # Pass the app instance

        self.connect_to_server()

        threading.Thread(target=self.listen, daemon=True).start()
        self.root.mainloop()

    def request_extension(self, minutes):
        try:
            self.sock.send(json.dumps({"cmd": "extend_request", "minutes": minutes}).encode())
        except Exception as e:
            print(f"Error requesting extension: {e}")

    def end_session(self):
        try:
            self.sock.send(json.dumps({"cmd": "end"}).encode())
        except Exception as e:
            print(f"Error requesting end session: {e}")

