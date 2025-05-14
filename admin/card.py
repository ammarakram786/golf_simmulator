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
        self.remaining_time = 0

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

        # Main container frame
        main_frame = Frame(self, style="Card.TFrame")
        main_frame.pack(fill="x", expand=True)

        # Left side - Client info
        info_frame = Frame(main_frame, style="Card.TFrame")
        info_frame.pack(side="left", fill="y", padx=(0, 20))

        # Name with icon-like styling
        name_frame = Frame(info_frame, style="Card.TFrame")
        name_frame.pack(fill="x", pady=(0, 10))
        
        Label(name_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        Label(name_frame, 
              text=f"NAME: {name.upper()}", 
              style="Title.TLabel").pack(side="left")

        # IP with icon-like styling
        ip_frame = Frame(info_frame, style="Card.TFrame")
        ip_frame.pack(fill="x", pady=(0, 10))
        
        Label(ip_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),
              foreground=self.colors['info'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        Label(ip_frame, 
              text=f"IP: {ip}", 
              style="Subtitle.TLabel").pack(side="left")

        # Timer with icon-like styling
        timer_frame = Frame(info_frame, style="Card.TFrame")
        timer_frame.pack(fill="x", pady=(0, 10))
        
        Label(timer_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        self.timer_label = Label(timer_frame,
                                text="00:00",
                                font=("Helvetica", 48, "bold"),
                                foreground=self.colors['text'],
                                background=self.colors['card_bg'])
        self.timer_label.pack(side="left")

        # Status with icon-like styling
        status_frame = Frame(info_frame, style="Card.TFrame")
        status_frame.pack(fill="x", pady=(0, 10))
        
        Label(status_frame, 
              text="●",  # Bullet point as icon
              font=("Helvetica", 20),
              foreground=self.colors['info'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 10))
              
        self.status = Label(status_frame, 
                           text="IDLE", 
                           style="Status.TLabel")
        self.status.pack(side="left")

        # Right side - Timer controls
        control_frame = Frame(main_frame, style="Card.TFrame")
        control_frame.pack(side="right", fill="y")

        # Start/Stop buttons
        button_frame = Frame(control_frame, style="Card.TFrame")
        button_frame.pack(pady=(0, 20))

        # Start button with green border
        start_btn = RoundButton(button_frame,
                              text="START",
                              command=lambda: self.add_session(60),
                              bg=self.colors['primary'],
                              width=300,
                              height=100)
        start_btn.pack(side="left", padx=20)

        # Stop button with red border
        stop_btn = RoundButton(button_frame,
                             text="STOP",
                             command=self.end_session,
                             bg=self.colors['warning'],
                             width=300,
                             height=100)
        stop_btn.pack(side="left", padx=20)

        # Time increment frame
        increment_frame = Frame(control_frame, style="Card.TFrame")
        increment_frame.pack()

        # First row (60 minutes)
        row_frame1 = Frame(increment_frame, style="Card.TFrame")
        row_frame1.pack(pady=10)

        minus_btn1 = RoundButton(row_frame1,
                               text="-",
                               command=lambda: self.subtract_session(60),
                               bg=self.colors['warning'],
                               width=80,
                               height=80)
        minus_btn1.pack(side="left", padx=10)

        time_label1 = Label(row_frame1,
                          text="60 MIN",
                          font=("Helvetica", 24, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8)
        time_label1.pack(side="left", padx=20)

        plus_btn1 = RoundButton(row_frame1,
                              text="+",
                              command=lambda: self.add_session(60),
                              bg=self.colors['primary'],
                              width=80,
                              height=80)
        plus_btn1.pack(side="left", padx=10)

        # Second row (30 minutes)
        row_frame2 = Frame(increment_frame, style="Card.TFrame")
        row_frame2.pack(pady=10)

        minus_btn2 = RoundButton(row_frame2,
                               text="-",
                               command=lambda: self.subtract_session(30),
                               bg=self.colors['warning'],
                               width=80,
                               height=80)
        minus_btn2.pack(side="left", padx=10)

        time_label2 = Label(row_frame2,
                          text="30 MIN",
                          font=("Helvetica", 24, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8)
        time_label2.pack(side="left", padx=20)

        plus_btn2 = RoundButton(row_frame2,
                              text="+",
                              command=lambda: self.add_session(30),
                              bg=self.colors['primary'],
                              width=80,
                              height=80)
        plus_btn2.pack(side="left", padx=10)

        # Third row (1 minute)
        row_frame3 = Frame(increment_frame, style="Card.TFrame")
        row_frame3.pack(pady=10)

        minus_btn3 = RoundButton(row_frame3,
                               text="-",
                               command=lambda: self.subtract_session(1),
                               bg=self.colors['warning'],
                               width=80,
                               height=80)
        minus_btn3.pack(side="left", padx=10)

        time_label3 = Label(row_frame3,
                          text="1 MIN",
                          font=("Helvetica", 24, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8)
        time_label3.pack(side="left", padx=20)

        plus_btn3 = RoundButton(row_frame3,
                              text="+",
                              command=lambda: self.add_session(1),
                              bg=self.colors['primary'],
                              width=80,
                              height=80)
        plus_btn3.pack(side="left", padx=10)

        self.update_status("IDLE", connected=True)


    def update_timer(self):
        if self.remaining_time <= 0:
            self.timer_label.configure(text="00:00")
            self.timer_label.update()
            return
        mins, secs = divmod(self.remaining_time, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        self.timer_label.update()
        self.remaining_time -= 1
        if self.remaining_time >= 0:  # Changed condition to include zero
            self.timer_label.after(1000, self.update_timer)

    def update_status(self, status, connected):
        if connected:
            style = "Success.TLabel" if status == "ACTIVE" else "Error.TLabel"
        else:
            style = "Error.TLabel"
        self.status.configure(text=status.upper(), style=style)  # Convert status to uppercase

    def ask_duration(self):
        duration_win = Toplevel(self.master)
        duration_win.title("Select Session Duration")
        
        # Set initial size
        window_width = 600
        window_height = 400
        
        # Configure window style first
        duration_win.configure(bg=self.colors['card_bg'])
        duration_win.attributes('-topmost', True)
        
        # Make window modal and set focus
        duration_win.transient(self.master)
        duration_win.grab_set()
        duration_win.focus_set()
        
        # Force window to update and get screen dimensions
        duration_win.update_idletasks()
        
        # Get screen dimensions
        screen_width = duration_win.winfo_screenwidth()
        screen_height = duration_win.winfo_screenheight()
        
        # Calculate position for center of screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position and size in one call
        duration_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Prevent window from being resized
        duration_win.resizable(False, False)

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
        handle_duration_win = Toplevel(self.master)
        handle_duration_win.title("Edit Session Duration")
        
        # Set initial size
        window_width = 700
        window_height = 400
        
        # Configure window style first
        handle_duration_win.configure(bg=self.colors['card_bg'])
        handle_duration_win.attributes('-topmost', True)
        
        # Make window modal and set focus
        handle_duration_win.transient(self.master)
        handle_duration_win.grab_set()
        handle_duration_win.focus_set()
        
        # Force window to update and get screen dimensions
        handle_duration_win.update_idletasks()
        
        # Get screen dimensions
        screen_width = handle_duration_win.winfo_screenwidth()
        screen_height = handle_duration_win.winfo_screenheight()
        
        # Calculate position for center of screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position and size in one call
        handle_duration_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Prevent window from being resized
        handle_duration_win.resizable(False, False)

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
        self.remaining_time = minutes * 60  # Set the time directly
        self.update_timer()  # Start the timer

    def add_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "add", "minutes": minutes})
        self.update_status("ACTIVE", connected=True)
        self.remaining_time += minutes * 60
        if self.remaining_time == minutes * 60:  # If this is the first time being set
            self.update_timer()  # Start the timer

    def subtract_session(self, minutes):
        self.server.send_command(self.sock, {"cmd": "sub", "minutes": minutes})
        self.update_status("ACTIVE", connected=True)
        self.remaining_time = max(0, self.remaining_time - minutes * 60)  # Ensure time doesn't go negative
        if self.remaining_time == 0:
            self.timer_label.configure(text="00:00")
            self.timer_label.update()
            self.update_status("IDLE", connected=True)  # Update status when time reaches zero

    def end_session(self):
        self.server.send_command(self.sock, {"cmd": "end"})
        self.update_status("IDLE", connected=True)
        self.remaining_time = 0
        self.timer_label.configure(text="00:00")
        self.timer_label.update()

    def lock_now(self):
        self.server.send_command(self.sock, {"cmd": "lock"})

    def disconnect(self):
        self.update_status("Disconnected", connected=False)

    def handle_extension_request(self, minutes):
        request_win = Toplevel(self.master)
        request_win.title(f"Extension Request from {self.name}")
        
        # Set initial size
        window_width = 600
        window_height = 350
        
        # Configure window style first
        request_win.configure(bg=self.colors['background'])
        request_win.attributes('-topmost', True)
        
        # Make window modal and set focus
        request_win.transient(self.master)
        request_win.grab_set()
        request_win.focus_set()
        
        # Force window to update and get screen dimensions
        request_win.update_idletasks()
        
        # Get screen dimensions
        screen_width = request_win.winfo_screenwidth()
        screen_height = request_win.winfo_screenheight()
        
        # Calculate position for center of screen
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window position and size in one call
        request_win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Prevent window from being resized
        # request_win.resizable(False, False)

        # Title with icon
        title_frame = Frame(request_win, style="Card.TFrame")
        title_frame.pack(pady=20)
        
        Label(title_frame,
              text="⏰",  # Alarm clock emoji as icon
              font=("Helvetica", 32),
              foreground=self.colors['warning'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 15))
              
        Label(title_frame,
              text="EXTENSION REQUEST",
              font=("Helvetica", 28, "bold"),
              foreground=self.colors['text'],
              background=self.colors['card_bg']).pack(side="left")

        # Message frame with modern styling
        message_frame = Frame(request_win, style="Card.TFrame")
        message_frame.pack(fill="x", padx=40, pady=20)

        # Client name with highlight
        name_label = Label(message_frame,
                          text=f"CLIENT: {self.name.upper()}",
                          font=("Helvetica", 20, "bold"),
                          foreground=self.colors['primary'],
                          background=self.colors['card_bg'])
        name_label.pack(anchor='w', pady=(0, 10))

        # Duration request with highlight
        duration_label = Label(message_frame,
                             text=f"REQUESTING: {minutes} MINUTES",
                             font=("Helvetica", 20, "bold"),
                             foreground=self.colors['info'],
                             background=self.colors['card_bg'])
        duration_label.pack(anchor='w')

        # Buttons frame
        button_frame = Frame(request_win, style="Card.TFrame")
        button_frame.pack(pady=30)

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
               width=200,
               height=60)
        approve_btn.pack(side="left", padx=15)

        deny_btn = RoundButton(button_frame,
               text="DENY",
               command=deny,
               bg=self.colors['warning'],
               width=200,
               height=60)
        deny_btn.pack(side="left", padx=15)



        