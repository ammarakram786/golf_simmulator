import socket, threading, json
from ui import ClientCard

class AdminServer:
    def __init__(self, host='0.0.0.0', port=9999):
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
        except Exception as e:
            print("Client error:", e)

    def send_command(self, sock, cmd):
        try:
            sock.send(json.dumps(cmd).encode())
        except:
            print("Send failed")
