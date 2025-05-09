import tkinter as tk
from tkinter import messagebox
import socket
import threading
import platform
import json
import subprocess
from overlay import SessionOverlay

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
                elif data['cmd'] == 'end':
                    self.overlay.end_session()
                elif data['cmd'] == 'lock':
                    subprocess.call("rundll32.exe user32.dll,LockWorkStation")
                elif data['cmd'] == 'extend':
                    if data.get('approved'):
                        self.overlay.extend_session(data['minutes'])
                        tk.messagebox.showinfo("Info", "Admin Accepted your extension request.")
                    else:
                        tk.messagebox.showinfo("Info", "Admin denied your extension request.")
            except:
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

