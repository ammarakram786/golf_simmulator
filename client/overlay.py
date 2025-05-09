import json
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class SessionOverlay:
    def __init__(self, root, app):
        self.app = app
        self.extension_asked = False
        self.remaining = None
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.geometry("300x100+{}+{}".format(self.win.winfo_screenwidth()-310, self.win.winfo_screenheight()-150))
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        self.label = tk.Label(self.win, text="", font=("Arial", 32), fg='white', bg='black')
        self.label.pack(expand=True, fill='both')
        self.running = False
        self.win.withdraw()

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

        if self.remaining <= 55:
            if not self.extension_asked:
                self.ask_extension()
            self.win.configure(bg='red')
            self.label.configure(bg='red')
        else:
            self.win.configure(bg='black')
            self.label.configure(bg='black')

        self.label.config(text=f"{mins:02}:{secs:02}")
        self.win.update()

        if self.remaining == 0:
            self.label.config(text="TIME'S UP")
            self.win.update()
            threading.Timer(5,self.lock_and_close).start()
            return

        self.remaining -= 1
        self.win.after(1000, self.update_timer)



    def ask_extension(self):
        if hasattr(self, 'extension_asked') and self.extension_asked:
            return
        self.extension_asked = True

        extension_win = tk.Toplevel(self.root)
        extension_win.title("Extend Session Duration")
        extension_win.geometry("300x250")
        extension_win.configure(bg="#f0f0f0")  # Light gray background

        # Title label
        title_label = tk.Label(
            extension_win,
            text="Extend Your Session",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=10)

        # Frame for radio buttons
        options_frame = tk.Frame(extension_win, bg="#f0f0f0")
        options_frame.pack(pady=10)

        var = tk.IntVar(value=30)
        options = [("6 minutes", 1), ("30 minutes", 30), ("1 hour", 60), ("1.5 hours", 90), ("2 hours", 120)]
        for label, val in options:
            tk.Radiobutton(
                options_frame,
                text=label,
                variable=var,
                value=val,
                bg="#f0f0f0",
                anchor="w"
            ).pack(anchor='w', padx=10)

        # Buttons
        button_frame = tk.Frame(extension_win, bg="#f0f0f0")
        button_frame.pack(pady=10)

        def confirm():
            minutes = var.get()
            extension_win.destroy()
            self.app.request_extension(minutes)
        def close():
            extension_win.destroy()

        ttk.Button(button_frame, text="Confirm", command=confirm).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=close).pack(side="left", padx=5)

    def extend_session(self, minutes):
        self.remaining += minutes * 60
        self.extension_asked = False

    def end_session(self):
        self.running = False
        self.win.withdraw()

    def lock_and_close(self):
        subprocess.call("rundll32.exe user32.dll,LockWorkStation")
        self.win.withdraw()
