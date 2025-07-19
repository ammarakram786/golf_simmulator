import socket
import tkinter as tk
from datetime import datetime
from ttkbootstrap import Frame, Style, Label
from admin.card import ClientCard


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


class AdminDashboard(Frame):
    def __init__(self, master, server):
        super().__init__(master, padding=20)
        self.server = server
        self.ip_address = get_ip_address()
        self.server.ui = self
        self.cards = {}
        
        # Minty theme colors with additional colors
        self.colors = {
            'primary': '#2ecc71',    # Mint green
            'secondary': '#27ae60',  # Darker mint
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
            'card_bg': '#f8f9fa',   # Light gray for card background
            'header_bg': '#1a1a1a', # Dark background for header
            'header_text': '#ffffff' # White text for header
        }

        # Configure styles
        style = Style()
        
        # Header styles
        style.configure("Header.TFrame",
                       background=self.colors['header_bg'],
                       relief="flat")
        
        style.configure("HeaderTitle.TLabel",
                       font=("Helvetica", 24, "bold"),
                       foreground=self.colors['header_text'],
                       background=self.colors['header_bg'])
        
        style.configure("HeaderSubtitle.TLabel",
                       font=("Helvetica", 12),
                       foreground=self.colors['header_text'],
                       background=self.colors['header_bg'])
        
        style.configure("HeaderInfo.TLabel",
                       font=("Helvetica", 12),
                       foreground=self.colors['primary'],
                       background=self.colors['header_bg'])

        # Create header frame with dark background
        header_frame = Frame(self, style="Header.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))

        # Left side of header (Title and Subtitle)
        title_frame = Frame(header_frame, style="Header.TFrame")
        title_frame.pack(side="left", padx=20, pady=15)

        # Golf icon and title
        Label(title_frame,
              text="⛳",  # Golf emoji
              font=("Helvetica", 28),
              foreground=self.colors['primary'],
              background=self.colors['header_bg']).pack(side="left", padx=(0, 10))
              
        Label(title_frame,
              text="Golf Simulator Dashboard",
              style="HeaderTitle.TLabel").pack(side="left")

        # Subtitle with current time
        Label(title_frame,
              text="Admin Control Panel",
              style="HeaderSubtitle.TLabel").pack(side="left", padx=(10, 0))

        # Right side of header (Server Info)
        info_frame = Frame(header_frame, style="Header.TFrame")
        info_frame.pack(side="right", padx=20, pady=15)

        # Server status indicator
        self.status_indicator = Label(info_frame,
                                    text="●",  # Bullet point as status indicator
                                    font=("Helvetica", 16),
                                    foreground=self.colors['success'],
                                    background=self.colors['header_bg'])
        self.status_indicator.pack(side="left", padx=(0, 5))

        # Server info
        Label(info_frame,
              text=f"Server: {self.ip_address}:{self.server.port}",
              style="HeaderInfo.TLabel").pack(side="left")

        # Main content area with scrollbar
        self.main_frame = Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.main_frame, highlightthickness=0, bg=self.colors['background'])
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, style="Card.TFrame")

        # Configure canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas and make it expand to fill width
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_width()
        )

        # Make the canvas expand to fill the frame
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind events for proper resizing
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Create a frame to hold the grid of cards
        self.cards_frame = Frame(self.scrollable_frame, style="Card.TFrame")
        self.cards_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid columns to have equal weight
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)

        # Start time update
        self.update_time()

    def _on_canvas_configure(self, event):
        # Update the width of the frame to match the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        # Update time in header if needed
        self.after(1000, self.update_time)

    def add_client(self, addr, sock, info):
        if addr in self.cards:
            card = self.cards[addr]
            card.update_status("IDLE", connected=True)
        else:
            card = ClientCard(self.cards_frame, info['name'], info['ip'], sock, self.server)
            # Calculate the position in the grid
            row = len(self.cards) // 2
            col = len(self.cards) % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.cards[addr] = card
            # Update scroll region after adding new card
            self._on_frame_configure()

    # def remove_disconnected_clients(self):
    #     for addr, card in list(self.cards.items()):
    #         try:
    #             card.sock.send(b"")
    #         except (socket.error, OSError):
    #             card.update_status("Disconnected", connected=False)
    #             card.destroy()
    #             del self.cards[addr]
    #             # Update scroll region after removing card
    #             self._on_frame_configure()

    def remove_disconnected_clients(self):
        for addr, card in list(self.cards.items()):
            try:
                card.sock.send(b"")
            except (socket.error, OSError):
                card.update_status("Disconnected", connected=False)
                card.destroy()
                del self.cards[addr]

        # Rearrange the remaining cards
        for index, card in enumerate(self.cards.values()):
            row = index // 2
            col = index % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Update scroll region after rearranging cards
        self._on_frame_configure()

    def remove_client_by_ip(self, ip_address):
        for addr, card in list(self.cards.items()):
            if card.ip == ip_address:
                print(f"Removing client card for IP: {ip_address}")
                card.destroy()  # Destroy the tkinter widget
                del self.cards[addr] # Remove from our dictionary
                self.rearrange_cards() # Rearrange remaining cards after removal
                return # Assuming only one client per IP is possible at this point

    def rearrange_cards(self):
        # This method will rearrange the cards in the grid after one is removed
        for index, (addr, card) in enumerate(list(self.cards.items())):
            row = index // 2
            col = index % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Update the scroll region after rearranging
        self._on_frame_configure()

    def stop_cleanup(self):
        self.running = False

    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



