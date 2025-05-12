import configparser
import os
import sys

from ttkbootstrap import Style, Window, Button
from admin.server_app import AdminServer
from admin.dashboard import AdminDashboard

# Configure Minty theme with custom styles
style = Style('minty')
root = style.master

# Configure custom styles
style.configure("Danger.Vertical.TScrollbar",
                gripcount=0,
                background="#e74c3c",  # Danger red
                troughcolor="#f8f9fa",  # Light background
                bordercolor="#dc3545",  # Darker red for border
                arrowcolor="#ffffff")  # White arrows

# Configure button styles with rounded corners
style.configure("Primary.TButton",
                font=("Helvetica", 12, "bold"),
                background="#2ecc71",
                foreground="#ffffff",
                borderwidth=0,
                padding=(15, 8),
                relief="flat")

style.configure("Warning.TButton",
                font=("Helvetica", 12, "bold"),
                background="#e74c3c",
                foreground="#ffffff",
                borderwidth=0,
                padding=(15, 8),
                relief="flat")

style.configure("Info.TButton",
                font=("Helvetica", 12, "bold"),
                background="#3498db",
                foreground="#ffffff",
                borderwidth=0,
                padding=(15, 8),
                relief="flat")

style.configure("Purple.TButton",
                font=("Helvetica", 12, "bold"),
                background="#9b59b6",
                foreground="#ffffff",
                borderwidth=0,
                padding=(15, 8),
                relief="flat")

style.configure("Orange.TButton",
                font=("Helvetica", 12, "bold"),
                background="#e67e22",
                foreground="#ffffff",
                borderwidth=0,
                padding=(15, 8),
                relief="flat")

# Configure window
root.title("Golf Simulator Admin Dashboard")
root.geometry("1200x800")  # Increased size for better visibility

# Add window icon and configure window properties
root.configure(bg="#ffffff")  # White background
root.attributes('-alpha', 0.98)  # Slight transparency for modern look

# Load configuration
# config_path = os.path.join(os.path.dirname(__file__), "config.ini")


# Get path where .exe or script is located
# Get path where .exe or script is located
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(app_path, "config.ini"))  #

admin_ip = config.get('Admin', 'ip')
admin_port = config.getint('Admin', 'port')



# Start server
server = AdminServer(host=admin_ip, port=int(admin_port))
server.start()

# Launch dashboard UI with modern styling
app = AdminDashboard(root, server)
app.pack(fill='both', expand=True, padx=20, pady=20)  # Added padding for better spacing

# Configure window minimum size
root.minsize(800, 600)

# Start the application
root.mainloop()