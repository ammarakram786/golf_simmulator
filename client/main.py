import configparser
import os
import sys

from client.client_app import ClientApp


# Determine app path whether frozen (exe) or not
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)  # Running from .exe
else:
    app_path = os.path.dirname(os.path.abspath(__file__))  # Running from .py

# Read configuration from config.ini in the same folder as the exe or script
config_path = os.path.join(app_path, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

# Get Server IP and Port
server_ip = config.get('Client', 'server')
server_port = config.getint('Client', 'port')
name = config.get('Client', 'name')

# Initialize and run the client application
app = ClientApp(server_ip, server_port, name)
app.run()
