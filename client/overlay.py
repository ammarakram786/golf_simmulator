import json
import subprocess
import threading
import tkinter as tk


class SessionOverlay:
    def __init__(self, root):
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
        dlg = tk.Toplevel(self.root)
        dlg.title("Extend Session")
        tk.Label(dlg, text="Extend session by (minutes):").pack(pady=5)
        entry = tk.Entry(dlg)
        entry.pack(pady=5)

        def request_extend():
            try:
                minutes = int(entry.get())
                self.sock.send(json.dumps({"cmd": "extend_request", "minutes": minutes}).encode())
                dlg.destroy()
            except:
                pass

        tk.Button(dlg, text="Request", command=request_extend).pack(pady=5)

    def extend_session(self, minutes):
        self.remaining += minutes * 60
        self.extension_asked = False

    def end_session(self):
        self.running = False
        self.win.withdraw()

    def lock_and_close(self):
        subprocess.call("rundll32.exe user32.dll,LockWorkStation")
        self.win.withdraw()
