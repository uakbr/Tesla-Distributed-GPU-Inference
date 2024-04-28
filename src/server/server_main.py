# server_main.py
# Main server script for managing task distribution and result aggregation in the Distributed Inference System across Tesla Fleet

import threading
import socket
from .scheduler import TaskScheduler
from .data_manager import DataManager
from .result_aggregator import ResultAggregator
from .utilities import setup_logging, log_system_activity
from .config import Config

class ServerMain:
    def __init__(self):
        setup_logging()
        self.scheduler = TaskScheduler()
        self.data_manager = DataManager()
        self.result_aggregator = ResultAggregator()
        self.server_socket = self.setup_server_socket()

    def setup_server_socket(self):
        """
        Sets up the server socket to listen for incoming connections from vehicles.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', 5000))  # Bind to all interfaces on port 5000
        server_socket.listen(5)
        log_system_activity("Server socket setup and listening", "INFO")
        return server_socket

    def handle_vehicle_connection(self, client_socket, addr):
        """
        Handles the connection from a vehicle, processing incoming data and sending tasks.
        """
        log_system_activity(f"Connected to vehicle at {addr}", "INFO")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                processed_data = self.data_manager.process_incoming_data(data)
                task = self.scheduler.allocate_task(processed_data)
                client_socket.send(task)
        except Exception as e:
            log_system_activity(f"Error handling vehicle connection: {e}", "ERROR")
        finally:
            client_socket.close()
            log_system_activity(f"Connection closed for vehicle at {addr}", "INFO")

    def accept_connections(self):
        """
        Accepts incoming connections from vehicles and handles them in separate threads.
        """
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_vehicle_connection, args=(client_socket, addr)).start()
        except Exception as e:
            log_system_activity(f"Error accepting connections: {e}", "ERROR")
            self.server_socket.close()

    def aggregate_results(self):
        """
        Periodically triggers result aggregation from the collected data.
        """
        self.result_aggregator.aggregate_results()

    def run(self):
        """
        Runs the main server functionalities.
        """
        log_system_activity("Starting server main functionalities", "INFO")
        threading.Thread(target=self.accept_connections).start()
        threading.Thread(target=self.aggregate_results).start()

if __name__ == "__main__":
    server = ServerMain()
    server.run()
