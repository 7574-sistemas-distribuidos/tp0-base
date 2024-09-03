import logging
from src.signal_controller import SignalController
from src.network.socket_tcp import SocketTCP
from src.client import Client


class Server:
    def __init__(self, port, listen_backlog):
        self._set_graceful_shutdown()
        self._server_socket = SocketTCP("", port)
        self._server_socket.bind_and_listen(listen_backlog)
        self._is_running = True
        self._clients = []

    def _set_graceful_shutdown(self):
        signal_controller = SignalController()
        signal_controller.add_handler(signal_controller.SIGTERM, self._sigterm_handler)

    def _sigterm_handler(self, signum, frame):
        logging.info("action: releasing_resources | result: in_progress")        
        self._is_running = False
        self._stop_clients()
        logging.info("action: releasing_resources | result: success")

    def _release_resources(self):
        self._server_socket.close()
        self._clean_clients()

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        while self._is_running:
            client_socket = self._accept_new_connection()
            if client_socket is None:
                continue

            client = Client(client_socket)
            client.start()
            self._clients.append(client)
            self._clean_non_running_clients()

        self._release_resources()

    def _clean_non_running_clients(self):
        running_clients = [client for client in self._clients if client.is_running()]
        non_running_clients = [client for client in self._clients if not client.is_running()]
        for non_running_client in non_running_clients:
            non_running_client.join()
        self._clients = running_clients
    
    def _clean_clients(self):
        for client in self._clients:
            client.join()

    def _stop_clients(self):
        for client in self._clients:
            client.stop()

    def _accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        try:
            logging.info("action: accept_connections | result: in_progress")
            client_socket, addr = self._server_socket.accept()
            logging.info(
                f"action: accept_connections | result: success | ip: {addr[0]}"
            )
            return client_socket
        except OSError as e:
            logging.info(f"action: accept_connections | result: fail | error: {e}")
            return None
