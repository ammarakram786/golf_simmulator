import socket
import time
import threading
import os
import sys
import ctypes

# Server settings
SERVER_HOST = "127.0.0.1"  # Change to server IP when testing on different machines
SERVER_PORT = 9095

# Reconnection settings
RECONNECT_INTERVAL = 5  # seconds

class GolfSimulatorClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.running = True
        self.reconnect_thread = None

    def connect_to_server(self):
        """Connect to the admin server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.connected = False
            self.socket = None
            return False

    def lock_windows_screen(self):
        """Lock Windows screen using Win+L shortcut"""
        if sys.platform == 'win32':
            try:
                # Method 1: Using ctypes to call Windows API
                user32 = ctypes.WinDLL('user32')
                user32.LockWorkStation()
                print("Screen locked using Windows API")
                return
            except Exception as e:
                print(f"Failed to lock using Windows API: {e}")
                
            try:
                # Method 2: Using keyboard library as fallback
                import keyboard
                keyboard.send('windows+l')
                print("Screen locked using keyboard simulation")
                return
            except Exception as e:
                print(f"Failed to lock using keyboard simulation: {e}")
                
            try:
                # Method 3: Using os.system as last resort
                os.system('rundll32.exe user32.dll,LockWorkStation')
                print("Screen locked using rundll32")
            except Exception as e:
                print(f"Failed to lock using rundll32: {e}")
        else:
            print("Screen locking is only supported on Windows")

    def handle_server_messages(self):
        """Handle messages from the server"""
        while self.running and self.connected:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    print("Server closed connection")
                    break
                
                print(f"Received from server: {data}")
                
                # Handle commands from server
                if data == "START_SESSION":
                    print("Starting session...")
                    # Add code to start your application
                
                elif data == "END_SESSION":
                    print("Ending session...")
                    # Add code to close your application
                
                elif data == "LOCK_SCREEN":
                    print("Locking screen...")
                    # Simply lock Windows screen
                    self.lock_windows_screen()
                
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        
        # If we exit the loop, we're disconnected
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        
        # Start reconnection if we're still running
        if self.running and not self.reconnect_thread:
            self.reconnect_thread = threading.Thread(target=self.reconnect_loop)
            self.reconnect_thread.daemon = True
            self.reconnect_thread.start()

    def reconnect_loop(self):
        """Try to reconnect to server periodically"""
        while self.running and not self.connected:
            print(f"Attempting to reconnect in {RECONNECT_INTERVAL} seconds...")
            time.sleep(RECONNECT_INTERVAL)
            
            if self.connect_to_server():
                # Start handling messages again
                message_thread = threading.Thread(target=self.handle_server_messages)
                message_thread.daemon = True
                message_thread.start()
                break
        
        self.reconnect_thread = None

    def start(self):
        """Start the client"""
        if self.connect_to_server():
            message_thread = threading.Thread(target=self.handle_server_messages)
            message_thread.daemon = True
            message_thread.start()
        else:
            # Start reconnection loop
            self.reconnect_thread = threading.Thread(target=self.reconnect_loop)
            self.reconnect_thread.daemon = True
            self.reconnect_thread.start()
    
    def stop(self):
        """Stop the client"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

# Run client
if __name__ == "__main__":
    client = GolfSimulatorClient()
    client.start()
    
    try:
        # Keep main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down client...")
        client.stop()