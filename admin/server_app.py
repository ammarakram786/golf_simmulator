import json
import socket
import threading


class AdminServer:
    def __init__(self, host, port):
        self.host, self.port = host, port
        self.clients = {}  # key: addr, value: (sock, info)
        self.ui = None

    def start(self):
        threading.Thread(target=self.listen_for_clients, daemon=True).start()

    def listen_for_clients(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        while True:
            client_sock, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(client_sock, addr), daemon=True).start()

    def handle_client(self, sock, addr):
        try:
            info = sock.recv(1024).decode()
            info = json.loads(info)
            self.clients[addr] = (sock, info)
            if self.ui:
                self.ui.add_client(addr, sock, info)
            threading.Thread(target=self.listen_client_messages, args=(sock, addr), daemon=True).start()
        except Exception as e:
            print("Client error:", e)

    def listen_client_messages(self, sock, addr):
        while True:
            try:
                msg = sock.recv(1024).decode()
                data = json.loads(msg)
                if data['cmd'] == 'extend_request':
                    if self.ui and addr in self.ui.cards:
                        client_card = self.ui.cards[addr]
                        client_card.handle_extension_request(data['minutes'])
            except Exception as e:
                print(f"Error in client message handling: {e}")
                break

    def send_command(self, sock, cmd):
        try:
            sock.send(json.dumps(cmd).encode())
        except Exception as e:
            print(f"Command failed: {e}")
            # Find the client by socket and remove it
            for addr, (client_sock, _) in list(self.clients.items()):
                if client_sock == sock:
                    # Remove from UI
                    if self.ui and addr in self.ui.cards:
                        self.ui.cards[addr].update_status("Disconnected", connected=False)
                        self.ui.cards[addr].destroy()
                        del self.ui.cards[addr]
                    # Remove from server's client list
                    del self.clients[addr]
                    break
