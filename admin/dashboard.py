import socket
import threading
import tkinter as tk
import time
from ttkbootstrap import Frame
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
        self.info_label = tk.Label(
            self,
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

    def _run_cleanup_loop(self):
        while self.running:
            self.remove_disconnected_clients()
            time.sleep(5)  # Run every 5 seconds

    def add_client(self, addr, sock, info):
        if addr in self.cards:
            card = self.cards[addr]
            card.update_status("IDLE", connected=True)
        else:
            card = ClientCard(self, info['name'], info['ip'], sock, self.server)
            card.pack(pady=10, padx=10, fill='x')
            self.cards[addr] = card

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
