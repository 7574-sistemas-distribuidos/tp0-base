import socket
import logging
import signal
from common.utils import NAME_LEN_BYTE_POSITION, HEADER_LEN, Bet, store_bets, recv_exactly, send_all

TIMEOUT = 0.75
STORED_BET_MSG = bytes(0xff)

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.settimeout(TIMEOUT)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.running = True
        signal.signal(signal.SIGTERM, self.handle_SIG_TERM)

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """
        # TODO: Modify this program to handle signal to graceful shutdown
        # the server
        while self.running:
            try:
                client_sock = self.__accept_new_connection()
            except socket.timeout:
                continue
            self.__handle_client_connection(client_sock)

        logging.debug("Cerrando socket")
        self._server_socket.close()

    def handle_SIG_TERM(self, _signum, _frame):
        self.running = False

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            # TODO: Modify the receive to avoid short-reads
            msg_header = recv_exactly(client_sock, HEADER_LEN)
            names = recv_exactly(client_sock, msg_header[NAME_LEN_BYTE_POSITION])
            bet = Bet.from_bytes(msg_header + names)
            store_bets([bet])
            logging.info(f'action: apuesta_almacenada | result: success | dni: {bet.document} | numero: {bet.number}')

            send_all(client_sock, STORED_BET_MSG)

        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
