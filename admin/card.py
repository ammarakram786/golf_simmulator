import tkinter as tk

from ttkbootstrap import Frame, Label, Toplevel, IntVar
from ttkbootstrap import Style


class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=60, bg="#2ecc71", fg="#000000",hover_bg="#950606", **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        # fg = "#000000"
        # fg = "#000000"   #8cc751

        # Draw the rectangular button with no visible outline
        self.rect = self.create_rectangle(0, 0, width, height, fill=bg, outline=bg)

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
        self.tag_bind(self.rect, "<Enter>", self._on_hover)
        self.tag_bind(self.text, "<Enter>", self._on_hover)
        self.tag_bind(self.rect, "<Leave>", self._on_leave)
        self.tag_bind(self.text, "<Leave>", self._on_leave)

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
        super().__init__(master, padding=20)  # Increased padding
        self.name, self.ip, self.sock, self.server = name, ip, sock, server
        self.remaining_time = 0

        # Minty theme colors with additional button colors
        self.colors = {
            'primary': '#D3F36B',    # Mint green
            'secondary': '#272bae',  # Darker mint
            'warning': '#d65237',    # Red for warning
            'background': '#ffffff', # White (This is likely for the main window, not the card)
            'text': '#ffffff',      # White text
            'light_text': '#ffffff', # White text
            'border': '#e0e0e0',    # Light gray for borders
            'success': '#2ecc71',   # Green for success
            'error': '#e74c3c',     # Red for error
            'info': '#3498db',      # Blue for info
            'purple': '#9b59b6',    # Purple for special actions
            'orange': '#e67e22',    # Orange for warnings
            'card_bg': '#1a1a1a' ,  # Black for card background
            #   #FF0000
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
                       font=("Helvetica", 14, "bold"),  # Increased from 12
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Subtitle.TLabel",
                       font=("Helvetica", 12),  # Increased from 10
                       foreground=self.colors['text'],
                       background=self.colors['card_bg'])
        
        style.configure("Status.TLabel",
                       font=("Helvetica", 14, "bold"),  # Increased from 12
                       background=self.colors['card_bg'])
        
        style.configure("Success.TLabel",
                       foreground=self.colors['success'])
        
        style.configure("Error.TLabel",
                       foreground=self.colors['error'])

        # Apply card style
        self.configure(style="Card.TFrame", padding=15)  # Increased padding from 10

        # Main container frame
        main_frame = Frame(self, style="Card.TFrame")
        main_frame.pack(fill="x", expand=True)

        # Left column - Client info
        left_column = Frame(main_frame, style="Card.TFrame")
        left_column.pack(side="left", fill="y", padx=(0, 15))  # Increased padding

        # Name and IP in a single row
        name_ip_frame = Frame(left_column, style="Card.TFrame")
        name_ip_frame.pack(fill="x", pady=(0, 5))  # Increased padding

        Label(name_ip_frame, 
              text="●",
              font=("Helvetica", 12),  # Increased from 10
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 3))  # Increased padding

        Label(name_ip_frame,
              text=f"{name.upper()}",
              font=("Helvetica", 28, "bold"),  # Match the timer font size
              style="Title.TLabel").pack(side="left", padx=(0, 15))  # Increased padding

        Label(name_ip_frame, 
              text="●",
              font=("Helvetica", 12),  # Increased from 10
              foreground=self.colors['info'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 3))  # Increased padding
              
        Label(name_ip_frame, 
              text=f"{ip}", 
              style="Subtitle.TLabel").pack(side="left")

        # Timer and Status in a single row
        timer_status_frame = Frame(left_column, style="Card.TFrame")
        timer_status_frame.pack(fill="x", pady=(0, 5))  # Increased padding

        Label(timer_status_frame, 
              text="●",
              font=("Helvetica", 12),  # Increased from 10
              foreground=self.colors['primary'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 3))  # Increased padding
              
        self.timer_label = Label(timer_status_frame,
                                text="00:00",
                                font=("Helvetica", 28, "bold"),  # Increased from 24
                                foreground=self.colors['text'],
                                background=self.colors['card_bg'])
        self.timer_label.pack(side="left", padx=(0, 15))  # Increased padding

        Label(timer_status_frame, 
              text="●",
              font=("Helvetica", 12),  # Increased from 10
              foreground=self.colors['info'],
              background=self.colors['card_bg']).pack(side="left", padx=(0, 3))  # Increased padding
              
        self.status = Label(timer_status_frame,
                           text="IDLE",
                           style="Status.TLabel",
                           foreground=self.colors['text'], # Ensure text color is white
                           background=self.colors['card_bg']) # Ensure background is black
        self.status.pack(side="left")

        # Right column - Controls
        right_column = Frame(main_frame, style="Card.TFrame")
        right_column.pack(side="right", fill="y")

        # Start/Stop buttons in a single row
        button_frame = Frame(right_column, style="Card.TFrame")
        button_frame.pack(pady=(0, 10))  # Increased padding

        start_btn = RoundButton(button_frame,
                              text="START",
                              command=lambda: self.add_session(60),
                              bg=self.colors['primary'],
                              fg="#000000",  # White text for visibility on colored button
                              hover_bg="#8cc751",  # White text for visibility on colored button
                              width=120,  # Increased from 100
                              height=40)  # Increased from 35
        start_btn.pack(side="left", padx=5, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

        stop_btn = RoundButton(button_frame,
                             text="Lock",
                             command=self.end_session,
                             bg=self.colors['warning'],
                             hover_bg="#950606",
                             fg="#ffffff",  # White text for visibility on colored button
                             width=120,  # Increased from 100
                             height=40)  # Increased from 35
        stop_btn.pack(side="left", padx=5, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

        # Time controls in two columns
        time_controls_frame = Frame(right_column, style="Card.TFrame")
        time_controls_frame.pack(pady=8)  # Increased padding

        # First column (60 and 1 minutes)
        col1_frame = Frame(time_controls_frame, style="Card.TFrame")
        col1_frame.pack(side="left", padx=(0, 15))  # Increased padding between columns

        # 60 minutes controls
        time_frame_60 = Frame(col1_frame, style="Card.TFrame")
        time_frame_60.pack(pady=5)  # Increased padding between rows

        minus_btn1 = RoundButton(time_frame_60,
                               text="-",
                               command=lambda: self.subtract_session(60),
                               bg=self.colors['warning'],
                               hover_bg="#950606",
                               fg="#ffffff",  # White text for visibility on colored button
                               width=40,  # Increased from 30
                               height=40)  # Increased from 30
        minus_btn1.pack(side="left", padx=2, pady=0)  # Adjusted padding and added fill/expand

        time_label1 = Label(time_frame_60,
                          text="60 min",
                          font=("Helvetica", 14, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8,
                          anchor="center")  # Added anchor="center"
        time_label1.pack(side="left", padx=2, pady=0, expand=True, fill="both")

        plus_btn1 = RoundButton(time_frame_60,
                              text="+",
                              command=lambda: self.add_session(60),
                              bg=self.colors['primary'],
                                hover_bg="#8cc751",  # White text for visibility on colored button
                              fg="#000000",  # White text for visibility on colored button
                              width=40,  # Increased from 30
                              height=40)  # Increased from 30
        plus_btn1.pack(side="left", padx=2, pady=0)  # Adjusted padding and added fill/expand

        # 1 minute controls
        time_frame_1 = Frame(col1_frame, style="Card.TFrame")
        time_frame_1.pack(pady=5)  # Increased padding between rows

        minus_btn3 = RoundButton(time_frame_1,
                               text="-",
                               command=lambda: self.subtract_session(1),
                               bg=self.colors['warning'],
                                 hover_bg="#950606",
                               fg="#ffffff",  # White text for visibility on colored button
                               width=40,  # Increased from 30
                               height=40)  # Increased from 30
        minus_btn3.pack(side="left", padx=2, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

        time_label3 = Label(time_frame_1,
                          text="1 min",
                          font=("Helvetica", 14, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8,
                          anchor="center")  # Added anchor="center"
        time_label3.pack(side="left", padx=2, pady=0, expand=True, fill="both")

        plus_btn3 = RoundButton(time_frame_1,
                              text="+",
                              command=lambda: self.add_session(1),
                              bg=self.colors['primary'],
                                hover_bg="#8cc751",  # White text for visibility on colored button
                              fg="#000000",  # White text for visibility on colored button
                              width=40,  # Increased from 30
                              height=40)  # Increased from 30
        plus_btn3.pack(side="left", padx=2, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

        # Second column (30 minutes)
        col2_frame = Frame(time_controls_frame, style="Card.TFrame")
        col2_frame.pack(side="left", pady=5)  # Match the pady of time_frame_60

        # 30 minutes controls
        time_frame_30 = Frame(col2_frame, style="Card.TFrame")
        time_frame_30.pack(pady=5)  # Remove pady to align with 60 minutes

        minus_btn2 = RoundButton(time_frame_30,
                               text="-",
                               command=lambda: self.subtract_session(30),
                               bg=self.colors['warning'],
                                 hover_bg="#950606",
                               fg="#ffffff",  # White text for visibility on colored button
                               width=40,  # Increased from 30
                               height=40)  # Increased from 30
        minus_btn2.pack(side="left", padx=2, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

        time_label2 = Label(time_frame_30,
                          text="30 min",
                          font=("Helvetica", 14, "bold"),
                          foreground=self.colors['text'],
                          background=self.colors['card_bg'],
                          width=8,
                          anchor="center")  # Added anchor="center"
        time_label2.pack(side="left", padx=2, pady=0, expand=True, fill="both")

        plus_btn2 = RoundButton(time_frame_30,
                              text="+",
                              command=lambda: self.add_session(30),
                              bg=self.colors['primary'],
                                hover_bg="#8cc751", # White text for visibility on colored button
                              fg="#000000",  # White text for visibility on colored button
                              width=40,  # Increased from 30
                              height=40)  # Increased from 30
        plus_btn2.pack(side="left", padx=2, pady=0, expand=True, fill="both")  # Adjusted padding and added fill/expand

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



        