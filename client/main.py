import tkinter as tk

import socket, threading, platform, json, time, subprocess
from overlay import SessionOverlay

SERVER_IP = '127.0.0.1'  # Replace with actual admin IP
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, PORT))

name = platform.node()
ip = socket.gethostbyname(socket.gethostname())
sock.send(json.dumps({"name": name, "ip": ip}).encode())

root = tk.Tk()
root.withdraw()

overlay = SessionOverlay(root)


def listen():
    while True:
        msg = sock.recv(1024).decode()
        data = json.loads(msg)
        if data['cmd'] == 'start':
            overlay.start_session(data['minutes'])
        elif data['cmd'] == 'end':
            overlay.end_session()
        elif data['cmd'] == 'lock':
            subprocess.call("rundll32.exe user32.dll,LockWorkStation")

threading.Thread(target=listen, daemon=True).start()
root.mainloop()
