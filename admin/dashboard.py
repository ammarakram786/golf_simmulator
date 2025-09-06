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
        
        # New color palette based on design specifications
        self.colors = {
            'primary': '#4CAF50',    # Green for active/start buttons
            'secondary': '#43A047',  # Darker green for hover
            'warning': '#E53935',    # Red for lock/error
            'background': '#1E1E1E', # Dark charcoal gray main background
            'text': '#FFFFFF',      # White main text
            'light_text': '#CCCCCC', # Light gray secondary text
            'border': '#2A2A2A',    # Card border color
            'success': '#4CAF50',   # Green for success/active
            'error': '#E53935',     # Red for error/locked
            'info': '#FFB300',      # Amber yellow for time buttons
            'purple': '#9b59b6',    # Purple for special actions
            'orange': '#FFA000',    # Darker amber for hover
            'card_bg': '#2A2A2A',   # Slightly lighter gray for card background
            'header_bg': '#1E1E1E', # Dark background for header
            'header_text': '#FFFFFF', # White text for header
            'timer_text': '#FFFFFF', # White for timer numbers
            'timer_label': '#AAAAAA' # Light gray for "Remaining" label
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

        # # Subtitle with current time
        # Label(title_frame,
        #       text="Admin Control Panel",
        #       style="HeaderSubtitle.TLabel").pack(side="left", padx=(10, 0))

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
        
        # Bind window resize events for responsive behavior
        self.bind('<Configure>', self._on_window_resize)
        # Also bind to the root window for better resize detection
        self.master.bind('<Configure>', self._on_root_resize)

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
        
        # Configure grid columns to be responsive
        # Will be updated dynamically based on window size
        for i in range(5):  # Maximum 5 columns
            self.cards_frame.grid_columnconfigure(i, weight=1, minsize=420)
        
        # Configure grid rows to be responsive
        for i in range(10):  # Support up to 10 rows
            self.cards_frame.grid_rowconfigure(i, weight=1)

        # Start time update
        self.update_time()
        
        # Set initial responsive layout
        self.after(100, self._adjust_card_layout)

    def _on_canvas_configure(self, event):
        # Update the width of the frame to match the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
        
    def _on_window_resize(self, event):
        """Handle window resize events for responsive layout"""
        # Update canvas width when window is resized
        if event.width > 1:  # Avoid invalid resize events
            self.canvas.itemconfig(self.canvas_frame, width=event.width - 50)  # Account for scrollbar
            
            # Rearrange cards to fit new layout after a short delay to avoid excessive updates
            self.after(100, self._adjust_card_layout)
    
    def _on_root_resize(self, event):
        """Handle root window resize events for responsive layout"""
        # Only respond to root window resize events
        if event.widget == self.master and event.width > 1:
            # Rearrange cards to fit new layout after a short delay
            self.after(150, self._adjust_card_layout)
            
    def _adjust_card_layout(self):
        """Adjust card layout based on current window size"""
        if not self.cards:
            return
            
        # Get current window dimensions
        window_width = self.winfo_width()
        
        # Determine number of columns based on window width
        # Card minimum width is 420px, with 20px padding between cards
        min_card_width = 420
        padding = 20
        
        if window_width < 800:
            # Small window: single column
            columns = 1
            card_width = max(min_card_width, window_width - 100)
        elif window_width < 1200:
            # Medium window: 2 columns
            columns = 2
            card_width = max(min_card_width, (window_width - 100) // 2)
        elif window_width < 1600:
            # Large window: 3 columns
            columns = 3
            card_width = max(min_card_width, (window_width - 100) // 3)
        elif window_width < 2000:
            # Extra large window: 4 columns
            columns = 4
            card_width = max(min_card_width, (window_width - 100) // 4)
        else:
            # Very large window: 5 columns maximum
            columns = 5
            card_width = max(min_card_width, (window_width - 100) // 5)
            
        # print(f"Window width: {window_width}, Columns: {columns}, Card width: {card_width}")  # Debug output
            
        # Clear all existing grid configurations
        for i in range(10):  # Reset all columns
            self.cards_frame.grid_columnconfigure(i, weight=0, minsize=0)
            
        # Update grid configuration with proper minimum sizes for active columns
        for i in range(columns):
            self.cards_frame.grid_columnconfigure(i, weight=1, minsize=card_width)
            
        # Rearrange cards with new column count
        self._rearrange_cards_responsive(columns)
        
    def _rearrange_cards_responsive(self, columns):
        """Rearrange cards based on responsive column count"""
        if not self.cards:
            return
            
        # Sort cards alphabetically
        sorted_cards = sorted(self.cards.items(), key=lambda x: x[1].name.upper())
        
        # First, remove all cards from grid
        for addr, card in self.cards.items():
            card.grid_remove()
        
        # Position cards in responsive grid with proper sizing
        for index, (addr, card) in enumerate(sorted_cards):
            row = index // columns
            col = index % columns
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Ensure card maintains minimum size for visibility
            card.grid_propagate(False)  # Prevent card from shrinking
            
        # Update scroll region after a short delay to ensure layout is complete
        self.after(50, self._on_frame_configure)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        # Update time in header if needed
        self.after(1000, self.update_time)

    def add_client(self, addr, sock, info):
        if addr in self.cards:
            # Client reconnected - just update status, keep position
            card = self.cards[addr]
            card.update_status("IDLE", connected=True)
        else:
            # New client - add and maintain alphabetical order
            card = ClientCard(self.cards_frame, info['name'], info['ip'], sock, self.server)
            self.cards[addr] = card
            self.rearrange_cards_alphabetically()
            # Update scroll region after adding new card
            self._on_frame_configure()



    def rearrange_cards_alphabetically(self):
        """Rearrange all cards in alphabetical order (BAY 1, BAY 2, BAY 3, etc.)"""
        if not self.cards:
            return
            
        # Use responsive layout instead of fixed 2-column layout
        self._adjust_card_layout()

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

        # Rearrange the remaining cards alphabetically
        self.rearrange_cards_alphabetically()

    def remove_client_by_ip(self, ip_address):
        for addr, card in list(self.cards.items()):
            if card.ip == ip_address:
                print(f"Removing client card for IP: {ip_address}")
                card.destroy()  # Destroy the tkinter widget
                del self.cards[addr] # Remove from our dictionary
                self.rearrange_cards_alphabetically() # Rearrange remaining cards alphabetically after removal
                return # Assuming only one client per IP is possible at this point

    def rearrange_cards(self):
        # This method will rearrange the cards in the grid after one is removed
        # Now uses alphabetical ordering
        self.rearrange_cards_alphabetically()



    def stop_cleanup(self):
        self.running = False

    def _on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



