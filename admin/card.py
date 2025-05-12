import tkinter as tk

from ttkbootstrap import Frame, Label, Toplevel, IntVar
from ttkbootstrap import Style


class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=60, bg="#2ecc71", fg="white", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg

        # Draw the rounded rectangle
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, radius=30, fill=bg, outline=bg)

        # Add text in the center
        self.text = self.create_text(
            width // 2, height // 2,
            text=text.upper(),  # Convert text to uppercase
            font=("Helvetica", 18, "bold"),  # Increased font size for touch
            fill=fg
        )

        # Bind events
        self.tag_bind(self.rect, "<Button-1>", self._on_click)
        self.tag_bind(self.text, "<Button-1>", self._on_click)
        self.tag_bind(self.rect, "<Enter>", self._on_enter)
        self.tag_bind(self.rect, "<Leave>", self._on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=30, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_enter(self, event):
        # Darken the color on hover
        r, g, b = self.winfo_rgb(self.bg)
        darker = f'#{int(r/256*0.8):02x}{int(g/256*0.8):02x}{int(b/256*0.8):02x}'
        self.itemconfig(self.rect, fill=darker, outline=darker)

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg, outline=self.bg)


class ClientCard(Frame):
    def __init__(self, master, name, ip, sock, server):
        super().__init__(master, padding=20)  # Increased padding
        self.name, self.ip, self.sock, self.server = name, ip, sock, server

        # Minty theme colors with additional button colors
        self.colors = {
            'primary': '#2ecc71',    # Mint green
            'secondary': '#272bae',  # Darker mint
            'warning': '#e74c3c',    # Red for warning
            'background': '#ffffff', # White
            'text': '#2c3e50',      # Dark blue-gray
            'light_text': '#ffffff', # White text
            'border': '#e0e0e0',    # Light gray for borders
            'success': '#2ecc71',   # Green for success
            'error': '#e74c3c',     # Red for error
            'info': '#3498db',      # Blue for info
            'purple': '#9b59b6',    # Purple for special actions
            'orange': '#e67e22',    # Orange for warnings
            'card_bg': '#f8f9fa'    # Light gray for card background
        }

        # Configure styles
        style = Style()
        
        # Card styles
        style.configure("Card.TFrame",
                       background=self.colors['card_bg'],
                       relief="flat",
                       borderwidth=1)
        
        # Label styles with increased font sizes for touch
        style.configure("Title.TLabel",
                       font=("Helvetica", 24, "bold"),  # Increased for touch
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Subtitle.TLabel",
                       font=("Helvetica", 20),  # Increased for touch
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Status.TLabel",
                       font=("Helvetica", 22, "bold"),  # Increased for touch
                       background=self.colors['card_bg'])
        
        style.configure("Success.TLabel",
                       foreground=self.colors['success'])
        
        style.configure("Error.TLabel",
                       foreground=self.colors['error'])

        # Apply card style
        self.configure(style="Card.TFrame")

        # Client info section with shadow effect
        info_frame = Frame(self, style="Card.TFrame")
        info_frame.pack(fill="x", pady=(0, 15))  # Increased padding

        # Name with icon-like styling
        name_frame = Frame(info_frame, style="Card.TFrame")
        name_frame.pack(fill="x", pady=(0, 10))  # Increased padding
        
        Label(name_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),  # Increased for touch
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        Label(name_frame, 
              text=f"NAME: {name.upper()}", 
              style="Title.TLabel").pack(side="left")

        # IP with icon-like styling
        ip_frame = Frame(info_frame, style="Card.TFrame")
        ip_frame.pack(fill="x")
        
        Label(ip_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),  # Increased for touch
              foreground=self.colors['info'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        Label(ip_frame, 
              text=f"IP: {ip}", 
              style="Subtitle.TLabel").pack(side="left")

        # Status label with badge-like styling
        self.status = Label(info_frame, 
                           text="IDLE", 
                           style="Status.TLabel",
                           anchor='e')
        self.status.pack(anchor='e', padx=15)  # Increased padding

        # Buttons frame with modern layout
        button_frame = Frame(self, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(15, 0))  # Increased padding

        # Action buttons with different colors
        actions = [
            ("START", self.ask_duration, self.colors['primary']),
            ("EDIT", self.handle_duration, self.colors['info']),
            # ("- SUB TIME", partial(self.ask_duration, action='sub'), self.colors['warning']),
            ("END", self.end_session, self.colors['purple']),
            ("LOCK", self.lock_now, self.colors['orange'])
        ]

        for text, command, color in actions:
            btn = RoundButton(button_frame,
                  text=text,
                  command=command,
                  bg=color,
                  width=200,  # Increased for touch
                  height=60)  # Increased for touch
            btn.pack(side='left', padx=8)  # Increased padding

        self.update_status("IDLE", connected=True)

    def update_status(self, status, connected):
        if connected:
            style = "Success.TLabel" if status == "ACTIVE" else "Error.TLabel"
        else:
            style = "Error.TLabel"
        self.status.configure(text=status.upper(), style=style)  # Convert status to uppercase

    def ask_duration(self):
        duration_win = Toplevel(self.name)
        duration_win.title("Select Session Duration")
        duration_win.geometry("600x400")

        # Make window modal and set focus
        duration_win.transient(self)
        duration_win.grab_set()
        duration_win.focus_set()

        # Center the window
        duration_win.update_idletasks()
        width = duration_win.winfo_width()
        height = duration_win.winfo_height()
        x = (duration_win.winfo_screenwidth() // 2) - (width // 2)
        y = (duration_win.winfo_screenheight() // 2) - (height // 2)
        duration_win.geometry(f'{width}x{height}+{x}+{y}')

        # Configure window style
        duration_win.configure(bg=self.colors['card_bg'])
        duration_win.attributes('-topmost', True)

        # Title with icon
        title_frame = Frame(duration_win, style="Card.TFrame")
        title_frame.pack(pady=30)

        Label(title_frame,
              text="⏱",
              font=("Helvetica", 32),
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 15))

        Label(title_frame,
              text="SELECT DURATION",
              font=("Helvetica", 28, "bold"),
              foreground=self.colors['text'],
              background=self.colors['card_bg']).pack(side="left")

        # Increment frame
        increment_frame = Frame(duration_win, style="Card.TFrame")
        increment_frame.pack(pady=20)

        # Variable to hold the time value
        time_var = IntVar(value=30)

        # Increment and decrement functions
        def increment():
            time_var.set(time_var.get() + 1)

        def decrement():
            if time_var.get() > 0:
                time_var.set(time_var.get() - 1)

        # Minus button
        minus_btn = RoundButton(increment_frame, text="-", command=decrement, bg=self.colors['secondary'], width=60,
                                height=60)
        minus_btn.pack(side="left", padx=10)

        # Disabled input field
        time_entry = tk.Entry(increment_frame, textvariable=time_var, font=("Helvetica", 18), width=5, justify="center",
                              state="disabled", disabledbackground=self.colors['card_bg'],
                              disabledforeground=self.colors['text'])
        time_entry.pack(side="left", padx=10)

        # Plus button
        plus_btn = RoundButton(increment_frame, text="+", command=increment, bg=self.colors['primary'], width=60,
                               height=60)
        plus_btn.pack(side="left", padx=10)

        # Button frame
        button_frame = Frame(duration_win, style="Card.TFrame")
        button_frame.pack(pady=30)

        def confirm():
            try:
                minutes = time_var.get()
                if minutes > 0:
                    self.start_session(minutes)
                    duration_win.destroy()
            except Exception as e:
                print(f"Error in duration selection: {e}")

        def cancel():
            duration_win.destroy()

        # Add confirm and cancel buttons
        confirm_btn = RoundButton(button_frame, text="CONFIRM", command=confirm, bg=self.colors['primary'], width=200,
                                  height=60)
        confirm_btn.pack(side="left", padx=15)

        cancel_btn = RoundButton(button_frame, text="CANCEL", command=cancel, bg=self.colors['warning'], width=200,
                                 height=60)
        cancel_btn.pack(side="left", padx=15)

        # Bind Enter key to confirm
        duration_win.bind('<Return>', lambda e: confirm())
        # Bind Escape key to cancel
        duration_win.bind('<Escape>', lambda e: cancel())

        # Wait for window to be destroyed
        self.wait_window(duration_win)

    def handle_duration(self):
        handle_duration_win = Toplevel(self.name)
        handle_duration_win.title("Edit Session Duration")
        handle_duration_win.geometry("700x400")

        # Make window modal and set focus
        handle_duration_win.transient(self)
        handle_duration_win.grab_set()
        handle_duration_win.focus_set()

        # Center the window
        handle_duration_win.update_idletasks()
        width = handle_duration_win.winfo_width()
        height = handle_duration_win.winfo_height()
        x = (handle_duration_win.winfo_screenwidth() // 2) - (width // 2)
        y = (handle_duration_win.winfo_screenheight() // 2) - (height // 2)
        handle_duration_win.geometry(f'{width}x{height}+{x}+{y}')

        # Configure window style
        handle_duration_win.configure(bg=self.colors['card_bg'])
        handle_duration_win.attributes('-topmost', True)

        # Title with icon
        title_frame = Frame(handle_duration_win, style="Card.TFrame")
        title_frame.pack(pady=30)

        Label(title_frame,
              text="⏱",
              font=("Helvetica", 32),
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 15))

        Label(title_frame,
              text="SELECT DURATION",
              font=("Helvetica", 28, "bold"),
              foreground=self.colors['text'],
              background=self.colors['card_bg']).pack(side="left")

        # Increment frame
        increment_frame = Frame(handle_duration_win, style="Card.TFrame")
        increment_frame.pack(pady=20)

        # Variable to hold the time value
        time_var = IntVar(value=30)

        # Increment and decrement functions
        def increment():
            time_var.set(time_var.get() + 1)

        def decrement():
            if time_var.get() > 0:
                time_var.set(time_var.get() - 1)

        # Minus button
        minus_btn = RoundButton(increment_frame, text="-", command=decrement, bg=self.colors['secondary'], width=60,
                                height=60)
        minus_btn.pack(side="left", padx=10)

        # Disabled input field
        time_entry = tk.Entry(increment_frame, textvariable=time_var, font=("Helvetica", 18), width=5, justify="center",
                              state="disabled", disabledbackground=self.colors['card_bg'],
                              disabledforeground=self.colors['text'])
        time_entry.pack(side="left", padx=10)

        # Plus button
        plus_btn = RoundButton(increment_frame, text="+", command=increment, bg=self.colors['primary'], width=60,
                               height=60)
        plus_btn.pack(side="left", padx=10)

        # Button frame
        button_frame = Frame(handle_duration_win, style="Card.TFrame")
        button_frame.pack(pady=30)

        def add():
            try:
                minutes = time_var.get()
                if minutes > 0:
                    self.add_session(minutes)
                    handle_duration_win.destroy()
            except Exception as e:
                print(f"Error in duration selection: {e}")
        def sub():
            try:
                minutes = time_var.get()
                if minutes > 0:
                    self.subtract_session(minutes)
                    handle_duration_win.destroy()
            except Exception as e:
                print(f"Error in duration selection: {e}")

        def cancel():
            handle_duration_win.destroy()

        # Add confirm and cancel buttons
        add_btn = RoundButton(button_frame, text="ADD", command=add, bg=self.colors['primary'], width=200,
                                  height=60)
        add_btn.pack(side="left", padx=15)

        sub_btn = RoundButton(button_frame, text="REMOVE", command=sub, bg=self.colors['info'], width=200,
                                  height=60)
        sub_btn.pack(side="left", padx=15)

        cancel_btn = RoundButton(button_frame, text="CANCEL", command=cancel, bg=self.colors['warning'], width=200,
                                 height=60)
        cancel_btn.pack(side="left", padx=15)

        # Bind Escape key to cancel
        handle_duration_win.bind('<Escape>', lambda e: cancel())

        # Wait for window to be destroyed
        self.wait_window(handle_duration_win)



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
        request_win = Toplevel(self.name)
        request_win.title(f"Extension Request from {self.name}")
        request_win.geometry("700x350")  # Increased window size
        
        # Center the window
        request_win.update_idletasks()
        width = request_win.winfo_width()
        height = request_win.winfo_height()
        x = (request_win.winfo_screenwidth() // 2) - (width // 2)
        y = (request_win.winfo_screenheight() // 2) - (height // 2)
        request_win.geometry(f'{width}x{height}+{x}+{y}')

        # Title with icon
        title_frame = Frame(request_win, style="Card.TFrame")
        title_frame.pack(pady=20)  # Increased padding
        
        Label(title_frame,
              text="⏰",  # Alarm clock emoji as icon
              font=("Helvetica", 32),  # Increased for touch
              foreground=self.colors['warning'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 15))
              
        Label(title_frame,
              text="EXTENSION REQUEST",
              font=("Helvetica", 28, "bold"),  # Increased for touch
              foreground=self.colors['text'],
              background=self.colors['card_bg']).pack(side="left")

        # Message
        Label(request_win,
              text=f"CLIENT {self.name.upper()} REQUESTS {minutes} MINUTES EXTENSION.",
              font=("Helvetica", 18),  # Increased for touch
              foreground=self.colors['text'],
              background=self.colors['card_bg']).pack(pady=20)  # Increased padding

        # Buttons frame
        button_frame = Frame(request_win, style="Card.TFrame")
        button_frame.pack(pady=30)  # Increased padding

        def approve():
            request_win.destroy()
            self.server.send_command(self.sock, {"cmd": "extend", "approved": True, "minutes": minutes})

        def deny():
            request_win.destroy()
            self.server.send_command(self.sock, {"cmd": "extend", "approved": False, "minutes": minutes})

        approve_btn = RoundButton(button_frame,
               text="APPROVE",
               command=approve,
               bg=self.colors['primary'],
               width=200,  # Increased for touch
               height=60)  # Increased for touch
        approve_btn.pack(side="left", padx=15)  # Increased padding

        deny_btn = RoundButton(button_frame,
               text="DENY",
               command=deny,
               bg=self.colors['warning'],
               width=200,  # Increased for touch
               height=60)  # Increased for touch
        deny_btn.pack(side="left", padx=15)  # Increased padding