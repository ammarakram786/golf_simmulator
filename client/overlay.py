import tkinter as tk

import threading
import time
import subprocess

class SessionOverlay:
    def __init__(self, root):
        self.remaining = None
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.attributes('-fullscreen', True)
        self.win.attributes('-topmost', True)
        self.label = tk.Label(self.win, text="", font=("Arial", 80), fg='white', bg='black')
        self.label.pack(expand=True)
        self.running = False

    def start_session(self, minutes):
        self.remaining = minutes * 60
        self.running = True
        self.win.deiconify()
        self.win.configure(bg='black')
        self.update_timer()

    def update_timer(self):
        if not self.running:
            return
        mins, secs = divmod(self.remaining, 60)
        self.label.config(text=f"{mins:02}:{secs:02}")
        if self.remaining <= 300:
            self.win.configure(bg='red')
        if self.remaining == 0:
            self.label.config(text="TIME'S UP")
            threading.Timer(300, lambda: subprocess.call("rundll32.exe user32.dll,LockWorkStation")).start()
            return
        self.remaining -= 1
        self.win.after(1000, self.update_timer)

    def end_session(self):
        self.running = False
        self.win.withdraw()