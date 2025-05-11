import socket
import threading
import tkinter as tk
import time
from ttkbootstrap import Frame, Scrollbar, Style
from admin.card import ClientCard


def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


class AdminDashboard(Frame):
    def __init__(self, master, server):
        super().__init__(master)
        self.server = server
        self.ip_address = get_ip_address()
        self.server.ui = self
        self.cards = {}

        style = Style()
        style.configure("Custom.Vertical.TScrollbar",
                        gripcount=0,
                        background="#d3d3d3",
                        troughcolor="#f0f0f0",
                        bordercolor="#a9a9a9",
                        arrowcolor="#000000")

        # Canvas + Scrollbar + Inner Frame
        container = Frame(self)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.scrollbar = Scrollbar(container, orient="vertical", command=self.canvas.yview,
                                   style="Custom.Vertical.TScrollbar")
        self.scrollable_frame = Frame(self.canvas)

        # Link canvas and scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Add scrollable frame to canvas
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Scroll region update
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_canvas)

        # Enable mouse wheel scrolling
        self._bind_mouse_wheel(self.canvas)


        self.info_label = tk.Label(
            self.scrollable_frame,
            text=f"Server running on {self.ip_address}:{self.server.port}",
            font=("Arial", 16),
            bg="white",
            anchor="center"
        )
        self.info_label.pack(pady=10, fill="x")

        # Start the background thread
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._run_cleanup_loop, daemon=True)
        self.cleanup_thread.start()

    def _update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas(self, event):
        self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)

    def _bind_mouse_wheel(self, widget):
        # Windows and Mac
        widget.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / Mac
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _run_cleanup_loop(self):
        while self.running:
            self.remove_disconnected_clients()
            time.sleep(5)  # Run every 5 seconds

    def add_client(self, addr, sock, info):
        if addr in self.cards:
            card = self.cards[addr]
            card.update_status("IDLE", connected=True)
        else:
            card = ClientCard(self.scrollable_frame, info['name'], info['ip'], sock, self.server)
            card.pack(pady=10, padx=10, fill='x')
            self.cards[addr] = card
            self._update_scroll_region(None)

    def remove_disconnected_clients(self):
        for addr, card in list(self.cards.items()):
            try:
                card.sock.send(b"")
            except (socket.error, OSError):
                card.update_status("Disconnected", connected=False)
                card.destroy()
                del self.cards[addr]

    def stop_cleanup(self):
        self.running = False



