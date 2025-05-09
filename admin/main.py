import configparser
from ttkbootstrap import Style
from server_app import AdminServer
from dashboard import AdminDashboard

style = Style('superhero')
root = style.master
root.title("Golf Simulator Admin Dashboard")
root.geometry("1000x600")

config = configparser.ConfigParser()
config.read('../config.ini')

# Get Admin IP and Port
admin_ip = config.get('Admin', 'ip')
admin_port = config.getint('Admin', 'port')

# Start server
server = AdminServer(host=admin_ip, port=admin_port)
server.start()

# Launch dashboard UI
app = AdminDashboard(root, server)
app.pack(fill='both', expand=True)
root.mainloop()