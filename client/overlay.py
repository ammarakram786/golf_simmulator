import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import time


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


class SessionOverlay:
    def __init__(self, root, app):
        self.app = app
        self.extension_asked = False
        self.remaining = 0
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.geometry("200x100")  # Smaller window size
        self.win.overrideredirect(True)
        self.win.attributes('-topmost', True)
        
        # Position window in bottom right corner
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        window_width = 200
        window_height = 100
        x = screen_width - window_width - 20  # 20 pixels from right edge
        y = screen_height - window_height - 40  # 40 pixels from bottom edge
        self.win.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Minty theme colors
        self.colors = {
            'primary': '#2ecc71',  # Mint green
            'secondary': '#27ae60',  # Darker mint
            'warning': '#e74c3c',  # Red for warning
            'background': '#ffffff',  # White
            'text': '#2c3e50',  # Dark blue-gray
            'light_text': '#ffffff'  # White text
        }
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Minty.TLabel', 
                           font=('Helvetica', 32, 'bold'),  # Smaller font size
                           background=self.colors['background'],
                           foreground=self.colors['text'])

        # Main timer label
        self.label = tk.Label(self.win, 
                            text="",
                            font=("Helvetica", 32, "bold"),  # Smaller font size
                            fg=self.colors['text'],
                            bg=self.colors['background'])
        self.label.pack(expand=True, fill='both')
        
        self.running = False
        self.win.withdraw()

    def start_session(self, minutes):
        self.remaining = minutes * 60
        self.running = True
        self.win.deiconify()
        self.win.configure(bg=self.colors['background'])
        self.update_timer()

    def update_session(self, minutes, add_type):
        if add_type:
            if self.remaining <= 0:
                self.start_session(minutes)
            else:
                self.remaining += minutes * 60
        else:
            if self.remaining < minutes * 60:
                self.remaining = 0
            else:
                self.remaining -= minutes * 60

    def update_timer(self):
        if not self.running:
            return
        mins, secs = divmod(self.remaining, 60)

        if self.remaining <= 55:
            if not self.extension_asked:
                self.ask_extension()
            self.win.configure(bg=self.colors['warning'])
            self.label.configure(bg=self.colors['warning'], fg=self.colors['light_text'])
        else:
            self.win.configure(bg=self.colors['background'])
            self.label.configure(bg=self.colors['background'], fg=self.colors['text'])

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
        extension_win.geometry("800x600")  # Increased window size
        extension_win.configure(bg=self.colors['background'])
        
        # Make window appear in center
        extension_win.update_idletasks()
        width = extension_win.winfo_width()
        height = extension_win.winfo_height()
        x = (extension_win.winfo_screenwidth() // 2) - (width // 2)
        y = (extension_win.winfo_screenheight() // 2) - (height // 2)
        extension_win.geometry(f'{width}x{height}+{x}+{y}')

        # Title label with modern styling
        title_label = tk.Label(
            extension_win,
            text="EXTEND YOUR SESSION",
            font=("Helvetica", 28, "bold"),  # Increased for touch
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        title_label.pack(pady=30)  # Increased padding

        # Frame for radio buttons with modern styling
        options_frame = tk.Frame(extension_win, bg=self.colors['background'])
        options_frame.pack(pady=20)  # Increased padding

        var = tk.IntVar(value=30)
        options = [("6 MINUTES", 1), ("30 MINUTES", 30), ("1 HOUR", 60), 
                  ("1.5 HOURS", 90), ("2 HOURS", 120)]
        
        for label, val in options:
            rb = tk.Radiobutton(
                options_frame,
                text=label,
                variable=var,
                value=val,
                bg=self.colors['background'],
                fg=self.colors['text'],
                font=("Helvetica", 20),  # Increased for touch
                selectcolor=self.colors['background'],
                activebackground=self.colors['background'],
                activeforeground=self.colors['primary']
            )
            rb.pack(anchor='w', padx=30, pady=10)  # Increased padding

        # Buttons with modern styling
        button_frame = tk.Frame(extension_win, bg=self.colors['background'])
        button_frame.pack(pady=30)  # Increased padding

        def confirm():
            minutes = var.get()
            extension_win.destroy()
            self.app.request_extension(minutes)

        def close():
            extension_win.destroy()

        # Use RoundButton for rounded corners
        confirm_btn = RoundButton(
            button_frame,
            text="CONFIRM",
            command=confirm,
            bg=self.colors['primary'],
            width=200,  # Increased for touch
            height=60   # Increased for touch
        )
        confirm_btn.pack(side="left", padx=15)  # Increased padding

        cancel_btn = RoundButton(
            button_frame,
            text="CANCEL",
            command=close,
            bg=self.colors['warning'],
            width=200,  # Increased for touch
            height=60   # Increased for touch
        )
        cancel_btn.pack(side="left", padx=15)  # Increased padding

    def extend_session(self, minutes):
        self.remaining += minutes * 60
        self.extension_asked = False

    def end_session(self):
        self.running = False
        self.lock_and_close()
        self.win.withdraw()

    def lock_and_close(self):
        subprocess.call("rundll32.exe user32.dll,LockWorkStation")
        self.app.end_session()
        self.win.withdraw()
