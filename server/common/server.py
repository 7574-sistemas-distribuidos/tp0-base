import socket
import logging
import signal
import sys
from common.utils import *
from common.protocol import *

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        # Init client sockets list
        self.client_sockets = []

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        signal.signal(signal.SIGTERM, self.__handle_SIGTERM)
       
        # the server
        while True:
            client_sock = self.__accept_new_connection()
            self.__handle_client_connection(client_sock)

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            while True:
                bets = receive_bets(client_sock)
                if bets == []:
                    break

                store_bets(bets)

                logging.info(f'action: store_bets | result: success | total_bets: {len(bets)}')
                send_ack(client_sock)

        except OSError as e:
            logging.error(f"action: client_disconnected | result: fail | error: {e}")
            self.__close_socket(client_sock)

        finally:
            sock_address = client_sock.getpeername()  
            sock_ip = sock_address[0]  
            sock_port = sock_address[1]  
            logging.info(f"action: finish_connection | result: success | remote_address: {sock_ip}:{sock_port}")

            self.__close_socket(client_sock)

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        # Add new client socket to the list
        self.client_sockets.append(c)
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c

    def __handle_SIGTERM(self, sig, frame):
        logging.info('SIGTERM received, shutting down gracefully')

        self._server_socket.close()

        for client_sock in self.client_sockets:
            client_sock.close()

        self.client_sockets.clear()

        sys.exit(0)

    def __close_socket(self, client_sock):
        client_sock.close()
        # Remove socket from the list
        self.client_sockets.remove(client_sock)