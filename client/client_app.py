import ctypes
import json
import socket
import subprocess
import threading
import time
import tkinter as tk

from client.overlay import SessionOverlay

def block_input(block=True):
    ctypes.windll.user32.BlockInput(block)


class ClientApp:
    def __init__(self, server_ip, port, name):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.overlay = None
        self.root = None
        self.name = name

    def connect_to_server(self):
        while True:
            try:
                self.sock.connect((self.server_ip, self.port))
                break
            except ConnectionRefusedError:
                print("Server not available, retrying in 3 seconds...")
                time.sleep(3)
        # name = platform.node()
        ip = socket.gethostbyname(socket.gethostname())
        self.sock.send(json.dumps({"name": self.name, "ip": ip}).encode())

    def listen(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                data = json.loads(msg)
                print('message',msg)
                print('data',data)
                if data['cmd'] == 'start':
                    print('hi Start')
                    self.overlay.start_session(data['minutes'])
                elif data['cmd'] == 'add':
                    self.overlay.update_session(data['minutes'], add_type=True)
                elif data['cmd'] == 'sub':
                    self.overlay.update_session(data['minutes'], add_type=False)
                elif data['cmd'] == 'end':
                    self.overlay.end_session()
                elif data['cmd'] == 'lock':
                    subprocess.call("rundll32.exe user32.dll,LockWorkStation")
                # elif data['cmd'] == 'extend':
                #     if data.get('approved'):
                #         self.overlay.extend_session(data['minutes'])
                #         ModernMessageBox(self.root, "Success", "Admin accepted your extension request.", "✓", "#2ecc71")
                #     else:
                #         ModernMessageBox(self.root, "Notice", "Admin denied your extension request.", "✕", "#e74c3c")
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

    def end_session(self):
        try:
            self.sock.send(json.dumps({"cmd": "end"}).encode())
        except Exception as e:
            print(f"Error requesting end session: {e}")

