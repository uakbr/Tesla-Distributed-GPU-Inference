# communication.py
# Handles all network communications to and from the vehicle, including data transfer and receiving instructions.

import socket
import ssl
from .utilities import encrypt_data, decrypt_data, log_system_activity
from .config import Config

class CommunicationModule:
    def __init__(self):
        self.server_address = Config.SERVER_URL
        self.vpn_endpoint = Config.VPN_TUNNEL_ENDPOINT
        self.socket = None

    def setup_secure_connection(self):
        """
        Establishes a secure socket connection to the server through a VPN tunnel.
        """
        try:
            # Create a raw socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Wrap the socket with SSL for encryption
            self.socket = ssl.wrap_socket(self.socket, keyfile=None, certfile=None, server_side=False,
                                          cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1_2)
            
            # Connect to the VPN tunnel
            self.socket.connect((self.vpn_endpoint, 443))
            log_system_activity("Secure connection established with VPN endpoint.", "INFO")
        except Exception as e:
            log_system_activity(f"Failed to establish secure connection: {str(e)}", "ERROR")

    def send_data(self, data):
        """
        Sends encrypted data to the server.
        :param data: Data to send (str).
        """
        try:
            encrypted_data = encrypt_data(data)
            self.socket.sendall(encrypted_data)
            log_system_activity("Data sent to server successfully.", "DEBUG")
        except Exception as e:
            log_system_activity(f"Error sending data: {str(e)}", "ERROR")

    def receive_data(self):
        """
        Receives data from the server and decrypts it.
        :return: Decrypted data (str).
        """
        try:
            received_data = self.socket.recv(1024)  # Buffer size
            decrypted_data = decrypt_data(received_data)
            log_system_activity("Data received and decrypted successfully.", "DEBUG")
            return decrypted_data
        except Exception as e:
            log_system_activity(f"Error receiving data: {str(e)}", "ERROR")
            return None

    def close_connection(self):
        """
        Closes the secure connection.
        """
        try:
            if self.socket:
                self.socket.close()
                log_system_activity("Connection closed successfully.", "INFO")
        except Exception as e:
            log_system_activity(f"Failed to close connection: {str(e)}", "ERROR")

# Example usage
if __name__ == "__main__":
    comm_module = CommunicationModule()
    comm_module.setup_secure_connection()
    comm_module.send_data("Hello, server!")
    response = comm_module.receive_data()
    print(f"Response from server: {response}")
    comm_module.close_connection()
