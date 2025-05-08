import socket
import tkinter as tk
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
        # Use a Label widget to display the text statically
        self.info_label = tk.Label(
            self,
            text=f"Server running on {self.ip_address}:{self.server.port}",
            font=("Arial", 16),
            bg="white",
            anchor="center"
        )
        self.info_label.pack(pady=10, fill="x")

    def add_client(self, addr, sock, info):
        if addr in self.cards:
            # Update existing client card
            card = self.cards[addr]
            card.update_status("Idle", connected=True)
        else:
            # Add new client card
            card = ClientCard(self, info['name'], info['ip'], sock, self.server)
            card.pack(pady=10, padx=10, fill='x')
            self.cards[addr] = card

    def remove_disconnected_clients(self):
        for addr, card in list(self.cards.items()):
            try:
                # Check if the socket is still connected
                card.sock.send(b"")  # Sending an empty byte to check connection
            except (socket.error, OSError):
                # If the socket is not connected, mark as disconnected and remove
                card.update_status("Disconnected", connected=False)
                card.destroy()  # Remove the card from the UI
                del self.cards[addr]  # Remove the card from the dictionary # Remove the card from the dictionary
