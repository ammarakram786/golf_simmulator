from functools import partial

from ttkbootstrap import Frame, Label, Button, Toplevel, Radiobutton, IntVar
from ttkbootstrap import Style

class ClientCard(Frame):
    def __init__(self, master, name, ip, sock, server):
        super().__init__(master, padding=10, relief='ridge', style="Red.TFrame")
        self.name, self.ip, self.sock, self.server = name, ip, sock, server

        # Define styles for status labels
        style = Style()
        style.configure("Green.TLabel", foreground="green", font=("Arial", 18, "bold"))
        style.configure("Red.TLabel", foreground="red", font=("Arial", 18, "bold"))
        style.configure("Custom.TButton", font=("Arial", 14, "bold"), padding=5)
        # Labels for client information
        Label(self, text=f"Name: {name}", font=("Arial", 20, "bold")).pack(anchor='w')
        Label(self, text=f"IP: {ip}", font=("Arial", 20, "bold")).pack(anchor='w')

        # Status label on the right
        self.status = Label(self, text="IDLE", style="Red.TLabel", anchor='e')
        self.status.pack(anchor='e', padx=10)

        # Apply the style to the buttons
        Button(self, text="Start Session", style="Custom.TButton",
               command=partial(self.ask_duration, action='start')).pack(side='left', padx=5)
        Button(self, text="+ ADD TIME", style="Custom.TButton",
               command=partial(self.ask_duration, action='add')).pack(side='left', padx=5)
        Button(self, text="- SUB TIME", style="Custom.TButton",
               command=partial(self.ask_duration, action='sub')).pack(side='left', padx=5)
        Button(self, text="End", style="Custom.TButton",
               command=self.end_session).pack(side='left', padx=5)
        Button(self, text="Lock", style="Custom.TButton",
               command=self.lock_now).pack(side='left', padx=5)
        self.update_status("IDLE", connected=True)

    def update_status(self, status, connected):
        if connected:
            style = "Green.TLabel" if status == "ACTIVE" else "Red.TLabel"
        else:
            style = "Red.TLabel"
        self.status.config(text=status, style=style)

    # def ask_duration(self, action):
    #     duration_win = Toplevel(self.name)
    #     duration_win.title("Select Session Duration")
    #     duration_win.geometry("250x200")
    #     var = IntVar(value=30)
    #
    #     options = [("6 minutes", 1), ("30 minutes", 30), ("1 hour", 60), ("1.5 hours", 90), ("2 hours", 120)]
    #     for label, val in options:
    #         Radiobutton(duration_win, text=label, variable=var, value=val).pack(anchor='w')
    #
    #     def confirm():
    #         minutes = var.get()
    #         if action == "add":
    #             self.add_session(minutes)
    #         elif action == "sub":
    #             self.subtract_session(minutes)
    #         elif action == "start":
    #             self.start_session(minutes)
    #         duration_win.destroy()
    #
    #     Button(duration_win, text="Start", command=confirm).pack(pady=10)

    def ask_duration(self, action):
        # Define styles
        style = Style()
        style.configure("Custom.TRadiobutton", font=("Arial", 12))
        style.configure("Custom.TButton", font=("Arial", 12, "bold"), padding=5)

        # Create the duration window
        duration_win = Toplevel(self.name)
        duration_win.title("Select Session Duration")
        duration_win.geometry("250x200")  # Light gray background

        var = IntVar(value=30)
        options = [("6 minutes", 1), ("30 minutes", 30), ("1 hour", 60), ("1.5 hours", 90), ("2 hours", 120)]
        for label, val in options:
            Radiobutton(
                duration_win,
                text=label,
                variable=var,
                value=val,
                style="Custom.TRadiobutton",
            ).pack(anchor='w', padx=10, pady=5)

        def confirm():
            minutes = var.get()
            if action == "add":
                self.add_session(minutes)
            elif action == "sub":
                self.subtract_session(minutes)
            elif action == "start":
                self.start_session(minutes)
            duration_win.destroy()

        Button(duration_win, text="Start", style="Custom.TButton", command=confirm).pack(pady=10)
    def start_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "start", "minutes": minutes})
        self.update_status("ACTIVE", connected=True)

    def add_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "add", "minutes": minutes})
        self.update_status("ACTIVE", connected=True)

    def subtract_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "sub", "minutes": minutes})
        self.update_status("ACTIVE", connected=True)


    def end_session(self):
        self.server.send_command(self.sock, {"cmd": "end"})
        self.update_status("IDLE", connected=True)

    def lock_now(self):
        self.server.send_command(self.sock, {"cmd": "lock"})

    def disconnect(self):
        self.update_status("Disconnected", connected=False)

    def handle_extension_request(self, minutes):
        style = Style()
        style.configure("Custom.TButton", font=("Arial", 14, "bold"), padding=5)
        request_win = Toplevel(self.name)
        request_win.title(f"Extension Request from {self.name}")  # Add PC name to the title
        request_win.geometry("500x150")



        Label(request_win, text=f"Client {self.name} requests {minutes} minutes extension.", font=("Arial", 16, "bold")).pack(pady=10)

        def approve():
            request_win.destroy()
            self.server.send_command(self.sock, {"cmd": "extend","approved": True, "minutes": minutes})

        def deny():
            request_win.destroy()
            self.server.send_command(self.sock, {"cmd": "extend","approved": True, "minutes": minutes})

        Button(request_win,style="Custom.TButton", text="Approve", command=approve).pack(side="left", padx=5)
        Button(request_win,style="Custom.TButton", text="Deny", command=deny).pack(side="left", padx=5)