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

            incoming_ip = info['ip']

            # Check for existing clients with the same IP and remove them
            clients_to_remove = []
            for existing_addr, (existing_sock, existing_info) in list(self.clients.items()):
                if existing_info['ip'] == incoming_ip:
                    clients_to_remove.append(existing_addr)

            for old_addr in clients_to_remove:
                print(f"Removing existing client with IP {incoming_ip} at address {old_addr}")
                old_sock, _ = self.clients[old_addr]
                if self.ui:
                    self.ui.remove_client_by_ip(incoming_ip) # Call the new method
                old_sock.close()
                del self.clients[old_addr]

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
                elif data['cmd'] == 'end':
                    if self.ui and addr in self.ui.cards:
                        client_card = self.ui.cards[addr]
                        client_card.update_status("IDLE", connected=True)
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
