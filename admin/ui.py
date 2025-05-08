import tkinter as tk
from ttkbootstrap import Frame, Label, Button, Toplevel, Radiobutton, IntVar
import time

class AdminDashboard(Frame):
    def __init__(self, master, server):
        super().__init__(master)
        self.server = server
        self.server.ui = self
        self.cards = {}

    def add_client(self, addr, sock, info):
        card = ClientCard(self, info['name'], info['ip'], sock, self.server)
        card.pack(pady=10, padx=10, fill='x')
        self.cards[addr] = card

class ClientCard(Frame):
    def __init__(self, master, name, ip, sock, server):
        super().__init__(master, padding=10, relief='ridge')
        self.name, self.ip, self.sock, self.server = name, ip, sock, server
        self.status = Label(self, text="Idle")
        Label(self, text=f"Name: {name}").pack(anchor='w')
        Label(self, text=f"IP: {ip}").pack(anchor='w')
        self.status.pack(anchor='w')
        Button(self, text="Start Session", command=self.ask_duration).pack(side='left')
        Button(self, text="End", command=self.end_session).pack(side='left')
        Button(self, text="Lock", command=self.lock_now).pack(side='left')

    def ask_duration(self):
        duration_win = Toplevel(self)
        duration_win.title("Select Session Duration")
        duration_win.geometry("250x200")
        var = IntVar(value=30)

        options = [("30 minutes", 30), ("1 hour", 60), ("1.5 hours", 90), ("2 hours", 120)]
        for label, val in options:
            Radiobutton(duration_win, text=label, variable=var, value=val).pack(anchor='w')

        def confirm():
            minutes = var.get()
            self.start_session(minutes)
            duration_win.destroy()

        Button(duration_win, text="Start", command=confirm).pack(pady=10)

    def start_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "start", "minutes": minutes})
        self.status.config(text="Active")

    def end_session(self):
        self.server.send_command(self.sock, {"cmd": "end"})
        self.status.config(text="Idle")

    def lock_now(self):
        self.server.send_command(self.sock, {"cmd": "lock"})

