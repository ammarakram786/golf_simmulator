import tkinter as tk

from ttkbootstrap import Frame, Label, Toplevel, IntVar
from ttkbootstrap import Style


class RoundButton(tk.Canvas):

    def __init__(self, parent, text, command=None, width=200, height=60, bg="#2ecc71", fg="#000000", hover_bg=None, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        if hover_bg is None:
            self.hover_bg = self._darken_color(bg, 0.15)
        else:
            self.hover_bg = hover_bg

        # Draw rounded rectangle button with very minimal radius
        radius = min(2, height // 12)  # Very minimal border radius - almost square
        self.rect = self.create_round_rectangle(0, 0, width, height, radius, fill=bg, outline=bg)

        # Add text in the center
        font_size = max(8, min(16, width // 8))  # Dynamic font size based on button width
        self.text = self.create_text(
            width // 2, height // 2,
            text=text.upper(),  # Convert text to uppercase
            font=("Helvetica", font_size, "bold"),
            fill=fg
        )

        # Bind events
        self.tag_bind(self.rect, "<Button-1>", self._on_click)
        self.tag_bind(self.text, "<Button-1>", self._on_click)
        self.tag_bind(self.rect, "<Enter>", self._on_hover)
        self.tag_bind(self.text, "<Enter>", self._on_hover)
        self.tag_bind(self.rect, "<Leave>", self._on_leave)
        self.tag_bind(self.text, "<Leave>", self._on_leave)

    def create_round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle"""
        points = []
        # Top edge
        points.extend([x1 + radius, y1, x2 - radius, y1])
        # Top right corner
        points.extend([x2, y1, x2, y1 + radius])
        # Right edge
        points.extend([x2, y1 + radius, x2, y2 - radius])
        # Bottom right corner
        points.extend([x2, y2, x2 - radius, y2])
        # Bottom edge
        points.extend([x2 - radius, y2, x1 + radius, y2])
        # Bottom left corner
        points.extend([x1, y2, x1, y2 - radius])
        # Left edge
        points.extend([x1, y2 - radius, x1, y1 + radius])
        # Top left corner
        points.extend([x1, y1, x1 + radius, y1])
        
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_hover(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)

    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg, outline=self.hover_bg)

    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg, outline=self.bg)


class ClientCard(Frame):
    def __init__(self, master, name, ip, sock, server):
        super().__init__(master, padding=20)
        self.name, self.ip, self.sock, self.server = name, ip, sock, server
        self.remaining_time = 0

        # New color palette based on design specifications
        self.colors = {
            'primary': '#4CAF50',    # Green for active/start buttons
            'secondary': '#43A047',  # Darker green for hover
            'warning': '#E53935',    # Red for lock/error
            'background': '#1E1E1E', # Dark charcoal gray main background
            'text': '#FFFFFF',      # White main text
            'light_text': '#CCCCCC', # Light gray secondary text
            'border': '#2A2A2A',    # Dark gray card border color
            'success': '#4CAF50',   # Green for success/active
            'error': '#E53935',     # Red for error/locked
            'info': '#FFB300',      # Amber yellow for time buttons
            'purple': '#9b59b6',    # Purple for special actions
            'orange': '#FFA000',    # Darker amber for hover
            'card_bg': '#2A2A2A',   # Dark gray for card background
            'timer_text': '#FFFFFF', # White for timer numbers
            'timer_label': '#AAAAAA' # Light gray for "Remaining" label
        }

        # Configure styles
        style = Style()
        
        # Card styles with rounded corners
        style.configure("Card.TFrame",
                       background=self.colors['card_bg'],
                       relief="flat",
                       borderwidth=0)
        
        # Create a custom rounded frame
        self.configure(style="Card.TFrame", padding=20)
        self.configure(width=420, height=320)  # Wider and shorter for more rectangular shape
        self.pack_propagate(False)  # Prevent card from resizing
        
        # Add rounded corners effect using a canvas overlay
        self.canvas_overlay = tk.Canvas(self, highlightthickness=0, bg=self.colors['card_bg'])
        self.canvas_overlay.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Add the create_round_rectangle method to canvas
        def create_round_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
            points = []
            # Top edge
            points.extend([x1 + radius, y1, x2 - radius, y1])
            # Top right corner
            points.extend([x2, y1, x2, y1 + radius])
            # Right edge
            points.extend([x2, y1 + radius, x2, y2 - radius])
            # Bottom right corner
            points.extend([x2, y2, x2 - radius, y2])
            # Bottom edge
            points.extend([x2 - radius, y2, x1 + radius, y2])
            # Bottom left corner
            points.extend([x1, y2, x1, y2 - radius])
            # Left edge
            points.extend([x1, y2 - radius, x1, y1 + radius])
            # Top left corner
            points.extend([x1, y1, x1 + radius, y1])
            return canvas.create_polygon(points, smooth=True, **kwargs)
        
        # Draw rounded rectangle background with very subtle radius
        create_round_rectangle(self.canvas_overlay, 0, 0, 420, 320, 3, 
                              fill=self.colors['card_bg'], 
                              outline=self.colors['border'], 
                              width=1)
        
        # Label styles
        style.configure("Title.TLabel",
                       font=("Helvetica", 14, "bold"),
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Subtitle.TLabel",
                       font=("Helvetica", 12),
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Status.TLabel",
                       font=("Helvetica", 14, "bold"),
                       background=self.colors['card_bg'])
        
        style.configure("Success.TLabel",
                       foreground=self.colors['success'])
        
        style.configure("Error.TLabel",
                       foreground=self.colors['error'])

        # Apply card style with fixed size
        self.configure(style="Card.TFrame", padding=20)
        self.configure(width=400, height=350)  # Further increased height to fit all buttons
        self.pack_propagate(False)  # Prevent card from resizing

        # Main container frame
        main_frame = Frame(self, style="Card.TFrame")
        main_frame.pack(fill="both", expand=True)

        # Header frame with Bay name and status
        header_frame = Frame(main_frame, style="Card.TFrame")
        header_frame.pack(fill="x", pady=(0, 15))

        # Bay name on the left
        bay_name_label = Label(header_frame,
                              text=f"{name.upper()}",
                              font=("Helvetica", 20, "bold"),
                              foreground=self.colors['text'],
                              background=self.colors['card_bg'])
        bay_name_label.pack(side="left")

        # Small unlock button at top right
        unlock_btn = RoundButton(header_frame,
                               text="🔓",
                               command=self.unlock_computer,
                               bg=self.colors['card_bg'],
                               fg=self.colors['text'],
                               hover_bg=self.colors['light_text'],
                               width=25,
                               height=25)
        unlock_btn.pack(side="right", padx=(5, 0))

        # Status indicator with lock icon in top right
        status_frame = Frame(header_frame, style="Card.TFrame")
        status_frame.pack(side="right")
        
        self.status = Label(status_frame,
                           text="ACTIVE",
                           font=("Helvetica", 10, "bold"),
                           foreground=self.colors['error'],
                           background=self.colors['card_bg'])
        self.status.pack(side="left", padx=(0, 5))
        
        # Lock icon
        lock_icon = Label(status_frame,
                         text="🔒",
                         font=("Helvetica", 12),
                         foreground=self.colors['text'],
                         background=self.colors['card_bg'])
        lock_icon.pack(side="left")

        # IP address
        ip_label = Label(main_frame,
                        text=f"IP: {ip}",
                        font=("Helvetica", 12),
                        foreground=self.colors['light_text'],
                        background=self.colors['card_bg'])
        ip_label.pack(anchor="w", pady=(0, 15))

        # Timer section
        timer_frame = Frame(main_frame, style="Card.TFrame")
        timer_frame.pack(fill="x", pady=(0, 15))

        # Timer display centered
        timer_display_frame = Frame(timer_frame, style="Card.TFrame")
        timer_display_frame.pack()
        
        self.timer_label = Label(timer_display_frame,
                                text="00:00:00",
                                font=("Helvetica", 28, "bold"),
                                foreground=self.colors['timer_text'],
                                background=self.colors['card_bg'])
        self.timer_label.pack()

        # "Remaining" label centered below timer
        remaining_label = Label(timer_display_frame,
                               text="Remaining",
                               font=("Helvetica", 12),
                               foreground=self.colors['timer_label'],
                               background=self.colors['card_bg'])
        remaining_label.pack()

        # Controls section
        controls_frame = Frame(main_frame, style="Card.TFrame")
        controls_frame.pack(fill="x", pady=(0, 5))

        # Start and Lock buttons (center-aligned)
        button_frame = Frame(controls_frame, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Center the buttons
        button_container = Frame(button_frame, style="Card.TFrame")
        button_container.pack(expand=True)

        start_btn = RoundButton(button_container,
                              text="START",
                              command=lambda: self.add_session(60),
                              bg=self.colors['primary'],
                              fg="#FFFFFF",
                              hover_bg=self.colors['secondary'],
                              width=130,
                              height=45)
        start_btn.pack(side="left", padx=(0, 10))

        lock_btn = RoundButton(button_container,
                             text="LOCK",
                             command=self.end_session,
                             bg=self.colors['warning'],
                             hover_bg="#C62828",
                             fg="#FFFFFF",
                             width=130,
                             height=45)
        lock_btn.pack(side="left")

        # Time increment buttons (center-aligned, 3 buttons = 2 button space)
        time_buttons_frame = Frame(controls_frame, style="Card.TFrame")
        time_buttons_frame.pack(fill="x", pady=(5, 0))
        
        # Center the time buttons
        time_container = Frame(time_buttons_frame, style="Card.TFrame")
        time_container.pack(expand=True)

        # Each time button takes 1/3 of the space (same total width as 2 main buttons)
        # 2 main buttons: 130 + 10 + 130 = 270, so each timer button = 270/3 = 90
        button_width = 90  # 3 * 90 = 270, same as 2 * 130 + 10 = 270

        # +1 MIN button
        plus_1_btn = RoundButton(time_container,
                               text="+1 MIN",
                               command=lambda: self.add_session(1),
                               bg=self.colors['info'],
                               fg="#000000",
                               hover_bg=self.colors['orange'],
                               width=button_width,
                               height=45)
        plus_1_btn.pack(side="left", padx=(0, 5))

        # +30 MIN button
        plus_30_btn = RoundButton(time_container,
                                text="+30 MIN",
                                command=lambda: self.add_session(30),
                                bg=self.colors['info'],
                                fg="#000000",
                                hover_bg=self.colors['orange'],
                                width=button_width,
                                height=45)
        plus_30_btn.pack(side="left", padx=(0, 5))

        # +60 MIN button
        plus_60_btn = RoundButton(time_container,
                                text="+60 MIN",
                                command=lambda: self.add_session(60),
                                bg=self.colors['info'],
                                fg="#000000",
                                hover_bg=self.colors['orange'],
                                width=button_width,
                                height=45)
        plus_60_btn.pack(side="left")

        self.update_status("IDLE", connected=True)

    def update_timer(self):
        if self.remaining_time <= 0:
            self.timer_label.configure(text="00:00:00")
            self.timer_label.update()
            self.update_status("IDLE", connected=True)  # Change to IDLE when timer reaches zero
            return
        hours, remainder = divmod(self.remaining_time, 3600)
        mins, secs = divmod(remainder, 60)
        self.timer_label.configure(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
        self.timer_label.update()
        self.remaining_time -= 1
        if self.remaining_time >= 0:
            self.timer_label.after(1000, self.update_timer)

    def update_status(self, status, connected):
        if connected:
            if status == "ACTIVE":
                style = "Error.TLabel"  # Red color for ACTIVE
                text = "ACTIVE"
            elif status == "IDLE":
                style = "Error.TLabel"  # Red color for IDLE
                text = "IDLE"
            else:  # LOCKED
                style = "Error.TLabel"
                text = "LOCKED"
        else:
            style = "Error.TLabel"
            text = "DISCONNECTED"
        self.status.configure(text=text, style=style)

    def unlock_computer(self):
        """Unlock the computer without a timer"""
        self.server.send_command(self.sock, {"cmd": "unlock"})
        self.update_status("ACTIVE", connected=True)

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
            self.timer_label.configure(text="00:00:00")
            self.timer_label.update()
            self.update_status("IDLE", connected=True)  # Update status to IDLE when time reaches zero

    def end_session(self):
        self.server.send_command(self.sock, {"cmd": "end"})
        self.update_status("LOCKED", connected=True)
        self.remaining_time = 0
        self.timer_label.configure(text="00:00:00")
        self.timer_label.update()

    def lock_now(self):
        self.server.send_command(self.sock, {"cmd": "lock"})

    def disconnect(self):
        self.update_status("DISCONNECTED", connected=False)

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