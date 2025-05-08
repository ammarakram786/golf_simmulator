from ttkbootstrap import Style

from server import AdminServer
from dashboard import AdminDashboard

style = Style('superhero')
root = style.master
root.title("Golf Simulator Admin Dashboard")
root.geometry("1000x600")

# Start server
server = AdminServer()
server.start()

# Launch dashboard UI
app = AdminDashboard(root, server)
app.pack(fill='both', expand=True)
root.mainloop()