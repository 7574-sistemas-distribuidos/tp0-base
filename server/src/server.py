import logging
from src.signal_controller import SignalController
from src.network.socket_tcp import SocketTCP
from src.communication.protocol import Protocol
from src.communication.command_dispatcher import CommandDispatcher


class Server:
    def __init__(self, port, listen_backlog):
        self._set_graceful_shutdown()
        self._server_socket = SocketTCP("", port)
        self._server_socket.bind_and_listen(listen_backlog)
        self._is_running = True

    def _set_graceful_shutdown(self):
        signal_controller = SignalController()
        signal_controller.add_handler(signal_controller.SIGTERM, self._sigterm_handler)

    def _sigterm_handler(self, signum, frame):
        logging.info("action: releasing_resources | result: in_progress")        
        self._is_running = False
        logging.info("action: releasing_resources | result: success")

    def _release_resources(self):
        self._server_socket.close()

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
            self._handle_client_connection(client_socket)

        self._release_resources()

    def _handle_client_connection(self, client_socket):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            command = ""
            while self._is_running and command != "CLOSE_LOAD_OF_BETS" and command != "GET_WINNERS":
                protocol = Protocol(client_socket)
                packet = protocol.receivePacket()
                command = packet.command
                packetResponse = CommandDispatcher.dispatch(packet)
                protocol.sendPacket(packetResponse)                    
        except OSError as e:
            logging.error(f"action: receive_message | result: fail | error: {e}")
        finally:
            client_socket.close()

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
