from ttkbootstrap import Frame, Label, Button, Toplevel, Radiobutton, IntVar


from ttkbootstrap import Style

class ClientCard(Frame):
    def __init__(self, master, name, ip, sock, server):
        super().__init__(master, padding=10, relief='ridge', style="Red.TFrame")
        self.name, self.ip, self.sock, self.server = name, ip, sock, server

        # Define styles for status labels
        style = Style()
        style.configure("Green.TLabel", foreground="green", font=("Arial", 10, "bold"))
        style.configure("Red.TLabel", foreground="red", font=("Arial", 10, "bold"))

        # Labels for client information
        Label(self, text=f"Name: {name}").pack(anchor='w')
        Label(self, text=f"IP: {ip}").pack(anchor='w')

        # Status label on the right
        self.status = Label(self, text="Idle", style="Red.TLabel", anchor='e')
        self.status.pack(anchor='e', padx=10)

        # Buttons for actions
        # Button(self, text="Start Session", command=self.ask_duration).pack(side='left')
        # Button(self, text="End", command=self.end_session).pack(side='left')
        # Button(self, text="Lock", command=self.lock_now).pack(side='left')
        Button(self, text="Start Session", command=self.ask_duration).pack(side='left', padx=5)
        Button(self, text="End", command=self.end_session).pack(side='left', padx=5)
        Button(self, text="Lock", command=self.lock_now).pack(side='left', padx=5)

        self.update_status("Idle", connected=True)

    def update_status(self, status, connected):
        if connected:
            style = "Green.TLabel" if status == "Active" else "Red.TLabel"
        else:
            style = "Red.TLabel"
        self.status.config(text=status, style=style)

    def ask_duration(self):
        duration_win = Toplevel(self)
        duration_win.title("Select Session Duration")
        duration_win.geometry("250x200")
        var = IntVar(value=30)

        options = [("6 minutes", 1), ("30 minutes", 30), ("1 hour", 60), ("1.5 hours", 90), ("2 hours", 120)]
        for label, val in options:
            Radiobutton(duration_win, text=label, variable=var, value=val).pack(anchor='w')

        def confirm():
            minutes = var.get()
            self.start_session(minutes)
            duration_win.destroy()

        Button(duration_win, text="Start", command=confirm).pack(pady=10)

    def start_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "start", "minutes": minutes})
        self.update_status("Active", connected=True)

    def end_session(self):
        self.server.send_command(self.sock, {"cmd": "end"})
        self.update_status("Idle", connected=True)

    def lock_now(self):
        self.server.send_command(self.sock, {"cmd": "lock"})

    def disconnect(self):
        self.update_status("Disconnected", connected=False)