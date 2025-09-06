#!/usr/bin/env python3
"""
Test script to show the new dashboard design with sample data
"""

import tkinter as tk
from ttkbootstrap import Style, Frame
from admin.card import ClientCard
from admin.dashboard import AdminDashboard

class MockServer:
    """Mock server for testing"""
    def __init__(self):
        self.port = 8080
        
    def send_command(self, sock, cmd):
        print(f"Command sent: {cmd}")

def test_dashboard():
    """Test the new dashboard design with sample data"""
    
    # Create main window
    root = tk.Tk()
    root.title("Golf Simulator Dashboard - Test")
    root.geometry("1400x900")
    root.configure(bg="#1E1E1E")
    
    # Create mock server
    mock_server = MockServer()
    
    # Create dashboard
    dashboard = AdminDashboard(root, mock_server)
    dashboard.pack(fill="both", expand=True)
    
    # Add some test bay cards
    test_bays = [
        ("Bay 1", "192.168.1.151"),
        ("Bay 2", "192.168.1.152"), 
        ("Bay 3", "192.168.1.153"),
        ("Bay 4", "192.168.1.154"),
        ("Bay 5", "192.168.1.155"),
        ("Bay 6", "192.168.1.156"),
        ("Bay 7", "192.168.1.157"),
        ("Bay 8", "192.168.1.158"),
    ]
    
    # Add test cards to dashboard
    for i, (name, ip) in enumerate(test_bays):
        # Create mock socket (just use None for testing)
        card = ClientCard(dashboard.cards_frame, name, ip, None, mock_server)
        dashboard.cards[f"test_{i}"] = card
        
        # Add some test data
        if i == 0:  # Bay 1 - 1 hour session
            card.add_session(60)
        elif i == 1:  # Bay 2 - 30 minute session  
            card.add_session(30)
        elif i == 2:  # Bay 3 - 1.5 hour session
            card.add_session(90)
        elif i == 3:  # Bay 4 - Active but no timer
            card.update_status("ACTIVE", True)
        elif i == 4:  # Bay 5 - Locked
            card.update_status("LOCKED", True)
        elif i == 5:  # Bay 6 - 2 hour session
            card.add_session(120)
        elif i == 6:  # Bay 7 - 45 minute session
            card.add_session(45)
        elif i == 7:  # Bay 8 - Disconnected
            card.update_status("DISCONNECTED", False)
    
    # Trigger initial layout
    dashboard._adjust_card_layout()
    
    print("Test dashboard loaded with 8 sample bays")
    print("Try resizing the window to see the responsive layout!")
    
    root.mainloop()

if __name__ == "__main__":
    test_dashboard()
