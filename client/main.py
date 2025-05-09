import configparser
from client_app import ClientApp

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('../config.ini')

# Get Server IP and Port
server_ip = config.get('Admin', 'ip')
server_port = config.getint('Admin', 'port')


# Initialize and run the client application
app = ClientApp(server_ip, server_port)
app.run()